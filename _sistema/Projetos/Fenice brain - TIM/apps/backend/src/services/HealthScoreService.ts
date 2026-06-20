/**
 * Health Score Service - Tridimensional Scoring (Lincoln Murphy)
 *
 * Health Score = (Desired Outcome Status) + (Engagement Level) + (Risk Indicators)
 *
 * This is the CORE ENGINE that drives all business decisions in Fenice B2B
 */

interface HealthScoreResult {
  outcomeScore: number; // 0-10: Is customer achieving their Desired Outcome?
  engagementScore: number; // 0-10: Is customer actively using service?
  riskScore: number; // 0-10 (inverted): Are there warning signals?
  overallScore: number; // 0-10: Composite
  status: 'GREEN' | 'YELLOW' | 'RED';
  signals: string[]; // What's driving this score?
}

export class HealthScoreService {
  /**
   * Calculate tridimensional health score
   * MVP: Simplified version (full version in V1 with real data)
   */
  calculateHealthScore(accountData: {
    mrrTrend: number; // % change in MRR (last 90 days)
    interactionCount: number; // tickets/calls/emails in last 90 days
    daysSinceLastInteraction: number;
    dataUsageTrend: number; // % change in data usage
    desiredOutcomeStatus: 'ACHIEVED' | 'IN_PROGRESS' | 'NOT_ACHIEVED' | 'UNKNOWN';
    contestedInvoices: number;
    slaBreaches: number;
  }): HealthScoreResult {
    const signals: string[] = [];

    // DIMENSION 1: Desired Outcome Status (40% weight)
    let outcomeScore = 5.0;
    switch (accountData.desiredOutcomeStatus) {
      case 'ACHIEVED':
        outcomeScore = 9.0;
        signals.push('✅ Desired outcome achieved');
        break;
      case 'IN_PROGRESS':
        outcomeScore = 6.5;
        signals.push('⏳ Desired outcome in progress');
        break;
      case 'NOT_ACHIEVED':
        outcomeScore = 3.0;
        signals.push('❌ Desired outcome NOT achieved (RISK)');
        break;
    }

    // DIMENSION 2: Engagement Level (40% weight)
    let engagementScore = 5.0;

    // Sub-metric: Interaction frequency
    let interactionScore = 5.0;
    if (accountData.interactionCount >= 4) {
      interactionScore = 9.0; // Healthy: 1 ticket/month
      signals.push('✅ Good engagement (4+ interactions/90d)');
    } else if (accountData.interactionCount === 0) {
      interactionScore = 1.0;
      signals.push('🚨 CHURN FANTASMA: Zero interactions in 90 days (CRITICAL)');
    } else if (accountData.interactionCount <= 2) {
      interactionScore = 3.0;
      signals.push('⚠️ Low engagement (1-2 interactions/90d)');
    }

    // Sub-metric: Silence duration
    let silenceScore = 5.0;
    if (accountData.daysSinceLastInteraction <= 30) {
      silenceScore = 9.0;
    } else if (accountData.daysSinceLastInteraction <= 90) {
      silenceScore = 6.0;
    } else if (accountData.daysSinceLastInteraction > 180) {
      silenceScore = 1.0;
      signals.push('🚨 CHURN FANTASMA: 180+ days silence (CRITICAL)');
    } else {
      silenceScore = 3.0;
      signals.push('⚠️ Extended silence (90-180 days)');
    }

    engagementScore = (interactionScore + silenceScore) / 2;

    // DIMENSION 3: Risk Indicators (20% weight, inverted)
    let riskScore = 5.0; // 0-10 (lower = better)

    // Sub-metric: MRR trend
    if (accountData.mrrTrend >= 10) {
      riskScore -= 2.0; // Growing = lower risk
      signals.push('✅ MRR growing (+10%)');
    } else if (accountData.mrrTrend < -30) {
      riskScore += 3.0; // Declining = higher risk
      signals.push('🔴 MRR down >30% (CRITICAL RISK)');
    } else if (accountData.mrrTrend < 0) {
      riskScore += 1.5;
      signals.push('⚠️ MRR declining');
    }

    // Sub-metric: Data usage trend (ghost detection)
    if (accountData.dataUsageTrend < -40) {
      riskScore += 2.5;
      signals.push('👻 CHURN FANTASMA: Data usage -40% (CRITICAL)');
    } else if (accountData.dataUsageTrend < -20) {
      riskScore += 1.5;
      signals.push('⚠️ Data usage down 20-40%');
    }

    // Sub-metric: Contested invoices
    if (accountData.contestedInvoices > 2) {
      riskScore += 2.0;
      signals.push('🔴 Multiple contested invoices (RISK)');
    } else if (accountData.contestedInvoices > 0) {
      riskScore += 1.0;
      signals.push('⚠️ Billing dispute detected');
    }

    // Sub-metric: SLA breaches
    if (accountData.slaBreaches > 3) {
      riskScore += 2.0;
      signals.push('🔴 Multiple SLA breaches (RISK)');
    } else if (accountData.slaBreaches > 0) {
      riskScore += 1.0;
      signals.push('⚠️ SLA breach occurred');
    }

    riskScore = Math.max(0, Math.min(10, riskScore)); // Clamp 0-10

    // COMPOSITE SCORE (weighted average)
    const overallScore = outcomeScore * 0.4 + engagementScore * 0.4 + (10 - riskScore) * 0.2;

    // CLASSIFICATION
    let status: 'GREEN' | 'YELLOW' | 'RED';
    if (overallScore >= 7.5) {
      status = 'GREEN';
      signals.push('✅ SAUDÁVEL - Candidato para Up-Sell/Cross-Sell');
    } else if (overallScore >= 5.0) {
      status = 'YELLOW';
      signals.push('⚠️ EM ALERTA - Requer intervenção');
    } else {
      status = 'RED';
      signals.push('🔴 CRÍTICO - Risco imediato de churn');
    }

    return {
      outcomeScore,
      engagementScore,
      riskScore,
      overallScore: Math.round(overallScore * 10) / 10,
      status,
      signals,
    };
  }

  /**
   * Detect Churn Fantasma
   * Silent churn: customer is technically active (pays) but operationally dead
   */
  detectChurnFantasma(accountData: {
    dataUsageTrend: number;
    interactionCount: number;
    daysSinceLastInteraction: number;
    mrrTrend: number;
  }): { isFantasma: boolean; severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' } {
    // Fantasma = stable MRR BUT declining usage + no interactions
    const isFantasma =
      accountData.dataUsageTrend < -30 &&
      accountData.interactionCount === 0 &&
      accountData.daysSinceLastInteraction > 90 &&
      accountData.mrrTrend > -10; // MRR still OK (that's why it's "silent")

    if (!isFantasma) {
      return { isFantasma: false, severity: 'LOW' };
    }

    // Determine severity
    let severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'MEDIUM';
    if (accountData.daysSinceLastInteraction > 180 && accountData.dataUsageTrend < -50) {
      severity = 'CRITICAL'; // Dead account, will cancel soon
    } else if (accountData.daysSinceLastInteraction > 120) {
      severity = 'HIGH'; // Strong churn signals
    }

    return { isFantasma: true, severity };
  }

  /**
   * Recommend next action based on health score
   * This drives what Farmer should do TODAY
   */
  recommendAction(health: HealthScoreResult): string[] {
    const actions: string[] = [];

    if (health.status === 'GREEN') {
      actions.push('📞 Schedule QBR (quarterly business review)');
      actions.push('💰 Present Up-Sell opportunity (Cloud/IoT/TI Total)');
      actions.push('🔒 Discuss renewal terms (lock-in 24 months)');
    } else if (health.status === 'YELLOW') {
      actions.push('☎️ Call customer TODAY');
      actions.push('🔍 Audit: Is Desired Outcome being met?');
      actions.push('🛠️ Offer technical review (free)');
      actions.push('💳 Review billing (contestations?)');
    } else {
      // RED
      actions.push('🚨 EMERGENCY: Escalate to Manager');
      actions.push('📋 Prepare Recovery Plan (what went wrong?)');
      actions.push('💬 Executive call (C-level if Key Account)');
      actions.push('💰 Retention offer (discount? SLA upgrade? Free service?)');
      actions.push('🤝 Offer offboarding (if leaving, keep door open)');
    }

    return actions;
  }
}

export const healthScoreService = new HealthScoreService();
