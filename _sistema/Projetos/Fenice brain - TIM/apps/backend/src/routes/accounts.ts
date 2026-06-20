import { Router, Request, Response, NextFunction, Express } from 'express';

interface Account {
  id: number;
  cnpj: string;
  company_name: string;
  segment: 'PME' | 'KA';
  mrr: number;
  health_score_overall: 'GREEN' | 'YELLOW' | 'RED';
  created_at: string;
}

// Mock data for MVP
const mockAccounts: Account[] = [
  {
    id: 1,
    cnpj: '12.345.678/0001-00',
    company_name: 'TechFlow Solutions',
    segment: 'PME',
    mrr: 85000,
    health_score_overall: 'GREEN',
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    cnpj: '98.765.432/0001-00',
    company_name: 'Global Logistics',
    segment: 'KA',
    mrr: 320000,
    health_score_overall: 'YELLOW',
    created_at: new Date().toISOString(),
  },
];

export const accountRoutes = (): Router => {
  const router = Router();

  // GET /api/v1/accounts
  router.get('/', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { health_score, segment } = req.query;

      let filtered = [...mockAccounts];

      if (health_score) {
        filtered = filtered.filter((a) => a.health_score_overall === health_score);
      }

      if (segment) {
        filtered = filtered.filter((a) => a.segment === segment);
      }

      res.json({
        data: filtered,
        count: filtered.length,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // GET /api/v1/accounts/:id
  router.get('/:id', (req: Request, res: Response, next: NextFunction) => {
    try {
      const account = mockAccounts.find((a) => a.id === parseInt(req.params.id));

      if (!account) {
        return res.status(404).json({
          error: 'Account not found',
          id: req.params.id,
        });
      }

      res.json({
        data: account,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // POST /api/v1/accounts
  router.post('/', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { cnpj, company_name, segment, mrr } = req.body;

      if (!cnpj || !company_name || !segment) {
        return res.status(400).json({
          error: 'Missing required fields: cnpj, company_name, segment',
        });
      }

      const newAccount: Account = {
        id: Math.max(...mockAccounts.map((a) => a.id)) + 1,
        cnpj,
        company_name,
        segment,
        mrr: mrr || 0,
        health_score_overall: 'GREEN',
        created_at: new Date().toISOString(),
      };

      mockAccounts.push(newAccount);

      res.status(201).json({
        data: newAccount,
        message: 'Account created successfully',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  return router;
};
