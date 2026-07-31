#!/usr/bin/env python3
"""FASE 7, Bloco F - consolida a anotacao GO em nivel de gene a partir das
2 fontes independentes (eggNOG-mapper, Bloco C; InterProScan6, Bloco D),
com a fonte de cada par gene-GO rastreavel (nao um merge cego). Uniao,
nao intersecao - um gene "tem" um termo GO se qualquer uma das 2 fontes
o atribuiu, convencao padrao ao combinar anotadores complementares (cada
um usa evidencia de homologia diferente: eggNOG = ortologia por diamond
contra o eggNOG DB; InterProScan = assinaturas de dominio por familia,
14+ member-databases).

Ambas as fontes ja operam sobre o MESMO proteoma representativo (1
proteina/gene, 14.238 genes protein_coding - ver correcao do Bloco B).
"""
import pandas as pd
import re

GENE_MAP = "resultados_server/fase7_blocoB/gene_to_representative_protein.tsv"
EGGNOG_GO = "resultados_server/fase7_blocoC/gene_to_go.csv"
IPS6_TSV = "resultados_server/fase7_blocoD/protein_representative.faa.tsv"

OUT_CONSOLIDATED = "resultados_server/fase7_blocoF/gene_to_go_consolidated.csv"
OUT_SUMMARY = "resultados_server/fase7_blocoF/annotation_coverage_summary.csv"

IPS6_COLS = [
    "protein_id", "md5", "length", "analysis", "sig_acc", "sig_desc",
    "start", "stop", "score", "status", "date", "ipr_acc", "ipr_desc",
    "go", "pathways",
]


def main():
    gene_map = pd.read_csv(GENE_MAP, sep="\t")
    n_genes_total = gene_map["gene_id"].nunique()
    protein_to_gene = dict(zip(gene_map["protein_id"], gene_map["gene_id"]))

    # --- Fonte 1: eggNOG-mapper (ja em nivel de gene, Bloco C) ---
    eggnog_go = pd.read_csv(EGGNOG_GO)
    eggnog_pairs = set(zip(eggnog_go["gene_id"], eggnog_go["go_id"].str.strip()))
    print(f"eggNOG: {len(eggnog_pairs)} pares gene-GO, {eggnog_go['gene_id'].nunique()} genes")

    # --- Fonte 2: InterProScan6 (nivel de proteina, agregar para gene) ---
    ips6 = pd.read_csv(IPS6_TSV, sep="\t", header=None, names=IPS6_COLS, quoting=3)
    ips6 = ips6[ips6["go"] != "-"]
    ips6["gene_id"] = ips6["protein_id"].map(protein_to_gene)
    ips6 = ips6.dropna(subset=["gene_id"])

    ips6_pairs = set()
    go_pattern = re.compile(r"GO:\d{7}")
    for gene_id, go_field in zip(ips6["gene_id"], ips6["go"]):
        for go_id in go_pattern.findall(go_field):
            ips6_pairs.add((gene_id, go_id))
    print(f"InterProScan6: {len(ips6_pairs)} pares gene-GO, {len({g for g, _ in ips6_pairs})} genes")

    # --- Uniao, com fonte rastreavel ---
    all_genes_go = {}
    for gene_id, go_id in eggnog_pairs:
        all_genes_go.setdefault((gene_id, go_id), set()).add("eggNOG")
    for gene_id, go_id in ips6_pairs:
        all_genes_go.setdefault((gene_id, go_id), set()).add("InterProScan6")

    rows = [
        {"gene_id": g, "go_id": go, "fonte": ";".join(sorted(src))}
        for (g, go), src in all_genes_go.items()
    ]
    consolidated = pd.DataFrame(rows).sort_values(["gene_id", "go_id"])
    consolidated.to_csv(OUT_CONSOLIDATED, index=False)
    print(f"Escrito: {OUT_CONSOLIDATED} ({len(consolidated)} pares gene-GO)")

    genes_eggnog_only = {g for (g, go), src in all_genes_go.items() if src == {"eggNOG"}}
    genes_ips6_only = {g for (g, go), src in all_genes_go.items() if src == {"InterProScan6"}}
    genes_both_sources = {g for (g, go), src in all_genes_go.items() if len(src) == 2}
    genes_any_go = {g for g, go in all_genes_go}

    n_eggnog_genes = eggnog_go["gene_id"].nunique()
    n_ips6_genes = len({g for g, _ in ips6_pairs})
    n_combined = len(genes_any_go)

    print(f"\nGenes com GO (eggNOG apenas): {n_eggnog_genes} ({100*n_eggnog_genes/n_genes_total:.1f}%)")
    print(f"Genes com GO (InterProScan6 apenas): {n_ips6_genes} ({100*n_ips6_genes/n_genes_total:.1f}%)")
    print(f"Genes com GO (uniao das 2 fontes): {n_combined} ({100*n_combined/n_genes_total:.1f}%)")
    print(f"Genes anotados nas 2 fontes simultaneamente (concordancia de presenca): {len(genes_both_sources | (genes_eggnog_only & genes_ips6_only))}")

    # Concordancia: genes que aparecem nas 2 fontes (independente do GO exato)
    genes_in_eggnog = set(eggnog_go["gene_id"].unique())
    genes_in_ips6 = {g for g, _ in ips6_pairs}
    genes_in_both = genes_in_eggnog & genes_in_ips6
    jaccard_genes = len(genes_in_both) / len(genes_in_eggnog | genes_in_ips6)
    print(f"Jaccard de genes anotados (eggNOG vs InterProScan6, independente do termo exato): {jaccard_genes:.4f}")

    summary = pd.DataFrame([{
        "n_genes_total": n_genes_total,
        "genes_go_eggnog": n_eggnog_genes,
        "pct_go_eggnog": round(100 * n_eggnog_genes / n_genes_total, 2),
        "genes_go_interproscan6": n_ips6_genes,
        "pct_go_interproscan6": round(100 * n_ips6_genes / n_genes_total, 2),
        "genes_go_uniao": n_combined,
        "pct_go_uniao": round(100 * n_combined / n_genes_total, 2),
        "jaccard_genes_anotados_eggnog_vs_ips6": round(jaccard_genes, 4),
        "pares_gene_go_total": len(consolidated),
    }])
    summary.to_csv(OUT_SUMMARY, index=False)
    print(f"\nEscrito: {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
