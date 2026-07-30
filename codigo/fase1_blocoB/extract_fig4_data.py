"""
Extrai as curvas de qualidade antes/depois (Figure 4) para um CSV pequeno
e versionavel, para que a figura seja reproduzivel sem depender dos JSONs
completos do fastp (~45MB no servidor, nao versionados no repo).
"""
import json, os, csv

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/post_trim")
SAMPLES = ["ID-1", "ID-7", "ID-8", "ID-9", "ID-10"]
LABELS = {
    "ID-1": "Control_R1", "ID-7": "Benzamidine_R2", "ID-8": "Benzamidine_R3",
    "ID-9": "SKTI_R1", "ID-10": "SKTI_R2",
}

rows = []
for s in SAMPLES:
    with open(os.path.join(QC_DIR, f"{s}.fastp.json")) as f:
        d = json.load(f)
    before = d["read1_before_filtering"]["quality_curves"]["mean"]
    after = d["read1_after_filtering"]["quality_curves"]["mean"]
    for cycle, q in enumerate(before, start=1):
        rows.append(dict(sample=s, label=LABELS[s], cycle=cycle, stage="before", mean_phred=round(q, 4)))
    for cycle, q in enumerate(after, start=1):
        rows.append(dict(sample=s, label=LABELS[s], cycle=cycle, stage="after", mean_phred=round(q, 4)))

out_path = os.path.join(QC_DIR, "figure4_quality_curves.csv")
with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["sample", "label", "cycle", "stage", "mean_phred"])
    w.writeheader()
    w.writerows(rows)
print(f"CSV: {out_path} ({len(rows)} linhas)")
