#!/usr/bin/env python3
"""FASE 3, Bloco E - constroi tx2gene.tsv (transcript_id, gene_id) direto do
GTF real (ja corrigido, fase3_blocoA/fix_gtf_missing_geneid.sh), para o
tximport. Diferente do RNA-Seq-not-model/scripts/00_tximport.R original, que
le um gene_trans_map do Trinity (nao existe aqui - este projeto e'
genoma-guiado, nao de novo).

So' precisa das linhas "transcript" (uma por transcrito, ja com
transcript_id e gene_id no mesmo registro) - nao precisa varrer as linhas
de exon, que repetem o mesmo par varias vezes por transcrito.
"""
import csv
import re

# Este script roda no SERVIDOR, com cwd em ~/rnaseq-Anticarsia-GORE3/ (mesma
# convencao dos outros scripts de fase3 que leem genome_annotation/* com
# caminho relativo, ja que la' os scripts ficam soltos na raiz do projeto,
# nao replicando a estrutura codigo/faseN_blocoX/ do repo local).
GTF_PATH = "genome_annotation/GCF_050436995.1_RS_2026_04.fixed.gtf"
OUT_TX2GENE = "genome_annotation/tx2gene.tsv"
OUT_SUMMARY_CSV = "resultados/fase3_blocoE_tx2gene_summary.csv"

ATTR_RE = re.compile(r'transcript_id "([^"]+)"; gene_id "([^"]+)"')


def main():
    pairs = {}
    with open(GTF_PATH, encoding="utf-8") as fh:
        for line in fh:
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 9 or fields[2] != "transcript":
                continue
            m = ATTR_RE.search(fields[8])
            if not m:
                continue
            tx_id, gene_id = m.group(1), m.group(2)
            pairs[tx_id] = gene_id

    with open(OUT_TX2GENE, "w", encoding="utf-8") as fh:
        for tx_id, gene_id in sorted(pairs.items()):
            fh.write(f"{tx_id}\t{gene_id}\n")

    n_genes = len(set(pairs.values()))
    print(f"{len(pairs)} transcritos -> {n_genes} genes unicos")
    print(f"Escrito: {OUT_TX2GENE}")

    # resumo pequeno, versionavel (nao a tabela completa - seguem so contagens)
    with open(OUT_SUMMARY_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["n_transcripts", "n_genes"])
        w.writerow([len(pairs), n_genes])
    print(f"Escrito: {OUT_SUMMARY_CSV}")


if __name__ == "__main__":
    main()
