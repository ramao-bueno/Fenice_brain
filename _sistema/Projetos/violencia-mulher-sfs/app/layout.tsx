import type { Metadata, Viewport } from "next";
import { Playfair_Display, Inter } from "next/font/google";
import TabNav from "@/components/nav/TabNav";
import Rodape from "@/components/ui/Rodape";
import AnimacaoScroll from "@/components/ui/AnimacaoScroll";
import "./globals.css";

const display = Playfair_Display({
  subsets: ["latin"],
  weight: ["400", "700", "900"],
  display: "swap",
  variable: "--font-display",
});

const body = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-body",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export const metadata: Metadata = {
  title: "Observatório da Mulher SFS | Dados e Propostas — São Francisco do Sul",
  description:
    "Análise dos dados judiciais de violência contra a mulher em São Francisco do Sul (2021–2027) e quatro propostas de ação. Projeto de extensão da UNIVILLE — Observatório de Dados.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${display.variable} ${body.variable}`}>
      <body className="bg-areia text-ink font-sans antialiased">
        <TabNav />
        {children}
        <Rodape />
        <AnimacaoScroll />
      </body>
    </html>
  );
}
