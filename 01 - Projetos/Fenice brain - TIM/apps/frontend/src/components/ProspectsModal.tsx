import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

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
  statusContato:
    | 'nao_contatado'
    | 'email_enviado'
    | 'call_agendada'
    | 'call_feita'
    | 'proposta_enviada'
    | 'conversao'
    | 'rejeicao';
  dataPrimeiroContato?: string;
  dataProximoContato?: string;
  resultado?: string;
  notas?: string;
  prioridade: 'alta' | 'media' | 'baixa';
  estimatedMRR?: number;
  createdAt?: string;
}

const statusColors: Record<Prospect['statusContato'], string> = {
  nao_contatado: 'bg-gray-100 text-gray-700',
  email_enviado: 'bg-blue-100 text-blue-700',
  call_agendada: 'bg-purple-100 text-purple-700',
  call_feita: 'bg-indigo-100 text-indigo-700',
  proposta_enviada: 'bg-yellow-100 text-yellow-700',
  conversao: 'bg-green-100 text-green-700',
  rejeicao: 'bg-red-100 text-red-700',
};

const prioridadeColors: Record<Prospect['prioridade'], string> = {
  alta: '🔴',
  media: '🟡',
  baixa: '🟢',
};

function ProspectsModal() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState('');
  const [filterPrioridade, setFilterPrioridade] = useState<string>('');
  const [filterEstado, setFilterEstado] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [selectedProspect, setSelectedProspect] = useState<Prospect | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editData, setEditData] = useState<Partial<Prospect>>({});

  // Fetch prospects
  const { data: prospectsData, isLoading } = useQuery({
    queryKey: ['prospects', { filterPrioridade, filterEstado, filterStatus }],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filterPrioridade) params.append('prioridade', filterPrioridade);
      if (filterEstado) params.append('estado', filterEstado);
      if (filterStatus) params.append('statusContato', filterStatus);

      const res = await fetch(`/api/v1/prospects?${params.toString()}`);
      return res.json();
    },
  });

  // Fetch stats
  const { data: statsData } = useQuery({
    queryKey: ['prospects-stats'],
    queryFn: async () => {
      const res = await fetch('/api/v1/prospects/stats');
      return res.json();
    },
  });

  // Search
  const searchResults = search
    ? prospectsData?.data?.filter(
        (p: Prospect) =>
          p.razaoSocial.toLowerCase().includes(search.toLowerCase()) ||
          p.cnpj.includes(search) ||
          p.email?.toLowerCase().includes(search.toLowerCase())
      ) || []
    : prospectsData?.data || [];

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: async (data: Prospect) => {
      const res = await fetch(`/api/v1/prospects/${data.cnpj}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prospects'] });
      queryClient.invalidateQueries({ queryKey: ['prospects-stats'] });
      setIsEditModalOpen(false);
      setSelectedProspect(null);
    },
  });

  const handleOpenEdit = (prospect: Prospect) => {
    setSelectedProspect(prospect);
    setEditData(prospect);
    setIsEditModalOpen(true);
  };

  const handleSaveEdit = () => {
    if (selectedProspect) {
      updateMutation.mutate({
        ...selectedProspect,
        ...editData,
      } as Prospect);
    }
  };

  const stats = statsData?.data;

  return (
    <div className="w-full bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">📋 Gerenciamento de Prospects</h1>
        <p className="text-gray-600 mt-2">Manage sua carteira TIM Business aqui</p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-blue-900">{stats.total}</div>
            <div className="text-sm text-blue-700">Total Prospects</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-green-900">{stats.byStatus.conversao}</div>
            <div className="text-sm text-green-700">Conversões</div>
          </div>
          <div className="bg-red-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-red-900">{stats.byStatus.nao_contatado}</div>
            <div className="text-sm text-red-700">Não Contatados</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-purple-900">
              R$ {(stats.totalMRR / 1000).toFixed(0)}K
            </div>
            <div className="text-sm text-purple-700">MRR Estimado</div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <input
          type="text"
          placeholder="🔍 Buscar por empresa, CNPJ ou email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="col-span-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <select
          value={filterPrioridade}
          onChange={(e) => setFilterPrioridade(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Todas Prioridades</option>
          <option value="alta">🔴 Alta</option>
          <option value="media">🟡 Média</option>
          <option value="baixa">🟢 Baixa</option>
        </select>

        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Todos Status</option>
          <option value="nao_contatado">⚪ Não Contatado</option>
          <option value="email_enviado">📧 Email Enviado</option>
          <option value="call_agendada">📅 Call Agendada</option>
          <option value="call_feita">☎️ Call Feita</option>
          <option value="proposta_enviada">📄 Proposta Enviada</option>
          <option value="conversao">✅ Conversão</option>
          <option value="rejeicao">❌ Rejeição</option>
        </select>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-100 border-b">
              <th className="px-4 py-2 text-left font-semibold text-gray-700">Empresa</th>
              <th className="px-4 py-2 text-left font-semibold text-gray-700">Email</th>
              <th className="px-4 py-2 text-left font-semibold text-gray-700">Estado</th>
              <th className="px-4 py-2 text-left font-semibold text-gray-700">MRR</th>
              <th className="px-4 py-2 text-left font-semibold text-gray-700">Prioridade</th>
              <th className="px-4 py-2 text-left font-semibold text-gray-700">Status</th>
              <th className="px-4 py-2 text-left font-semibold text-gray-700">Ações</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan={7} className="px-4 py-4 text-center text-gray-500">
                  Carregando prospects...
                </td>
              </tr>
            ) : searchResults.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-4 py-4 text-center text-gray-500">
                  Nenhum prospect encontrado
                </td>
              </tr>
            ) : (
              searchResults.map((prospect: Prospect) => (
                <tr key={prospect.cnpj} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-2">
                    <div className="font-semibold text-gray-900">{prospect.razaoSocial}</div>
                    <div className="text-xs text-gray-500">{prospect.cnpj}</div>
                  </td>
                  <td className="px-4 py-2 text-gray-600">{prospect.email || '-'}</td>
                  <td className="px-4 py-2 text-gray-600">{prospect.estado}</td>
                  <td className="px-4 py-2 font-semibold text-gray-900">
                    R$ {prospect.estimatedMRR?.toLocaleString() || '0'}
                  </td>
                  <td className="px-4 py-2 text-lg">{prioridadeColors[prospect.prioridade]}</td>
                  <td className="px-4 py-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[prospect.statusContato]}`}>
                      {prospect.statusContato.replace('_', ' ').toUpperCase()}
                    </span>
                  </td>
                  <td className="px-4 py-2">
                    <button
                      onClick={() => handleOpenEdit(prospect)}
                      className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-xs"
                    >
                      ✏️ Editar
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Edit Modal */}
      {isEditModalOpen && selectedProspect && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-2xl max-w-2xl w-full mx-4 max-h-screen overflow-y-auto">
            {/* Modal Header */}
            <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 text-white flex justify-between items-center">
              <h2 className="text-xl font-bold">{selectedProspect.razaoSocial}</h2>
              <button
                onClick={() => setIsEditModalOpen(false)}
                className="text-2xl hover:opacity-80"
              >
                ✕
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 space-y-4">
              {/* Status */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Status</label>
                <select
                  value={editData.statusContato || ''}
                  onChange={(e) =>
                    setEditData({
                      ...editData,
                      statusContato: e.target.value as any,
                    })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="nao_contatado">⚪ Não Contatado</option>
                  <option value="email_enviado">📧 Email Enviado</option>
                  <option value="call_agendada">📅 Call Agendada</option>
                  <option value="call_feita">☎️ Call Feita</option>
                  <option value="proposta_enviada">📄 Proposta Enviada</option>
                  <option value="conversao">✅ Conversão</option>
                  <option value="rejeicao">❌ Rejeição</option>
                </select>
              </div>

              {/* Datas */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Primeiro Contato
                  </label>
                  <input
                    type="date"
                    value={editData.dataPrimeiroContato || ''}
                    onChange={(e) =>
                      setEditData({
                        ...editData,
                        dataPrimeiroContato: e.target.value,
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Próximo Contato
                  </label>
                  <input
                    type="date"
                    value={editData.dataProximoContato || ''}
                    onChange={(e) =>
                      setEditData({
                        ...editData,
                        dataProximoContato: e.target.value,
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              {/* Resultado e Notas */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Resultado</label>
                <input
                  type="text"
                  placeholder="Ex: Aceitou auditoria, Agendar semana que vem..."
                  value={editData.resultado || ''}
                  onChange={(e) =>
                    setEditData({
                      ...editData,
                      resultado: e.target.value,
                    })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Notas</label>
                <textarea
                  placeholder="Anotações sobre o prospect..."
                  value={editData.notas || ''}
                  onChange={(e) =>
                    setEditData({
                      ...editData,
                      notas: e.target.value,
                    })
                  }
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Email e Telefone */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
                  <input
                    type="email"
                    value={editData.email || ''}
                    onChange={(e) =>
                      setEditData({
                        ...editData,
                        email: e.target.value,
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Telefone</label>
                  <input
                    type="tel"
                    value={editData.telefone || ''}
                    onChange={(e) =>
                      setEditData({
                        ...editData,
                        telefone: e.target.value,
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              {/* Prioridade e MRR */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Prioridade
                  </label>
                  <select
                    value={editData.prioridade || ''}
                    onChange={(e) =>
                      setEditData({
                        ...editData,
                        prioridade: e.target.value as any,
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="alta">🔴 Alta</option>
                    <option value="media">🟡 Média</option>
                    <option value="baixa">🟢 Baixa</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    MRR Estimado
                  </label>
                  <input
                    type="number"
                    value={editData.estimatedMRR || 0}
                    onChange={(e) =>
                      setEditData({
                        ...editData,
                        estimatedMRR: parseInt(e.target.value),
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="sticky bottom-0 bg-gray-50 px-6 py-4 flex justify-end gap-2 border-t">
              <button
                onClick={() => setIsEditModalOpen(false)}
                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300"
              >
                Cancelar
              </button>
              <button
                onClick={handleSaveEdit}
                disabled={updateMutation.isPending}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {updateMutation.isPending ? 'Salvando...' : '💾 Salvar'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProspectsModal;
