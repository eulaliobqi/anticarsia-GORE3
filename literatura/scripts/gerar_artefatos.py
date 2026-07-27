#!/usr/bin/env python3
"""
Gera os artefatos derivados a partir de ../metadata.json (verificado no
Europe PMC): BibTeX, INDEX.json, PDFS_PENDENTES.md e os esqueletos das
fichas tematicas.

REGRA DE PROVENIENCIA: este script NAO escreve interpretacao de artigo.
Ele emite metadados verificados e marca o campo interpretativo como
PENDENTE DE FICHAMENTO. O texto de "O que estabelece" e escrito a mao,
depois de ler a fonte, e o campo "Lido de" registra o que foi lido.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from fichas_tier1 import FICHAS

BASE = Path(__file__).resolve().parent.parent
META = json.loads((BASE / "metadata.json").read_text(encoding="utf-8"))

TEMAS = {
    1: ("01_peptideos_inibidores_tripsina.md",
        "Tema 1 — Peptideos inibidores de tripsina"),
    2: ("02_rnaseq.md", "Tema 2 — RNA-Seq"),
    3: ("03_biologia_estrutural.md", "Tema 3 — Biologia estrutural"),
    4: ("04_manejo_anticarsia.md", "Tema 4 — Manejo de Anticarsia com peptideos"),
}

EIXOS = {
    "1A": "Peptideos curtos racionalmente desenhados e derivados de reactive center loop",
    "1B": "Tripsinas digestivas de Lepidoptera: isoformas e especificidade",
    "1C": "Adaptacao do inseto e resposta compensatoria a inibidores",
    "1D": "Cinetica de inibicao e o modelo canonico",
    "2A": "Artigos-fonte das ferramentas prescritas na metodologia",
    "2B": "Benchmarks e boas praticas (recencia exigida: 2023+)",
    "2C": "Transcriptomica de intestino de inseto sob estresse",
    "2D": "Fronteira 2024-2026",
    "3A": "Predicao de estrutura",
    "3B": "Docking proteina-peptideo",
    "3C": "Campos de forca e dinamica molecular",
    "3D": "Energia livre de ligacao e suas limitacoes",
    "3E": "Arquitetura de subsitios de serino-proteases",
    "4A": "A praga e o dano (fonte primaria)",
    "4B": "Taticas atuais de controle",
    "4C": "Bioinseticidas peptidicos, entrega e seletividade",
    "4D": "Recursos genomicos",
}

LATEX = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_"}


def esc(txt):
    if not txt:
        return ""
    for k, v in LATEX.items():
        txt = txt.replace(k, v)
    return txt


def autores_bibtex(s):
    """'Silva J, Souza M A' -> 'Silva, J. and Souza, M. A.'"""
    saida = []
    for a in (s or "").split(","):
        a = a.strip()
        if not a:
            continue
        p = a.split()
        if len(p) > 1 and all(len(x) <= 2 and x.isupper() for x in p[-1:]):
            saida.append(f"{' '.join(p[:-1])}, {'. '.join(p[-1])}.")
        else:
            saida.append(a)
    return " and ".join(saida)


def gerar_bib(regs):
    out = [
        "% " + "=" * 58,
        "% Levantamento bibliografico — Pos-doc GORE3",
        "% Gerado por literatura/scripts/gerar_artefatos.py",
        "%",
        "% REGRA: so entram aqui referencias com DOI ou PMID VERIFICADO.",
        "% Metadados (DOI, volume, paginas, status de acesso aberto) obtidos",
        "% do Europe PMC (resultType=core) em 27/07/2026, a partir de PMIDs",
        "% localizados nas buscas registradas em 00_PROTOCOLO_BUSCA.md.",
        "%",
        "% O campo 'note' registra tema/eixo e o nivel de acesso obtido:",
        "%   fulltext = texto completo salvo em literatura/fulltext/",
        "%   pdf      = PDF salvo em literatura/pdfs/",
        "%   abstract = apenas abstract salvo em literatura/abstracts/",
        "% " + "=" * 58,
        "",
    ]
    for tema in sorted(TEMAS):
        doreg = [r for r in regs if r["tema"] == tema and not r["ja_no_bib"]]
        if not doreg:
            continue
        out += ["", "% " + "-" * 58,
                f"% {TEMAS[tema][1].upper()}",
                "% " + "-" * 58, ""]
        for r in sorted(doreg, key=lambda x: (x["eixo"], x["chave"])):
            campos = [
                ("author", autores_bibtex(r["autores"])),
                ("title", esc(r["titulo"])),
                ("journal", esc(r["revista"])),
                ("volume", r["volume"]),
                ("number", r["numero"]),
                ("pages", (r["paginas"] or "").replace("-", "--") or None),
                ("year", r["ano"]),
                ("doi", r["doi"]),
                ("pmid", r["pmid"]),
                ("pmcid", r["pmcid"]),
            ]
            out.append(f"@article{{{r['chave']},")
            for k, v in campos:
                if v:
                    out.append(f"  {k:8s}= {{{v}}},")
            nivel = {"fulltext": "texto completo", "pdf": "PDF",
                     }.get(r["nivel_acesso"], "abstract")
            out.append(f"  note    = {{eixo {r['eixo']}; tier {r['tier']}; "
                       f"acesso: {nivel}}}")
            out.append("}")
            out.append("")
    return "\n".join(out)


def gerar_fichas(regs):
    for tema, (arquivo, titulo) in TEMAS.items():
        doreg = [r for r in regs if r["tema"] == tema]
        if not doreg:
            continue
        porx = defaultdict(list)
        for r in doreg:
            porx[r["eixo"]].append(r)

        n_full = sum(1 for r in doreg if r["nivel_acesso"] == "fulltext")
        n_fich = sum(1 for r in doreg if r["chave"] in FICHAS)
        L = [
            f"# {titulo}",
            "",
            f"{len(doreg)} referências | {n_full} com texto completo em disco | "
            f"**{n_fich} fichadas** | busca de 27/07/2026",
            "",
            "Todos os metadados (DOI, volume, páginas) foram verificados no",
            "Europe PMC. O campo **Lido de** declara o que foi efetivamente lido",
            "**ao escrever a ficha** — ter o texto completo salvo em disco não",
            "significa tê-lo lido. Ficha marcada `abstract` não contém número ou",
            "detalhe de protocolo que só apareceria no corpo do artigo; onde o",
            "dado falta e importa, a ressalva diz isso em vez de preencher.",
            "",
            "Ver [protocolo de busca](00_PROTOCOLO_BUSCA.md) e",
            "[PDFs pendentes](PDFS_PENDENTES.md).",
            "",
            "---",
            "",
        ]
        for eixo in sorted(porx):
            L += [f"## {eixo} — {EIXOS.get(eixo, '')}", ""]
            for r in sorted(porx[eixo], key=lambda x: (x["tier"], x["ano"] or "")):
                ident = []
                if r["doi"]:
                    ident.append(f"DOI: [{r['doi']}](https://doi.org/{r['doi']})")
                ident.append(
                    f"PMID: [{r['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/)")
                if r["pmcid"]:
                    ident.append(f"PMC: {r['pmcid']}")

                # O que foi efetivamente LIDO ao escrever a ficha — nao o que
                # esta disponivel em disco. Ter o texto completo salvo nao
                # significa te-lo lido.
                ficha = FICHAS.get(r["chave"])
                if ficha:
                    lido = {"fulltext": "**texto completo** — seções de "
                                        "resultados/discussão",
                            "abstract": "**abstract**"}[ficha["lido"]]
                else:
                    disp = {"fulltext": "texto completo disponível",
                            "pdf": "PDF disponível"}.get(
                                r["nivel_acesso"],
                                "abstract disponível" if r["tem_abstract"]
                                else "só metadados")
                    lido = f"nada ainda ({disp})"

                loc = (f"`{r['revista_abrev'] or r['revista']}` "
                       f"{r['ano']}")
                if r["volume"]:
                    loc += f";{r['volume']}"
                    if r["numero"]:
                        loc += f"({r['numero']})"
                if r["paginas"]:
                    loc += f":{r['paginas']}"

                marca = " ✅ ja em docs/referencias.bib" if r["ja_no_bib"] else ""
                L += [
                    f"### `{r['chave']}` — Tier {r['tier']}{marca}",
                    f"**{r['autores']}** ({r['ano']}). {r['titulo']}. {loc}.",
                    "",
                    " · ".join(ident),
                    f"**Lido de:** {lido}"
                    + (f" · arquivo: `{r['arquivo']}`" if r["arquivo"] else ""),
                    "",
                ]
                if ficha:
                    L += [f"**O que estabelece:** {ficha['estabelece']}", "",
                          f"**Onde entra:** {ficha['onde_entra']}", "",
                          f"**Ressalva:** {ficha['ressalva']}", ""]
                else:
                    L += ["**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO",
                          "**Onde entra:** ⚠️ PENDENTE", ""]
        (BASE / arquivo).write_text("\n".join(L), encoding="utf-8")
        print(f"  {arquivo}: {len(doreg)} refs")


def gerar_pendentes(regs):
    fechados = [r for r in regs if r["nivel_acesso"] == "so_metadados"]
    L = [
        "# PDFs pendentes de download manual",
        "",
        f"{len(fechados)} de {len(regs)} artigos nao tem versao de acesso aberto",
        "recuperavel automaticamente. Para estes, so o abstract foi salvo.",
        "",
        "Baixar manualmente via CAFe/UFV (o link do DOI resolve para a pagina do",
        "editor; com a sessao institucional ativa o PDF fica disponivel).",
        "Salvar em `pdfs/{chave}.pdf` usando exatamente a chave BibTeX da tabela.",
        "",
        "Rotas ja tentadas automaticamente, todas sem sucesso para estes itens:",
        "Europe PMC `fullTextXML` e Unpaywall `best_oa_location`.",
        "",
        "| Chave BibTeX | Tema/eixo | Tier | Ano | Revista | Link |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(fechados, key=lambda x: (x["tema"], x["eixo"], x["tier"])):
        link = (f"[DOI](https://doi.org/{r['doi']})" if r["doi"]
                else f"[PubMed](https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/)")
        L.append(f"| `{r['chave']}` | {r['eixo']} | {r['tier']} | {r['ano']} | "
                 f"{r['revista_abrev'] or r['revista']} | {link} |")
    L += ["", f"Prioridade: os {sum(1 for r in fechados if r['tier'] == 1)} "
          "itens Tier 1 primeiro — sao os que precisam de leitura integral."]
    (BASE / "PDFS_PENDENTES.md").write_text("\n".join(L), encoding="utf-8")
    return len(fechados)


def main():
    (BASE / "referencias_novas.bib").write_text(gerar_bib(META),
                                                encoding="utf-8")
    gerar_fichas(META)
    n_fechados = gerar_pendentes(META)

    (BASE / "INDEX.json").write_text(json.dumps({
        "gerado_em": "2026-07-27",
        "fonte_metadados": "Europe PMC REST resultType=core",
        "total": len(META),
        "por_tema": dict(Counter(r["tema"] for r in META)),
        "por_eixo": dict(sorted(Counter(r["eixo"] for r in META).items())),
        "por_tier": dict(Counter(r["tier"] for r in META)),
        "por_acesso": dict(Counter(r["nivel_acesso"] for r in META)),
        "artigos": META,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    anos = [int(r["ano"]) for r in META if (r["ano"] or "").isdigit()]
    anos.sort()
    print(f"\nreferencias_novas.bib | INDEX.json | PDFS_PENDENTES.md "
          f"({n_fechados} fechados)")
    print(f"mediana de ano: {anos[len(anos) // 2]} | "
          f"{sum(1 for a in anos if a >= 2023)} de {len(anos)} sao 2023+")


if __name__ == "__main__":
    main()
