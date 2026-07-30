#!/usr/bin/env python3
"""FASE 3/4 - reverifica a assimetria de profundidade entre grupos de
tratamento (declarada na FASE 1, artigo.md Secao 3.7) usando reads
efetivamente atribuidos a genes (featureCounts, Bloco C) - nao mais so a
sobrevivencia bruta da trimagem (FASE 1) - para responder ao item 1 do
plano de acao declarado em artigo.md Secao 4 ("re-verify per-contrast
depth asymmetry after alignment").
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FC_SUMMARY = BASE / "resultados" / "fase3_blocoC_featurecounts_summary.csv"
OUT_CSV = BASE / "resultados" / "fase3_blocoF_depth_asymmetry_recheck.csv"


def main():
    groups = {}
    with open(FC_SUMMARY, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            label = row["label"]
            if label == "FatBody":
                continue
            group = label.rsplit("_R", 1)[0]
            groups.setdefault(group, []).append(int(row["assigned_reads"]))

    control_mean = sum(groups["Control"]) / len(groups["Control"])

    rows = []
    for group, vals in groups.items():
        total = sum(vals)
        mean = total / len(vals)
        pct_of_control = round(100 * mean / control_mean, 1)
        rows.append({
            "group": group, "n": len(vals), "assigned_reads_sum": total,
            "assigned_reads_mean": round(mean),
            "pct_of_control_mean": pct_of_control,
        })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Escrito: {OUT_CSV}")
    for r in rows:
        print(f"  {r['group']:14s} soma={r['assigned_reads_sum']:>12,} "
              f"media={r['assigned_reads_mean']:>10,} "
              f"({r['pct_of_control_mean']}% do controle)")


if __name__ == "__main__":
    main()
