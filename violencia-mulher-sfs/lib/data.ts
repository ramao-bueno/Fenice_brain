import audienciasAnuaisRaw from "@/data/audiencias_anuais.json";
import competencias2026Raw from "@/data/competencias_2026.json";
import parcial2027Raw from "@/data/parcial_2027.json";
import generoShareRaw from "@/data/genero_share.json";
import indicadoresRaw from "@/data/indicadores_nacionais.json";
import recortesRaw from "@/data/recortes.json";
import propostasRaw from "@/data/propostas.json";
import metaRaw from "@/data/meta.json";
import creditosImagensRaw from "@/data/creditos_imagens.json";

export type AudienciaAno = { ano: number; total: number; observacao: string };
export type Competencia = { competencia: string; qtd: number; pct: number; destaque?: boolean };
export type Crescimento = { de: number; para: number; pct: number };
export type CreditoImagem = { arquivo: string; autor: string; fonte: string; licenca: string; url: string };

export const audienciasAnuais = audienciasAnuaisRaw as AudienciaAno[];
export const competencias2026 = competencias2026Raw as Competencia[];
export const parcial2027 = parcial2027Raw as {
  total: number; periodo: string; designadaPct: number; redesignadaPct: number; notaAnomalia: string;
};
export const generoShare = generoShareRaw as { ano: number; genero: number; comum_jec: number; demais: number }[];
export const indicadoresNacionais = indicadoresRaw as { indicador: string; v2017: number; v2023: number }[];
export const recortes = recortesRaw as {
  feminicidio: { processo: string; ano: number; competencia: string };
  backlog: { anoProcesso: number; anoJulgamento: number; esperaAnos: number }[];
  bombeiros: { a2025: number; a2026Parcial: number; a2026Ate: string; limitacao: string };
};
export const propostas = propostasRaw as { n: number; titulo: string; descricao: string }[];
export const meta = metaRaw as {
  fonte: string; comarca: string; orgaos: string[]; periodo: string; audienciaPublica: string;
};
export const creditosImagens = creditosImagensRaw as CreditoImagem[];

// Crescimento ano-a-ano (valores do relatorio; 2021->2022 omitido por subnotificacao)
export const crescimento: Crescimento[] = [
  { de: 2022, para: 2023, pct: 437 },
  { de: 2023, para: 2024, pct: 107 },
  { de: 2024, para: 2025, pct: 113 },
];
