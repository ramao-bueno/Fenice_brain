import { meta, creditosImagens } from "@/lib/data";

export default function Creditos() {
  return (
    <footer
      className="mt-20 text-white"
      style={{ background: "linear-gradient(135deg, #00432e 0%, #00271b 100%)" }}
    >
      <div className="max-w-5xl mx-auto px-4 py-14 flex flex-col gap-8">
        <p className="font-serif font-black text-2xl">Observatório da Mulher SFS</p>
        <div className="grid gap-8 md:grid-cols-3 text-sm text-white/80 leading-relaxed">
          <div>
            <h3 className="font-semibold text-white mb-2">Dados</h3>
            <p>{meta.fonte}</p>
            <p>Comarca de {meta.comarca}</p>
            <p>Período: {meta.periodo}</p>
          </div>
          <div>
            <h3 className="font-semibold text-white mb-2">Autoria</h3>
            <p>Acadêmicos Turma 2025/1</p>
            <p className="mt-1">Orientadora: Profª Ma. Larissa Machado Barcelos</p>
            <p className="mt-1">Projeto de Extensão — UNIVILLE, Campus São Francisco do Sul</p>
          </div>
          <div>
            <h3 className="font-semibold text-white mb-2">Créditos de imagem</h3>
            {creditosImagens.length === 0 ? (
              <p className="text-white/60">Imagens próprias / a creditar.</p>
            ) : (
              <ul className="space-y-1">
                {creditosImagens.map((c) => (
                  <li key={c.arquivo}>
                    <a href={c.url} target="_blank" rel="noreferrer" className="underline hover:text-white">
                      {c.autor}
                    </a>{" "}
                    — {c.fonte} ({c.licenca})
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="border-t border-white/15 pt-5 text-xs text-white/45 text-center leading-relaxed">
          © 2026 Fenice It Justech.ia. Todos os direitos reservados.
          {" "}Developed by Ramão Bueno da Silva Neto / Tech Lead
        </div>
      </div>
    </footer>
  );
}
