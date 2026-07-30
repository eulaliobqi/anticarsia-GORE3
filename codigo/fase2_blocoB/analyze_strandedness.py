"""
FASE 2, Bloco B - le os sumarios do featureCounts (check_strandedness.sh,
uma corrida com -s 1 e outra com -s 2, para ID-1 e ID-8) e decide qual
sentido de strandedness bate com os dados reais.

Logica da decisao: featureCounts escreve, para cada BAM, um arquivo
"<saida>.summary" com uma linha "Assigned" (reads atribuidos a algum gene)
e varias linhas "Unassigned_*" (reads nao atribuidos, por motivos
diferentes - sem feature no lugar certo, mapeamento ambiguo, etc). Se o
parametro -s escolhido bate com o sentido real da biblioteca, a fracao de
reads "Assigned" e' ALTA (a maioria dos reads de mRNA cai dentro de algum
gene anotado). Se o parametro esta' invertido (testando o sentido oposto
ao real), quase todo mundo cai em "Unassigned_NoFeature", porque o
featureCounts esta' checando a fita errada do gene.
"""
import os
import csv

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/fase2_blocoB_strandcheck")
OUT_CSV = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/resultados/fase2_blocoB_strandedness.csv")

SAMPLES = ["ID-1", "ID-8"]
STRANDS = [1, 2]
STRAND_LABEL = {1: "forward (-s 1)", 2: "reverse (-s 2)"}


def parse_summary(path):
    """Le o arquivo <saida>.summary do featureCounts e devolve
    (reads_assigned, reads_total) - total = soma de TODAS as categorias
    (Assigned + todas as Unassigned_*), nao so os mapeados, porque e' essa
    soma que o featureCounts usa como denominador implicito do resultado."""
    assigned = 0
    total = 0
    with open(path) as f:
        next(f)  # primeira linha e' so o cabecalho "Status <bam>"
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 2:
                continue
            status, count = parts[0], int(parts[1])
            total += count
            if status == "Assigned":
                assigned = count
    return assigned, total


rows = []
for s in SAMPLES:
    for strand in STRANDS:
        summary_path = os.path.join(QC_DIR, f"{s}_s{strand}.txt.summary")
        assigned, total = parse_summary(summary_path)
        rows.append(dict(
            sample=s,
            strand_tested=STRAND_LABEL[strand],
            reads_assigned=assigned,
            reads_total=total,
            pct_assigned=round(100 * assigned / total, 2) if total else None,
        ))

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
with open(OUT_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

hdr = list(rows[0].keys())
print("\t".join(hdr))
for r in rows:
    print("\t".join(str(r[h]) for h in hdr))
print(f"\nCSV: {OUT_CSV}")

# ---- Decisao: para cada amostra, qual -s teve maior %assigned? ----
print("\n=== Decisao de strandedness por amostra ===")
winners = []
for s in SAMPLES:
    sample_rows = [r for r in rows if r["sample"] == s]
    winner = max(sample_rows, key=lambda r: r["pct_assigned"])
    winners.append(winner["strand_tested"])
    print(f"{s}: {winner['strand_tested']} vence com {winner['pct_assigned']}% assigned "
          f"(vs. {[r['pct_assigned'] for r in sample_rows if r is not winner]}% na outra config)")

if len(set(winners)) == 1:
    print(f"\n=> CONSISTENTE entre as {len(SAMPLES)} amostras testadas: usar {winners[0]} "
          f"na producao (Bloco C, quando planejado).")
else:
    print(f"\n=> INCONSISTENTE entre amostras ({winners}) - investigar antes de fixar o "
          f"parametro de strand para o Bloco C. Nao assumir um valor default sem resolver isso.")
