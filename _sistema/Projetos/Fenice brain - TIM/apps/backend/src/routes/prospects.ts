import { Router, Request, Response, NextFunction } from 'express';
import { prospectsService } from '../services/ProspectsService.js';

export const prospectsRoutes = (): Router => {
  const router = Router();

  // GET /api/v1/prospects - List all prospects with filters
  router.get('/', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { prioridade, estado, statusContato } = req.query;

      const prospects = prospectsService.listAll({
        prioridade: prioridade as string,
        estado: estado as string,
        statusContato: statusContato as string,
      });

      res.json({
        data: prospects,
        count: prospects.length,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // GET /api/v1/prospects/stats - Get statistics
  router.get('/stats', (req: Request, res: Response, next: NextFunction) => {
    try {
      const stats = prospectsService.getStats();
      res.json({
        data: stats,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // GET /api/v1/prospects/search/:query - Search prospects
  router.get('/search/:query', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { query } = req.params;
      const results = prospectsService.search(query);

      res.json({
        data: results,
        count: results.length,
        query,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // POST /api/v1/prospects - Create a new prospect
  router.post('/', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { cnpj, razaoSocial, nomeFantasia, estado, municipio, email, prioridade } = req.body;

      if (!cnpj || !razaoSocial) {
        return res.status(400).json({
          error: 'Missing required fields: cnpj, razaoSocial',
        });
      }

      const newProspect = prospectsService.create({
        cnpj,
        razaoSocial,
        nomeFantasia,
        estado: estado || '',
        municipio: municipio || '',
        faturamento: '',
        funcionarios: '',
        email,
        telefone: '',
        prioridade: prioridade || 'media',
        statusContato: 'nao_contatado',
      });

      res.status(201).json({
        data: newProspect,
        message: 'Prospect created',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // PUT /api/v1/prospects/:cnpj - Update prospect
  router.put('/:cnpj', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { cnpj } = req.params;
      const updates = req.body;

      const updated = prospectsService.update(cnpj, updates);

      if (!updated) {
        return res.status(404).json({
          error: 'Prospect not found',
          cnpj,
        });
      }

      res.json({
        data: updated,
        message: 'Prospect updated',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // DELETE /api/v1/prospects/:cnpj - Delete prospect
  router.delete('/:cnpj', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { cnpj } = req.params;
      const deleted = prospectsService.delete(cnpj);

      if (!deleted) {
        return res.status(404).json({
          error: 'Prospect not found',
          cnpj,
        });
      }

      res.json({
        message: 'Prospect deleted',
        cnpj,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  // POST /api/v1/prospects/import - Import from array (Excel data)
  router.post('/import', (req: Request, res: Response, next: NextFunction) => {
    try {
      const { data } = req.body;

      if (!Array.isArray(data)) {
        return res.status(400).json({
          error: 'Expected data to be an array',
        });
      }

      const result = prospectsService.importFromArray(data);

      res.json({
        success: result.success,
        errors: result.errors,
        message: `Imported ${result.success} prospects, ${result.errors.length} errors`,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      next(error);
    }
  });

  return router;
};
