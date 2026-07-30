#!/usr/bin/env python3
"""FASE 3, Bloco F - tres checagens de consistencia entre os dois
quantificadores independentes (featureCounts Bloco C, Salmon+tximport
Blocos D-E), equivalente ao cross-check que a FASE 2
(analyze_blocoB2_alignment.py) fez entre STAR e a contagem pos-trimagem da
FASE 1.

1. featureCounts Assigned vs. reads unicamente mapeados do STAR: como o
   Bloco C nao usa -M, Assigned nao deveria superar
   uniquely_mapped_pct x reads de cada amostra - alerta se superar ou se o
   gap for atipico numa amostra especifica.
2. Taxa de mapeamento Salmon vs. STAR: nao e' esperada igualdade exata
   (metodos estruturalmente diferentes - selective alignment
   transcriptoma+decoy vs. alinhamento genomico) - banda de tolerancia de
   ~10pp, alerta so fora dela.
3. Concordancia gene a gene entre os dois quantificadores (Spearman,
   featureCounts vs. tximport) - checagem nova desta fase, os dois
   quantificadores deveriam concordar em nivel de gene mesmo medindo
   coisas estruturalmente diferentes.
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

BASE = Path(__file__).resolve().parents[2]
STAR_SUMMARY = BASE / "resultados" / "fase2_blocoB_star_mapping_summary.csv"
FC_SUMMARY = BASE / "resultados" / "fase3_blocoC_featurecounts_summary.csv"
SALMON_SUMMARY = BASE / "resultados" / "fase3_blocoD_salmon_mapping_summary.csv"
FC_COUNTS = BASE / "resultados" / "fase3_blocoC_gene_counts.txt"
TXIMPORT_COUNTS = BASE / "resultados" / "fase3_blocoE_salmon_gene_counts.tsv"
OUT_CSV = BASE / "resultados" / "fase3_blocoF_crosscheck.csv"
OUT_FIGURE = BASE / "figuras" / "Figure8_fase3_blocoF_featurecounts_vs_salmon_concordance.png"

TOLERANCE_PP = 10.0


def check1_assigned_vs_unique(star_rows, fc_rows):
    star_by_id = {r["id"]: r for r in star_rows}
    flags = []
    for r in fc_rows:
        star = star_by_id[r["id"]]
        # unique reads em numero absoluto = uniquely_mapped_pct% dos reads totais
        total_reads = int(r["total_reads"])
        unique_pct = float(star["uniquely_mapped_pct"])
        unique_reads_abs = unique_pct / 100 * total_reads
        assigned = int(r["assigned_reads"])
        ok = assigned <= unique_reads_abs
        flags.append({
            "id": r["id"], "check": "assigned_vs_unique",
            "assigned": assigned, "unique_reads_est": round(unique_reads_abs),
            "ok": ok,
        })
    return flags


def check2_salmon_vs_star_band(salmon_rows):
    flags = []
    for r in salmon_rows:
        diff = abs(float(r["diff_pp"]))
        ok = diff <= TOLERANCE_PP
        flags.append({"id": r["id"], "check": "salmon_vs_star_band", "diff_pp": r["diff_pp"], "ok": ok})
    return flags


def check3_concordance():
    # featureCounts: Geneid + colunas por BAM; tximport: genes x amostras (rounded counts)
    with open(FC_COUNTS, encoding="utf-8") as fh:
        lines = [l for l in fh if not l.startswith("#")]
    fc_header = lines[0].rstrip("\n").split("\t")
    fc_samples = [Path(c).stem for c in fc_header[6:]]
    fc_data = {}
    for line in lines[1:]:
        parts = line.rstrip("\n").split("\t")
        fc_data[parts[0]] = [int(v) for v in parts[6:]]

    with open(TXIMPORT_COUNTS, encoding="utf-8") as fh:
        tx_header = fh.readline().rstrip("\n").split("\t")
        tx_samples = tx_header[1:]
        tx_data = {}
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            tx_data[parts[0]] = [float(v) for v in parts[1:]]

    common_samples = [s for s in fc_samples if s in tx_samples]
    common_genes = sorted(set(fc_data) & set(tx_data))

    rhos = []
    for s in common_samples:
        fc_idx = fc_samples.index(s)
        tx_idx = tx_samples.index(s)
        fc_vals = [fc_data[g][fc_idx] for g in common_genes]
        tx_vals = [tx_data[g][tx_idx] for g in common_genes]
        rho, _ = spearmanr(fc_vals, tx_vals)
        rhos.append((s, rho))
    return rhos, common_samples


def main():
    star_rows = list(csv.DictReader(open(STAR_SUMMARY, newline="", encoding="utf-8")))
    fc_rows = list(csv.DictReader(open(FC_SUMMARY, newline="", encoding="utf-8")))
    salmon_rows = list(csv.DictReader(open(SALMON_SUMMARY, newline="", encoding="utf-8")))

    c1 = check1_assigned_vs_unique(star_rows, fc_rows)
    c2 = check2_salmon_vs_star_band(salmon_rows)
    rhos, common_samples = check3_concordance()

    all_ok_1 = all(f["ok"] for f in c1)
    all_ok_2 = all(f["ok"] for f in c2)
    print(f"Checagem 1 (Assigned <= unique mapped): {'OK' if all_ok_1 else 'ALERTA'}")
    for f in c1:
        if not f["ok"]:
            print(f"  ALERTA {f['id']}: assigned={f['assigned']} > unique_est={f['unique_reads_est']}")
    print(f"Checagem 2 (Salmon vs STAR dentro de {TOLERANCE_PP}pp): {'OK' if all_ok_2 else 'ALERTA'}")
    for f in c2:
        if not f["ok"]:
            print(f"  ALERTA {f['id']}: diff={f['diff_pp']}pp")
    print("Checagem 3 (concordancia Spearman featureCounts x tximport, por amostra):")
    for s, rho in rhos:
        print(f"  {s}: rho={rho:.3f}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["sample", "spearman_rho_featurecounts_vs_tximport"])
        for s, rho in rhos:
            w.writerow([s, round(rho, 4)])
    print(f"Escrito: {OUT_CSV}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([s for s, _ in rhos], [rho for _, rho in rhos], color="#762a83")
    ax.set_ylabel("Spearman rho (gene counts)")
    ax.set_ylim(0, 1)
    ax.set_title("Figure 8 | Gene-level concordance: featureCounts vs. Salmon+tximport")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUT_FIGURE, dpi=300)
    print(f"Escrito: {OUT_FIGURE}")


if __name__ == "__main__":
    main()
