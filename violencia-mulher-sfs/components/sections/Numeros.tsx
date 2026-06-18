import SectionDivider from "@/components/ui/SectionDivider";
import Callout from "@/components/ui/Callout";
import BigStat from "@/components/ui/BigStat";
import EvolucaoAnual from "@/components/charts/EvolucaoAnual";
import DistribuicaoCompetencia from "@/components/charts/DistribuicaoCompetencia";
import GeneroShare from "@/components/charts/GeneroShare";
import { crescimento } from "@/lib/data";

export default function Numeros() {
  return (
    <section className="pb-4">
      <SectionDivider id="numeros" kicker="Sao Francisco do Sul" titulo="Os numeros da nossa comarca" />

      <div className="mt-8 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm">
        <h3 className="font-serif font-bold text-xl mb-4">Audiencias criminais por ano (2021-2025)</h3>
        <EvolucaoAnual />
      </div>
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-6">
        {crescimento.map((c) => (
          <BigStat
            key={c.para}
            valor={`+${c.pct}%`}
            rotulo={`${c.de} para ${c.para}`}
            nota="crescimento de audiencias"
          />
        ))}
      </div>

      <div className="mt-12 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm">
        <h3 className="font-serif font-bold text-xl mb-1">Por competencia em 2026</h3>
        <p className="text-sm text-ink/60 mb-4">399 audiencias - ano quase completo (falta dezembro).</p>
        <DistribuicaoCompetencia />
      </div>
      <p className="mt-6 font-serif text-2xl md:text-3xl font-bold text-verde max-w-3xl leading-snug">
        Maria da Penha somada aos crimes contra a dignidade sexual ja representa 31% das audiencias de 2026.
      </p>

      <div className="mt-12 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm">
        <h3 className="font-serif font-bold text-xl mb-4">
          A participacao dos crimes de genero e sexuais cresce
        </h3>
        <GeneroShare />
      </div>
      <div className="mt-6">
        <Callout>
          Em 2021 e 2022, os registros de Maria da Penha eram praticamente inexistentes na comarca
          (zero casos). Em poucos anos, a soma de Maria da Penha e crimes sexuais salta para cerca
          de 31% das audiencias. A leitura mais provavel nao e apenas &quot;mais crime&quot;: e
          tambem mais denuncia e mais estrutura registrando o que antes ficava invisivel.
        </Callout>
      </div>
    </section>
  );
}
