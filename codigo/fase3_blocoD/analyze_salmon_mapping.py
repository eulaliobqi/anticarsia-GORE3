#!/usr/bin/env python3
"""FASE 3, Bloco D - le a taxa de mapeamento que o Salmon reporta no proprio
log (salmon/{amostra}/logs/salmon_quant.log) para as 13 amostras, compara
com a taxa combinada do STAR (resultados/fase2_blocoB_star_mapping_summary.csv)
e gera a Figura 7. Nao espera igualdade exata - Salmon (selective alignment
contra transcriptoma+decoy) e STAR (alinhamento contra genoma) sao
estruturalmente diferentes; a comparacao serve so como banda de
consistencia (ver Bloco F para o criterio numerico formal).
"""
import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parents[2]
STAR_SUMMARY = BASE / "resultados" / "fase2_blocoB_star_mapping_summary.csv"
TRIM_SUMMARY = BASE / "resultados" / "blocoB_trim_summary.csv"
SALMON_LOG_DIR = BASE / "qc" / "fase3_blocoD_salmon_logs"  # copiados do servidor antes de rodar isto
OUT_CSV = BASE / "resultados" / "fase3_blocoD_salmon_mapping_summary.csv"
OUT_FIGURE = BASE / "figuras" / "Figure7_fase3_blocoD_salmon_vs_star_mapping.png"

SAMPLES = ["ID-1", "ID-2", "ID-3", "ID-5", "ID-7", "ID-8", "ID-9",
           "ID-10", "ID-12", "ID-14", "ID-15", "ID-16", "ID-18"]

GROUP_ORDER = [
    "Control_R1", "Control_R2", "Control_R3",
    "Benzamidine_R1", "Benzamidine_R2", "Benzamidine_R3",
    "SKTI_R1", "SKTI_R2", "SKTI_R3",
    "GORE3_R1", "GORE3_R2", "GORE3_R3",
    "FatBody",
]


def parse_salmon_mapping_rate(log_path: Path) -> float:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Mapping rate = ([\d.]+)%", text)
    if not m:
        raise ValueError(f"taxa de mapeamento nao encontrada em {log_path}")
    return float(m.group(1))


def main():
    label_by_id = {}
    with open(TRIM_SUMMARY, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            label_by_id[row["id"]] = row["label"]

    star_combined = {}
    with open(STAR_SUMMARY, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            star_combined[row["id"]] = float(row["combined_mapped_pct"])

    rows = []
    for s in SAMPLES:
        log_path = SALMON_LOG_DIR / s / "salmon_quant.log"
        salmon_pct = parse_salmon_mapping_rate(log_path)
        star_pct = star_combined[s]
        rows.append({
            "id": s,
            "label": label_by_id[s],
            "salmon_mapping_pct": salmon_pct,
            "star_combined_mapping_pct": star_pct,
            "diff_pp": round(salmon_pct - star_pct, 2),
        })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Escrito: {OUT_CSV}")
    for r in rows:
        print(f"  {r['label']:16s} salmon={r['salmon_mapping_pct']:.2f}%  "
              f"star={r['star_combined_mapping_pct']:.2f}%  diff={r['diff_pp']:+.2f}pp")

    by_label = {r["label"]: r for r in rows}
    salmon_vals = [by_label[l]["salmon_mapping_pct"] for l in GROUP_ORDER]
    star_vals = [by_label[l]["star_combined_mapping_pct"] for l in GROUP_ORDER]

    x = np.arange(len(GROUP_ORDER))
    width = 0.38
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - width / 2, star_vals, width, label="STAR (unique + multi-mapped)", color="#2166ac")
    ax.bar(x + width / 2, salmon_vals, width, label="Salmon (decoy-aware, selective alignment)", color="#1b7837")
    ax.set_ylabel("Mapping rate (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(GROUP_ORDER, rotation=45, ha="right")
    ax.set_ylim(0, 100)
    ax.legend(loc="lower right", fontsize=9)
    ax.set_title("Figure 7 | Salmon vs. STAR mapping rate, all 13 libraries")
    fig.tight_layout()
    fig.savefig(OUT_FIGURE, dpi=300)
    print(f"Escrito: {OUT_FIGURE}")


if __name__ == "__main__":
    main()
