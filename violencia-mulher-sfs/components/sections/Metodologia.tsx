import SectionDivider from "@/components/ui/SectionDivider";
import { meta, parcial2027 } from "@/lib/data";

const PONTOS = [
  {
    t: "Dado judicial nao e o total de casos",
    d: "Os numeros referem-se a audiencias realizadas na comarca. Muitos casos nao chegam ao Judiciario - portanto, estes dados sao um piso, nao o retrato completo da violencia na cidade.",
  },
  {
    t: "2021 e 2022 provavelmente subnotificados",
    d: "Com apenas 9 e 8 audiencias, esses anos refletem registro parcial e subnotificacao, nao ausencia de crimes. Devem ser lidos com cautela.",
  },
  {
    t: "2027 e um recorte parcial",
    d: parcial2027.notaAnomalia,
  },
  {
    t: "Corpo de Bombeiros nao separa por genero",
    d: "Os atendimentos de agressao do Corpo de Bombeiros nao distinguem o genero da vitima, servindo apenas como indicador de contexto.",
  },
];

export default function Metodologia() {
  return (
    <section className="pb-4">
      <SectionDivider id="metodologia" kicker="Como lemos os dados" titulo="Metodologia e limites" />
      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {PONTOS.map((p) => (
          <div key={p.t} className="rounded-lg border border-ink/10 bg-white/40 p-5">
            <h3 className="font-semibold text-base mb-1">{p.t}</h3>
            <p className="text-sm text-ink/70 leading-relaxed">{p.d}</p>
          </div>
        ))}
      </div>
      <p className="mt-8 text-sm text-ink/60 max-w-3xl leading-relaxed">
        Fonte: {meta.fonte}. Comarca de {meta.comarca}. Periodo: {meta.periodo}. Orgaos:{" "}
        {meta.orgaos.join("; ")}. Material de uso academico e educacional, produzido para subsidiar
        o debate publico.
      </p>
    </section>
  );
}
