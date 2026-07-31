#!/usr/bin/env python3
"""FASE 5, Bloco E - verificacao cruzada R (DESeq2) x Python (PyDESeq2),
achado empirico proprio deste dataset (mesmo padrao ja usado no Bloco F da
FASE 3 entre featureCounts e Salmon).

POR QUE ISSO NAO E' UMA CITACAO DA LITERATURA: o proprio artigo do
PyDESeq2 (muzellec2023pydeseq2, PMID 37669147) nao reporta um benchmark
quantitativo de concordancia de log2FC/genes-DE contra o DESeq2 em R - so
compara conjuntos de genes/vias de forma qualitativa em 8 datasets do
TCGA. Nao ha citacao pronta que garanta que os dois motores batem neste
projeto - rodar os dois e medir a concordancia aqui e', portanto, um
resultado verificado deste dataset, nao uma suposicao.

ASSIMETRIA JA DECLARADA (Bloco C2/D2): PyDESeq2 nao tem o offset de
comprimento de transcrito do tximport (so log(size_factors) escalar) - a
concordancia deve ser lida com essa ressalva, nao como equivalencia
100% esperada.
"""
import pandas as pd
from scipy.stats import pearsonr, spearmanr

D_DIR = "resultados_server/fase5_blocoD"
OUT_CSV = "resultados_server/fase5_blocoE/cross_engine_comparison.csv"

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]


def jaccard(set_a, set_b):
    union = set_a | set_b
    if len(union) == 0:
        return float("nan")
    return len(set_a & set_b) / len(union)


def main():
    import os
    os.makedirs("resultados_server/fase5_blocoE", exist_ok=True)

    rows = []
    for rotulo in CONTRASTS:
        r_all = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_all.csv", index_col="gene_id")
        py_all = pd.read_csv(f"{D_DIR}/pydeseq2_{rotulo}_all.csv", index_col="gene_id")

        # Merge por gene_id - so genes presentes nos dois motores (ambos
        # partem do mesmo filtro rowSums/soma >= 10 sobre a mesma matriz
        # tximport, entao a lista de genes deveria ser identica; checar,
        # nao supor).
        merged = r_all[["log2FoldChange"]].join(
            py_all[["log2FoldChange"]], lsuffix="_R", rsuffix="_py", how="inner"
        )
        n_r_only = len(set(r_all.index) - set(py_all.index))
        n_py_only = len(set(py_all.index) - set(r_all.index))

        pearson_r, pearson_p = pearsonr(merged["log2FoldChange_R"], merged["log2FoldChange_py"])
        spearman_r, spearman_p = spearmanr(merged["log2FoldChange_R"], merged["log2FoldChange_py"])

        r_sig = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_sig.csv", index_col="gene_id")
        py_sig = pd.read_csv(f"{D_DIR}/pydeseq2_{rotulo}_sig.csv", index_col="gene_id")
        set_r_sig = set(r_sig.index)
        set_py_sig = set(py_sig.index)
        jac = jaccard(set_r_sig, set_py_sig)
        intersect_n = len(set_r_sig & set_py_sig)

        rows.append({
            "contraste": rotulo,
            "genes_comparados": len(merged),
            "genes_so_no_R": n_r_only,
            "genes_so_no_python": n_py_only,
            "pearson_r_log2fc": pearson_r,
            "pearson_p": pearson_p,
            "spearman_rho_log2fc": spearman_r,
            "spearman_p": spearman_p,
            "n_sig_R": len(set_r_sig),
            "n_sig_python": len(set_py_sig),
            "n_sig_intersecao": intersect_n,
            "jaccard_sig": jac,
        })

        print(f"\n=== {rotulo} ===")
        print(f"Genes comparados: {len(merged)} (so R: {n_r_only}, so Python: {n_py_only})")
        print(f"Pearson r (log2FC encolhido): {pearson_r:.4f} (p={pearson_p:.2e})")
        print(f"Spearman rho (log2FC encolhido): {spearman_r:.4f} (p={spearman_p:.2e})")
        print(f"DE significativos: R={len(set_r_sig)}, Python={len(set_py_sig)}, "
              f"intersecao={intersect_n}, Jaccard={jac:.4f}")

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_CSV, index=False)
    print(f"\nEscrito: {OUT_CSV}")
    print("\nBloco E (verificacao cruzada R x Python) concluido.")


if __name__ == "__main__":
    main()
