"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from "recharts";
import { audienciasAnuais } from "@/lib/data";

export default function EvolucaoAnual() {
  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart data={audienciasAnuais} margin={{ top: 28, right: 8, left: 8, bottom: 0 }}>
        <XAxis dataKey="ano" tickLine={false} axisLine={false} tick={{ fontSize: 14 }} />
        <YAxis hide />
        <Tooltip
          cursor={{ fill: "rgba(0,104,71,0.08)" }}
          formatter={(v) => [`${v} audiencias`, "Total"]}
          labelFormatter={(l) => `Ano ${l}`}
        />
        <Bar dataKey="total" name="Audiencias" fill="#006847" radius={[6, 6, 0, 0]} isAnimationActive={false}>
          <LabelList dataKey="total" position="top" fill="#1a1a1a" fontWeight={700} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
