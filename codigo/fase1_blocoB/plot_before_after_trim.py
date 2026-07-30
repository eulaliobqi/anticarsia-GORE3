"""
Figure 4 - before/after trimming, per-base R1 quality, for the 4 affected
libraries + 1 clean reference. Uses fastp's own before/after quality_curves
(same tool, same JSON, avoids cross-tool binning inconsistencies).
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/post_trim")
SAMPLES = ["ID-1", "ID-7", "ID-8", "ID-9", "ID-10"]
LABELS = {
    "ID-1": "Control_R1 (clean, reference)",
    "ID-7": "Benzamidine_R2",
    "ID-8": "Benzamidine_R3",
    "ID-9": "SKTI_R1",
    "ID-10": "SKTI_R2",
}

fig, axes = plt.subplots(1, 5, figsize=(19, 3.8), dpi=300, sharey=True)

for ax, s in zip(axes, SAMPLES):
    with open(os.path.join(QC_DIR, f"{s}.fastp.json")) as f:
        d = json.load(f)
    before = d["read1_before_filtering"]["quality_curves"]["mean"]
    after = d["read1_after_filtering"]["quality_curves"]["mean"]
    x_before = list(range(1, len(before) + 1))
    x_after = list(range(1, len(after) + 1))

    ax.plot(x_before, before, color="#c0392b", linewidth=1.3, label="Before trimming")
    ax.plot(x_after, after, color="#2c3e50", linewidth=1.3, label="After trimming (Set B)")
    ax.axvspan(44, 90, color="grey", alpha=0.15, linewidth=0)
    ax.set_title(LABELS[s], fontsize=9)
    ax.set_xlabel("Read-1 cycle")
    ax.set_ylim(0, 42)
    ax.set_xlim(1, 151)

axes[0].set_ylabel("Mean Phred quality")
handles, hlabels = axes[0].get_legend_handles_labels()
fig.legend(handles, hlabels, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.08), fontsize=9, frameon=False)
fig.suptitle("Read-1 per-base quality before and after fastp trimming (Set B)", fontsize=11, y=1.16)
plt.tight_layout()
fig_path = os.path.join(QC_DIR, "Figure4_blocoB_before_after.png")
plt.savefig(fig_path, bbox_inches="tight")
print(f"Figura: {fig_path}")
