import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react';
import ProspectsModal from './components/ProspectsModal';

interface Account {
  id: number;
  cnpj: string;
  company_name: string;
  segment: 'PME' | 'KA';
  mrr: number;
  health_score_overall: 'GREEN' | 'YELLOW' | 'RED';
  created_at: string;
}

const fetchAccounts = async (): Promise<Account[]> => {
  const response = await axios.get('/api/v1/accounts');
  return response.data.data;
};

const healthScoreSummary = (accounts: Account[]) => {
  return {
    green: accounts.filter((a) => a.health_score_overall === 'GREEN').length,
    yellow: accounts.filter((a) => a.health_score_overall === 'YELLOW').length,
    red: accounts.filter((a) => a.health_score_overall === 'RED').length,
  };
};

const healthScoreColor = (status: string) => {
  switch (status) {
    case 'GREEN':
      return 'bg-green-100 text-green-800 border-green-300';
    case 'YELLOW':
      return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    case 'RED':
      return 'bg-red-100 text-red-800 border-red-300';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-300';
  }
};

const healthScoreIcon = (status: string) => {
  switch (status) {
    case 'GREEN':
      return <CheckCircle className="w-4 h-4" />;
    case 'YELLOW':
      return <AlertTriangle className="w-4 h-4" />;
    case 'RED':
      return <AlertCircle className="w-4 h-4" />;
    default:
      return null;
  }
};

function App() {
  const [activeTab, setActiveTab] = useState<'accounts' | 'prospects'>('accounts');

  const { data: accounts = [], isLoading, error } = useQuery({
    queryKey: ['accounts'],
    queryFn: fetchAccounts,
  });

  const summary = healthScoreSummary(accounts);
  const totalMRR = accounts.reduce((sum, a) => sum + a.mrr, 0);

  const chartData = [
    { name: 'Green', value: summary.green, fill: '#10b981' },
    { name: 'Yellow', value: summary.yellow, fill: '#f59e0b' },
    { name: 'Red', value: summary.red, fill: '#ef4444' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="bg-black/40 backdrop-blur-md border-b border-slate-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center mb-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xs">FB</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Fenice B2B</h1>
          </div>
          <p className="text-slate-400 text-sm">Customer Success Platform</p>
        </div>

        {/* Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex gap-4 border-t border-slate-700">
          <button
            onClick={() => setActiveTab('accounts')}
            className={`px-4 py-3 font-semibold transition-colors ${
              activeTab === 'accounts'
                ? 'text-blue-400 border-b-2 border-blue-400'
                : 'text-slate-400 hover:text-slate-300'
            }`}
          >
            👥 Accounts (Customers)
          </button>
          <button
            onClick={() => setActiveTab('prospects')}
            className={`px-4 py-3 font-semibold transition-colors ${
              activeTab === 'prospects'
                ? 'text-blue-400 border-b-2 border-blue-400'
                : 'text-slate-400 hover:text-slate-300'
            }`}
          >
            📋 Prospects (Pipeline)
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'prospects' ? (
          <ProspectsModal />
        ) : (
          <>
            {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-lg p-6 text-white">
            <p className="text-slate-400 text-sm mb-2">Total Accounts</p>
            <p className="text-3xl font-bold">{accounts.length}</p>
            <p className="text-slate-400 text-xs mt-2">Portfolio size</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-lg p-6 text-white">
            <p className="text-slate-400 text-sm mb-2">Total MRR</p>
            <p className="text-3xl font-bold">R$ {(totalMRR / 1000).toFixed(0)}K</p>
            <p className="text-slate-400 text-xs mt-2">Monthly recurring revenue</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-lg p-6">
            <p className="text-slate-400 text-sm mb-2">Green</p>
            <p className="text-3xl font-bold text-green-400">{summary.green}</p>
            <p className="text-slate-400 text-xs mt-2">Healthy accounts</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-lg p-6">
            <p className="text-slate-400 text-sm mb-2">At Risk</p>
            <p className="text-3xl font-bold text-red-400">{summary.yellow + summary.red}</p>
            <p className="text-slate-400 text-xs mt-2">Yellow + Red</p>
          </div>
        </div>

        {/* Chart */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-white mb-6">Health Score Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }} />
              <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Accounts Table */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-lg overflow-hidden">
          <div className="p-6 border-b border-white/10">
            <h2 className="text-xl font-bold text-white">Portfolio Accounts</h2>
          </div>

          {isLoading && (
            <div className="p-8 text-center text-slate-400">
              <p>Loading accounts...</p>
            </div>
          )}

          {error && (
            <div className="p-8 text-center text-red-400">
              <p>Error loading accounts</p>
            </div>
          )}

          {accounts.length > 0 && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-white/5 border-b border-white/10">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-semibold text-slate-300">Company</th>
                    <th className="px-6 py-3 text-left text-xs font-semibold text-slate-300">CNPJ</th>
                    <th className="px-6 py-3 text-left text-xs font-semibold text-slate-300">Segment</th>
                    <th className="px-6 py-3 text-left text-xs font-semibold text-slate-300">MRR</th>
                    <th className="px-6 py-3 text-left text-xs font-semibold text-slate-300">Health</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {accounts.map((account) => (
                    <tr key={account.id} className="hover:bg-white/5 transition-colors">
                      <td className="px-6 py-4 text-sm text-white font-medium">{account.company_name}</td>
                      <td className="px-6 py-4 text-sm text-slate-400">{account.cnpj}</td>
                      <td className="px-6 py-4 text-sm">
                        <span className="inline-block bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-xs">
                          {account.segment}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-white">R$ {(account.mrr / 1000).toFixed(0)}K</td>
                      <td className="px-6 py-4 text-sm">
                        <span
                          className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs border ${healthScoreColor(
                            account.health_score_overall
                          )}`}
                        >
                          {healthScoreIcon(account.health_score_overall)}
                          {account.health_score_overall}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

            {/* Info Banner */}
            <div className="mt-8 bg-blue-500/10 border border-blue-500/20 rounded-lg p-4 text-blue-300 text-sm">
              <p>
                💡 <strong>MVP Note:</strong> This dashboard is using mock data. Connect your PostgreSQL database and integrate Claude AI
                for full Health Score calculation and Churn Fantasma detection.
              </p>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
