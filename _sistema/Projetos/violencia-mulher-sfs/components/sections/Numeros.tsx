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
      <SectionDivider id="numeros" kicker="São Francisco do Sul" titulo="Os números da nossa comarca" />

      <div data-animate data-delay="1" className="mt-8 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm card-hover overflow-hidden">
        <h3 className="font-serif font-bold text-xl mb-4">Audiências criminais por ano (2021–2025)</h3>
        <EvolucaoAnual />
      </div>

      <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-6">
        {crescimento.map((c, i) => (
          <div key={c.para} data-animate data-delay={String(i + 2)}>
            <BigStat
              valor={`+${c.pct}%`}
              rotulo={`${c.de} para ${c.para}`}
              nota="crescimento de audiências"
            />
          </div>
        ))}
      </div>

      <div data-animate data-delay="1" className="mt-12 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm card-hover">
        <h3 className="font-serif font-bold text-xl mb-1">Por competência em 2026</h3>
        <p className="text-sm text-ink/60 mb-4">399 audiências — ano quase completo (sem dados para o mês de dezembro).</p>
        <DistribuicaoCompetencia />
      </div>

      <p data-animate data-delay="2" className="mt-6 font-serif text-2xl md:text-3xl font-bold text-verde max-w-3xl leading-snug">
        Maria da Penha somada aos crimes contra a dignidade sexual já representa 31% das audiências de 2026.
      </p>

      <div data-animate data-delay="1" className="mt-12 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm card-hover">
        <h3 className="font-serif font-bold text-xl mb-4">
          A incidência dos crimes de gênero e sexuais na pauta de audiências cresce
        </h3>
        <GeneroShare />
      </div>

      <div data-animate data-delay="2" className="mt-6">
        <Callout>
          Em 2021 e 2022, os registros de Maria da Penha eram praticamente inexistentes na comarca
          (zero casos). Em poucos anos, a soma de Maria da Penha e crimes sexuais salta para cerca
          de 31% das audiências. A leitura mais provável não é apenas &quot;mais crime&quot;: é
          também maior número de denúncias e mais estrutura de apoio à mulher, indicando possível diminuição da subnotificação.
        </Callout>
      </div>
    </section>
  );
}
