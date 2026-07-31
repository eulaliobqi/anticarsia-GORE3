#!/usr/bin/env python3
"""FASE 5, Bloco D2 (Python) - aplica o mesmo criterio de significancia da
via R (Bloco D1: padj < 0,05 & |log2FoldChange| > 0,25, log2FC ja encolhido
por apeglm) sobre os CSVs que o Bloco C2 (run_pydeseq2.py) ja escreveu com
o log2FoldChange encolhido (stat.lfc_shrink() roda ANTES de stat.results_df
ser lido, dentro do proprio run_pydeseq2.py) - nao precisa reajustar o
modelo, so filtrar e renomear para a convencao de nome do Bloco D
(consistente com o lado R: {motor}_{rotulo}_all.csv / _sig.csv).
"""
import pandas as pd

IN_DIR = "resultados_server/fase5_blocoC"
OUT_DIR = "resultados_server/fase5_blocoD"

PADJ_CUTOFF = 0.05
LFC_CUTOFF = 0.25

CONTRASTS = [
    ("Benzamidine", "Benzamidine_vs_Control"),
    ("SKTI", "SKTI_vs_Control"),
    ("GORE3", "GORE3_vs_Control"),
]


def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)

    for tratamento, rotulo in CONTRASTS:
        in_path = f"{IN_DIR}/pydeseq2_{tratamento}_vs_Control_all.csv"
        res = pd.read_csv(in_path, index_col=0)
        res.index.name = "gene_id"

        regulation = pd.Series("ns", index=res.index)
        up = (res["padj"] < PADJ_CUTOFF) & (res["log2FoldChange"] > LFC_CUTOFF)
        down = (res["padj"] < PADJ_CUTOFF) & (res["log2FoldChange"] < -LFC_CUTOFF)
        regulation[up.fillna(False)] = "up"
        regulation[down.fillna(False)] = "down"
        res["regulation"] = regulation

        res = res.sort_values(["padj", "log2FoldChange"], key=lambda c: c.abs() if c.name == "log2FoldChange" else c)

        res_sig = res[res["regulation"] != "ns"]

        out_all = f"{OUT_DIR}/pydeseq2_{rotulo}_all.csv"
        out_sig = f"{OUT_DIR}/pydeseq2_{rotulo}_sig.csv"
        res.to_csv(out_all)
        res_sig.to_csv(out_sig)

        n_up = (res_sig["regulation"] == "up").sum()
        n_down = (res_sig["regulation"] == "down").sum()
        print(f"Escrito: {out_all} ({res.shape[0]} genes)")
        print(f"Escrito: {out_sig} ({res_sig.shape[0]} DE: {n_up} up / {n_down} down)")

    print("\nBloco D2 (Python/PyDESeq2) concluido para os 3 contrastes.")


if __name__ == "__main__":
    main()
