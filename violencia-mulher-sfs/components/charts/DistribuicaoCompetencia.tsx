"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from "recharts";
import { competencias2026 } from "@/lib/data";

export default function DistribuicaoCompetencia() {
  const data = [...competencias2026].sort((a, b) => b.qtd - a.qtd);
  return (
    <ResponsiveContainer width="100%" height={440}>
      <BarChart layout="vertical" data={data} margin={{ top: 0, right: 36, left: 8, bottom: 0 }}>
        <XAxis type="number" hide />
        <YAxis
          type="category"
          dataKey="competencia"
          width={190}
          tickLine={false}
          axisLine={false}
          tick={{ fontSize: 12 }}
        />
        <Tooltip
          cursor={{ fill: "rgba(0,104,71,0.08)" }}
          formatter={(v) => [`${v} audiencias`, "Total"]}
        />
        <Bar dataKey="qtd" radius={[0, 6, 6, 0]} isAnimationActive={false}>
          {data.map((d, i) => (
            <Cell key={i} fill={d.destaque ? "#006847" : "#7fba00"} />
          ))}
          <LabelList dataKey="qtd" position="right" fill="#1a1a1a" fontSize={12} fontWeight={600} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
