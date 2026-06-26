import SectionDivider from "@/components/ui/SectionDivider";
import { propostas } from "@/lib/data";

export default function Propostas() {
  return (
    <section className="pb-4">
      <SectionDivider id="propostas" kicker="O que podemos fazer" titulo="Quatro propostas para São Francisco do Sul" />

      <div data-animate data-delay="1"
        className="mt-8 rounded-2xl p-6 md:p-8 text-white"
        style={{ background: "linear-gradient(135deg, #005c2a 0%, #3db554 100%)" }}
      >
        <p className="text-lg md:text-xl leading-relaxed font-medium">
          Os dados apontam um caminho. São quatro medidas concretas que podem orientar esforços
          conjuntos do poder público, instituições e comunidade para{" "}
          <strong>fortalecer a proteção das mulheres</strong> na cidade.
        </p>
        <div className="mt-5 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            "Estruturação da DPCAMI implementada",
            "Criação de Vara Judicial Especializada na Comarca",
            "Rede de acolhimento",
            "Monitoramento de dados",
          ].map((tag, i) => (
            <div key={i} className="rounded-xl bg-white/15 px-4 py-3 text-sm font-semibold text-white/90 text-center backdrop-blur">
              {i + 1}. {tag}
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8 grid gap-5 md:grid-cols-2">
        {propostas.map((p, i) => (
          <div
            key={p.n}
            data-animate
            data-delay={String(i + 1)}
            className="rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm card-hover"
          >
            <span className="font-serif font-black text-5xl text-verde leading-none">{p.n}</span>
            <h3 className="font-serif font-bold text-xl mt-3">{p.titulo}</h3>
            <p className="text-ink/70 border-t border-verde/20 mt-3 pt-3 text-sm md:text-base leading-relaxed">{p.descricao}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
