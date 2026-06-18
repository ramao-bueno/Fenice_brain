"use client";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LabelList,
} from "recharts";
import { generoShare } from "@/lib/data";

export default function GeneroShare() {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={generoShare} margin={{ top: 28, right: 28, left: 8, bottom: 0 }}>
        <XAxis dataKey="ano" tickLine={false} axisLine={false} tick={{ fontSize: 14 }} />
        <YAxis hide domain={[0, 40]} />
        <Tooltip formatter={(v) => [`${v}%`, "Maria da Penha + Crimes Sexuais"]} labelFormatter={(l) => `Ano ${l}`} />
        <Line type="monotone" dataKey="pct" stroke="#006847" strokeWidth={3} dot={{ r: 5, fill: "#006847" }} isAnimationActive={false}>
          <LabelList dataKey="pct" position="top" formatter={(v) => `${v}%`} fill="#1a1a1a" fontWeight={700} />
        </Line>
      </LineChart>
    </ResponsiveContainer>
  );
}
