import Image from "next/image";
import { meta } from "@/lib/data";

const ease = "cubic-bezier(0.22, 1, 0.36, 1)";

export default function Abertura() {
  return (
    <section id="topo" className="relative isolate overflow-hidden text-white scroll-mt-20">
      <Image
        src="/img/hero-sfs.jpg"
        alt="Rua do centro histórico de São Francisco do Sul"
        fill
        className="object-cover -z-10"
        sizes="100vw"
        priority
      />
      <div
        className="absolute inset-0 -z-10"
        style={{ background: "linear-gradient(135deg, rgba(0,31,14,0.97) 0%, rgba(0,77,34,0.93) 35%, rgba(0,130,60,0.88) 65%, rgba(61,181,84,0.80) 85%, rgba(125,194,66,0.65) 100%)" }}
      />

      {/* padding topo reduzido — texto mais colado ao nav */}
      <div className="max-w-5xl mx-auto px-4 pt-8 pb-12 md:pt-10 md:pb-16 lg:pt-12 lg:pb-20 flex flex-col gap-5">

        {/* Logo — escala */}
        <div
          className="flex items-center gap-3"
          style={{ animation: `heroEscala 0.7s ${ease} forwards`, opacity: 0 }}
        >
          <div className="bg-white rounded-xl p-2 shadow-lg flex-shrink-0">
            <Image src="/img/logo-univille.png" alt="Logo Univille" width={48} height={48} className="object-contain" />
          </div>
          <div className="flex flex-col">
            <span className="font-sans font-bold text-xs uppercase tracking-widest text-white/90 leading-tight">
              UNIVILLE — Campus São Francisco do Sul
            </span>
            <span className="font-sans text-xs text-white/60 tracking-wide mt-0.5">
              PROJETO DE EXTENSÃO / SOLUÇÃO CONSENSUAL DE CONFLITOS E CULTURA DA PAZ
            </span>
          </div>
        </div>

        {/* Título — slide da esquerda — -5% menor */}
        <h1
          className="font-serif font-black leading-[1.05] text-3xl md:text-5xl lg:text-6xl max-w-3xl mt-1 break-words"
          style={{ animation: `heroEsquerda 0.9s ${ease} 0.15s forwards`, opacity: 0 }}
        >
          Observatório de Dados de Violência contra a Mulher — São Francisco do Sul/SC
        </h1>

        {/* Subtítulo */}
        <p
          className="font-sans text-base md:text-xl text-white/90 max-w-2xl"
          style={{ animation: `heroFade 0.9s ${ease} 0.35s forwards`, opacity: 0 }}
        >
          O que os dados judiciais de 2021 a 2027 revelam — e o que a cidade pode fazer agora.
        </p>

        {/* Autores */}
        <div
          className="mt-1 text-sm text-white/80 max-w-2xl leading-relaxed"
          style={{ animation: `heroFade 0.9s ${ease} 0.5s forwards`, opacity: 0 }}
        >
          <p className="font-medium">Acadêmicos Turma 2025/1</p>
          <p className="text-white/65 text-sm mt-0.5">Orientadora: Profª Ma. Larissa Machado Barcelos</p>
        </div>

        {/* Badge */}
        <div
          className="mt-1 inline-flex flex-wrap w-fit items-center gap-2 rounded-full px-4 py-1.5 text-sm font-semibold backdrop-blur border border-white/30"
          style={{
            background: "rgba(125,194,66,0.25)",
            animation: `heroFade 0.9s ${ease} 0.65s forwards`,
            opacity: 0,
          }}
        >
          Audiência Pública: {meta.audienciaPublica}
        </div>
      </div>

      <div className="w-full h-1" style={{ background: "#7dc242" }} />
    </section>
  );
}
