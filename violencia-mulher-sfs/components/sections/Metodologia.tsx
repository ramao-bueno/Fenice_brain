import SectionDivider from "@/components/ui/SectionDivider";
import { meta, parcial2027 } from "@/lib/data";

const PONTOS = [
  {
    t: "Dados judiciais não representam o total de casos de violência contra a mulher",
    d: "Os números se referem a audiências realizadas na comarca. Muitos casos não chegam ao Poder Judiciário — portanto, estes dados apresentam o cenário de audiências realizadas demonstrando os números que efetivamente chegaram ao judiciário e tiveram audiências pautadas.",
  },
  {
    t: "2021 e 2022 - possível caso de subnotificação",
    d: "Com apenas 9 e 8 audiências, esses anos podem refletir registro parcial e subnotificação, não ausência de crimes, bem como são impactados pelo período pandêmico de Covid-19 e a adaptação dos serviços judiciais às medidas de controle. Devem ser lidos com cautela.",
  },
  {
    t: "2027 - recorte parcial",
    d: parcial2027.notaAnomalia,
  },
  {
    t: "Processo de elaboração",
    d: "O trabalho foi desenvolvido a partir da divisão da turma em 5 grupos e, após o levantamento dos dados, foi submetido à correção por pares, bem como a mais duas revisões finais por revisoras eleitas pela turma.",
  },
  {
    t: "Corpo de Bombeiros não separa por gênero",
    d: "Os atendimentos de agressão do Corpo de Bombeiros não distinguem o gênero da vítima, servindo apenas como indicador de contexto.",
  },
];

export default function Metodologia() {
  return (
    <section className="pb-4">
      <SectionDivider id="metodologia" kicker="Como lemos os dados" titulo="Metodologia e limites" />
      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {PONTOS.map((p, i) => (
          <div
            key={p.t}
            data-animate
            data-delay={String(i + 1)}
            className="rounded-lg border border-ink/10 bg-white/40 p-5 card-hover"
          >
            <h3 className="font-semibold text-base mb-1">{p.t}</h3>
            <p className="text-sm text-ink/70 leading-relaxed">{p.d}</p>
          </div>
        ))}
      </div>
      <p data-animate data-delay="6" className="mt-8 text-sm text-ink/60 max-w-3xl leading-relaxed">
        Fonte: {meta.fonte}. Comarca de {meta.comarca}. Período: {meta.periodo}.
      </p>
    </section>
  );
}
