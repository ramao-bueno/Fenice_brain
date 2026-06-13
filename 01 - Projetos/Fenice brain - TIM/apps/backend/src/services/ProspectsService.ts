import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

interface Prospect {
  id?: number;
  cnpj: string;
  razaoSocial: string;
  nomeFantasia?: string;
  estado: string;
  municipio: string;
  faturamento: string;
  funcionarios: string;
  email?: string;
  telefone?: string;

  // Controle de vendas
  statusContato: 'nao_contatado' | 'email_enviado' | 'call_agendada' | 'call_feita' | 'proposta_enviada' | 'conversao' | 'rejeicao';
  dataPrimeiroContato?: string;
  dataProximoContato?: string;
  resultado?: string;
  notas?: string;

  // Fenice
  prioridade: 'alta' | 'media' | 'baixa';
  estimatedMRR?: number;
  createdAt?: string;
}

class ProspectsService {
  private prospects: Map<string, Prospect> = new Map();
  private nextId = 1;
  private dbPath = path.join(__dirname, '../../prospects-db.json');

  constructor() {
    this.loadFromDisk();
  }

  private loadFromDisk() {
    try {
      if (fs.existsSync(this.dbPath)) {
        const data = fs.readFileSync(this.dbPath, 'utf-8');
        const prospects: Prospect[] = JSON.parse(data);
        prospects.forEach((p) => {
          this.prospects.set(p.cnpj, p);
          this.nextId = Math.max(this.nextId, (p.id || 0) + 1);
        });
        console.log(`✅ Loaded ${prospects.length} prospects from disk`);
      } else {
        console.log('📝 Database file not found, initializing with mock data');
        this.initializeMockData();
        this.saveToDisk();
      }
    } catch (error) {
      console.error('❌ Error loading database:', error);
      this.initializeMockData();
    }
  }

  private saveToDisk() {
    try {
      const prospects = Array.from(this.prospects.values());
      fs.writeFileSync(this.dbPath, JSON.stringify(prospects, null, 2), 'utf-8');
    } catch (error) {
      console.error('❌ Error saving database:', error);
    }
  }

  private initializeMockData() {
    const mockProspects: Prospect[] = [
      {
        id: 1,
        cnpj: '00517766000148',
        razaoSocial: 'TROCOLATOR INDUSTRIA MECANICA LTDA',
        nomeFantasia: 'TROCOLATOR',
        estado: 'RJ',
        municipio: 'RIO DE JANEIRO',
        faturamento: 'R$ 100.000.001 a 300.000.000',
        funcionarios: '501 a 1000',
        email: 'marketing@trocolor.com.br',
        telefone: '(21) 3372-8484',
        prioridade: 'alta',
        statusContato: 'nao_contatado',
        estimatedMRR: 15000,
      },
      {
        id: 2,
        cnpj: '04754815000117',
        razaoSocial: 'UP OFFSHORE APOIO MARITIMO LTDA',
        estado: 'RJ',
        municipio: 'RIO DE JANEIRO',
        faturamento: 'R$ 100.000.001 a 300.000.000',
        funcionarios: '501 a 1000',
        email: 'financeiro@upoffshore.com.br',
        telefone: '(21) 3861-9250',
        prioridade: 'alta',
        statusContato: 'nao_contatado',
        estimatedMRR: 25000,
      },
      {
        id: 3,
        cnpj: '30923783000146',
        razaoSocial: 'MOTOCAR MOTO CARIOCA LTDA',
        estado: 'RJ',
        municipio: 'RIO DE JANEIRO',
        faturamento: 'R$ 100.000.001 a 300.000.000',
        funcionarios: '501 a 1000',
        email: 'relacionamento@motocarhonda.com.br',
        telefone: '(21) 2139-4848',
        prioridade: 'alta',
        statusContato: 'nao_contatado',
        estimatedMRR: 12000,
      },
      {
        id: 4,
        cnpj: '06134590000121',
        razaoSocial: 'EXPRO DO BRASIL SERVICOS LTDA',
        estado: 'RJ',
        municipio: 'RIO DE JANEIRO',
        faturamento: 'R$ 100.000.001 a 300.000.000',
        funcionarios: '501 a 1000',
        email: 'marketing@exprogroup.com',
        telefone: '(21) 3763-5040',
        prioridade: 'alta',
        statusContato: 'nao_contatado',
        estimatedMRR: 18000,
      },
      {
        id: 5,
        cnpj: '05279707000100',
        razaoSocial: 'FLOWERS CONSULTORIA IMOBILIARIA LTDA',
        nomeFantasia: 'FLOWERS CONSULTING',
        estado: 'RJ',
        municipio: 'RIO DE JANEIRO',
        faturamento: 'R$ 100.000.001 a 300.000.000',
        funcionarios: '501 a 1000',
        email: 'luiz@flowers.com.br',
        telefone: '(21) 3598-7860',
        prioridade: 'alta',
        statusContato: 'nao_contatado',
        estimatedMRR: 20000,
      },
    ];

    mockProspects.forEach((p) => {
      this.prospects.set(p.cnpj, p);
      this.nextId = Math.max(this.nextId, (p.id || 0) + 1);
    });
  }

  listAll(filters?: {
    prioridade?: string;
    estado?: string;
    statusContato?: string;
  }): Prospect[] {
    let result = Array.from(this.prospects.values());

    if (filters?.prioridade) {
      result = result.filter((p) => p.prioridade === filters.prioridade);
    }
    if (filters?.estado) {
      result = result.filter((p) => p.estado === filters.estado);
    }
    if (filters?.statusContato) {
      result = result.filter((p) => p.statusContato === filters.statusContato);
    }

    return result.sort((a, b) => (b.id || 0) - (a.id || 0));
  }

  getByEmail(email: string): Prospect | undefined {
    return Array.from(this.prospects.values()).find((p) => p.email === email);
  }

  getByEmpresa(razaoSocial: string): Prospect | undefined {
    return Array.from(this.prospects.values()).find(
      (p) => p.razaoSocial.toLowerCase() === razaoSocial.toLowerCase()
    );
  }

  create(prospect: Omit<Prospect, 'id'>): Prospect {
    const newProspect: Prospect = {
      ...prospect,
      id: this.nextId++,
      createdAt: new Date().toISOString(),
    };
    this.prospects.set(newProspect.cnpj, newProspect);
    this.saveToDisk();
    return newProspect;
  }

  update(cnpj: string, data: Partial<Prospect>): Prospect | null {
    const prospect = this.prospects.get(cnpj);
    if (!prospect) return null;

    const updated = { ...prospect, ...data, cnpj }; // Prevent CNPJ change
    this.prospects.set(cnpj, updated);
    this.saveToDisk();
    return updated;
  }

  delete(cnpj: string): boolean {
    const result = this.prospects.delete(cnpj);
    if (result) this.saveToDisk();
    return result;
  }

  getStats() {
    const all = Array.from(this.prospects.values());
    const byStatus = {
      nao_contatado: 0,
      email_enviado: 0,
      call_agendada: 0,
      call_feita: 0,
      proposta_enviada: 0,
      conversao: 0,
      rejeicao: 0,
    };

    all.forEach((p) => {
      byStatus[p.statusContato]++;
    });

    return {
      total: all.length,
      totalMRR: all.reduce((sum, p) => sum + (p.estimatedMRR || 0), 0),
      byPrioridade: {
        alta: all.filter((p) => p.prioridade === 'alta').length,
        media: all.filter((p) => p.prioridade === 'media').length,
        baixa: all.filter((p) => p.prioridade === 'baixa').length,
      },
      byStatus,
      byEstado: {
        RJ: all.filter((p) => p.estado === 'RJ').length,
        SP: all.filter((p) => p.estado === 'SP').length,
        SC: all.filter((p) => p.estado === 'SC').length,
        outros: all.filter((p) => !['RJ', 'SP', 'SC'].includes(p.estado)).length,
      },
    };
  }

  search(query: string): Prospect[] {
    const q = query.toLowerCase();
    return Array.from(this.prospects.values()).filter(
      (p) =>
        p.razaoSocial.toLowerCase().includes(q) ||
        p.nomeFantasia?.toLowerCase().includes(q) ||
        p.email?.toLowerCase().includes(q) ||
        p.cnpj.includes(query) ||
        p.municipio.toLowerCase().includes(q)
    );
  }

  importFromArray(data: any[]): { success: number; errors: any[] } {
    const errors: any[] = [];
    let success = 0;

    data.forEach((row, idx) => {
      try {
        if (!row.cnpj || !row.razaoSocial) {
          errors.push({ row: idx, error: 'CNPJ ou Razão Social faltando' });
          return;
        }

        if (!this.prospects.has(row.cnpj)) {
          const newProspect: Prospect = {
            id: this.nextId++,
            cnpj: row.cnpj,
            razaoSocial: row.razaoSocial,
            nomeFantasia: row.nomeFantasia,
            estado: row.estado || '',
            municipio: row.municipio || '',
            faturamento: row.faturamento || '',
            funcionarios: row.funcionarios || '',
            email: row.email,
            telefone: row.telefone,
            prioridade: row.estado === 'RJ' ? 'alta' : 'media',
            statusContato: 'nao_contatado',
            createdAt: new Date().toISOString(),
          };
          this.prospects.set(row.cnpj, newProspect);
          success++;
        }
      } catch (error) {
        errors.push({ row: idx, error: String(error) });
      }
    });

    if (success > 0) this.saveToDisk();
    return { success, errors };
  }
}

export const prospectsService = new ProspectsService();
