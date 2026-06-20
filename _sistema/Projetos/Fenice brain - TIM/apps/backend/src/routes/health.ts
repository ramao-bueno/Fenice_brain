import { Router, Request, Response } from 'express';

export const healthCheckRoutes = (): Router => {
  const router = Router();

  router.get('/', (req: Request, res: Response) => {
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
    });
  });

  return router;
};
