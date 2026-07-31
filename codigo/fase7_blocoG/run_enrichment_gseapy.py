#!/usr/bin/env python3
"""FASE 7, Bloco G2 (Python) - segunda implementacao independente do
enriquecimento GO (gseapy sobre o mesmo TERM2GENE consolidado do Bloco F
+ nomes de termo exportados do GO.db no Bloco G1), mesmo espirito da
dupla implementacao R/Python ja estabelecida na FASE 5
(DESeq2/PyDESeq2)."""
import pandas as pd
import gseapy as gp

GO_MAP = "resultados_server/fase7_blocoF/gene_to_go_consolidated.csv"
GO_NAMES = "resultados_server/fase7_blocoF/go_term_names.csv"
D_DIR = "resultados_server/fase5_blocoD"
OUT_DIR = "resultados_server/fase7_blocoG"

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]
PVALUE_CUTOFF = 0.05


def build_gene_sets():
    go_map = pd.read_csv(GO_MAP)
    names = pd.read_csv(GO_NAMES).set_index("GOID")["TERM"].to_dict()
    gene_sets = {}
    for go_id, sub in go_map.groupby("go_id"):
        label = f"{go_id}_{names.get(go_id, 'NA')}"[:200]
        gene_sets[label] = sorted(set(sub["gene_id"]))
    return gene_sets


def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    gene_sets = build_gene_sets()
    print(f"TERM2GENE (Python): {len(gene_sets)} termos GO")

    for rotulo in CONTRASTS:
        print(f"\n=== {rotulo} ===")
        sig = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_sig.csv")
        all_genes = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_all.csv")
        de_genes = sig["gene_id"].tolist()
        universe = all_genes["gene_id"].tolist()
        print(f"DE: {len(de_genes)} genes | universo testado: {len(universe)} genes")

        try:
            enr = gp.enrich(
                gene_list=de_genes,
                gene_sets=gene_sets,
                background=universe,
                outdir=None,
            )
            res = enr.results
            res = res[res["Adjusted P-value"] < PVALUE_CUTOFF].copy()
            res[["go_id", "go_name"]] = res["Term"].str.split("_", n=1, expand=True)
            out = f"{OUT_DIR}/gseapy_GO_{rotulo}.csv"
            res.to_csv(out, index=False)
            print(f"GO: {len(res)} termos significativos (padj<{PVALUE_CUTOFF}) -> {out}")
        except Exception as e:
            print(f"gseapy.enrich() falhou: {e}")
            pd.DataFrame().to_csv(f"{OUT_DIR}/gseapy_GO_{rotulo}.csv", index=False)

    print("\nBloco G2 (Python/gseapy: GO) concluido para os 3 contrastes.")


if __name__ == "__main__":
    main()
