"use client";
import { useEffect, useRef, useState } from "react";

function parseValor(valor: string) {
  const m = valor.match(/^([^0-9]*)(\d+)(.*)$/);
  if (!m) return null;
  return { prefix: m[1], num: parseInt(m[2], 10), suffix: m[3] };
}

function easeOut(t: number) {
  return 1 - Math.pow(1 - t, 3);
}

export default function BigStat({
  valor,
  rotulo,
  nota,
  tom = "default",
}: {
  valor: string;
  rotulo: string;
  nota?: string;
  tom?: "default" | "alerta";
}) {
  const parsed = parseValor(valor);
  const [exibido, setExibido] = useState(
    parsed ? `${parsed.prefix}0${parsed.suffix}` : valor
  );
  const ref = useRef<HTMLDivElement>(null);
  const iniciado = useRef(false);

  useEffect(() => {
    if (!parsed || iniciado.current) return;
    const el = ref.current;
    if (!el) return;

    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !iniciado.current) {
          iniciado.current = true;
          obs.disconnect();

          const duracao = parsed.num <= 5 ? 600 : 1400;
          const inicio = performance.now();

          const tick = (agora: number) => {
            const t = Math.min((agora - inicio) / duracao, 1);
            const val = Math.round(easeOut(t) * parsed.num);
            setExibido(`${parsed.prefix}${val}${parsed.suffix}`);
            if (t < 1) requestAnimationFrame(tick);
          };

          requestAnimationFrame(tick);
        }
      },
      { threshold: 0.5 }
    );

    obs.observe(el);
    return () => obs.disconnect();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div ref={ref} className="flex flex-col gap-1">
      <span
        className={`font-serif font-black leading-none whitespace-nowrap text-5xl sm:text-4xl md:text-5xl lg:text-7xl tabular-nums ${
          tom === "alerta" ? "text-alerta" : "text-verde"
        }`}
      >
        {exibido}
      </span>
      <span className="font-sans font-semibold text-base md:text-lg">{rotulo}</span>
      {nota && <span className="text-sm text-ink/60">{nota}</span>}
    </div>
  );
}
