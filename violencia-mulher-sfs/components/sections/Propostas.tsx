import SectionDivider from "@/components/ui/SectionDivider";
import FiguraComCredito from "@/components/ui/FiguraComCredito";
import { propostas } from "@/lib/data";

export default function Propostas() {
  return (
    <section className="pb-4">
      <SectionDivider
        id="propostas"
        kicker="O que pedimos a Camara"
        titulo="Quatro propostas para Sao Francisco do Sul"
      />
      <p className="mt-6 text-lg text-ink/80 max-w-2xl leading-relaxed">
        Os dados apontam um caminho. Sao quatro medidas concretas, ao alcance do municipio, para
        proteger melhor as mulheres da cidade.
      </p>
      <FiguraComCredito
        className="mt-8"
        src="/img/propostas-delegacia.jpg"
        alt="Fachada de uma Delegacia de Defesa da Mulher"
        credito="Delegacia de Defesa da Mulher. Foto: Governo do Estado de Sao Paulo (CC BY 2.0)."
      />
      <div className="mt-8 grid gap-5 md:grid-cols-2">
        {propostas.map((p) => (
          <div key={p.n} className="rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm">
            <span className="font-serif font-black text-5xl text-verde leading-none">{p.n}</span>
            <h3 className="font-serif font-bold text-xl mt-3">{p.titulo}</h3>
            <p className="text-ink/70 mt-2 text-sm md:text-base leading-relaxed">{p.descricao}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
