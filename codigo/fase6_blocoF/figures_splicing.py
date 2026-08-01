"""FASE 6, Bloco F - figuras: UpSet dos genes com splicing significativo
(uniao rMATS/MAJIQ) entre os 3 contrastes, e barra splicing x DE (Bloco E).
Paleta ja validada nas FASES 5/7 via skill dataviz - reaproveitada sem
revalidar: Controle=#2a78d6 (nao usado aqui, sem contraste proprio),
Benzamidina=#eb6834, SKTI=#1baf7a, GORE3=#4a3aa7.
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from upsetplot import UpSet, from_contents

BASE = Path(__file__).resolve().parents[2]
FASE6D_DIR = BASE / "resultados" / "fase6_blocoD"
FASE6E_DIR = BASE / "resultados" / "fase6_blocoE"
FIG_DIR = BASE / "figuras" / "fase6_blocoF"
FIG_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {"Benzamidine": "#eb6834", "SKTI": "#1baf7a", "GORE3": "#4a3aa7"}
CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]
LABELS = {"Benzamidine_vs_Control": "Benzamidine", "SKTI_vs_Control": "SKTI", "GORE3_vs_Control": "GORE3"}


def load_gene_set(path):
    genes = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            genes.add(row["gene_id"].strip('"'))
    return genes


def main():
    sets = {}
    for contrast in CONTRASTS:
        rmats_genes = load_gene_set(FASE6D_DIR / f"rmats_sig_{contrast}.csv")
        majiq_genes = load_gene_set(FASE6D_DIR / f"majiq_sig_{contrast}.csv")
        sets[LABELS[contrast]] = rmats_genes | majiq_genes

    # --- Figura 1: UpSet dos genes com splicing significativo, 3 contrastes ---
    data = from_contents(sets)
    upset = UpSet(data, subset_size="count", show_counts=True, sort_by="cardinality")
    fig = plt.figure(figsize=(8, 5))
    upset.plot(fig=fig)
    fig.suptitle("Genes with significant alternative splicing (rMATS-turbo ∪ MAJIQ)\nvs. Control, by treatment", fontsize=11)
    out1 = FIG_DIR / "fig_upset_splicing_genes.png"
    fig.savefig(out1, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Salvo: {out1}")

    # --- Figura 2: splicing x DE, barras empilhadas por contraste ---
    rows = []
    with open(FASE6E_DIR / "cross_reference_summary.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    labels = [LABELS[r["contrast"]] for r in rows]
    with_de = [int(r["splicing_E_de_ambos"]) for r in rows]
    without_de = [int(r["splicing_SEM_de_apenas_isoforma"]) for r in rows]
    colors_bar = [COLORS[l] for l in labels]

    fig2, ax = plt.subplots(figsize=(6, 4.5))
    x = range(len(labels))
    ax.bar(x, without_de, label="Splicing only (not DE)", color=colors_bar, alpha=0.45)
    ax.bar(x, with_de, bottom=without_de, label="Splicing + differentially expressed", color=colors_bar, alpha=1.0)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Genes with significant alternative splicing")
    ax.set_title("Overlap between splicing and differential expression\n(vs. Control, per treatment)")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    for i, (wd, wo) in enumerate(zip(with_de, without_de)):
        ax.text(i, wo + wd + 2, f"{wd}/{wo+wd}", ha="center", fontsize=8)
    fig2.tight_layout()
    out2 = FIG_DIR / "fig_splicing_vs_de_overlap.png"
    fig2.savefig(out2, dpi=300, bbox_inches="tight")
    plt.close(fig2)
    print(f"Salvo: {out2}")


if __name__ == "__main__":
    main()
