import json, os, csv, statistics

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/post_trim")
SAMPLES = ["ID-1","ID-2","ID-3","ID-5","ID-7","ID-8","ID-9","ID-10","ID-12","ID-14","ID-15","ID-16","ID-18"]
LABELS = {
    "ID-1":"Control_R1","ID-2":"Control_R2","ID-3":"Control_R3",
    "ID-5":"Benzamidine_R1","ID-7":"Benzamidine_R2","ID-8":"Benzamidine_R3",
    "ID-9":"SKTI_R1","ID-10":"SKTI_R2","ID-12":"SKTI_R3",
    "ID-14":"GORE3_R1","ID-15":"GORE3_R2","ID-16":"GORE3_R3",
    "ID-18":"FatBody",
}
GC_VENDOR = {"ID-1":51.8,"ID-2":53.4,"ID-3":49.1,"ID-5":52.3,"ID-7":59.7,"ID-8":63.1,
             "ID-9":54.7,"ID-10":60.8,"ID-12":49.1,"ID-14":48.4,"ID-15":48.8,"ID-16":50.3,"ID-18":49.5}

rows = []
for s in SAMPLES:
    with open(os.path.join(QC_DIR, f"{s}.fastp.json")) as f:
        d = json.load(f)
    bf, af = d["summary"]["before_filtering"], d["summary"]["after_filtering"]
    fr = d["filtering_result"]
    total_before = bf["total_reads"]
    total_after = af["total_reads"]
    dimer = fr.get("adapter_dimer_reads", 0)
    rows.append(dict(
        id=s, label=LABELS[s], gc_vendor=GC_VENDOR[s],
        reads_before=total_before, reads_after=total_after,
        pct_survival=round(100*total_after/total_before, 2),
        pct_adapter_dimer=round(100*dimer/total_before, 2),
        pct_low_quality=round(100*fr.get("low_quality_reads",0)/total_before, 2),
        pct_too_short=round(100*fr.get("too_short_reads",0)/total_before, 2),
        q30_before=round(bf["q30_rate"]*100,2), q30_after=round(af["q30_rate"]*100,2),
        mean_len_after=af["read1_mean_length"],
    ))

csv_path = os.path.join(QC_DIR, "blocoB_trim_summary.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

hdr = list(rows[0].keys())
print("\t".join(hdr))
for r in rows:
    print("\t".join(str(r[h]) for h in hdr))

# correlation: adapter_dimer% vs GC%
x = [r["gc_vendor"] for r in rows]
y = [r["pct_adapter_dimer"] for r in rows]
n = len(x)
mx, my = statistics.mean(x), statistics.mean(y)
cov = sum((xi-mx)*(yi-my) for xi,yi in zip(x,y))/n
sx, sy = statistics.pstdev(x), statistics.pstdev(y)
r_pearson = cov/(sx*sy)
def rank(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks=[0]*len(vals)
    for rnk, idx in enumerate(order): ranks[idx]=rnk+1
    return ranks
rx, ry = rank(x), rank(y)
mrx, mry = statistics.mean(rx), statistics.mean(ry)
covr = sum((a-mrx)*(b-mry) for a,b in zip(rx,ry))/n
sxr, syr = statistics.pstdev(rx), statistics.pstdev(ry)
rho = covr/(sxr*syr)
print(f"\nPearson r (GC% vs %adapter_dimer): {r_pearson:.4f}")
print(f"Spearman rho: {rho:.4f}")
print(f"\nCSV: {csv_path}")

# ---- Figure 3: survival + adapter-dimer% per sample ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

labels = [r["label"] for r in rows]
survival = [r["pct_survival"] for r in rows]
dimer = [r["pct_adapter_dimer"] for r in rows]
# limiar visual escolhido apos ver a distribuicao real: gap claro entre
# ~7% (grupo limpo) e ~16% (grupo afetado) - nao e um limiar pre-declarado
# como o do Bloco A, e' so estetica de figura para separar os dois clusters
# visiveis nos dados.
colors = ["#c0392b" if d > 10 else "#2c3e50" for d in dimer]

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), dpi=300)
axes[0].bar(labels, survival, color=colors, width=0.6)
axes[0].set_ylabel("Reads surviving trimming (%)")
axes[0].set_xlabel("Sample")
axes[0].set_title("(a) Post-trimming read survival", fontsize=10)
axes[0].set_ylim(0, 105)
plt.setp(axes[0].get_xticklabels(), rotation=45, ha="right", fontsize=8)

axes[1].scatter([r["gc_vendor"] for r in rows], dimer, c=colors, s=60, zorder=3)
for r in rows:
    axes[1].annotate(r["label"], (r["gc_vendor"], r["pct_adapter_dimer"]),
                      fontsize=6, xytext=(3,3), textcoords="offset points")
axes[1].set_xlabel("Vendor-reported GC content (%)")
axes[1].set_ylabel("Adapter-dimer reads (%)")
axes[1].set_title(f"(b) Adapter-dimer rate vs. GC (r={r_pearson:.2f}, $\\rho$={rho:.2f})", fontsize=10)

plt.tight_layout()
fig_path = os.path.join(QC_DIR, "Figure3_blocoB_trimming.png")
plt.savefig(fig_path, bbox_inches="tight")
print(f"Figura: {fig_path}")
