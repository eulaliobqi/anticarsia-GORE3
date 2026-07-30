#!/usr/bin/env python3
"""FASE 3, Bloco E - deriva o samplesheet (sample,condition,replicate) para o
tximport a partir dos rotulos ja confirmados em resultados/blocoB_trim_summary.csv
(ex. "Control_R1" -> condition=Control, replicate=1) - nao re-digitar/
re-derivar o mapeamento amostra->grupo manualmente."""
import csv
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
TRIM_SUMMARY = BASE / "resultados" / "blocoB_trim_summary.csv"
OUT_CSV = BASE / "resultados" / "fase3_blocoE_samplesheet.csv"

LABEL_RE = re.compile(r"^(.+?)_R(\d+)$")


def main():
    rows = []
    with open(TRIM_SUMMARY, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            label = row["label"]
            m = LABEL_RE.match(label)
            if m:
                condition, replicate = m.group(1), m.group(2)
            else:
                # FatBody: sem replicata, fora do desenho de 4 grupos
                condition, replicate = label, ""
            rows.append({"sample": row["id"], "condition": condition, "replicate": replicate})

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["sample", "condition", "replicate"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Escrito: {OUT_CSV}")
    for r in rows:
        print(f"  {r['sample']:6s} {r['condition']:14s} rep={r['replicate']}")


if __name__ == "__main__":
    main()
