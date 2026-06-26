"use client";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { indicadoresNacionais } from "@/lib/data";
import { useMobile } from "@/hooks/useMobile";

const CORES = ["#005c2a", "#7dc242", "#b23a48", "#f0a500"];
const RADIAN = Math.PI / 180;

function LabelExterno({ cx, cy, midAngle, outerRadius, percent }: any) {
  if (percent < 0.12) return null;
  const r = outerRadius + 44;
  const x = cx + r * Math.cos(-midAngle * RADIAN);
  const y = cy + r * Math.sin(-midAngle * RADIAN);
  return (
    <text x={x} y={y} fill="#1a1a1a" textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central" fontSize={12} fontWeight={600}>
      {`${(percent * 100).toFixed(1)}%`}
    </text>
  );
}

export default function IndicadoresNacionais() {
  const isMobile = useMobile();
  const anos = [
    { ano: "2017", dados: indicadoresNacionais.map((d) => ({ name: d.indicador, value: d.v2017 })) },
    { ano: "2023", dados: indicadoresNacionais.map((d) => ({ name: d.indicador, value: d.v2023 })) },
  ];

  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {anos.map(({ ano, dados }) => (
          <div key={ano} className="flex flex-col items-center">
            <p className="font-serif font-bold text-xl mb-2">{ano}</p>
            <ResponsiveContainer width="100%" height={isMobile ? 220 : 290}>
              <PieChart margin={isMobile
                ? { top: 0, right: 0, bottom: 0, left: 0 }
                : { top: 16, right: 72, bottom: 16, left: 72 }}>
                <Pie
                  data={dados}
                  cx="50%"
                  cy="50%"
                  outerRadius={isMobile ? 74 : 96}
                  dataKey="value"
                  label={isMobile ? undefined : LabelExterno}
                  labelLine={isMobile ? false : (props: any) => {
                    if ((props.percent ?? 0) < 0.12) return <></>;
                    return <line x1={props.points[0].x} y1={props.points[0].y}
                      x2={props.points[1].x} y2={props.points[1].y}
                      stroke="#888" strokeWidth={1} />;
                  }}
                  isAnimationActive={false}
                >
                  {dados.map((_, i) => <Cell key={i} fill={CORES[i % CORES.length]} />)}
                </Pie>
                <Tooltip formatter={(v: any, name) => [`${v}%`, String(name ?? "")]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        ))}
      </div>

      {/* Legenda compartilhada abaixo dos dois gráficos */}
      <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 mt-4 text-sm">
        {indicadoresNacionais.map((d, i) => (
          <span key={d.indicador} className="flex items-center gap-1.5">
            <span className="inline-block w-3 h-3 rounded-full flex-shrink-0"
              style={{ background: CORES[i % CORES.length] }} />
            {d.indicador}
          </span>
        ))}
      </div>
    </div>
  );
}
