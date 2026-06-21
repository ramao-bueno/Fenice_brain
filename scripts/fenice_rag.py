#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Híbrido via Supabase REST API
FTS usa RPC buscar_legislacao(); keyword usa filtro ILIKE via REST.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

import requests


def _cfg() -> Dict[str, str]:
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

    return {
        "url": os.environ.get("SUPABASE_URL", "").rstrip("/"),
        "key": os.environ.get("SUPABASE_SERVICE_KEY", ""),
    }


class FeniceRAG:
    """
    Motor de recuperação híbrido (FTS + keyword) via Supabase REST API.
    FTS usa a RPC buscar_legislacao() com ts_headline e ts_rank.
    Não requer psycopg2 nem senha do banco — apenas SUPABASE_SERVICE_KEY.
    """

    def __init__(self):
        cfg = _cfg()
        self._url = cfg["url"]
        self._key = cfg["key"]
        self._headers = {
            "apikey": self._key,
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
        }
        # conn não-None indica que as credenciais estão presentes
        self.conn = (self._url and self._key) or None

    def fechar(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.fechar()

    def contar_leis(self) -> int:
        """Retorna total de registros em legislacao_brasileira."""
        try:
            r = requests.head(
                f"{self._url}/rest/v1/legislacao_brasileira",
                headers={**self._headers, "Prefer": "count=exact"},
                params={"select": "*"},
                timeout=10,
            )
            m = re.search(r"/(\d+)$", r.headers.get("Content-Range", ""))
            return int(m.group(1)) if m else 0
        except Exception:
            return 0

    def buscar_hibrido(
        self,
        query: str,
        limite: int = 5,
        modo: str = "fts",
    ) -> List[Dict]:
        if not self.conn:
            raise RuntimeError(
                "FeniceRAG: Supabase não configurado. "
                "Verifique SUPABASE_URL e SUPABASE_SERVICE_KEY no .env."
            )
        if modo in ("fts", "hibrido"):
            return self._buscar_fts(query, limite)
        elif modo == "keyword":
            return self._buscar_keyword(query, limite)
        else:
            raise ValueError(f"Modo desconhecido: '{modo}'. Use 'fts', 'keyword' ou 'hibrido'.")

    def _buscar_fts(self, query: str, limite: int) -> List[Dict]:
        """FTS via RPC buscar_legislacao() — retorna ts_headline e ts_rank."""
        try:
            r = requests.post(
                f"{self._url}/rest/v1/rpc/buscar_legislacao",
                headers=self._headers,
                json={"p_query": query, "p_limite": limite},
                timeout=15,
            )
            r.raise_for_status()
            return r.json() or []
        except Exception as exc:
            print(f"[FeniceRAG] FTS falhou ({exc}), tentando keyword como fallback.")
            return self._buscar_keyword(query, limite)

    def _buscar_keyword(self, query: str, limite: int) -> List[Dict]:
        """Busca ILIKE em ementa e numero_ano via REST."""
        try:
            r = requests.get(
                f"{self._url}/rest/v1/legislacao_brasileira",
                headers=self._headers,
                params={
                    "select": "numero_ano,tipo_ato,ementa,texto_vigente",
                    "or": f"(ementa.ilike.*{query}*,numero_ano.ilike.*{query}*)",
                    "limit": str(limite),
                    "order": "numero_ano",
                },
                timeout=15,
            )
            r.raise_for_status()
            rows = r.json() or []
        except Exception:
            return []

        return [
            {
                "numero_ano":       row.get("numero_ano", ""),
                "tipo_ato":         row.get("tipo_ato", ""),
                "ementa":           row.get("ementa"),
                "trecho_relevante": (row.get("texto_vigente") or "")[:500],
                "relevancia":       1.0,
            }
            for row in rows
        ]

    def construir_contexto(
        self,
        resultados: List[Dict],
        max_chars: int = 4000,
    ) -> str:
        if not resultados:
            return "(nenhum resultado encontrado na base de dados)"

        blocos: List[str] = []
        total = 0

        for r in resultados:
            numero_ano = r.get("numero_ano", "Desconhecido")
            ementa     = r.get("ementa") or ""
            trecho     = r.get("trecho_relevante") or ""

            trecho_curto = trecho[:500].rstrip()
            if len(trecho) > 500:
                trecho_curto += "..."

            bloco = (
                f"--- {numero_ano} ---\n"
                + (f"Ementa: {ementa}\n" if ementa else "")
                + f"{trecho_curto}\n"
            )

            if total + len(bloco) > max_chars:
                break

            blocos.append(bloco)
            total += len(bloco)

        return "\n".join(blocos)

    def responder_com_contexto(
        self,
        pergunta: str,
        prompt_template: str,
        limite: int = 5,
        modo: str = "fts",
        max_chars: int = 4000,
    ) -> Dict:
        resultados = self.buscar_hibrido(pergunta, limite=limite, modo=modo)
        contexto   = self.construir_contexto(resultados, max_chars=max_chars)

        prompt_preenchido = prompt_template
        for placeholder, valor in {
            "{contexto_juridico}":   contexto,
            "{contexto_filosofico}": contexto,
            "{vade_mecum_contexto}": contexto,
            "{pergunta}":            pergunta,
        }.items():
            prompt_preenchido = prompt_preenchido.replace(placeholder, valor)

        return {
            "pergunta":          pergunta,
            "resultados_banco":  resultados,
            "contexto":          contexto,
            "prompt_preenchido": prompt_preenchido,
        }

    @staticmethod
    def carregar_prompt(nome_arquivo: str) -> str:
        prompts_dir = Path(__file__).parent / "prompts"
        caminho = prompts_dir / nome_arquivo
        if not caminho.exists():
            raise FileNotFoundError(
                f"Template '{nome_arquivo}' não encontrado em {prompts_dir}"
            )
        return caminho.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI de teste rápido
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    termos = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "licitacao dispensa contrato"

    with FeniceRAG() as rag:
        print(f"Buscando: '{termos}' (modo=fts, limite=3)")
        resultados = rag.buscar_hibrido(termos, limite=3)

        if not resultados:
            print("Nenhum resultado encontrado.")
        else:
            for r in resultados:
                print(f"\n  {r['numero_ano']} — {r['tipo_ato']}")
                print(f"  Relevancia: {r.get('relevancia', 0):.4f}")
                print(f"  Ementa: {(r['ementa'] or '')[:80]}...")

        print("\n--- CONTEXTO GERADO ---")
        print(rag.construir_contexto(resultados)[:800])
