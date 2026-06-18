import type { Metadata } from "next";
import { Playfair_Display, Inter } from "next/font/google";
import TabNav from "@/components/nav/TabNav";
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

export const metadata: Metadata = {
  title: "Violencia contra a Mulher em Sao Francisco do Sul | Dados e propostas",
  description:
    "Analise dos dados judiciais de violencia contra a mulher em Sao Francisco do Sul (2021-2027) e quatro propostas de politica publica. Projeto de extensao da UNIVILLE.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${display.variable} ${body.variable}`}>
      <body className="bg-areia text-ink font-sans antialiased">
        <TabNav />
        {children}
      </body>
    </html>
  );
}
