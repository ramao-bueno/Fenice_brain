import Image from "next/image";
import { meta } from "@/lib/data";

export default function Abertura() {
  return (
    <section id="topo" className="relative isolate overflow-hidden text-white scroll-mt-20">
      <Image
        src="/img/hero-sfs.jpg"
        alt="Rua do centro historico de Sao Francisco do Sul"
        fill
        className="object-cover -z-10"
        sizes="100vw"
      />
      <div
        className="absolute inset-0 -z-10"
        style={{ background: "linear-gradient(135deg, rgba(0,58,40,0.94) 0%, rgba(0,104,71,0.80) 100%)" }}
      />
      <div className="max-w-5xl mx-auto px-4 py-24 md:py-32 flex flex-col gap-6">
        <p className="font-sans uppercase tracking-widest text-xs md:text-sm text-white/80 font-semibold">
          Projeto de extensao - UNIVILLE, Campus Sao Francisco do Sul
        </p>
        <h1 className="font-serif font-black leading-[1.05] text-4xl md:text-6xl lg:text-7xl max-w-3xl">
          Violencia contra a mulher em Sao Francisco do Sul
        </h1>
        <p className="font-sans text-lg md:text-2xl text-white/90 max-w-2xl">
          O que os dados judiciais de 2021 a 2027 revelam - e o que a cidade pode fazer agora.
        </p>
        <div className="mt-6 text-sm md:text-base text-white/80 max-w-2xl leading-relaxed">
          <p>Ana Clara Baptista, Ana Luiza de Souza Alves, Isadora Barasuol Carbonera e Jane Kelly Pereira.</p>
          <p>Orientacao: Profa. Me. Larissa Machado Barcelos.</p>
        </div>
        <div className="mt-4 inline-flex w-fit items-center gap-2 rounded-full bg-white/15 px-4 py-2 text-sm font-semibold backdrop-blur">
          Audiencia publica: {meta.audienciaPublica}
        </div>
      </div>
    </section>
  );
}
