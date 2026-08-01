"""FASE 9, Bloco E - o teste real de H1: para os 166 genes curados como
tripsinas digestivas verdadeiras (Bloco C - dominio Pfam PF00089 +
motivo PROSITE + triade catalitica confirmada por MSA), quais sao DE
(FASE 5) e/ou tem splicing significativo (FASE 6) em GORE3 vs. Controle,
comparado a SKTI e Benzamidina. Para os que tem splicing: caracteriza se
a mudanca e' de NIVEL (so' DE) ou de IDENTIDADE (so' splicing) ou ambos -
a pergunta central de H1 (docs/07_analise_rnaseq.md Sec.10, item 4).

Roda local - todas as entradas ja estao no repo (FASE 5/6, artigo 1) ou
foram baixadas do servidor nesta sessao (Bloco C, paper-2).
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # eulalio-pos-doc/
PAPER2 = ROOT / "paper-2"

FASE5_DIR = ROOT / "resultados" / "fase5_blocoD"
FASE6_DIR = ROOT / "resultados" / "fase6_blocoD"
BLOCOC_CSV = PAPER2 / "resultados" / "fase9_blocoC" / "triad_curated.csv"

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]
LABELS = {"Benzamidine_vs_Control": "Benzamidine", "SKTI_vs_Control": "SKTI", "GORE3_vs_Control": "GORE3"}


def load_curated_genes():
    genes = []
    with open(BLOCOC_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["curated_pass"] == "PASS":
                genes.append(row["gene_id"])
    return genes


def load_gene_set(path, col="gene_id"):
    genes = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            genes.add(row[col].strip('"'))
    return genes


def main():
    curated = load_curated_genes()
    print(f"Genes curados como tripsinas digestivas verdadeiras (Bloco C): {len(curated)}\n")

    de_sets = {}
    splicing_sets = {}
    for contrast in CONTRASTS:
        de_sets[contrast] = load_gene_set(FASE5_DIR / f"deseq2_{contrast}_sig.csv")
        rmats = load_gene_set(FASE6_DIR / f"rmats_sig_{contrast}.csv")
        majiq = load_gene_set(FASE6_DIR / f"majiq_sig_{contrast}.csv")
        splicing_sets[contrast] = rmats | majiq

    summary_rows = []
    detail_rows = []
    for gene in curated:
        row = {"gene_id": gene}
        for contrast in CONTRASTS:
            label = LABELS[contrast]
            is_de = gene in de_sets[contrast]
            is_splice = gene in splicing_sets[contrast]
            if is_de and is_splice:
                status = "nivel+identidade"
            elif is_de:
                status = "so_nivel(DE)"
            elif is_splice:
                status = "so_identidade(splicing)"
            else:
                status = "sem_mudanca_significativa"
            row[f"{label}_status"] = status
        detail_rows.append(row)

    out_detail = PAPER2 / "resultados" / "fase9_blocoE"
    out_detail.mkdir(parents=True, exist_ok=True)
    with open(out_detail / "h1_gene_level_detail.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(detail_rows[0].keys()))
        w.writeheader()
        w.writerows(detail_rows)

    for contrast in CONTRASTS:
        label = LABELS[contrast]
        counts = {"nivel+identidade": 0, "so_nivel(DE)": 0, "so_identidade(splicing)": 0, "sem_mudanca_significativa": 0}
        changed_genes = []
        for row in detail_rows:
            status = row[f"{label}_status"]
            counts[status] += 1
            if status != "sem_mudanca_significativa":
                changed_genes.append((row["gene_id"], status))
        print(f"=== {label} vs. Controle ===")
        print(f"  nivel+identidade (DE E splicing): {counts['nivel+identidade']}")
        print(f"  so nivel (DE, sem splicing):        {counts['so_nivel(DE)']}")
        print(f"  so identidade (splicing, sem DE):   {counts['so_identidade(splicing)']}")
        print(f"  sem mudanca significativa:          {counts['sem_mudanca_significativa']}")
        print(f"  total com QUALQUER mudanca:          {len(changed_genes)}/{len(curated)}")
        if changed_genes:
            print(f"  genes: {changed_genes}")
        print()
        summary_rows.append({
            "contrast": label,
            "total_curated": len(curated),
            **{k.replace("+", "_e_").replace("(", "_").replace(")", ""): v for k, v in counts.items()},
            "total_com_mudanca": len(changed_genes),
        })

    with open(out_detail / "h1_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)

    print(f"Salvo em {out_detail}")


if __name__ == "__main__":
    main()
