"use client";
import { useEffect, useState } from "react";

const ABAS = [
  { id: "problema", label: "O problema" },
  { id: "numeros", label: "Os numeros" },
  { id: "recortes", label: "Recortes" },
  { id: "propostas", label: "Propostas" },
  { id: "metodologia", label: "Metodologia" },
];

export default function TabNav() {
  const [ativa, setAtiva] = useState<string>("");
  const [aberto, setAberto] = useState(false);

  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) setAtiva(e.target.id);
        }),
      { rootMargin: "-40% 0px -55% 0px" }
    );
    ABAS.forEach((a) => {
      const el = document.getElementById(a.id);
      if (el) obs.observe(el);
    });
    return () => obs.disconnect();
  }, []);

  return (
    <header className="sticky top-0 z-50 bg-areia/90 backdrop-blur border-b border-ink/10">
      <nav className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <a href="#topo" className="font-serif font-black text-lg tracking-tight">
          SFS pela Mulher
        </a>
        <button
          className="md:hidden text-sm font-semibold px-2 py-1"
          onClick={() => setAberto((v) => !v)}
          aria-expanded={aberto}
          aria-label="Abrir menu de navegacao"
        >
          {aberto ? "Fechar" : "Menu"}
        </button>
        <ul className="hidden md:flex gap-6 text-sm">
          {ABAS.map((a) => (
            <li key={a.id}>
              <a
                href={`#${a.id}`}
                className={`hover:text-verde transition-colors ${
                  ativa === a.id ? "text-verde font-semibold" : "text-ink/70"
                }`}
              >
                {a.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      {aberto && (
        <ul className="md:hidden px-4 pb-3 flex flex-col gap-1 text-sm border-t border-ink/10">
          {ABAS.map((a) => (
            <li key={a.id}>
              <a
                href={`#${a.id}`}
                onClick={() => setAberto(false)}
                className={`block py-2 ${ativa === a.id ? "text-verde font-semibold" : "text-ink/80"}`}
              >
                {a.label}
              </a>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}
