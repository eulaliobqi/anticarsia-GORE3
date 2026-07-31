#!/usr/bin/env python3
"""FASE 7, Bloco I (Python) - diagrama de Venn de 3 vias dos genes DE
(valido nesta escala, 3 conjuntos - literatura consultada no plano desta
fase confirma que Venn nao deve ser usado acima de ~5 conjuntos) +
UpSet dos termos GO significativos por contraste (nao dos genes brutos -
resolve a ressalva ja deixada no artigo, Fig. 13 da FASE 5: 'nao
interpretar [UpSet de genes] como prova de mecanismo compartilhado sem
enriquecimento funcional')."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import pandas as pd
from upsetplot import UpSet, from_contents

D_DIR = "resultados_server/fase5_blocoD"
G_DIR = "resultados_server/fase7_blocoG"
OUT_DIR = "resultados_server/fase7_blocoI"

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]
LABELS = ["Benzamidine", "SKTI", "GORE3"]
PAL = {"Benzamidine": "#eb6834", "SKTI": "#1baf7a", "GORE3": "#4a3aa7"}


def make_venn_genes():
    sets = {}
    for rotulo, label in zip(CONTRASTS, LABELS):
        sig = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_sig.csv")
        sets[label] = set(sig["gene_id"])

    fig, ax = plt.subplots(figsize=(7, 7))
    v = venn3([sets["Benzamidine"], sets["SKTI"], sets["GORE3"]],
              set_labels=("Benzamidine", "SKTI", "GORE3"), ax=ax)
    for label, color in PAL.items():
        patch_id = {"Benzamidine": "100", "SKTI": "010", "GORE3": "001"}[label]
        patch = v.get_patch_by_id(patch_id)
        if patch:
            patch.set_color(color)
            patch.set_alpha(0.55)
    ax.set_title("Genes DE por contraste vs. Controle (Venn de 3 vias)")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/fig_venn3_de_genes.pdf")
    fig.savefig(f"{OUT_DIR}/fig_venn3_de_genes.png", dpi=300)
    plt.close(fig)
    print(f"Escrito: {OUT_DIR}/fig_venn3_de_genes.pdf + .png")


def make_upset_go_terms():
    sets = {}
    for rotulo, label in zip(CONTRASTS, LABELS):
        df = pd.read_csv(f"{G_DIR}/clusterprofiler_GO_{rotulo}.csv")
        sets[label] = set(df["ID"]) if "ID" in df.columns and len(df) else set()

    data = from_contents(sets)
    fig = plt.figure(figsize=(8, 5.5))
    upset = UpSet(data, subset_size="count", show_counts=False, sort_by="cardinality")
    axes = upset.plot(fig=fig)
    for container in axes["intersections"].containers:
        axes["intersections"].bar_label(container, fontsize=8)
    fig.suptitle("Termos GO significativos por contraste (clusterProfiler, padj<0.05)")
    fig.savefig(f"{OUT_DIR}/fig_upset_go_terms.pdf")
    fig.savefig(f"{OUT_DIR}/fig_upset_go_terms.png", dpi=300)
    plt.close(fig)
    print(f"Escrito: {OUT_DIR}/fig_upset_go_terms.pdf + .png")
    for label, s in sets.items():
        print(f"  {label}: {len(s)} termos GO significativos")


if __name__ == "__main__":
    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    make_venn_genes()
    make_upset_go_terms()
    print("\nBloco I (Python: Venn genes, UpSet termos GO) concluido.")
