import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export interface GenerateTemplateInput {
  phase: 'PRE_VENDA' | 'ONBOARD' | 'POSVENDA' | 'EXPANSAO';
  companyName: string;
  segment: 'PME' | 'KA';
  healthScore: 'GREEN' | 'YELLOW' | 'RED';
  mrr: number;
  currentOutcome?: string;
  goal: 'RETENÇÃO' | 'UP_SELL' | 'CROSS_SELL' | 'RENOVAÇÃO';
  industry?: string;
}

export interface GeneratedTemplate {
  subject: string;
  body: string;
  callToAction: string;
  estimatedROI?: string;
  script?: string;
}

/**
 * Gera template consultivo usando Claude AI
 * Retorna email + script + proposta prontos para enviar
 * Este é o "magic" que Farmers pagam por
 */
export async function generateTemplate(input: GenerateTemplateInput): Promise<GeneratedTemplate> {
  const systemPrompt = `
You are a Customer Success expert for TIM Business (telecom operator in Brazil).
Generate professional, consultative templates based on account context.
Lincoln Murphy principle: Focus on helping customer achieve Desired Outcome, not selling.
Tone: Professional, pragmatic, consultive. Never say generic "we're here to help".
Always include ROI estimate (not exact, but reasonable).
`;

  const userPrompt = `
Generate a template for:
- Company: ${input.companyName}
- Segment: ${input.segment} (SME or Key Account)
- Phase: ${input.phase}
- Health Score: ${input.healthScore}
- MRR: R$ ${input.mrr.toLocaleString('pt-BR')}
- Goal: ${input.goal}
${input.currentOutcome ? `- Current Outcome Status: ${input.currentOutcome}` : ''}
${input.industry ? `- Industry: ${input.industry}` : ''}

Output format (JSON):
{
  "subject": "max 50 chars, specific to situation",
  "body": "2-3 paragraphs, consultive tone, reference ROI",
  "callToAction": "specific CTA (schedule, propose, discuss)",
  "estimatedROI": "R$ XX/month or XX% savings",
  "script": "60-second call script if relevant"
}
`;

  try {
    const message = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 1024,
      system: systemPrompt,
      messages: [
        {
          role: 'user',
          content: userPrompt,
        },
      ],
    });

    // Extract text from response
    const textContent = message.content.find((block) => block.type === 'text');
    if (!textContent || textContent.type !== 'text') {
      throw new Error('No text content in response');
    }

    // Parse JSON from response
    const jsonMatch = textContent.text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON found in response');
    }

    const parsed = JSON.parse(jsonMatch[0]);
    return {
      subject: parsed.subject || 'Opportunity Discussion',
      body: parsed.body || 'Let\'s discuss your needs',
      callToAction: parsed.callToAction || 'Schedule a call',
      estimatedROI: parsed.estimatedROI,
      script: parsed.script,
    };
  } catch (error) {
    console.error('Claude API error:', error);
    throw new Error('Failed to generate template from IA');
  }
}

/**
 * Gera proposta de renovação/expansão com blindagem contra concorrência
 */
export async function generateRenewalProposal(input: GenerateTemplateInput & { yearsOfPartnership: number }): Promise<GeneratedTemplate> {
  const systemPrompt = `
You are a Business Development specialist for TIM.
Generate RENEWAL/EXPANSION proposals that:
1. Recognize achievements (years of partnership)
2. Highlight new threats (competition, technology changes)
3. Propose expansion with NEW benefits
4. Lock-in for 24+ months
Never discount unless absolutely necessary.
`;

  const userPrompt = `
Generate a renewal proposal for:
- Company: ${input.companyName}
- Years of Partnership: ${input.yearsOfPartnership}
- Current MRR: R$ ${input.mrr.toLocaleString('pt-BR')}
- New Expansion: ${input.goal}
${input.currentOutcome ? `- What We Achieved: ${input.currentOutcome}` : ''}

Format (JSON):
{
  "subject": "Antecipated renewal with new benefits",
  "body": "Recognition + proposal + value",
  "callToAction": "Executive call to discuss",
  "estimatedROI": "Combined value of current + new solution"
}
`;

  try {
    const message = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 1024,
      system: systemPrompt,
      messages: [
        {
          role: 'user',
          content: userPrompt,
        },
      ],
    });

    const textContent = message.content.find((block) => block.type === 'text');
    if (!textContent || textContent.type !== 'text') {
      throw new Error('No text in response');
    }

    const jsonMatch = textContent.text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON in response');
    }

    const parsed = JSON.parse(jsonMatch[0]);
    return {
      subject: parsed.subject || 'Renewal Opportunity',
      body: parsed.body || 'Let\'s expand together',
      callToAction: parsed.callToAction || 'Schedule meeting',
      estimatedROI: parsed.estimatedROI,
    };
  } catch (error) {
    console.error('Claude API error:', error);
    throw new Error('Failed to generate renewal proposal');
  }
}
