# -*- coding: utf-8 -*-
import pdfplumber
import re
from typing import List, Dict
from config import PDF_PATH, LIVRO_MAPEAMENTO

class CPCExtractor:
    """Extrai artigos do PDF do Código de Processo Civil."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.artigos = []

    def extract_articles(self) -> List[Dict]:
        """Extrai todos os artigos do PDF."""
        print(f"📖 Abrindo PDF: {self.pdf_path}")

        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                texto_completo = ""
                total_pages = len(pdf.pages)

                for i, page in enumerate(pdf.pages):
                    if (i + 1) % 50 == 0:
                        print(f"   Lendo página {i + 1}/{total_pages}...")

                    texto_extraido = page.extract_text()
                    if texto_extraido:
                        texto_completo += texto_extraido + "\n"
        except Exception as e:
            print(f"❌ Erro ao abrir PDF: {e}")
            return []

        print(f"✅ PDF carregado ({len(texto_completo)} caracteres)")

        # Regex para encontrar artigos
        # Padrão: "Art. 123" ou "Art. 123 (parágrafo)" seguido por "—" ou "." e conteúdo
        # Captura até o próximo "Art." ou fim do documento
        pattern = r"Art\.\s+(\d+)(?:\s+\(.*?\))?\s*(?:—|\.)\s*(.+?)(?=\nArt\.\s+\d+|\Z)"
        matches = list(re.finditer(pattern, texto_completo, re.DOTALL | re.MULTILINE))

        print(f"🔍 Encontrados {len(matches)} padrões de artigo")

        for match in matches:
            try:
                num_artigo = match.group(1).strip()
                conteudo_bruto = match.group(2).strip()

                # Separa título da redação pela primeira quebra de linha
                linhas = conteudo_bruto.split('\n', 1)
                titulo = linhas[0].strip() if linhas else ""
                redacao = linhas[1].strip() if len(linhas) > 1 else titulo

                # Limpa números e caracteres lixo do início do título
                titulo = re.sub(r'^[\d\s.—\-]*', '', titulo).strip()
                titulo = titulo[:150]  # Máximo 150 chars de título

                # Limpa a redação
                redacao = re.sub(r'\n+', ' ', redacao)[:250]

                artigo_num = int(num_artigo)
                livro = self._determinar_livro(artigo_num)

                if livro != "SEM_LIVRO" and titulo:  # Só adiciona se tem título
                    self.artigos.append({
                        "numero": artigo_num,
                        "titulo": titulo,
                        "redacao": redacao,
                        "livro": livro
                    })

            except Exception as e:
                # Silencioso para não poluir output
                continue

        print(f"✅ {len(self.artigos)} artigos extraídos com sucesso")
        return sorted(self.artigos, key=lambda x: x["numero"])

    def _determinar_livro(self, numero: int) -> str:
        """Determina qual livro o artigo pertence baseado no número."""
        for sigla, config in LIVRO_MAPEAMENTO.items():
            inicio, fim = config["range"]
            if inicio <= numero <= fim:
                return sigla
        return "SEM_LIVRO"


if __name__ == "__main__":
    extractor = CPCExtractor(str(PDF_PATH))
    artigos = extractor.extract_articles()

    if artigos:
        print(f"\n📊 Amostra dos primeiros 5 artigos:")
        for art in artigos[:5]:
            print(f"\n   Art. {art['numero']} — {art['titulo']}")
            print(f"   Livro: {art['livro']}")
            print(f"   Redação: {art['redacao'][:100]}...")
    else:
        print("❌ Nenhum artigo extraído!")
