#!/usr/bin/env python3
"""FASE 3, Bloco C - resume o featureCounts de producao (gene_counts.txt.summary)
em % de reads atribuidos por amostra, e gera a Figura 6 (mesmo estilo visual
da Figura 5, agrupado por tratamento).

Reaproveita os rotulos de tratamento ja confirmados em
resultados/blocoB_trim_summary.csv (Control_R1, Benzamidine_R2, etc.) - nao
re-derivar do zero, mesma pratica das FASES anteriores.
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parents[2]
SUMMARY_RAW = BASE / "resultados" / "fase3_blocoC_gene_counts_summary_raw.txt"
TRIM_SUMMARY_CSV = BASE / "resultados" / "blocoB_trim_summary.csv"
OUT_CSV = BASE / "resultados" / "fase3_blocoC_featurecounts_summary.csv"
OUT_FIGURE = BASE / "figuras" / "Figure6_fase3_blocoC_featurecounts_assigned.png"

GROUP_ORDER = [
    "Control_R1", "Control_R2", "Control_R3",
    "Benzamidine_R1", "Benzamidine_R2", "Benzamidine_R3",
    "SKTI_R1", "SKTI_R2", "SKTI_R3",
    "GORE3_R1", "GORE3_R2", "GORE3_R3",
    "FatBody",
]


def main():
    # --- parseia o .summary (formato: linha "Status" com os nomes de BAM nas colunas) ---
    with open(SUMMARY_RAW, encoding="utf-8") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    header = rows[0]  # ["Status", "bam/star/ID-1.bam", ...]
    sample_ids = [Path(col).stem for col in header[1:]]  # "ID-1", "ID-2", ...

    data = {row[0]: [int(v) for v in row[1:]] for row in rows[1:]}

    # --- carrega rotulos de tratamento ja confirmados na FASE 1 ---
    label_by_id = {}
    with open(TRIM_SUMMARY_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            label_by_id[row["id"]] = row["label"]

    out_rows = []
    for i, sample_id in enumerate(sample_ids):
        assigned = data["Assigned"][i]
        total = sum(v[i] for v in data.values())
        pct = round(100 * assigned / total, 2)
        out_rows.append({
            "id": sample_id,
            "label": label_by_id[sample_id],
            "assigned_reads": assigned,
            "total_reads": total,
            "pct_assigned": pct,
        })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"Escrito: {OUT_CSV}")
    for r in sorted(out_rows, key=lambda r: -r["pct_assigned"]):
        print(f"  {r['label']:16s} {r['pct_assigned']:.2f}%")

    # --- Figura 6: % atribuido por amostra, ordenado por grupo de tratamento ---
    by_label = {r["label"]: r for r in out_rows}
    vals = [by_label[label]["pct_assigned"] for label in GROUP_ORDER]

    x = np.arange(len(GROUP_ORDER))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x, vals, color="#2166ac")
    ax.set_ylabel("Reads assigned to genes (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(GROUP_ORDER, rotation=45, ha="right")
    ax.set_ylim(0, 100)
    ax.set_title("Figure 6 | featureCounts gene-level assignment rate, 13 libraries")
    fig.tight_layout()
    fig.savefig(OUT_FIGURE, dpi=300)
    print(f"Escrito: {OUT_FIGURE}")


if __name__ == "__main__":
    main()
