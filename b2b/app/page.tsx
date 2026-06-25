"use client";
import { useState } from "react";

const PLANOS = [
  {
    nome: "Starter",
    preco: "R$ 497/mês",
    descricao: "Ideal para escritórios com até 5 usuários",
    itens: [
      "API REST completa (10.000 requisições/mês)",
      "Busca FTS em 1.474+ leis federais",
      "5.685 artigos indexados",
      "Suporte por e-mail",
    ],
    destaque: false,
    cta: "Começar agora",
  },
  {
    nome: "Pro",
    preco: "R$ 1.497/mês",
    descricao: "Para escritórios e departamentos jurídicos",
    itens: [
      "API REST ilimitada",
      "RAG semântico (pgvector)",
      "Assistente WhatsApp Fenice_Tim",
      "674 Súmulas STJ + 736 STF",
      "Acesso hermenêutico + TCC",
      "Suporte prioritário",
    ],
    destaque: true,
    cta: "Falar com especialista",
  },
  {
    nome: "Enterprise",
    preco: "Sob consulta",
    descricao: "Para grandes escritórios e corporações",
    itens: [
      "Tudo do Pro",
      "Deploy dedicado (VPC/on-premise)",
      "SLA 99,9% + suporte 24/7",
      "Integração com sistemas legados",
      "Treinamento personalizado da equipe",
      "Knowledge Graph exclusivo",
    ],
    destaque: false,
    cta: "Solicitar proposta",
  },
];

const DIFERENCIAIS = [
  { icone: "⚖️", titulo: "Base Jurídica Real", texto: "1.474+ leis federais, 674 Súmulas STJ e 736 STF indexadas com FTS em português." },
  { icone: "🤖", titulo: "IA Jurídica Especializada", texto: "RAG híbrido com pgvector + Groq — respostas fundamentadas em legislação real, nunca inventadas." },
  { icone: "📱", titulo: "Fenice_Tim (WhatsApp)", texto: "Assistente inteligente que roteisa prospects, qualifica leads e faz atendimento jurídico 24/7." },
  { icone: "🔒", titulo: "Segurança Enterprise", texto: "Supabase PostgreSQL + RLS + chaves de API individuais. LGPD compliant." },
  { icone: "🔗", titulo: "API REST Documentada", texto: "FastAPI com endpoints Free e Premium. Integra com qualquer sistema em minutos." },
  { icone: "📊", titulo: "Painel de Controle", texto: "Dashboard de uso, histórico de consultas e relatórios em tempo real. (em breve)" },
];

export default function B2BPage() {
  const [contatoEnviado, setContatoEnviado] = useState(false);
  const [form, setForm] = useState({ nome: "", empresa: "", email: "", plano: "Pro", mensagem: "" });
  const [enviando, setEnviando] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    // TODO: integrar com endpoint /api/contato-b2b
    await new Promise((r) => setTimeout(r, 1000));
    setContatoEnviado(true);
    setEnviando(false);
  }

  return (
    <main className="min-h-screen bg-[#0a0a0f] text-white">
      {/* Header */}
      <header className="border-b border-white/10 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl font-bold" style={{ color: "#c9a227" }}>🦅 Fenice IT</span>
          <span className="text-white/40 text-sm hidden sm:block">Justech.IA — Soluções B2B</span>
        </div>
        <a
          href="https://fenice.ia.br"
          className="text-sm px-4 py-2 rounded-lg border border-white/20 hover:border-yellow-500/50 transition-colors"
        >
          Ver API →
        </a>
      </header>

      {/* Hero */}
      <section className="px-6 py-20 text-center max-w-4xl mx-auto">
        <div className="inline-block px-4 py-1 rounded-full border border-yellow-500/30 text-yellow-400 text-sm mb-6">
          Plataforma Jurídica Inteligente para Empresas
        </div>
        <h1 className="text-4xl sm:text-5xl font-bold mb-6 leading-tight">
          Transforme seu escritório com{" "}
          <span style={{ color: "#c9a227" }}>IA Jurídica de Ponta</span>
        </h1>
        <p className="text-white/60 text-lg mb-10 max-w-2xl mx-auto">
          API REST jurídica com RAG semântico, assistente WhatsApp inteligente e base com
          1.474+ leis federais + 1.410 súmulas indexadas. Tudo pronto para integrar ao seu sistema.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <a
            href="#contato"
            className="px-8 py-3 rounded-lg font-semibold text-black"
            style={{ background: "#c9a227" }}
          >
            Falar com Especialista
          </a>
          <a
            href="https://fenice.ia.br"
            className="px-8 py-3 rounded-lg font-semibold border border-white/20 hover:border-white/40 transition-colors"
          >
            Ver Demo da API
          </a>
        </div>
      </section>

      {/* Diferenciais */}
      <section className="px-6 py-16 max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-center mb-12">Por que a Fenice IT?</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {DIFERENCIAIS.map((d) => (
            <div key={d.titulo} className="p-6 rounded-xl border border-white/10 bg-[#12121a]">
              <div className="text-3xl mb-3">{d.icone}</div>
              <h3 className="font-semibold mb-2">{d.titulo}</h3>
              <p className="text-white/50 text-sm">{d.texto}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Planos */}
      <section className="px-6 py-16 max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-center mb-4">Planos B2B</h2>
        <p className="text-white/50 text-center mb-12">Escolha o plano ideal para o tamanho da sua operação.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {PLANOS.map((p) => (
            <div
              key={p.nome}
              className={`p-6 rounded-xl border flex flex-col ${
                p.destaque
                  ? "border-yellow-500/50 bg-[#1a1600]"
                  : "border-white/10 bg-[#12121a]"
              }`}
            >
              {p.destaque && (
                <div className="text-yellow-400 text-xs font-semibold mb-3 uppercase tracking-wider">
                  ★ Mais Popular
                </div>
              )}
              <h3 className="text-xl font-bold mb-1">{p.nome}</h3>
              <div className="text-2xl font-bold mb-1" style={{ color: "#c9a227" }}>{p.preco}</div>
              <p className="text-white/50 text-sm mb-6">{p.descricao}</p>
              <ul className="space-y-2 mb-8 flex-1">
                {p.itens.map((item) => (
                  <li key={item} className="flex items-start gap-2 text-sm text-white/70">
                    <span className="text-green-400 mt-0.5">✓</span>
                    {item}
                  </li>
                ))}
              </ul>
              <a
                href="#contato"
                className={`py-3 rounded-lg text-center font-semibold text-sm transition-colors ${
                  p.destaque
                    ? "text-black"
                    : "border border-white/20 hover:border-yellow-500/50"
                }`}
                style={p.destaque ? { background: "#c9a227" } : {}}
              >
                {p.cta}
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* Formulário de contato */}
      <section id="contato" className="px-6 py-16 max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold text-center mb-4">Fale com um Especialista</h2>
        <p className="text-white/50 text-center mb-10">
          Nossa equipe entra em contato em até 24 horas úteis.
        </p>

        {contatoEnviado ? (
          <div className="p-8 rounded-xl border border-green-500/30 bg-green-900/10 text-center">
            <div className="text-4xl mb-4">✅</div>
            <h3 className="text-xl font-bold mb-2">Mensagem recebida!</h3>
            <p className="text-white/60">
              Nossa equipe entrará em contato em até 24 horas úteis.<br />
              <strong>contato@fenice.ia.br</strong>
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-white/60 mb-1">Nome *</label>
                <input
                  type="text" required
                  value={form.nome}
                  onChange={(e) => setForm({ ...form, nome: e.target.value })}
                  className="w-full bg-[#12121a] border border-white/10 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-yellow-500/50"
                  placeholder="Seu nome"
                />
              </div>
              <div>
                <label className="block text-sm text-white/60 mb-1">Empresa *</label>
                <input
                  type="text" required
                  value={form.empresa}
                  onChange={(e) => setForm({ ...form, empresa: e.target.value })}
                  className="w-full bg-[#12121a] border border-white/10 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-yellow-500/50"
                  placeholder="Razão social ou escritório"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm text-white/60 mb-1">E-mail *</label>
              <input
                type="email" required
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full bg-[#12121a] border border-white/10 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-yellow-500/50"
                placeholder="contato@seuescritorio.com"
              />
            </div>
            <div>
              <label className="block text-sm text-white/60 mb-1">Plano de interesse</label>
              <select
                value={form.plano}
                onChange={(e) => setForm({ ...form, plano: e.target.value })}
                className="w-full bg-[#12121a] border border-white/10 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-yellow-500/50"
              >
                <option value="Starter">Starter — R$ 497/mês</option>
                <option value="Pro">Pro — R$ 1.497/mês</option>
                <option value="Enterprise">Enterprise — Sob consulta</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-white/60 mb-1">Mensagem</label>
              <textarea
                rows={4}
                value={form.mensagem}
                onChange={(e) => setForm({ ...form, mensagem: e.target.value })}
                className="w-full bg-[#12121a] border border-white/10 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-yellow-500/50 resize-none"
                placeholder="Descreva sua necessidade ou dúvida..."
              />
            </div>
            <button
              type="submit"
              disabled={enviando}
              className="w-full py-4 rounded-lg font-semibold text-black disabled:opacity-60 transition-opacity"
              style={{ background: "#c9a227" }}
            >
              {enviando ? "Enviando..." : "Enviar mensagem →"}
            </button>
          </form>
        )}
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 px-6 py-8 text-center">
        <p className="text-white/30 text-xs">
          © 2026 Fenice IT Justech.ia · Todos os direitos reservados · Developed by Ramão Bueno da Silva Neto / Tech Lead
        </p>
      </footer>
    </main>
  );
}
