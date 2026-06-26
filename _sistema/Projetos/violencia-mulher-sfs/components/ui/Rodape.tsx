import Image from "next/image";
import { meta } from "@/lib/data";

export default function Rodape() {
  return (
    <footer className="relative overflow-hidden" style={{ background: "linear-gradient(135deg, #001f0e 0%, #004d22 50%, #007a38 100%)" }}>
      {/* Logo horizontal como fundo marca-d'água */}
      <div className="absolute inset-0 flex items-center justify-end pointer-events-none select-none pr-8 opacity-10">
        <Image
          src="/img/logo-univille-horizontal.png"
          alt=""
          width={520}
          height={140}
          className="object-contain"
        />
      </div>

      {/* Faixa verde-claro topo */}
      <div className="w-full h-1" style={{ background: "#7dc242" }} />

      <div className="relative max-w-5xl mx-auto px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Logo visível */}
        <Image
          src="/img/logo-univille-horizontal.png"
          alt="Univille"
          width={180}
          height={48}
          className="object-contain brightness-0 invert w-[140px] md:w-[180px]"
        />

        {/* Info central */}
        <div className="flex flex-col items-center md:items-start gap-1 text-center md:text-left">
          <p className="text-white/90 text-sm font-semibold">
            Projeto de Extensão — Solução Consensual de Conflitos e Cultura da Paz
          </p>
          <p className="text-white/55 text-xs">
            Campus São Francisco do Sul · Turma 2025/1
          </p>
          <p className="text-white/55 text-xs">
            Orientadora: Profª Ma. Larissa Machado Barcelos
          </p>
        </div>

        {/* Data / info direita */}
        <div className="flex flex-col items-center md:items-end gap-1 text-right">
          <p className="text-white/70 text-xs uppercase tracking-widest font-semibold">
            Audiência Pública
          </p>
          <p className="text-white/90 text-sm font-bold">{meta.audienciaPublica}</p>
          <p className="text-white/40 text-xs mt-1">univille.edu.br</p>
        </div>
      </div>

      {/* Faixa verde-claro base */}
      <div className="w-full h-1.5" style={{ background: "#7dc242" }} />

      {/* Copyright */}
      <div className="w-full bg-black/30 py-2 text-center">
        <p className="text-white/40 text-[10px] tracking-wide">
          © 2026 Fenice IT Justech.ia · Todos os direitos reservados · Developed by Ramão Bueno da Silva Neto / Tech Lead
        </p>
      </div>
    </footer>
  );
}
