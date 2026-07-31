#!/usr/bin/env python3
"""FASE 7, Bloco C - cobertura real de anotacao GO/KEGG (eggNOG-mapper)
sobre o proteoma representativo (14.238 genes, 1/gene)."""
import pandas as pd

ANNOT = "resultados_server/fase7_blocoC/pfam_eggnog_out.emapper.annotations"
GENE_MAP = "resultados_server/fase7_blocoB/gene_to_representative_protein.tsv"
OUT_CSV = "resultados_server/fase7_blocoC/eggnog_coverage_summary.csv"
OUT_GO = "resultados_server/fase7_blocoC/gene_to_go.csv"
OUT_KEGG = "resultados_server/fase7_blocoC/gene_to_kegg.csv"


def main():
    df = pd.read_csv(ANNOT, sep="\t", comment=None, skiprows=4, header=0)
    df = df.rename(columns={"#query": "query"})
    df = df[df["query"].notna() & ~df["query"].astype(str).str.startswith("##")]

    gene_map = pd.read_csv(GENE_MAP, sep="\t")
    n_genes_total = gene_map["gene_id"].nunique()
    protein_to_gene = dict(zip(gene_map["protein_id"], gene_map["gene_id"]))
    df["gene_id"] = df["query"].map(protein_to_gene)

    n_any_hit = df["gene_id"].nunique()
    has_go = df[df["GOs"].notna() & (df["GOs"] != "-")]
    has_kegg = df[df["KEGG_ko"].notna() & (df["KEGG_ko"] != "-")]
    n_go = has_go["gene_id"].nunique()
    n_kegg = has_kegg["gene_id"].nunique()

    print(f"Genes no proteoma representativo: {n_genes_total}")
    print(f"Genes com qualquer hit eggNOG: {n_any_hit} ({100*n_any_hit/n_genes_total:.1f}%)")
    print(f"Genes com GO term: {n_go} ({100*n_go/n_genes_total:.1f}%)")
    print(f"Genes com KEGG KO: {n_kegg} ({100*n_kegg/n_genes_total:.1f}%)")

    summary = pd.DataFrame([{
        "n_genes_total": n_genes_total,
        "genes_com_hit_eggnog": n_any_hit,
        "pct_com_hit_eggnog": round(100 * n_any_hit / n_genes_total, 2),
        "genes_com_go": n_go,
        "pct_com_go": round(100 * n_go / n_genes_total, 2),
        "genes_com_kegg": n_kegg,
        "pct_com_kegg": round(100 * n_kegg / n_genes_total, 2),
    }])
    summary.to_csv(OUT_CSV, index=False)
    print(f"Escrito: {OUT_CSV}")

    go_long = has_go[["gene_id", "GOs"]].copy()
    go_long["GOs"] = go_long["GOs"].str.split(",")
    go_long = go_long.explode("GOs").rename(columns={"GOs": "go_id"})
    go_long.to_csv(OUT_GO, index=False)
    print(f"Escrito: {OUT_GO} ({go_long['gene_id'].nunique()} genes, {len(go_long)} pares gene-GO)")

    kegg_long = has_kegg[["gene_id", "KEGG_ko"]].copy()
    kegg_long["KEGG_ko"] = kegg_long["KEGG_ko"].str.split(",")
    kegg_long = kegg_long.explode("KEGG_ko").rename(columns={"KEGG_ko": "kegg_ko"})
    kegg_long.to_csv(OUT_KEGG, index=False)
    print(f"Escrito: {OUT_KEGG} ({kegg_long['gene_id'].nunique()} genes, {len(kegg_long)} pares gene-KO)")


if __name__ == "__main__":
    main()
