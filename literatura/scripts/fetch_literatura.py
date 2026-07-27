#!/usr/bin/env python3
"""
Levantamento bibliografico do pos-doc GORE3.

Recebe uma lista curada de PMIDs (curados manualmente a partir de buscas
PubMed registradas em ../00_PROTOCOLO_BUSCA.md), busca os metadados
bibliograficos completos no Europe PMC e recupera o conteudo do artigo
apenas quando ha versao de acesso aberto.

Cascata de recuperacao (a primeira que funcionar vence). Prioriza TEXTO
COMPLETO sobre PDF: texto e pesquisavel e permite conferir cada afirmacao
contra a fonte, que e o requisito da regra de nao-fabricacao.
  1. Europe PMC -> /{PMCID}/fullTextXML, convertido para texto
  2. Unpaywall  -> best_oa_location.url_for_pdf

Duas rotas foram testadas e descartadas antes do lote, e nao devem ser
reintroduzidas sem novo teste:
  - Europe PMC /{PMCID}/fullTextPDF     -> 404 mesmo para artigo OA
  - NCBI PMC OA Web Service (oa.fcgi)   -> devolve link .tar.gz para
    ftp.ncbi.nlm.nih.gov cujo equivalente HTTPS retorna 404

Artigo fechado NAO e baixado: so o abstract e salvo, e o artigo entra em
PDFS_PENDENTES.md com o link do editor, para download manual via CAFe/UFV.

Saidas:
  ../metadata.json         metadados crus do Europe PMC (fonte de verdade)
  ../abstracts/{pmid}.txt  abstract salvo, um arquivo por artigo
  ../fulltext/{chave}.txt  texto completo de artigos OA
  ../pdfs/{chave}.pdf      PDFs de acesso aberto (git-ignored)
  ../PDFS_PENDENTES.md     o que nao pode ser recuperado, e por que
"""

import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent.parent
PDF_DIR = BASE / "pdfs"
ABS_DIR = BASE / "abstracts"
FULL_DIR = BASE / "fulltext"

EMAIL = "eulalio.santos@ufv.br"
TOOL = "eulalio-posdoc-gore3"
HEADERS = {"User-Agent": f"Mozilla/5.0 (research; {EMAIL})"}

EPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EPMC_XML = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
UNPAYWALL = "https://api.unpaywall.org/v2/{doi}"

SLEEP = 0.4  # sem NCBI_API_KEY o limite do E-utilities e 3 req/s


# ---------------------------------------------------------------------------
# Lista curada: pmid -> (tema, eixo, tier)
# tier 1 = fulltext lido e fichado; tier 2 = abstract + metadados verificados
# ---------------------------------------------------------------------------

CURADOS = {
    # ---- TEMA 1: peptideos inibidores de tripsina ----
    # 1A peptideos curtos desenhados / derivados de reactive center loop
    "32661389": (1, "1A", 1),
    "33357552": (1, "1A", 1),
    "34107869": (1, "1A", 2),
    "30570384": (1, "1A", 2),
    "30194598": (1, "1A", 2),
    "26620556": (1, "1A", 2),
    # 1B tripsinas digestivas de Lepidoptera
    "31587381": (1, "1B", 1),
    "26988941": (1, "1B", 2),
    "32004347": (1, "1B", 2),
    "34569086": (1, "1B", 2),
    # 1C adaptacao e resposta compensatoria a inibidores
    "25662099": (1, "1C", 1),
    "36127063": (1, "1C", 1),
    "41939357": (1, "1C", 1),
    "29661852": (1, "1C", 1),
    "31789444": (1, "1C", 2),
    "38375972": (1, "1C", 2),
    "32265951": (1, "1C", 2),
    # classicos do mecanismo de escape, resolvidos na auditoria do .docx
    "7644535": (1, "1C", 1),   # Jongsma 1995 PNAS: proteases insensiveis
    "15157229": (1, "1C", 1),  # Moon 2004: regulacao transcricional no bruquideo
    "19196350": (1, "1C", 2),  # Moon 2009: transcriptoma vs cistatina
    "16140320": (1, "1C", 2),  # Srinivasan 2005
    # 1A (cont.) linhagem da serie de peptideos sinteticos do grupo,
    # localizada por busca de autor (Merino-Cabrera) em 27/07/2026
    "28925864": (1, "1A", 1),  # origem: peptideos sinteticos vs serino-proteases
    "35315942": (1, "1A", 1),  # tripeptideos: Ki e estabilidade
    "35715046": (1, "1A", 1),  # dipeptideos contendo arginina
    "29486250": (1, "1A", 1),  # Saikhedkar 2018 - resolve pendencia do .bib
    "31077794": (1, "1A", 2),  # peptideos ciclicos Pin-II
    "32360954": (1, "1A", 2),  # peptideos mimeticos de Inga laurina
    # 1D cinetica de inibicao
    "32491140": (1, "1D", 1),
    "41572648": (1, "1D", 1),
    "41849700": (1, "1D", 1),
    "32342573": (1, "1D", 2),
    "34982841": (1, "1C", 2),
    "6996568": (1, "1D", 1),   # Laskowski & Kato 1980 - resolve pendencia
    "10708867": (1, "1D", 1),  # Laskowski & Qasim 2000 - resolve pendencia
    "16029159": (1, "1D", 2),
    # ---- TEMA 2: RNA-Seq ----
    # 2A artigos-fonte das ferramentas prescritas na metodologia
    "23104886": (2, "2A", 2),  # STAR
    "31375807": (2, "2A", 2),  # HISAT2
    "28263959": (2, "2A", 2),  # Salmon
    "26925227": (2, "2A", 1),  # tximport
    "25516281": (2, "2A", 2),  # DESeq2
    "24227677": (2, "2A", 2),  # featureCounts
    "30423086": (2, "2A", 2),  # fastp
    "41112039": (2, "2A", 2),  # fastp 1.0
    "27312411": (2, "2A", 2),  # MultiQC
    "34936221": (2, "2A", 2),  # BUSCO
    "34597405": (2, "2A", 2),  # eggNOG-mapper v2
    "34557778": (2, "2A", 2),  # clusterProfiler 4.0
    "19114008": (2, "2A", 2),  # WGCNA
    "24451626": (2, "2A", 2),  # InterProScan 5
    "23060610": (2, "2A", 2),  # CD-HIT
    "38396040": (2, "2A", 1),  # rMATS-turbo
    "32055031": (2, "2A", 2),  # nf-core
    "40731283": (2, "2A", 2),  # Nextflow + nf-core 2025
    # 2B benchmarks e boas praticas (recencia exigida: 2023+)
    "38475429": (2, "2B", 1),
    "35354358": (2, "2B", 1),
    "34034652": (2, "2B", 1),
    "37260511": (2, "2B", 2),
    "33629477": (2, "2B", 2),
    # 2C transcriptomica de intestino de inseto sob estresse
    "34022342": (2, "2C", 1),
    "32928099": (2, "2C", 2),
    "42496569": (2, "2C", 2),
    # 2D fronteira 2024-2026
    "38849569": (2, "2D", 1),
    "41709347": (2, "2D", 1),
    "41963350": (2, "2D", 2),
    "37426759": (2, "2D", 2),
    # ---- TEMA 3: biologia estrutural ----
    # 3A predicao de estrutura
    "37933859": (3, "3A", 2),  # AFDB 2024
    "39446390": (3, "3A", 2),
    "41130640": (3, "3A", 2),
    # 3B docking proteina-peptideo
    "38886530": (3, "3B", 1),  # HADDOCK 2.4
    "37888817": (3, "3B", 1),  # revisao de metodos proteina-peptideo
    "35013344": (3, "3B", 1),
    "32808340": (3, "3B", 1),  # AutoDock suite at 30
    "40053869": (3, "3B", 2),
    "34596658": (3, "3B", 2),
    "32621224": (3, "3B", 2),
    # 3C campos de forca
    "39536029": (3, "3C", 1),
    "32816485": (3, "3C", 1),
    "33591749": (3, "3C", 2),
    "38949117": (3, "3C", 2),
    # 3D energia livre de ligacao
    "34586825": (3, "3D", 1),  # gmx_MMPBSA
    "41160056": (3, "3D", 1),  # sampling challenges MM/PBSA
    "39480515": (3, "3D", 1),
    "38501198": (3, "3D", 1),
    "37378817": (3, "3D", 2),
    "42081673": (3, "3D", 2),
    "41907587": (3, "3D", 2),
    # 3E arquitetura de subsitios de serino-proteases; o eixo que sustenta
    # a hipotese H6 (modo de ligacao nao canonico do GORE3 = LALAY)
    "41232883": (3, "3E", 1),  # revisao recente de estrutura de tripsina
    "26106067": (3, "3E", 1),  # engenharia de tripsina p/ resistencia a inibidor
    "31435809": (3, "3E", 1),  # complexo NAO CANONICO inibidor x quimotripsina
    "29210603": (3, "3E", 1),  # troca inesperada de modo de ligacao de peptideo
    "28298600": (3, "3E", 2),  # inibidores explorando o lado prime (S')
    "35542712": (3, "3E", 2),  # desenho dirigido ao bolsao S1
    "32011145": (3, "3E", 2),  # protonacao do ligante ao ligar tripsina
    "9047374": (3, "3E", 1),   # cadeias laterais no bolsao S1 - o problema do LALAY
    "20800580": (3, "3E", 2),  # P1 ionizavel em S1 hidrofobico
    # ---- TEMA 4: manejo de Anticarsia com peptideos ----
    # 4A a praga e o dano (fonte primaria, substitui os links de noticia)
    "36520803": (4, "4A", 1),
    "30071611": (4, "4A", 1),
    "34545402": (4, "4A", 2),
    "34718639": (4, "4A", 2),
    # 4B taticas atuais de controle
    "31040309": (4, "4B", 2),
    "35293546": (4, "4B", 2),
    "30930188": (4, "4B", 2),
    "33334288": (4, "4B", 2),
    "38913262": (4, "4B", 1),
    "30145425": (4, "4B", 2),
    "31796830": (4, "4B", 2),
    "38940546": (4, "4B", 2),
    "26615220": (4, "4B", 2),
    # 4C bioinseticidas peptidicos e entrega
    "37229568": (4, "4C", 1),
    "33992010": (4, "4C", 2),
    "33796137": (4, "4C", 2),
    "37816687": (4, "4C", 1),
    "41696158": (4, "4C", 2),
    "32771931": (4, "4C", 2),
    # 4D recursos genomicos
    "36689934": (4, "4D", 2),
}

# Ja presentes em docs/referencias.bib. Reprocessados so para completar
# metadados faltantes (PMID/DOI/paginas) e tentar o PDF.
JA_NO_BIB = {
    "33200876": (1, "1D", 1),
    "31625209": (1, "1C", 1),
    "30365718": (4, "4B", 1),
    "28762531": (1, "1B", 1),
    "41510779": (1, "1A", 1),
    "41956187": (1, "1A", 1),
    "39534858": (4, "4B", 1),
    "36971261": (2, "2C", 2),
    "41999131": (4, "4C", 1),
    # ja no .bib como silvajunior2021proteases e abramson2024alphafold3;
    # reprocessados aqui so para completar o PMID que faltava nas entradas
    "33948994": (1, "1B", 1),
    "38718835": (3, "3A", 1),
}


def slug(txt):
    txt = unicodedata.normalize("NFKD", txt or "")
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", txt.lower())


# Particulas de sobrenome que nao podem virar a chave BibTeX:
# "de Almeida Barros" tem de dar "barros", nao "de".
PARTICULAS = {"de", "da", "do", "dos", "das", "van", "von", "del", "della",
              "di", "du", "la", "le", "el", "bin", "ibn", "ter", "ten"}


def chave_bibtex(art):
    """autor+ano+palavra, minusculo — convencao ja usada em docs/referencias.bib."""
    autores = (art.get("authorString") or "Anon").split(",")
    partes = autores[0].strip().split() if autores[0].strip() else ["anon"]
    sobrenome = next((p for p in partes if p.lower() not in PARTICULAS),
                     partes[-1])
    ano = art.get("pubYear") or "0000"
    titulo = art.get("title") or ""
    stop = {
        "the", "a", "an", "of", "for", "and", "in", "on", "to", "with", "from",
        "is", "are", "by", "at", "as", "its", "their",
    }
    palavra = ""
    for w in re.findall(r"[A-Za-z]+", titulo):
        if len(w) > 3 and w.lower() not in stop:
            palavra = w.lower()
            break
    return f"{slug(sobrenome)}{ano}{slug(palavra)}"


def buscar_metadados(pmids):
    """Europe PMC em lotes; resultType=core traz DOI, volume, paginas, OA."""
    out = {}
    pmids = list(pmids)
    for i in range(0, len(pmids), 20):
        lote = pmids[i:i + 20]
        query = " OR ".join(f"EXT_ID:{p}" for p in lote)
        r = requests.get(
            EPMC_SEARCH,
            params={"query": query, "format": "json",
                    "resultType": "core", "pageSize": 25},
            headers=HEADERS, timeout=90,
        )
        r.raise_for_status()
        for art in r.json().get("resultList", {}).get("result", []):
            if art.get("id") in lote:
                out[art["id"]] = art
        print(f"  metadados {i + len(lote)}/{len(pmids)}", file=sys.stderr)
        time.sleep(SLEEP)
    return out


def _salvar_pdf(conteudo, destino):
    if conteudo[:1024].find(b"%PDF") == -1:
        return False
    destino.write_bytes(conteudo)
    return destino.stat().st_size > 10_000


def _xml_para_texto(xml):
    """Extrai o corpo legivel do JATS XML do Europe PMC."""
    txt = re.sub(r"<(ref-list|back|front|table-wrap|fig)\b.*?</\1>", " ",
                 xml, flags=re.S)
    txt = re.sub(r"<title[^>]*>(.*?)</title>", r"\n\n## \1\n", txt, flags=re.S)
    txt = re.sub(r"</(p|sec|abstract)>", "\n\n", txt)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = (txt.replace("&lt;", "<").replace("&gt;", ">")
              .replace("&amp;", "&").replace("&#x000a0;", " "))
    txt = re.sub(r"[ \t]+", " ", txt)
    return re.sub(r"\n{3,}", "\n\n", txt).strip()


def baixar_texto(art, chave):
    """
    Busca o conteudo do artigo. Prioriza TEXTO COMPLETO sobre PDF: e
    pesquisavel e permite conferir cada afirmacao contra o texto real,
    que e o requisito da regra de nao-fabricacao.

    Retorna (nivel, rota) onde nivel e 'fulltext', 'pdf' ou None.
    """
    pmcid = art.get("pmcid")
    doi = art.get("doi")

    # 1. Europe PMC fullTextXML — rota mais confiavel para OA
    if pmcid:
        destino = FULL_DIR / f"{chave}.txt"
        if destino.exists() and destino.stat().st_size > 5_000:
            return "fulltext", "cache"
        try:
            r = requests.get(EPMC_XML.format(pmcid=pmcid),
                             headers=HEADERS, timeout=120)
            if r.ok and b"<article" in r.content[:2000]:
                texto = _xml_para_texto(r.text)
                if len(texto) > 5_000:
                    destino.write_text(
                        f"PMID {art.get('id')} | {pmcid} | {art.get('doi')}\n"
                        f"{art.get('title', '')}\n"
                        f"FONTE: Europe PMC fullTextXML\n"
                        f"{'=' * 70}\n\n{texto}\n", encoding="utf-8")
                    return "fulltext", "europepmc_xml"
        except requests.RequestException:
            pass
        time.sleep(SLEEP)

    # 2. Unpaywall — PDF quando houver deposito OA legivel
    if doi:
        destino = PDF_DIR / f"{chave}.pdf"
        if destino.exists() and destino.stat().st_size > 10_000:
            return "pdf", "cache"
        try:
            r = requests.get(UNPAYWALL.format(doi=doi),
                             params={"email": EMAIL}, headers=HEADERS,
                             timeout=60)
            if r.ok:
                loc = (r.json() or {}).get("best_oa_location") or {}
                url = loc.get("url_for_pdf")
                if url:
                    rr = requests.get(url, headers=HEADERS, timeout=120)
                    if rr.ok and _salvar_pdf(rr.content, destino):
                        return "pdf", "unpaywall"
        except (requests.RequestException, ValueError):
            pass
        if destino.exists():
            destino.unlink()
        time.sleep(SLEEP)

    return None, "fechado" if art.get("isOpenAccess") != "Y" else "oa_sem_texto"


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    ABS_DIR.mkdir(parents=True, exist_ok=True)
    FULL_DIR.mkdir(parents=True, exist_ok=True)

    todos = {**CURADOS, **JA_NO_BIB}
    print(f"Buscando metadados de {len(todos)} artigos...", file=sys.stderr)
    meta = buscar_metadados(todos)

    faltando = sorted(set(todos) - set(meta))
    if faltando:
        print(f"AVISO: sem metadados no Europe PMC: {faltando}", file=sys.stderr)

    registros = []
    for pmid, art in sorted(meta.items(), key=lambda kv: todos[kv[0]]):
        tema, eixo, tier = todos[pmid]
        chave = chave_bibtex(art)
        ji = art.get("journalInfo", {}) or {}
        jt = (ji.get("journal") or {})

        abstract = art.get("abstractText") or ""
        if abstract:
            (ABS_DIR / f"{pmid}.txt").write_text(
                f"PMID {pmid} | {art.get('title', '')}\n\n{abstract}\n",
                encoding="utf-8")

        nivel, rota = baixar_texto(art, chave)

        registros.append({
            "chave": chave,
            "pmid": pmid,
            "doi": art.get("doi"),
            "pmcid": art.get("pmcid"),
            "tema": tema,
            "eixo": eixo,
            "tier": tier,
            "ja_no_bib": pmid in JA_NO_BIB,
            "titulo": art.get("title", "").rstrip("."),
            "autores": art.get("authorString", ""),
            "revista": jt.get("title") or "",
            "revista_abrev": jt.get("medlineAbbreviation") or "",
            "ano": art.get("pubYear"),
            "volume": ji.get("volume"),
            "numero": ji.get("issue"),
            "paginas": art.get("pageInfo"),
            "oa": art.get("isOpenAccess") == "Y",
            "tem_abstract": bool(abstract),
            "nivel_acesso": nivel or "so_metadados",
            "arquivo": (f"fulltext/{chave}.txt" if nivel == "fulltext"
                        else f"pdfs/{chave}.pdf" if nivel == "pdf" else None),
            "rota": rota,
        })
        marca = {"fulltext": "TXT", "pdf": "PDF"}.get(nivel, "   ")
        print(f"  [{marca}] {pmid} {chave} ({rota})", file=sys.stderr)

    (BASE / "metadata.json").write_text(
        json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")

    n_full = sum(1 for r in registros if r["nivel_acesso"] == "fulltext")
    n_pdf = sum(1 for r in registros if r["nivel_acesso"] == "pdf")
    n_abs = sum(1 for r in registros if r["tem_abstract"])
    total = len(registros)
    print(f"\n{total} artigos | {n_full} texto completo | {n_pdf} PDF | "
          f"{n_abs} com abstract | "
          f"{100 * (n_full + n_pdf) / max(total, 1):.0f}% com conteudo integral",
          file=sys.stderr)


if __name__ == "__main__":
    main()
