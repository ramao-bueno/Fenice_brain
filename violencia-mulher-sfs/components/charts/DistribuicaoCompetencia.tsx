"use client";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer,
} from "recharts";
import { competencias2026 } from "@/lib/data";
import { useMobile } from "@/hooks/useMobile";

const CORES: Record<string, string> = {
  "Comum":                             "#005c2a",
  "Juizado Especial Criminal":         "#3db554",
  "Maria da Penha":                    "#b23a48",
  "Contra Dignidade Sexual":           "#e8604c",
  "Tribunal do Júri":                  "#7dc242",
  "Ambientais":                        "#a0c878",
  "Entorpecentes":                     "#f0a500",
  "Administração Pública":             "#4a90d9",
  "Trânsito":                          "#9b59b6",
  "Crimes contra Criança/Adolescente": "#e67e22",
};

const RADIAN = Math.PI / 180;

// Label externo apenas para fatias >= 6% — evita sobreposição nas pequenas
function LabelExterno({ cx, cy, midAngle, outerRadius, percent, value }: any) {
  if (percent < 0.06) return null;
  const radius = outerRadius + 52;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  return (
    <text
      x={x} y={y}
      fill="#1a1a1a"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
      fontSize={12}
      fontWeight={700}
    >
      {`${(percent * 100).toFixed(1)}%`}
    </text>
  );
}

// Legenda customizada com % ao lado do nome
function Legenda({ data }: { data: { name: string; value: number; pct: number }[] }) {
  return (
    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 mt-4 text-sm">
      {data.map((d) => (
        <li key={d.name} className="flex items-center gap-2">
          <span
            className="inline-block w-3 h-3 rounded-full flex-shrink-0"
            style={{ background: CORES[d.name] ?? "#888" }}
          />
          <span className="text-ink/80 flex-1 truncate">{d.name}</span>
          <span className="font-semibold text-ink/60 tabular-nums ml-auto pl-2">
            {d.pct.toFixed(1)}%
          </span>
        </li>
      ))}
    </ul>
  );
}

export default function DistribuicaoCompetencia() {
  const isMobile = useMobile();
  const data = competencias2026.map((d) => ({
    name: d.competencia,
    value: d.qtd,
    pct: d.pct,
  }));

  return (
    <div>
      <ResponsiveContainer width="100%" height={isMobile ? 320 : 420}>
        <PieChart margin={isMobile ? { top: 0, right: 0, bottom: 0, left: 0 } : { top: 20, right: 90, bottom: 20, left: 90 }}>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={isMobile ? 100 : 145}
            dataKey="value"
            label={isMobile ? undefined : LabelExterno}
            labelLine={isMobile ? false : (props: any) => {
              // Oculta linha-guia para fatias pequenas
              if ((props.percent ?? 0) < 0.06) return <></>;
              return (
                <line
                  x1={props.points[0].x}
                  y1={props.points[0].y}
                  x2={props.points[1].x}
                  y2={props.points[1].y}
                  stroke="#666"
                  strokeWidth={1}
                />
              );
            }}
            isAnimationActive={false}
          >
            {data.map((entry, i) => (
              <Cell key={i} fill={CORES[entry.name] ?? "#888"} />
            ))}
          </Pie>
          <Tooltip
            formatter={(v: any, name) => {
              const item = data.find((d) => d.name === String(name ?? ""));
              return [`${v} audiências (${item?.pct.toFixed(1)}%)`, String(name ?? "")];
            }}
          />
        </PieChart>
      </ResponsiveContainer>

      <Legenda data={data} />
    </div>
  );
}
