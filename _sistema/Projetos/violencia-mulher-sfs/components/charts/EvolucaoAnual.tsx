"use client";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { audienciasAnuais } from "@/lib/data";
import { useMobile } from "@/hooks/useMobile";

const CORES = ["#001f0e", "#004d22", "#005c2a", "#007a38", "#3db554", "#7dc242", "#a0c878"];

const RADIAN = Math.PI / 180;

function LabelExterno({ cx, cy, midAngle, outerRadius, percent, name }: any) {
  if (percent < 0.05) return null;
  const r = outerRadius + 48;
  const x = cx + r * Math.cos(-midAngle * RADIAN);
  const y = cy + r * Math.sin(-midAngle * RADIAN);
  return (
    <text x={x} y={y} fill="#1a1a1a" textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central" fontSize={12} fontWeight={600}>
      {`${(percent * 100).toFixed(1)}%`}
    </text>
  );
}

export default function EvolucaoAnual() {
  const isMobile = useMobile();
  const data = audienciasAnuais.map((d) => ({ name: String(d.ano), value: d.total }));

  return (
    <div>
      <ResponsiveContainer width="100%" height={isMobile ? 240 : 360}>
        <PieChart margin={isMobile
          ? { top: 0, right: 0, bottom: 0, left: 0 }
          : { top: 24, right: 80, bottom: 24, left: 80 }}>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={isMobile ? 88 : 120}
            dataKey="value"
            label={isMobile ? undefined : LabelExterno}
            labelLine={isMobile ? false : (props: any) => {
              if ((props.percent ?? 0) < 0.05) return <></>;
              return <line x1={props.points[0].x} y1={props.points[0].y}
                x2={props.points[1].x} y2={props.points[1].y}
                stroke="#888" strokeWidth={1} />;
            }}
            isAnimationActive={false}
          >
            {data.map((_, i) => <Cell key={i} fill={CORES[i % CORES.length]} />)}
          </Pie>
          <Tooltip formatter={(v: any, name) => [`${v} audiências`, `Ano ${String(name ?? "")}`]} />
        </PieChart>
      </ResponsiveContainer>

      {/* Legenda HTML fora do SVG — sem risco de sobreposição */}
      <div className="flex flex-wrap justify-center gap-x-5 gap-y-2 mt-3 text-sm">
        {data.map((d, i) => (
          <span key={d.name} className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-full flex-shrink-0"
              style={{ background: CORES[i % CORES.length] }} />
            {d.name}
          </span>
        ))}
      </div>
    </div>
  );
}
