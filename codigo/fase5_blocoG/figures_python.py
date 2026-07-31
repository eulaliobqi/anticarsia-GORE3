#!/usr/bin/env python3
"""FASE 5, Bloco G (Python) - UMAP (reforco nao-linear da PCA, yang2021umap
PMID 34320340) + UpSet plot dos 3 conjuntos de genes DE (conway2017upsetr
PMID 28645171, equivalente Python `upsetplot`).

Mesma paleta categorica validada via skill `dataviz` usada no lado R:
Control=azul #2a78d6, Benzamidine=laranja #eb6834, SKTI=aqua #1baf7a,
GORE3=violeta #4a3aa7.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import umap
from upsetplot import UpSet, from_contents

G_DIR = "resultados_server/fase5_blocoG"
D_DIR = "resultados_server/fase5_blocoD"

PAL = {"Control": "#2a78d6", "Benzamidine": "#eb6834", "SKTI": "#1baf7a", "GORE3": "#4a3aa7"}
CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]


def make_umap():
    # Mesma matriz VST (blind=FALSE) exportada pelo R (fig_pca) - o UMAP
    # descreve a MESMA heterogeneidade amostral que a PCA, nao uma
    # matriz recomputada a parte (yang2021umap recomenda UMAP como
    # reforco, nao substituto, da PCA).
    vst = pd.read_csv(f"{G_DIR}/vst_normalized_matrix.csv", index_col=0)
    meta = pd.read_csv(f"{G_DIR}/sample_metadata.csv", index_col="sample")

    X = vst.T  # amostras x genes
    meta = meta.loc[X.index]

    # n_neighbors baixo (12 amostras no total) - default (15) excederia
    # o proprio n de amostras; parametro ajustado ao desenho real, nao
    # deixado no default de dataset grande.
    reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, random_state=42)
    embedding = reducer.fit_transform(X.values)

    fig, ax = plt.subplots(figsize=(7.5, 6))
    for cond, color in PAL.items():
        mask = meta["condition"] == cond
        ax.scatter(embedding[mask.values, 0], embedding[mask.values, 1],
                   c=color, label=cond, s=90, alpha=0.9, edgecolors="none")
    # ID-8 (lote unico) marcado com contorno preto - mesma convencao da PCA em R.
    id8_mask = meta["is_id8"].values
    if id8_mask.any():
        ax.scatter(embedding[id8_mask, 0], embedding[id8_mask, 1],
                   facecolors="none", edgecolors="#0b0b0b", linewidths=1.4, s=160)
    for i, name in enumerate(X.index):
        ax.annotate(name, (embedding[i, 0], embedding[i, 1]), fontsize=7,
                    xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.set_title("UMAP - Anticarsia gemmatalis (VST, reforço da PCA)")
    ax.legend(title="Grupo", frameon=False)
    fig.tight_layout()
    fig.savefig(f"{G_DIR}/fig_umap.pdf")
    fig.savefig(f"{G_DIR}/fig_umap.png", dpi=300)
    plt.close(fig)
    print(f"Escrito: {G_DIR}/fig_umap.pdf + .png")


def make_upset():
    sets = {}
    for rotulo in CONTRASTS:
        sig = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_sig.csv")
        sets[rotulo.replace("_vs_Control", "")] = set(sig["gene_id"])

    data = from_contents(sets)
    fig = plt.figure(figsize=(8, 5.5))
    # show_counts=True quebra sob upsetplot 0.9.0 + matplotlib 3.11.1
    # (TypeError em text.py:863, convert_xunits recebe array em vez de
    # escalar - confirmado em teste isolado nesta sessao, bug real de
    # compatibilidade de versao, nao do codigo deste script). Workaround:
    # rotula as barras com bar_label() nativo do matplotlib, que nao usa
    # o caminho de codigo com bug do upsetplot.
    upset = UpSet(data, subset_size="count", show_counts=False, sort_by="cardinality")
    axes = upset.plot(fig=fig)
    for container in axes["intersections"].containers:
        axes["intersections"].bar_label(container, fontsize=8)
    fig.suptitle("Genes DE por contraste vs. Controle (DESeq2, FDR<0.05, |log2FC|>0.25)")
    fig.savefig(f"{G_DIR}/fig_upset_de_genes.pdf")
    fig.savefig(f"{G_DIR}/fig_upset_de_genes.png", dpi=300)
    plt.close(fig)
    print(f"Escrito: {G_DIR}/fig_upset_de_genes.pdf + .png")
    for name, s in sets.items():
        print(f"  {name}: {len(s)} genes DE")


if __name__ == "__main__":
    make_umap()
    make_upset()
    print("\nBloco G (Python: UMAP, UpSet) concluido.")
