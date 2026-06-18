"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { indicadoresNacionais } from "@/lib/data";

export default function IndicadoresNacionais() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        layout="vertical"
        data={indicadoresNacionais}
        margin={{ top: 0, right: 28, left: 8, bottom: 0 }}
      >
        <XAxis type="number" hide domain={[0, 60]} />
        <YAxis
          type="category"
          dataKey="indicador"
          width={200}
          tickLine={false}
          axisLine={false}
          tick={{ fontSize: 12 }}
        />
        <Tooltip cursor={{ fill: "rgba(0,104,71,0.08)" }} formatter={(v) => [`${v}%`, ""]} />
        <Legend />
        <Bar dataKey="v2017" name="2017" fill="#7fba00" radius={[0, 4, 4, 0]} isAnimationActive={false} />
        <Bar dataKey="v2023" name="2023" fill="#006847" radius={[0, 4, 4, 0]} isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}
