"""FASE 6, Bloco E - cruzamento entre splicing significativo (rMATS uniao
MAJIQ, Bloco D) e expressao diferencial (FASE 5, DESeq2/R), + flag para
genes com dominio Pfam de tripsina (PF00089, FASE 7 Bloco B) - insumo
direto para a FASE 9 (curadoria da familia de serino-proteases), nao uma
analise nova de anotacao.

Roda local (nao no servidor) porque as 3 entradas ja sao pequenas o
suficiente para estarem versionadas no repo: resultados/fase5_blocoD (DE),
resultados/fase6_blocoD (splicing, baixado do servidor nesta sessao),
resultados/fase6_blocoE/pfam_hits_per_gene_ref_fase7.csv (copia de
referencia do arquivo real da FASE 7, nao reprocessado).
"""
import csv
from pathlib import Path
from scipy.stats import hypergeom

BASE = Path(__file__).resolve().parents[2]
N_GENOME = 15773  # universo de genes quantificados, FASE 3/5 (nao o total de "genes" do GTF bruto)
FASE5_DIR = BASE / "resultados" / "fase5_blocoD"
FASE6D_DIR = BASE / "resultados" / "fase6_blocoD"
FASE6E_DIR = BASE / "resultados" / "fase6_blocoE"

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]


def load_gene_set(path, col="gene_id"):
    genes = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            genes.add(row[col].strip('"'))
    return genes


def main():
    trypsin_genes = set()
    with open(FASE6E_DIR / "pfam_hits_per_gene_ref_fase7.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "PF00089" in row["pfam_accessions"]:
                trypsin_genes.add(row["gene_id"])
    print(f"Genes com dominio Pfam de tripsina (PF00089, FASE 7): {len(trypsin_genes)}")
    print()

    summary_rows = []
    for contrast in CONTRASTS:
        rmats_genes = load_gene_set(FASE6D_DIR / f"rmats_sig_{contrast}.csv")
        majiq_genes = load_gene_set(FASE6D_DIR / f"majiq_sig_{contrast}.csv")
        splicing_genes = rmats_genes | majiq_genes
        splicing_both = rmats_genes & majiq_genes

        de_genes = load_gene_set(FASE5_DIR / f"deseq2_{contrast}_sig.csv")

        splicing_and_de = splicing_genes & de_genes
        splicing_only = splicing_genes - de_genes
        trypsin_with_splicing = splicing_genes & trypsin_genes

        # Enriquecimento: a sobreposicao splicing x DE eh maior que o
        # esperado so pelo DE cobrir uma fatia grande do genoma (ate 26%
        # em SKTI/GORE3)? Hipergeometrica: P(X >= k) dado universo N,
        # K=genes DE, n=genes com splicing sig., k=intersecao observada.
        k_obs = len(splicing_and_de)
        K_de = len(de_genes)
        n_splice = len(splicing_genes)
        pval_enrich = hypergeom.sf(k_obs - 1, N_GENOME, K_de, n_splice)
        expected_by_chance = n_splice * K_de / N_GENOME

        row = {
            "contrast": contrast,
            "splicing_genes_uniao_rmats_majiq": len(splicing_genes),
            "splicing_genes_intersecao_rmats_majiq": len(splicing_both),
            "de_genes_fase5": len(de_genes),
            "splicing_E_de_ambos": len(splicing_and_de),
            "splicing_E_de_esperado_ao_acaso": round(expected_by_chance, 1),
            "splicing_E_de_hypergeom_pvalue": pval_enrich,
            "splicing_SEM_de_apenas_isoforma": len(splicing_only),
            "genes_tripsina_com_splicing_sig": len(trypsin_with_splicing),
            "genes_tripsina_com_splicing_sig_lista": ";".join(sorted(trypsin_with_splicing)),
        }
        summary_rows.append(row)
        print(f"{contrast}:")
        print(f"  splicing (uniao rMATS/MAJIQ): {len(splicing_genes)} genes")
        print(f"  DE (FASE 5, DESeq2/R):        {len(de_genes)} genes ({100*K_de/N_GENOME:.1f}% do genoma quantificado)")
        print(f"  splicing E DE:                {len(splicing_and_de)} genes observados "
              f"vs. {expected_by_chance:.1f} esperados ao acaso (hipergeometrica p={pval_enrich:.2e})")
        print(f"  splicing SEM DE (so isoforma): {len(splicing_only)} genes")
        print(f"  tripsina (PF00089) com splicing sig.: {len(trypsin_with_splicing)} "
              f"-> {sorted(trypsin_with_splicing)}")
        print()

    out_path = FASE6E_DIR / "cross_reference_summary.csv"
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)
    print(f"Resumo salvo em {out_path}")


if __name__ == "__main__":
    main()
