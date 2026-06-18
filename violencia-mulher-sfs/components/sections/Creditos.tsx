import { meta, creditosImagens } from "@/lib/data";

export default function Creditos() {
  return (
    <footer
      className="mt-20 text-white"
      style={{ background: "linear-gradient(135deg, #00432e 0%, #00271b 100%)" }}
    >
      <div className="max-w-5xl mx-auto px-4 py-14 flex flex-col gap-8">
        <p className="font-serif font-black text-2xl">Sao Francisco do Sul pela Mulher</p>
        <div className="grid gap-8 md:grid-cols-3 text-sm text-white/80 leading-relaxed">
          <div>
            <h3 className="font-semibold text-white mb-2">Dados</h3>
            <p>{meta.fonte}</p>
            <p>Comarca de {meta.comarca}</p>
            <p>Periodo: {meta.periodo}</p>
          </div>
          <div>
            <h3 className="font-semibold text-white mb-2">Autoria</h3>
            <p>Ana Clara Baptista, Ana Luiza de Souza Alves, Isadora Barasuol Carbonera e Jane Kelly Pereira.</p>
            <p className="mt-1">Orientacao: Profa. Me. Larissa Machado Barcelos.</p>
            <p className="mt-1">Projeto de extensao - UNIVILLE, Campus Sao Francisco do Sul.</p>
          </div>
          <div>
            <h3 className="font-semibold text-white mb-2">Creditos de imagem</h3>
            {creditosImagens.length === 0 ? (
              <p className="text-white/60">Imagens proprias / a creditar.</p>
            ) : (
              <ul className="space-y-1">
                {creditosImagens.map((c) => (
                  <li key={c.arquivo}>
                    <a href={c.url} target="_blank" rel="noreferrer" className="underline hover:text-white">
                      {c.autor}
                    </a>{" "}
                    - {c.fonte} ({c.licenca})
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </footer>
  );
}
