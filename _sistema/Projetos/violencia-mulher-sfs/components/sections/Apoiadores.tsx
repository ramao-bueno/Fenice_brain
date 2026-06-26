import Image from "next/image";
import { QRCodeSVG } from "qrcode.react";
import FormApoiadores from "./FormApoiadores";

const URL_PAGINA = "https://observatorio-da-mulher-sfs.com.br";

const ACADEMICOS = [
  "Adilson João de Oliveira",
  "Adriane Cristina Maia de Lima",
  "Aimee Emanuela dos Santos",
  "Ana Clara Baptista",
  "Ana Luiza de Souza",
  "Denny Marcelo Moggi",
  "Driele de Cassia Costa da Silva",
  "Elissa Wagner Telles Schneider",
  "Giulia dos Reis Pereira",
  "Helena de Borba Santos",
  "Helena Nascimento Agacy",
  "Isadora Barasuol Carbonera",
  "Jane Kelli Aparecida Alves da Silva Pereira",
  "João Henrique Pikulski",
  "Juliana Correia Silva",
  "Kaique Olejuki",
  "Léo Vycthor Maçaneiro",
  "Lorena Bianca Machado",
  "Luciana Dominoni Doria",
  "Maria Clara Bispo dos Santos",
  "Ramão Bueno da Silva Neto",
  "Ricardo Gomes Ferreira",
  "Ricardo Luiz Fernandes",
  "Samuel Luiz Duarte Serpa",
  "Sandy Isabella Dainelli",
];

export default function Apoiadores() {
  return (
    <section
      id="apoiadores"
      className="relative min-h-screen overflow-hidden text-white"
      style={{ background: "linear-gradient(145deg, #001f0e 0%, #004d22 35%, #007a38 65%, #3db554 88%, #7dc242 100%)" }}
    >
      {/* ── Luzes decorativas ── */}
      <div className="pointer-events-none select-none absolute inset-0 overflow-hidden">
        {/* Bloom topo-centro — luz principal */}
        <div
          className="absolute -top-20 left-1/2 -translate-x-1/2 w-[700px] h-[400px] rounded-full hero-pulso"
          style={{ background: "radial-gradient(ellipse at center, rgba(125,194,66,0.22) 0%, transparent 70%)" }}
        />
        {/* Spot topo-direita */}
        <div
          className="absolute -top-32 -right-32 w-[560px] h-[560px] rounded-full"
          style={{ background: "radial-gradient(circle, rgba(125,194,66,0.18) 0%, transparent 65%)", opacity: 0.9 }}
        />
        {/* Luz diagonal esquerda */}
        <div
          className="absolute top-1/3 -left-24 w-[420px] h-[420px] rounded-full hero-pulso"
          style={{ background: "radial-gradient(circle, rgba(61,181,84,0.15) 0%, transparent 70%)", animationDelay: "3s" }}
        />
        {/* Spot base-direita */}
        <div
          className="absolute -bottom-20 right-1/4 w-[380px] h-[380px] rounded-full"
          style={{ background: "radial-gradient(circle, rgba(0,92,42,0.30) 0%, transparent 65%)" }}
        />
        {/* Brilho base-esquerda */}
        <div
          className="absolute -bottom-28 -left-28 w-[500px] h-[500px] rounded-full hero-pulso"
          style={{ background: "radial-gradient(circle, rgba(0,77,34,0.20) 0%, transparent 70%)", animationDelay: "5s" }}
        />
      </div>

      {/* Faixa decorativa topo */}
      <div className="w-full h-1" style={{ background: "#7dc242" }} />

      {/* -5% zoom: py reduzido, gaps menores, textos um step abaixo */}
      <div className="relative max-w-6xl mx-auto px-4 py-12 md:py-18 flex flex-col gap-12">

        {/* ── Header com logo ── */}
        <div className="flex flex-col sm:flex-row items-center gap-5">
          <div className="bg-white rounded-2xl p-3 shadow-2xl flex-shrink-0 w-24 sm:w-32 md:w-40">
            <Image src="/img/logo-univille.png" alt="Univille" width={148} height={148} className="object-contain" />
          </div>
          <div>
            <p className="text-white/60 text-xs uppercase tracking-widest font-semibold mb-1">
              UNIVILLE — Campus São Francisco do Sul
            </p>
            <h2 className="font-serif font-black text-xl md:text-2xl lg:text-4xl leading-tight">
              Apoie este Projeto
            </h2>
            <p className="text-white/70 mt-1.5 text-sm max-w-xl">
              Cada apoiador fortalece a rede de proteção às mulheres de São Francisco do Sul.
              Deixe seu contato e faça parte desta causa.
            </p>
          </div>
        </div>

        {/* ── Corpo: acadêmicos + formulário ── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">

          {/* Card dos Acadêmicos */}
          <div
            className="rounded-2xl p-5 md:p-7 shadow-2xl"
            style={{ background: "rgba(0,0,0,0.40)", border: "1px solid rgba(125,194,66,0.25)" }}
          >
            <div className="flex items-center gap-3">
              <span
                className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-black flex-shrink-0"
                style={{ background: "#7dc242", color: "#001f0e" }}
              >✦</span>
              <div>
                <h3 className="font-serif font-bold text-base md:text-lg text-white leading-tight">
                  Acadêmicos — Turma 2025/1
                </h3>
                <p className="text-white/50 text-xs mt-0.5">
                  Curso de Direito · UNIVILLE Campus São Francisco do Sul
                </p>
              </div>
            </div>

            <div className="border-t border-white/15 mt-4 mb-4" />

            <div className="grid grid-cols-2 gap-x-4 gap-y-1.5">
              {ACADEMICOS.map((nome, i) => (
                <div key={i} className="flex items-baseline gap-2 min-w-0">
                  <span
                    className="font-mono text-xs flex-shrink-0 w-5 text-right"
                    style={{ color: "#7dc242" }}
                  >
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span className="text-white/85 text-xs font-serif leading-snug truncate">
                    {nome}
                  </span>
                </div>
              ))}
            </div>

            <div className="border-t border-white/15 mt-4 pt-3 flex flex-col gap-1">
              <p className="text-xs text-white/70">
                <span className="font-semibold" style={{ color: "#7dc242" }}>Orientadora:</span>{" "}
                Profª Ma. Larissa Machado Barcelos
              </p>
              <p className="text-xs text-white/45">
                Componente Curricular: Solução Consensual de Conflitos e Cultura da Paz
              </p>
            </div>
          </div>

          {/* Formulário + QR code */}
          <div className="flex flex-col gap-6">

            <div
              className="rounded-2xl p-5 md:p-7 shadow-2xl"
              style={{ background: "rgba(0,0,0,0.40)", border: "1px solid rgba(125,194,66,0.25)" }}
            >
              <h3 className="font-serif font-bold text-lg mb-5 flex items-center gap-2">
                <span className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-black"
                  style={{ background: "#7dc242", color: "#001f0e" }}>✦</span>
                Cadastro de Apoiadores
              </h3>
              <FormApoiadores />
            </div>

            <div
              className="rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row items-center gap-5"
              style={{ background: "rgba(0,0,0,0.40)", border: "1px solid rgba(125,194,66,0.25)" }}
            >
              <div className="bg-white rounded-xl p-2.5 shadow-lg flex-shrink-0">
                <QRCodeSVG
                  value={URL_PAGINA}
                  size={96}
                  bgColor="#ffffff"
                  fgColor="#005c2a"
                  level="H"
                />
              </div>
              <div className="flex flex-col gap-1.5 text-center sm:text-left">
                <p className="font-semibold text-white text-sm">Acesse nossa página oficial</p>
                <p className="text-white/50 text-xs break-all">{URL_PAGINA}</p>
                <p className="text-white/40 text-xs">
                  Aponte a câmera do celular para o QR code
                </p>
              </div>
            </div>

          </div>
        </div>

        {/* ── Rodapé da seção ── */}
        <div
          className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t text-xs text-white/35"
          style={{ borderColor: "rgba(125,194,66,0.2)" }}
        >
          <div className="flex items-center gap-3">
            <div className="bg-white/10 rounded-lg px-3 py-1.5 backdrop-blur">
              <Image
                src="/img/logo-univille-horizontal.png"
                alt="Univille"
                width={80}
                height={22}
                className="object-contain brightness-0 invert opacity-60"
              />
            </div>
            <span>Projeto de Extensão 2025/1</span>
          </div>

<p className="tracking-widest uppercase font-semibold text-white/25">
            Desenvolvido por&nbsp;
            <span className="text-[#7dc242]/60 font-bold">Fenice IT</span>
            &nbsp;— São Francisco do Sul, SC
          </p>
        </div>

      </div>

      {/* Faixa decorativa base */}
      <div className="w-full h-1.5" style={{ background: "#7dc242" }} />
    </section>
  );
}
