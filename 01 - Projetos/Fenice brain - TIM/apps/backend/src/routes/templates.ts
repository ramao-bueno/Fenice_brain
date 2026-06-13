import { Router, Request, Response, NextFunction } from 'express';
import { generateTemplate, generateRenewalProposal, GenerateTemplateInput } from '../integrations/claudeAI.js';
import { healthScoreService } from '../services/HealthScoreService.js';

/**
 * TEMPLATE ROUTES
 *
 * This is the MONEY endpoint:
 * Farmers use this to generate professional templates using Claude AI
 * Core revenue model: SaaS subscription + template credits
 */

export const templateRoutes = (): Router => {
  const router = Router();

  /**
   * POST /api/v1/templates/generate
   *
   * Generate a template using Claude AI
   * Input: Account context + goal
   * Output: Email subject + body + CTA + estimated ROI
   *
   * Usage: Farmer gets email draft ready to send in 5 seconds
   * Price model: Included in subscription (or credits)
   */
  router.post('/generate', async (req: Request, res: Response, next: NextFunction) => {
    try {
      const {
        phase,
        company_name,
        segment,
        health_score,
        mrr,
        current_outcome,
        goal,
        industry,
      } = req.body;

      // Validate required fields
      if (!phase || !company_name || !segment || !health_score || !mrr || !goal) {
        return res.status(400).json({
          error: 'Missing required fields',
          required: [
            'phase (PRE_VENDA|ONBOARD|POSVENDA|EXPANSAO)',
            'company_name',
            'segment (PME|KA)',
            'health_score (GREEN|YELLOW|RED)',
            'mrr (number)',
            'goal (RETENÇÃO|UP_SELL|CROSS_SELL|RENOVAÇÃO)',
          ],
        });
      }

      // Call Claude AI
      const template = await generateTemplate({
        phase: phase as GenerateTemplateInput['phase'],
        companyName: company_name,
        segment: segment as 'PME' | 'KA',
        healthScore: health_score as 'GREEN' | 'YELLOW' | 'RED',
        mrr: parseFloat(mrr),
        currentOutcome: current_outcome,
        goal: goal as any,
        industry,
      });

      res.json({
        success: true,
        data: template,
        message: 'Template generated successfully',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  /**
   * POST /api/v1/templates/renewal
   *
   * Generate renewal proposal with expansion upsell
   * This is "Revenue Orchestration" — Tiffani Bova style
   *
   * Used when: Customer at 75% of contract OR Green health score
   * Output: Renewal letter + expansion proposal + estimated MRR increase
   */
  router.post('/renewal', async (req: Request, res: Response, next: NextFunction) => {
    try {
      const {
        company_name,
        segment,
        mrr,
        current_outcome,
        goal,
        years_of_partnership,
        industry,
      } = req.body;

      if (!company_name || !mrr || !goal || !years_of_partnership) {
        return res.status(400).json({
          error: 'Missing fields',
          required: ['company_name', 'mrr', 'goal', 'years_of_partnership'],
        });
      }

      const proposal = await generateRenewalProposal({
        phase: 'EXPANSAO',
        companyName: company_name,
        segment: segment || 'PME',
        healthScore: 'GREEN',
        mrr: parseFloat(mrr),
        currentOutcome: current_outcome,
        goal: goal as any,
        industry,
        yearsOfPartnership: parseInt(years_of_partnership),
      });

      res.json({
        success: true,
        data: proposal,
        message: 'Renewal proposal generated',
        note: 'This locks in customer for 24+ months at higher MRR',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  /**
   * POST /api/v1/templates/health-analysis
   *
   * Analyze account health + recommend actions + draft templates
   * This is the FULL MAGIC:
   * 1. Calculate Health Score
   * 2. Detect Churn Fantasma
   * 3. Recommend action
   * 4. Generate appropriate template
   *
   * Used by: Farmer opening account dashboard
   * Output: Complete action plan + ready-to-send template
   */
  router.post('/health-analysis', async (req: Request, res: Response, next: NextFunction) => {
    try {
      const {
        company_name,
        segment,
        health_data,
        mrr,
        industry,
      } = req.body;

      if (!company_name || !health_data) {
        return res.status(400).json({
          error: 'Missing fields',
          required: [
            'company_name',
            'health_data (mrrTrend, interactionCount, daysSinceLastInteraction, dataUsageTrend, desiredOutcomeStatus)',
          ],
        });
      }

      // Calculate health score
      const healthScore = healthScoreService.calculateHealthScore(health_data);

      // Detect Churn Fantasma
      const fantasma = healthScoreService.detectChurnFantasma(health_data);

      // Recommend actions
      const actions = healthScoreService.recommendAction(healthScore);

      // Generate appropriate template based on health
      let goal: any;
      if (healthScore.status === 'GREEN') {
        goal = 'UP_SELL';
      } else if (healthScore.status === 'YELLOW') {
        goal = 'RETENÇÃO';
      } else {
        goal = 'RETENÇÃO'; // RED also needs retention
      }

      const template = await generateTemplate({
        phase: 'POSVENDA',
        companyName: company_name,
        segment: (segment as 'PME' | 'KA') || 'PME',
        healthScore: healthScore.status,
        mrr: mrr || 0,
        goal,
        industry,
      });

      res.json({
        success: true,
        data: {
          health_score: {
            overall: healthScore.overallScore,
            status: healthScore.status,
            dimensions: {
              outcome: healthScore.outcomeScore,
              engagement: healthScore.engagementScore,
              risk: healthScore.riskScore,
            },
            signals: healthScore.signals,
          },
          churn_fantasma: fantasma,
          recommended_actions: actions,
          template: template,
        },
        message: 'Complete health analysis with recommended template',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  return router;
};
