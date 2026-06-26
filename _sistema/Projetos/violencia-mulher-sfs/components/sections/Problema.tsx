import SectionDivider from "@/components/ui/SectionDivider";
import Callout from "@/components/ui/Callout";
import IndicadoresNacionais from "@/components/charts/IndicadoresNacionais";

export default function Problema() {
  return (
    <section className="pb-4">
      <SectionDivider id="problema" kicker="O cenário nacional" titulo="Quando sofrem violência, o que as mulheres fazem?" />

      <div data-animate data-delay="1"
        className="mt-8 rounded-2xl p-6 md:p-8 text-white"
        style={{ background: "linear-gradient(135deg, #005c2a 0%, #007a38 100%)" }}
      >
        <p className="text-lg md:text-xl leading-relaxed font-medium">
          Antes de olhar para a nossa cidade, é preciso entender um problema nacional: a maior
          parte das mulheres que sofrem violência ainda <strong>não chega</strong> aos canais
          oficiais de denúncia.
        </p>
        <p className="mt-4 text-sm text-white/70">
          Fonte: Fórum Brasileiro de Segurança Pública / Datafolha, 2023.
        </p>
      </div>

      <div data-animate data-delay="2" className="mt-8 rounded-xl border border-ink/10 bg-white/60 p-6 shadow-sm card-hover">
        <h3 className="font-serif font-bold text-xl mb-4">
          Como a mulher reage à violência — Brasil, 2017 vs 2023
        </h3>
        <IndicadoresNacionais />
      </div>

      <div data-animate data-delay="3" className="mt-6">
        <Callout>
          Entre 2017 e 2023, caiu a procura pela delegacia comum (de 10% para 8,5%) e também a
          parcela de mulheres que &quot;não fizeram nada&quot; (de 52% para 45%). Ao mesmo tempo,
          cresceu a procura pela delegacia especializada da mulher (de 11% para 14%) — sinal de que
          serviços especializados aproximam a vítima da rede de proteção.
        </Callout>
      </div>
    </section>
  );
}
