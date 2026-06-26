"use client";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { generoShare } from "@/lib/data";
import { useMobile } from "@/hooks/useMobile";

const CORES = {
  genero:    "#b23a48",
  comum_jec: "#005c2a",
  demais:    "#7dc242",
};

const RADIAN = Math.PI / 180;

function LabelExterno({ cx, cy, midAngle, outerRadius, percent }: any) {
  if (percent < 0.06) return null;
  const radius = outerRadius + 44;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);
  return (
    <text
      x={x} y={y} fill="#1a1a1a"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
      fontSize={13}
      fontWeight={700}
    >
      {`${(percent * 100).toFixed(1)}%`}
    </text>
  );
}

export default function GeneroShare() {
  const isMobile = useMobile();
  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {generoShare.map((d) => {
          const dados = [
            { name: "Maria da Penha + Sexual",  value: d.genero },
            { name: "Crime Comum + JEC",         value: d.comum_jec },
            { name: "Demais crimes",             value: d.demais },
          ];
          return (
            <div key={d.ano} className="flex flex-col items-center">
              <p className="font-serif font-bold text-lg mb-1">{d.ano}</p>
              <ResponsiveContainer width="100%" height={isMobile ? 190 : 240}>
                <PieChart margin={isMobile ? { top: 0, right: 0, bottom: 0, left: 0 } : { top: 20, right: 55, bottom: 20, left: 55 }}>
                  <Pie
                    data={dados}
                    cx="50%"
                    cy="50%"
                    outerRadius={isMobile ? 60 : 78}
                    innerRadius={isMobile ? 24 : 30}
                    dataKey="value"
                    label={isMobile ? undefined : LabelExterno}
                    labelLine={isMobile ? false : (props: any) => {
                      if ((props.percent ?? 0) < 0.06) return <></>;
                      return <line x1={props.points[0].x} y1={props.points[0].y} x2={props.points[1].x} y2={props.points[1].y} stroke="#555" strokeWidth={1} />;
                    }}
                    isAnimationActive={false}
                  >
                    <Cell fill={CORES.genero} />
                    <Cell fill={CORES.comum_jec} />
                    <Cell fill={CORES.demais} />
                  </Pie>
                  <Tooltip formatter={(v: any, name) => [`${Number(v).toFixed(1)}%`, String(name)]} />
                </PieChart>
              </ResponsiveContainer>
              <p className="text-sm font-bold text-center mt-1" style={{ color: CORES.genero }}>
                {d.genero.toFixed(1)}%
              </p>
            </div>
          );
        })}
      </div>
      <div className="flex flex-wrap justify-center gap-5 text-sm">
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-3 h-3 rounded-full" style={{ background: CORES.genero }} />
          Maria da Penha + Dignidade Sexual
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-3 h-3 rounded-full" style={{ background: CORES.comum_jec }} />
          Crime Comum + Juizado Especial Criminal
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-3 h-3 rounded-full" style={{ background: CORES.demais }} />
          Demais crimes
        </span>
      </div>
    </div>
  );
}
