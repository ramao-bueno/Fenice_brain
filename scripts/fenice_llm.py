"""
fenice_llm.py — Cliente LLM unificado com fallback chain Fenice IT

Prioridade: Anthropic Claude → OpenAI → Gemini

Uso:
    from fenice_llm import FeniceClient

    client = FeniceClient()
    resposta = client.completar("seu prompt aqui")
    print(resposta.texto)
    print(resposta.provedor)  # "claude" | "openai" | "gemini"
"""

import os
import time
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

# ─── Modelos padrão por provedor ─────────────────────────────────────────────

MODELOS = {
    "claude":  os.environ.get("FENICE_CLAUDE_MODEL",  "claude-haiku-4-5-20251001"),
    "openai":  os.environ.get("FENICE_OPENAI_MODEL",  "gpt-4o-mini"),
    "gemini":  os.environ.get("FENICE_GEMINI_MODEL",  "gemini-2.5-flash"),
}

# Ordem de prioridade — pode ser sobrescrita por variável de ambiente
# ex: FENICE_LLM_CHAIN=openai,gemini  (pula Claude)
_chain_env = os.environ.get("FENICE_LLM_CHAIN", "claude,openai,gemini")
CHAIN_PADRAO = [p.strip() for p in _chain_env.split(",")]


@dataclass
class Resposta:
    texto: str
    provedor: str
    modelo: str
    tentativas: int


# ─── Provedores ──────────────────────────────────────────────────────────────

def _chamar_claude(prompt: str, max_tokens: int, temperature: float) -> str:
    import anthropic
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise EnvironmentError("ANTHROPIC_API_KEY não configurada")
    client = anthropic.Anthropic(api_key=key)
    msg = client.messages.create(
        model=MODELOS["claude"],
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def _chamar_openai(prompt: str, max_tokens: int, temperature: float) -> str:
    from openai import OpenAI
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise EnvironmentError("OPENAI_API_KEY não configurada")
    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model=MODELOS["openai"],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""


def _chamar_gemini(prompt: str, max_tokens: int, temperature: float) -> str:
    from google import genai
    from google.genai import types as gt
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise EnvironmentError("GEMINI_API_KEY não configurada")
    client = genai.Client(api_key=key)
    resp = client.models.generate_content(
        model=MODELOS["gemini"],
        contents=prompt,
        config=gt.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
    )
    return resp.text or ""


_PROVEDORES = {
    "claude": _chamar_claude,
    "openai": _chamar_openai,
    "gemini": _chamar_gemini,
}


# ─── Cliente principal ────────────────────────────────────────────────────────

class FeniceClient:
    """
    Cliente LLM com fallback automático.

    Parâmetros
    ----------
    chain : list[str] | None
        Ordem de provedores. None usa FENICE_LLM_CHAIN do .env ou o padrão
        ["claude", "openai", "gemini"].
    max_tokens : int
        Limite de tokens de saída (padrão 4000).
    temperature : float
        Temperatura (padrão 0.3).
    max_tentativas_por_provedor : int
        Retentativas em rate-limit antes de trocar de provedor (padrão 2).
    """

    def __init__(
        self,
        chain: list[str] | None = None,
        max_tokens: int = 4000,
        temperature: float = 0.3,
        max_tentativas_por_provedor: int = 2,
    ):
        self.chain = chain or CHAIN_PADRAO
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_tentativas = max_tentativas_por_provedor

    def completar(self, prompt: str) -> Resposta:
        """
        Envia o prompt pela chain de provedores.
        Retorna Resposta com o texto gerado e metadados.
        Levanta RuntimeError se todos os provedores falharem.
        """
        tentativas_total = 0
        erros = []

        for provedor in self.chain:
            fn = _PROVEDORES.get(provedor)
            if fn is None:
                log.warning("Provedor desconhecido: %s — ignorando", provedor)
                continue

            for tentativa in range(1, self.max_tentativas + 1):
                tentativas_total += 1
                try:
                    log.info("→ %s (tentativa %d)", provedor, tentativa)
                    texto = fn(self.prompt_com_contexto(prompt), self.max_tokens, self.temperature)
                    if texto.strip():
                        return Resposta(
                            texto=texto,
                            provedor=provedor,
                            modelo=MODELOS.get(provedor, provedor),
                            tentativas=tentativas_total,
                        )
                    log.warning("%s retornou resposta vazia", provedor)
                except EnvironmentError as e:
                    # Chave ausente — não tenta de novo, passa pro próximo
                    erros.append(f"{provedor}: {e}")
                    log.warning("Pulando %s: %s", provedor, e)
                    break
                except Exception as e:
                    msg = str(e)
                    erros.append(f"{provedor}[{tentativa}]: {msg}")
                    if self._e_rate_limit(msg):
                        espera = 30 * tentativa
                        log.warning("%s rate-limit — aguardando %ds", provedor, espera)
                        time.sleep(espera)
                    else:
                        log.error("%s erro: %s", provedor, e)
                        break  # erro não-transitório → próximo provedor

        raise RuntimeError(
            f"Todos os provedores falharam após {tentativas_total} tentativas.\n"
            + "\n".join(erros)
        )

    def prompt_com_contexto(self, prompt: str) -> str:
        return prompt

    @staticmethod
    def _e_rate_limit(msg: str) -> bool:
        sinais = ("429", "rate_limit", "rate limit", "quota", "resource exhausted",
                  "too many requests", "overloaded")
        m = msg.lower()
        return any(s in m for s in sinais)


# ─── Atalho funcional ─────────────────────────────────────────────────────────

def completar(prompt: str, **kwargs) -> Resposta:
    """Atalho para uso sem instanciar FeniceClient explicitamente."""
    return FeniceClient(**kwargs).completar(prompt)
