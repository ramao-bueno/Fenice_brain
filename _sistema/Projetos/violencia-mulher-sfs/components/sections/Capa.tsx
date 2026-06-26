import Image from "next/image";
import { meta } from "@/lib/data";

export default function Capa() {
  return (
    <section
      id="capa"
      className="relative min-h-screen flex flex-col items-center justify-between text-white overflow-hidden"
      style={{ background: "linear-gradient(160deg, #001f0e 0%, #004d22 30%, #007a38 60%, #3db554 80%, #7dc242 100%)" }}
    >
      {/* Pulso ambiental — radial verde que respira */}
      <div
        className="absolute inset-0 pointer-events-none select-none hero-pulso"
        style={{ background: "radial-gradient(ellipse 80% 55% at 65% 35%, rgba(125,194,66,0.14) 0%, transparent 70%)" }}
      />

      {/* Faixa decorativa superior */}
      <div className="w-full h-1.5" style={{ background: "#7dc242" }} />

      {/* Conteúdo central */}
      <div className="flex-1 flex flex-col items-center justify-center gap-10 px-6 py-16 text-center max-w-3xl mx-auto">
        {/* Logo */}
        <div className="hero-logo bg-white rounded-2xl p-6 shadow-2xl w-44 md:w-56 flex items-center justify-center">
          <Image
            src="/img/logo-univille.png"
            alt="Logo Univille"
            width={180}
            height={180}
            className="object-contain"
          />
        </div>

        {/* Identificação institucional */}
        <div className="hero-inst flex flex-col gap-1">
          <p className="font-sans text-xs md:text-sm uppercase tracking-widest text-white/70 font-semibold">
            Universidade da Região de Joinville — UNIVILLE
          </p>
          <p className="font-sans text-sm md:text-base text-white/80 font-medium">
            Campus São Francisco do Sul
          </p>
        </div>

        {/* Divisor */}
        <div className="hero-div w-16 h-0.5 bg-white/40 rounded-full" />

        {/* Título principal */}
        <div className="hero-title flex flex-col gap-4">
          <p className="font-sans text-xs md:text-sm uppercase tracking-widest text-white/60 font-semibold">
            Projeto de Extensão — Solução Consensual de Conflitos e Cultura da Paz
          </p>
          <h1 className="font-serif font-black text-3xl md:text-5xl lg:text-6xl leading-tight">
            Observatório de Dados de Violência contra a Mulher
          </h1>
          <p className="font-sans text-base md:text-xl text-white/85 font-medium">
            São Francisco do Sul — SC / BR
          </p>
          <p className="font-sans text-sm md:text-base text-white/70 max-w-xl mx-auto leading-relaxed mt-2">
            Análise dos dados judiciais de 2021 a 2027 e propostas de política pública para o município.
          </p>
        </div>

        {/* Divisor */}
        <div className="hero-div w-16 h-0.5 bg-white/40 rounded-full" />

        {/* Autores e orientação */}
        <div className="hero-autor flex flex-col gap-2 text-sm md:text-base text-white/80">
          <p className="font-medium">Acadêmicos Turma 2025/1</p>
          <p className="text-white/60 text-sm">Orientadora: Profª Ma. Larissa Machado Barcelos</p>
        </div>
      </div>

      {/* Rodapé da capa */}
      <div className="hero-foot w-full flex flex-col items-center gap-2 pb-8 px-6">
        <div className="w-full max-w-3xl flex items-center justify-between text-xs text-white/50 border-t border-white/20 pt-4">
          <span>Audiência Pública: {meta.audienciaPublica}</span>
          <span className="uppercase tracking-widest">univille.edu.br</span>
        </div>
      </div>

      {/* Faixa decorativa inferior */}
      <div className="w-full h-1.5" style={{ background: "#7dc242" }} />
    </section>
  );
}
