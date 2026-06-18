import SectionDivider from "@/components/ui/SectionDivider";
import Callout from "@/components/ui/Callout";
import FiguraComCredito from "@/components/ui/FiguraComCredito";
import IndicadoresNacionais from "@/components/charts/IndicadoresNacionais";

export default function Problema() {
  return (
    <section className="pb-4">
      <SectionDivider
        id="problema"
        kicker="O cenario nacional"
        titulo="Quando sofrem violencia, o que as mulheres fazem?"
      />
      <p className="mt-6 text-lg text-ink/80 max-w-2xl leading-relaxed">
        Antes de olhar para a nossa cidade, e preciso entender um problema nacional: a maior
        parte das mulheres que sofrem violencia ainda nao chega aos canais oficiais de denuncia.
      </p>
      <FiguraComCredito
        className="mt-8"
        src="/img/problema-comissao.jpg"
        alt="Sessao da Comissao Permanente Mista de Combate a Violencia contra a Mulher"
        credito="Comissao de Combate a Violencia contra a Mulher. Foto: Agencia Senado (CC BY 2.0)."
      />
      <div className="mt-8 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm">
        <h3 className="font-serif font-bold text-xl mb-4">
          Como a mulher reage a violencia (Brasil, 2017 vs 2023)
        </h3>
        <IndicadoresNacionais />
      </div>
      <div className="mt-6">
        <Callout>
          Entre 2017 e 2023, caiu a procura pela delegacia comum (de 10% para 8,5%) e tambem a
          parcela de mulheres que &quot;nao fizeram nada&quot; (de 52% para 45%). Ao mesmo tempo,
          cresceu a procura pela delegacia especializada da mulher (de 11% para 14%) - sinal de que
          servicos especializados aproximam a vitima da rede de protecao.
        </Callout>
      </div>
      <p className="mt-4 text-sm text-ink/50">
        Fonte: Forum Brasileiro de Seguranca Publica / Datafolha, 2023.
      </p>
    </section>
  );
}
