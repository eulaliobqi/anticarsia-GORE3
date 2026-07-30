"""
Bloco A (FASE 1) - analise objetiva do QC bruto FastQC/MultiQC.
Extrai Total Sequences, sincronia de pares R1/R2, e testa o criterio
pre-declarado de queda de qualidade na janela de ciclos 44-90 do R1
para as 13 amostras. Gera CSV + figura (Figure 1 do artigo.md).

Uso: python3 analyze_blocoA.py
Entrada: ~/rnaseq-Anticarsia-GORE3/qc/pre_trim/*_fastqc.zip
Saida:   ~/rnaseq-Anticarsia-GORE3/qc/pre_trim/blocoA_results.csv
         ~/rnaseq-Anticarsia-GORE3/qc/pre_trim/Figure1_blocoA_quality_dip.png
"""
import zipfile, glob, re, os, csv

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/pre_trim")
SAMPLES = ["ID-1","ID-2","ID-3","ID-5","ID-7","ID-8","ID-9","ID-10","ID-12","ID-14","ID-15","ID-16","ID-18"]
LABELS = {
    "ID-1":"Control_R1","ID-2":"Control_R2","ID-3":"Control_R3",
    "ID-5":"Benzamidine_R1","ID-7":"Benzamidine_R2","ID-8":"Benzamidine_R3",
    "ID-9":"SKTI_R1","ID-10":"SKTI_R2","ID-12":"SKTI_R3",
    "ID-14":"GORE3_R1","ID-15":"GORE3_R2","ID-16":"GORE3_R3",
    "ID-18":"FatBody",
}
DELTA_THRESHOLD = 5.0  # Phred, pre-declarado antes de rodar

def read_fastqc_data(sample, read):
    zpath = os.path.join(QC_DIR, f"{sample}_{read}_fastqc.zip")
    with zipfile.ZipFile(zpath) as z:
        inner = f"{sample}_{read}_fastqc/fastqc_data.txt"
        with z.open(inner) as f:
            return f.read().decode("utf-8", errors="replace")

def parse_total_sequences(text):
    m = re.search(r"Total Sequences\s+(\d+)", text)
    return int(m.group(1)) if m else None

def parse_module(text, name):
    pat = re.compile(r">>" + re.escape(name) + r"\t(\w+)\n(.*?)\n>>END_MODULE", re.S)
    m = pat.search(text)
    return (m.group(1), m.group(2)) if m else (None, None)

def parse_per_base_quality(block):
    rows = []
    for line in block.splitlines():
        if line.startswith("#Base"):
            continue
        parts = line.split("\t")
        base, mean = parts[0], float(parts[1])
        if "-" in base:
            lo, hi = map(int, base.split("-"))
        else:
            lo = hi = int(base)
        rows.append((lo, hi, mean))
    return rows

def windowed_mean(rows, lo_bound, hi_bound):
    total_w, total_wq = 0.0, 0.0
    for lo, hi, mean in rows:
        ov_lo, ov_hi = max(lo, lo_bound), min(hi, hi_bound)
        if ov_lo > ov_hi:
            continue
        w = ov_hi - ov_lo + 1
        total_w += w
        total_wq += w * mean
    return (total_wq / total_w) if total_w else None

results = []
for s in SAMPLES:
    d1, d2 = read_fastqc_data(s, 1), read_fastqc_data(s, 2)
    n1, n2 = parse_total_sequences(d1), parse_total_sequences(d2)
    _, block_pbq = parse_module(d1, "Per base sequence quality")
    rows = parse_per_base_quality(block_pbq)
    max_pos = max(hi for _, hi, _ in rows)
    q_window = windowed_mean(rows, 44, 90)
    q_flank_lo = windowed_mean(rows, 1, 43)
    q_flank_hi = windowed_mean(rows, 91, max_pos)
    w_lo, w_hi = 43, max_pos - 91 + 1
    q_flank = (q_flank_lo * w_lo + q_flank_hi * w_hi) / (w_lo + w_hi)
    delta = q_flank - q_window
    flagged = delta > DELTA_THRESHOLD
    results.append(dict(id=s, label=LABELS[s], reads_r1=n1, reads_r2=n2,
                         pares_sincronizados=(n1 == n2),
                         q_janela_44_90=round(q_window, 2),
                         q_flanco=round(q_flank, 2),
                         delta=round(delta, 2), flagged=flagged))

csv_path = os.path.join(QC_DIR, "blocoA_results.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader()
    w.writerows(results)
print(f"CSV: {csv_path}")

# ---- Figure 1: quality delta per sample ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

labels = [r["label"] for r in results]
deltas = [r["delta"] for r in results]
colors = ["#c0392b" if r["flagged"] else "#2c3e50" for r in results]

fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
bars = ax.bar(labels, deltas, color=colors, width=0.6)
ax.axhline(DELTA_THRESHOLD, color="grey", linestyle="--", linewidth=1)
ax.text(len(labels) - 0.5, DELTA_THRESHOLD + 0.15, f"pre-declared threshold = {DELTA_THRESHOLD} Phred",
        ha="right", va="bottom", fontsize=8, color="grey")
ax.set_ylabel("$\\Delta$Q (flanking $-$ cycles 44$-$90 window), R1")
ax.set_xlabel("Sample")
ax.set_title("Raw-read quality drop in cycles 44-90 (R1), by sample", fontsize=10)
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.tight_layout()
fig_path = os.path.join(QC_DIR, "Figure1_blocoA_quality_dip.png")
plt.savefig(fig_path)
print(f"Figura: {fig_path}")

for r in results:
    print(r)
