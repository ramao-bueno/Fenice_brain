import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Fenice IT Justech.IA — Soluções B2B",
  description:
    "Plataforma jurídica inteligente para escritórios de advocacia e empresas. API REST, RAG jurídico, integração enterprise.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="bg-[#0a0a0f] text-white antialiased">{children}</body>
    </html>
  );
}
