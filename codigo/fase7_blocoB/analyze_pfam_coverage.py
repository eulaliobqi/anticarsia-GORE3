#!/usr/bin/env python3
"""FASE 7, Bloco B - cobertura real de dominio Pfam sobre o proteoma
representativo (14.238 genes, 1 proteina/gene - ver correcao do Bloco B
no plano). Limiar: E-value de sequencia completa < 1e-5 (declarado
explicitamente, nao e' o --cut_ga por modelo do Pfam - mais simples e
uniforme entre todos os 20 mil+ modelos, escolha documentada aqui, nao
escondida).
"""
import pandas as pd

DOMTBLOUT = "resultados_server/fase7_blocoB/pfam_domtblout.tsv"
GENE_MAP = "resultados_server/fase7_blocoB/gene_to_representative_protein.tsv"
OUT_CSV = "resultados_server/fase7_blocoB/pfam_coverage_summary.csv"
OUT_HITS = "resultados_server/fase7_blocoB/pfam_hits_per_gene.csv"

EVALUE_CUTOFF = 1e-5

COLS = [
    "target_name", "target_accession", "tlen", "query_name", "query_accession",
    "qlen", "seq_evalue", "seq_score", "seq_bias", "dom_num", "dom_of",
    "dom_c_evalue", "dom_i_evalue", "dom_score", "dom_bias",
    "hmm_from", "hmm_to", "ali_from", "ali_to", "env_from", "env_to", "acc",
]


def main():
    rows = []
    with open(DOMTBLOUT) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split(None, len(COLS) - 1)
            rows.append(parts[: len(COLS)])
    df = pd.DataFrame(rows, columns=COLS)
    df["seq_evalue"] = df["seq_evalue"].astype(float)

    gene_map = pd.read_csv(GENE_MAP, sep="\t")
    n_genes_total = gene_map["gene_id"].nunique()

    sig = df[df["seq_evalue"] < EVALUE_CUTOFF]
    protein_to_gene = dict(zip(gene_map["protein_id"], gene_map["gene_id"]))
    sig = sig.copy()
    sig["gene_id"] = sig["query_name"].map(protein_to_gene)

    genes_with_domain = sig["gene_id"].dropna().nunique()
    n_domain_hits = len(sig)
    n_unique_pfam = sig["target_accession"].nunique()

    print(f"Genes no proteoma representativo: {n_genes_total}")
    print(f"Genes com >=1 dominio Pfam significativo (E<{EVALUE_CUTOFF}): {genes_with_domain} ({100*genes_with_domain/n_genes_total:.1f}%)")
    print(f"Total de hits de dominio significativos: {n_domain_hits}")
    print(f"Familias Pfam distintas encontradas: {n_unique_pfam}")

    summary = pd.DataFrame([{
        "n_genes_total": n_genes_total,
        "evalue_cutoff": EVALUE_CUTOFF,
        "genes_com_dominio_pfam": genes_with_domain,
        "pct_genes_com_dominio_pfam": round(100 * genes_with_domain / n_genes_total, 2),
        "total_hits_significativos": n_domain_hits,
        "familias_pfam_distintas": n_unique_pfam,
    }])
    summary.to_csv(OUT_CSV, index=False)
    print(f"Escrito: {OUT_CSV}")

    per_gene = (
        sig.dropna(subset=["gene_id"])
        .groupby("gene_id")["target_accession"]
        .apply(lambda s: ";".join(sorted(set(s))))
        .reset_index()
        .rename(columns={"target_accession": "pfam_accessions"})
    )
    per_gene.to_csv(OUT_HITS, index=False)
    print(f"Escrito: {OUT_HITS} ({len(per_gene)} genes)")


if __name__ == "__main__":
    main()
