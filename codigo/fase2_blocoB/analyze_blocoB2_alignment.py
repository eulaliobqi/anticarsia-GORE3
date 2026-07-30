#!/usr/bin/env python3
"""FASE 2, Bloco B - conferencia e consolidacao dos dois alinhamentos completos
(STAR e Subread, 13 bibliotecas cada), rodados no servidor
(~/rnaseq-Anticarsia-GORE3/qc/fase2_blocoB_star/*_Log.final.out e
qc/fase2_blocoB_subread/*.subread_align.log, copiados para
eulalio-pos-doc/qc/fase2_blocoB_{star,subread}/ so para esta analise local -
os BAMs em si continuam so no servidor, sao grandes demais para o repo).

O QUE este script faz, e POR QUE cada passo existe:

1. Parseia os 13 Log.final.out do STAR (formato chave|valor do proprio STAR)
   e extrai as metricas completas de mapeamento - nao so a taxa unica+multi
   que ja estava no resumo anterior (resultados/fase2_blocoB_star_mapping_summary.csv),
   mas tambem juncoes de splicing (total/anotadas/nao-canonicas), taxa de
   mismatch/indel e a decomposicao do que NAO mapeou (too-short vs. other).
   Isso importa porque a decisao de aceitar o alinhamento como valido nao
   deveria se basear so num numero-resumo (a % de mapeamento); a
   decomposicao mostra SE a perda residual e' do tipo esperado (too-short,
   coerente com fragmentos curtos ja documentados na FASE 1) ou de um tipo
   que indicaria problema novo (ex. mismatch rate anormalmente alto,
   sinalizando contaminacao ou genoma errado).

2. Cruza o "Number of input reads" de cada amostra do STAR contra o
   "reads_after" (contagem pos-trimagem da FASE 1 Bloco B, ja versionado em
   resultados/blocoB_trim_summary.csv) - o STAR conta PARES de leitura, o
   arquivo da FASE 1 conta leituras totais (R1+R2), entao a checagem e'
   reads_after == input_reads * 2. Isso e' uma auditoria de encadeamento
   entre fases: confirma que o STAR de fato rodou sobre o FASTQ trimado
   certo de cada amostra, nao sobre um arquivo storage errado ou uma copia
   antiga - um erro desse tipo nao apareceria na taxa de mapeamento (o STAR
   mapearia normalmente um FASTQ errado), so nessa contagem cruzada.

3. Parseia os 13 logs do Subread-align (formato de texto livre do proprio
   subread, en-dashes "||", numeros em locale pt-BR - "." como separador de
   milhar, "," como decimal, ja que o servidor roda com essa locale) e
   extrai a taxa "Mapped" (unica, ja que o script de producao roda com
   "--sortReadsByCoordinates" e SEM multi-mapping habilitado - configuracao
   deliberada para a via de splicing, ver run_subread_align_full.sh).

4. Gera resultados/fase2_blocoB_star_full_stats.csv (13 linhas, todas as
   metricas do STAR) e resultados/fase2_blocoB_subread_stats.csv (13
   linhas, metricas do Subread), e a Figura 5 (barras agrupadas por
   tratamento, STAR vs. Subread, mesmo estilo das Figuras 1-4 do artigo).
"""

import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parents[2]
STAR_LOG_DIR = BASE / "qc" / "fase2_blocoB_star"
SUBREAD_LOG_DIR = BASE / "qc" / "fase2_blocoB_subread"
TRIM_SUMMARY_CSV = BASE / "resultados" / "blocoB_trim_summary.csv"
OUT_STAR_CSV = BASE / "resultados" / "fase2_blocoB_star_full_stats.csv"
OUT_SUBREAD_CSV = BASE / "resultados" / "fase2_blocoB_subread_stats.csv"
OUT_FIGURE = BASE / "figuras" / "Figure5_fase2_blocoB_mapping_rates.png"

SAMPLES = [
    "ID-1", "ID-2", "ID-3", "ID-5", "ID-7", "ID-8", "ID-9",
    "ID-10", "ID-12", "ID-14", "ID-15", "ID-16", "ID-18",
]


def _pct(s: str) -> float:
    """STAR escreve porcentagens como '82.35%' (ponto decimal, locale C)."""
    return float(s.strip().rstrip("%"))


def parse_star_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields = {}
    for line in text.splitlines():
        if "|" not in line:
            continue
        key, _, val = line.partition("|")
        fields[key.strip()] = val.strip()

    unique_pct = _pct(fields["Uniquely mapped reads %"])
    multi_pct = _pct(fields["% of reads mapped to multiple loci"])
    return {
        "input_read_pairs": int(fields["Number of input reads"]),
        "avg_input_length": float(fields["Average input read length"]),
        "unique_mapped_pct": unique_pct,
        "multi_mapped_pct": multi_pct,
        "combined_mapped_pct": round(unique_pct + multi_pct, 2),
        "too_many_loci_pct": _pct(fields["% of reads mapped to too many loci"]),
        "unmapped_too_short_pct": _pct(fields["% of reads unmapped: too short"]),
        "unmapped_other_pct": _pct(fields["% of reads unmapped: other"]),
        "mismatch_rate_pct": _pct(fields["Mismatch rate per base, %"]),
        "splices_total": int(fields["Number of splices: Total"]),
        "splices_annotated": int(fields["Number of splices: Annotated (sjdb)"]),
        "splices_noncanonical": int(fields["Number of splices: Non-canonical"]),
    }


def _pt_br_int(s: str) -> int:
    """Subread escreve inteiros em locale pt-BR: '26.065.883' = 26065883
    (ponto = separador de milhar, nao decimal - conferido inspecionando os
    logs brutos antes de escrever este parser)."""
    return int(s.strip().replace(".", ""))


def parse_subread_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    def grab(label: str) -> str:
        m = re.search(rf"\|\|\s*{re.escape(label)}\s*:\s*([^\|]+?)\s*\|\|", text)
        if not m:
            raise ValueError(f"campo '{label}' nao encontrado em {path.name}")
        return m.group(1).strip()

    total_fragments = _pt_br_int(grab("Total fragments").split()[0])
    mapped_raw = grab("Mapped")
    mapped_n = _pt_br_int(mapped_raw.split()[0])
    mapped_pct = float(mapped_raw.split("(")[1].rstrip("%)").replace(",", "."))
    indels = _pt_br_int(grab("Indels"))
    completed = "Completed successfully." in text

    return {
        "total_fragments": total_fragments,
        "mapped_pct": mapped_pct,
        "mapped_n": mapped_n,
        "indels": indels,
        "completed_successfully": completed,
    }


def main() -> None:
    # --- carrega o mapa id -> label + reads_after da FASE 1, para o cruzamento (passo 2) ---
    trim = {}
    with open(TRIM_SUMMARY_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            trim[row["id"]] = row

    star_rows = []
    subread_rows = []
    crosscheck_failures = []

    for sample in SAMPLES:
        star = parse_star_log(STAR_LOG_DIR / f"{sample}_Log.final.out")
        subread = parse_subread_log(SUBREAD_LOG_DIR / f"{sample}.subread_align.log")

        expected_total_reads = int(trim[sample]["reads_after"])
        observed_total_reads = star["input_read_pairs"] * 2
        if observed_total_reads != expected_total_reads:
            crosscheck_failures.append(
                f"{sample}: STAR input_reads*2={observed_total_reads} != "
                f"FASE1 reads_after={expected_total_reads}"
            )

        label = trim[sample]["label"]
        star_rows.append({"id": sample, "label": label, **star})
        subread_rows.append({"id": sample, "label": label, **subread})

    # --- passo 2: auditoria de encadeamento FASE1 -> FASE2, falha alto e claro se algo nao bater ---
    if crosscheck_failures:
        raise SystemExit(
            "Cruzamento reads_after (FASE 1) x input_reads*2 (STAR) FALHOU:\n"
            + "\n".join(crosscheck_failures)
        )
    print(f"OK: input_reads*2 do STAR bate com reads_after da FASE 1 nas {len(SAMPLES)} amostras.")

    incomplete_subread = [r["id"] for r in subread_rows if not r["completed_successfully"]]
    if incomplete_subread:
        raise SystemExit(f"Subread sem marcador 'Completed successfully.': {incomplete_subread}")
    print(f"OK: as {len(SAMPLES)} amostras do Subread terminaram com 'Completed successfully.'")

    # --- passo 4a: escreve os CSVs ---
    with open(OUT_STAR_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(star_rows[0].keys()))
        writer.writeheader()
        writer.writerows(star_rows)

    with open(OUT_SUBREAD_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(subread_rows[0].keys()))
        writer.writeheader()
        writer.writerows(subread_rows)

    print(f"Escrito: {OUT_STAR_CSV}")
    print(f"Escrito: {OUT_SUBREAD_CSV}")

    # --- passo 4b: Figura 5 - STAR (combinado) vs. Subread (mapped), por amostra, agrupado por tratamento ---
    # Ordem por grupo de tratamento (mesma ordem das Tabelas 1-4 do artigo),
    # nao alfabetica por ID, para que o agrupamento visual corresponda ao
    # desenho experimental (4 grupos x 3 replicas + FatBody isolado).
    group_order = [
        "Control_R1", "Control_R2", "Control_R3",
        "Benzamidine_R1", "Benzamidine_R2", "Benzamidine_R3",
        "SKTI_R1", "SKTI_R2", "SKTI_R3",
        "GORE3_R1", "GORE3_R2", "GORE3_R3",
        "FatBody",
    ]
    star_by_label = {r["label"]: r for r in star_rows}
    subread_by_label = {r["label"]: r for r in subread_rows}

    star_vals = [star_by_label[label]["combined_mapped_pct"] for label in group_order]
    subread_vals = [subread_by_label[label]["mapped_pct"] for label in group_order]

    x = np.arange(len(group_order))
    width = 0.38

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - width / 2, star_vals, width, label="STAR (unique + multi-mapped)", color="#2166ac")
    ax.bar(x + width / 2, subread_vals, width, label="Subread (unique, multi-mapping disabled)", color="#b2182b")
    ax.axhline(80, color="black", linestyle="--", linewidth=1, label="80% acceptance threshold")

    ax.set_ylabel("Mapping rate (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(group_order, rotation=45, ha="right")
    ax.set_ylim(0, 100)
    ax.legend(loc="lower right", fontsize=9)
    ax.set_title(
        "Figure 5 | Full-batch mapping rate, STAR vs. Subread, all 13 libraries"
    )
    fig.tight_layout()
    fig.savefig(OUT_FIGURE, dpi=300)
    print(f"Escrito: {OUT_FIGURE}")


if __name__ == "__main__":
    main()
