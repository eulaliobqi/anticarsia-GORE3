#!/usr/bin/env python3
"""FASE 7, Bloco G3 - sobre-representacao de dominios Pfam entre genes DE
vs. universo testado, por contraste (teste exato de Fisher, tabela 2x2
por dominio: DE-com-dominio / DE-sem / nao-DE-com / nao-DE-sem).
Complementa GO/KEGG com granularidade de dominio proteico, nao de via
biologica - um gene pode ter GO amplo mas o sinal estar concentrado num
dominio especifico."""
import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

PFAM_HITS = "resultados_server/fase7_blocoB/pfam_hits_per_gene.csv"
D_DIR = "resultados_server/fase5_blocoD"
OUT_DIR = "resultados_server/fase7_blocoG"

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]
PVALUE_CUTOFF = 0.05


def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)

    pfam = pd.read_csv(PFAM_HITS)
    gene_to_domains = {}
    for gene_id, accs in zip(pfam["gene_id"], pfam["pfam_accessions"]):
        gene_to_domains[gene_id] = set(accs.split(";"))

    for rotulo in CONTRASTS:
        print(f"\n=== {rotulo} ===")
        sig = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_sig.csv")
        all_genes = pd.read_csv(f"{D_DIR}/deseq2_{rotulo}_all.csv")
        de_genes = set(sig["gene_id"])
        universe = set(all_genes["gene_id"])

        all_domains = set()
        for g in universe:
            all_domains |= gene_to_domains.get(g, set())

        rows = []
        for dom in all_domains:
            genes_with_dom = {g for g in universe if dom in gene_to_domains.get(g, set())}
            a = len(genes_with_dom & de_genes)
            b = len(de_genes) - a
            c = len(genes_with_dom) - a
            d = len(universe) - len(de_genes) - c
            if a == 0:
                continue
            odds, p = fisher_exact([[a, b], [c, d]], alternative="greater")
            rows.append({
                "pfam_accession": dom, "genes_com_dominio_universo": len(genes_with_dom),
                "genes_com_dominio_DE": a, "odds_ratio": odds, "pvalue": p,
            })

        res = pd.DataFrame(rows)
        if len(res) > 0:
            res["padj"] = multipletests(res["pvalue"], method="fdr_bh")[1]
            res = res.sort_values("padj")
            sig_res = res[res["padj"] < PVALUE_CUTOFF]
        else:
            sig_res = res

        out_all = f"{OUT_DIR}/pfam_fisher_{rotulo}_all.csv"
        out_sig = f"{OUT_DIR}/pfam_fisher_{rotulo}_sig.csv"
        res.to_csv(out_all, index=False)
        sig_res.to_csv(out_sig, index=False)
        print(f"Dominios testados: {len(res)} | significativos (padj<{PVALUE_CUTOFF}): {len(sig_res)}")
        print(f"Escrito: {out_all}, {out_sig}")

    print("\nBloco G3 (Fisher exato, dominios Pfam) concluido para os 3 contrastes.")


if __name__ == "__main__":
    main()
