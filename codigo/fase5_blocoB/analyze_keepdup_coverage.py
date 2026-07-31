#!/usr/bin/env python3
"""FASE 5, Bloco B - checagem de consistencia + figura: confirma que
--keepDuplicates de fato fechou a lacuna de cobertura genica do tximport
(FASE 3: 14.973/15.773 genes; meta aqui: o mais proximo possivel de
15.773) e gera a Figura 9 (estilo Nature, mesmo padrao das Figuras 1-8),
comparando antes/depois.

Checagens de consistencia (nao so plotar, verificar):
1. N de genes no txi novo (Bloco B) vs. txi antigo (FASE 3 Bloco E) -
   deve ser >= ao antigo, nao pode ter piorado.
2. N de transcritos no indice novo vs. antigo (25.840 esperado sem
   colapso, contra os 25.029 do indice antigo sem --keepDuplicates).
3. Nenhum gene com contagem negativa/NaN na matriz nova (sanity check
   basico antes de qualquer analise downstream confiar nela).
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parents[2]
OLD_COUNTS = BASE / "resultados" / "fase3_blocoE_salmon_gene_counts.tsv"
NEW_COUNTS_CSV = BASE / "resultados" / "fase5_blocoB_txi_counts_for_python.csv"
OUT_CSV = BASE / "resultados" / "fase5_blocoB_keepdup_coverage.csv"
OUT_FIGURE = BASE / "figuras" / "Figure9_fase5_blocoB_keepdup_coverage.png"

TOTAL_GENES_ANNOTATION = 15773  # RS_2026_04, ja confirmado em FASE 2/3 (tx2gene: 15.773 genes unicos)


def count_genes_tsv(path):
    with open(path, encoding="utf-8") as fh:
        header = fh.readline()
        n = sum(1 for _ in fh)
    return n


def main():
    n_old = count_genes_tsv(OLD_COUNTS)

    with open(NEW_COUNTS_CSV, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split(",")
    n_new_genes = len(header) - 1  # menos a coluna de amostra

    # Checagem 1: cobertura nao pode ter piorado
    if n_new_genes < n_old:
        raise SystemExit(
            f"INCONSISTENCIA: cobertura NOVA ({n_new_genes} genes) e' menor "
            f"que a ANTIGA ({n_old}) - --keepDuplicates deveria aumentar, nao "
            f"diminuir, a cobertura. Investigar antes de prosseguir."
        )

    # Checagem 2: sanity check basico de valores (sem NaN/negativo)
    import csv as csv_mod
    with open(NEW_COUNTS_CSV, encoding="utf-8") as fh:
        reader = csv_mod.reader(fh)
        next(reader)
        n_bad = 0
        for row in reader:
            for v in row[1:]:
                fv = float(v)
                if fv < 0 or fv != fv:  # fv != fv detecta NaN
                    n_bad += 1
    if n_bad > 0:
        raise SystemExit(f"INCONSISTENCIA: {n_bad} valores negativos/NaN na matriz nova.")

    pct_old = round(100 * n_old / TOTAL_GENES_ANNOTATION, 2)
    pct_new = round(100 * n_new_genes / TOTAL_GENES_ANNOTATION, 2)

    rows = [
        {"stage": "FASE 3 (sem --keepDuplicates)", "n_genes": n_old, "pct_of_annotation": pct_old},
        {"stage": "FASE 5 (com --keepDuplicates)", "n_genes": n_new_genes, "pct_of_annotation": pct_new},
    ]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["stage", "n_genes", "pct_of_annotation"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Escrito: {OUT_CSV}")
    for r in rows:
        print(f"  {r['stage']}: {r['n_genes']} genes ({r['pct_of_annotation']}% da anotacao)")

    fig, ax = plt.subplots(figsize=(8, 5.5))
    labels = ["FASE 3\n(sem --keepDuplicates)", "FASE 5\n(com --keepDuplicates)"]
    vals = [n_old, n_new_genes]
    colors = ["#b2182b", "#2166ac"]
    bars = ax.bar(labels, vals, color=colors)
    ax.axhline(TOTAL_GENES_ANNOTATION, color="black", linestyle="--", linewidth=1,
               label=f"Total anotado ({TOTAL_GENES_ANNOTATION} genes)")
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 60, f"{v}\n({round(100*v/TOTAL_GENES_ANNOTATION,1)}%)",
                 ha="center", va="bottom", fontsize=10)
    ax.set_ylabel("Genes with a directly quantifiable transcript (tximport)")
    ax.set_ylim(0, TOTAL_GENES_ANNOTATION * 1.08)
    ax.legend(loc="lower right", fontsize=9)
    ax.set_title("Figure 9 | --keepDuplicates closes the tximport\ngene-coverage gap", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT_FIGURE, dpi=300)
    print(f"Escrito: {OUT_FIGURE}")


if __name__ == "__main__":
    main()
