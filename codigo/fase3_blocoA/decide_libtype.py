#!/usr/bin/env python3
"""FASE 3, Bloco A - formaliza a decisao de strandedness (ja testada e
decidida em resultados/fase2_blocoB_strandedness.csv, FASE 2 Bloco B) como
o parametro unico que Blocos C/D desta fase vao ler - nenhum -s/--libType
fica hardcoded em mais de um script.

POR QUE ISSO IMPORTA (nao e' so reformatar um numero): featureCounts usa
`-s {0,1,2}`, Salmon usa `--libType {ISF,ISR,...}` - sao dois vocabularios
diferentes para a MESMA propriedade da biblioteca (orientacao de fita).
Se cada script da FASE 3 traduzisse esse valor por conta propria, um erro
de tradução em um dos dois (ex. inverter forward/reverse) so apareceria
muito depois, na fase de expressao diferencial - dificil de rastrear a
causa. Centralizando a traducao aqui, uma unica vez, com o mapeamento
explicito abaixo, o erro (se existir) fica visivel neste unico lugar.

Mapeamento -s -> --libType (paired-end, biblioteca stranded confirmada em
docs/07_analise_rnaseq.md §0 - kit "Illumina Stranded mRNA Prep,
Ligation"): -s 1 (forward) <-> ISF; -s 2 (reverse) <-> ISR. Fonte do
mapeamento: documentacao oficial do Salmon (--libType), nao inventado.
"""
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IN_CSV = os.path.join(BASE, "resultados", "fase2_blocoB_strandedness.csv")
OUT_CSV = os.path.join(BASE, "resultados", "fase3_blocoA_strand_decision.csv")

STRAND_TO_LIBTYPE = {
    "forward (-s 1)": ("1", "ISF"),
    "reverse (-s 2)": ("2", "ISR"),
}


def main():
    # Para cada amostra testada, pega a config com maior pct_assigned.
    best_per_sample = {}
    with open(IN_CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            s = row["sample"]
            pct = float(row["pct_assigned"])
            if s not in best_per_sample or pct > best_per_sample[s][1]:
                best_per_sample[s] = (row["strand_tested"], pct)

    winners = {s: v[0] for s, v in best_per_sample.items()}
    unique_winners = set(winners.values())

    samples_agree = len(unique_winners) == 1
    if not samples_agree:
        # Nao cair no default do nome do kit silenciosamente - isso
        # anularia o proposito do teste empirico (ver check_strandedness.sh).
        with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["featurecounts_s", "salmon_libtype", "decision_basis", "samples_agree"])
            w.writerow(["", "", "INCONCLUSIVE", "False"])
        print("INCONCLUSIVO: amostras discordam sobre o strand vencedor:")
        for s, w_ in winners.items():
            print(f"  {s}: {w_}")
        print("Nao decidir automaticamente - estender o teste a mais amostras "
              "(ver plano FASE 3 Bloco A) antes de prosseguir.")
        raise SystemExit(1)

    winning_strand = next(iter(unique_winners))
    fc_s, salmon_libtype = STRAND_TO_LIBTYPE[winning_strand]

    pct_by_sample = ", ".join(
        f"{s}={best_per_sample[s][1]:.2f}%" for s in sorted(best_per_sample)
    )
    decision_basis = (
        f"{winning_strand} venceu de forma consistente em "
        f"{len(best_per_sample)} amostras testadas ({pct_by_sample}), "
        f"confirmado empiricamente via featureCounts -s1 vs -s2 "
        f"(codigo/fase2_blocoB/check_strandedness.sh)."
    )

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["featurecounts_s", "salmon_libtype", "decision_basis", "samples_agree"])
        w.writerow([fc_s, salmon_libtype, decision_basis, "True"])

    print(f"Decisao: featureCounts -s {fc_s} / Salmon --libType {salmon_libtype}")
    print(decision_basis)
    print(f"Escrito: {OUT_CSV}")


if __name__ == "__main__":
    main()
