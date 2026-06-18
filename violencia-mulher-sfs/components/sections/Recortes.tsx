import SectionDivider from "@/components/ui/SectionDivider";
import Callout from "@/components/ui/Callout";
import BigStat from "@/components/ui/BigStat";
import { recortes } from "@/lib/data";

export default function Recortes() {
  return (
    <section className="pb-4">
      <SectionDivider id="recortes" kicker="Por tras dos numeros" titulo="Recortes que doem" />
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-8">
        <BigStat
          tom="alerta"
          valor="1"
          rotulo="feminicidio levado a juri (2025)"
          nota={`Processo ${recortes.feminicidio.processo}`}
        />
        <BigStat
          tom="alerta"
          valor="28 anos"
          rotulo="a espera mais longa por um julgamento"
          nota="Processo de 1998 julgado so em 2026"
        />
        <BigStat
          tom="alerta"
          valor="94"
          rotulo="atendimentos de agressao pelo Corpo de Bombeiros (2025)"
          nota={`${recortes.bombeiros.a2026Parcial} ocorrencias ate ${recortes.bombeiros.a2026Ate}`}
        />
      </div>
      <div className="mt-8">
        <Callout>
          {recortes.bombeiros.limitacao} Por isso, esse numero deve ser lido como um indicador de
          contexto, nao como total de casos contra mulheres.
        </Callout>
      </div>
    </section>
  );
}
