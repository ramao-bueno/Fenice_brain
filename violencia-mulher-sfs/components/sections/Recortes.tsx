import SectionDivider from "@/components/ui/SectionDivider";
import Callout from "@/components/ui/Callout";
import BigStat from "@/components/ui/BigStat";
import { recortes } from "@/lib/data";

export default function Recortes() {
  return (
    <section className="pb-4">
      <SectionDivider id="recortes" kicker="Sinais de alerta" titulo="Indicadores em destaque" />
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-8">
        {[
          { valor: "1",       rotulo: "feminicídio levado a júri (2025)",              nota: "Em todo o período analisado, apenas um feminicídio foi objeto de julgado pelo Tribunal do Júri", delay: "1" },
          { valor: "28 anos", rotulo: "a espera mais longa por um julgamento",         nota: "Processo de 1998 julgado só em 2026",                                                        delay: "2" },
          { valor: "94",      rotulo: "atendimentos de agressão pelo Corpo de Bombeiros Voluntários de São Francisco do Sul (2025)", nota: `${recortes.bombeiros.a2026Parcial} ocorrências até ${recortes.bombeiros.a2026Ate}`, delay: "3" },
        ].map((s) => (
          <div key={s.rotulo} data-animate data-delay={s.delay}>
            <BigStat tom="alerta" valor={s.valor} rotulo={s.rotulo} nota={s.nota} />
          </div>
        ))}
      </div>
      <div data-animate data-delay="4" className="mt-8">
        <Callout>
          {recortes.bombeiros.limitacao} Por isso, esse número deve ser lido como um indicador de
          contexto, não como total de casos contra mulheres.
        </Callout>
      </div>
    </section>
  );
}
