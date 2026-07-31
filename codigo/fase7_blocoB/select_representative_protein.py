#!/usr/bin/env python3
"""FASE 7, Bloco B (passo 0) - reduz o proteoma de 23.932 proteinas (todas
as isoformas) para 1 proteina representativa por gene (15.773 genes),
alinhando a unidade de analise da anotacao funcional com a unidade ja
usada em toda a FASE 3-5 (featureCounts/tximport agregam por gene_id, os
resultados de DE sao indexados por gene_id, nao por transcrito/proteina).

Achado do usuario que motivou esta correcao: anotar as 23.932 isoformas e
so depois agregar para nivel de gene exigiria uma decisao de agregacao
(uniao dos termos GO de todas as isoformas? so a mais longa?) tomada
silenciosamente. Reduzir ANTES evita essa ambiguidade.

Regra de selecao: isoforma mais longa por gene (convencao padrao quando
nao ha flag MANE/RefSeq-select disponivel neste assembly).

Mapeamento gene->mRNA->proteina extraido diretamente do GFF3 original da
NCBI (ja confirmado nesta sessao como a anotacao RS_2026_04 exata) - nao
do GTF convertido por gffread, que teve os atributos protein_id/Dbxref
descartados na conversao (achado tecnico real desta sessao).
"""
from Bio import SeqIO
import sys

GFF = "/home/eulalio/vg_search/genome/ncbi_dataset/data/GCF_050436995.1/genomic.gff"
PROTEIN_FAA = "genome_annotation/proteome/protein.faa"
OUT_FAA = "genome_annotation/proteome/protein_representative.faa"
OUT_MAP = "resultados_server/fase7_blocoB/gene_to_representative_protein.tsv"

# Passo 1: gene_id -> mRNA_id (Parent) a partir das linhas "mRNA"
mrna_to_gene = {}
with open(GFF) as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 9 or cols[2] != "mRNA":
            continue
        attrs = dict(kv.split("=", 1) for kv in cols[8].split(";") if "=" in kv)
        mrna_id = attrs.get("ID", "").removeprefix("rna-")
        gene_id = attrs.get("Parent", "")
        if mrna_id and gene_id:
            mrna_to_gene[mrna_id] = gene_id

# Passo 2: protein_id -> mRNA_id (Parent) a partir das linhas "CDS"
protein_to_mrna = {}
with open(GFF) as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 9 or cols[2] != "CDS":
            continue
        attrs = dict(kv.split("=", 1) for kv in cols[8].split(";") if "=" in kv)
        protein_id = attrs.get("protein_id", "")
        mrna_id = attrs.get("Parent", "").removeprefix("rna-")
        if protein_id and mrna_id:
            protein_to_mrna[protein_id] = mrna_id

print(f"mRNA->gene: {len(mrna_to_gene)} entradas | protein->mRNA: {len(protein_to_mrna)} entradas", file=sys.stderr)

# Passo 3: gene_id -> lista de protein_id (via mRNA)
gene_to_proteins = {}
missing_mrna = 0
for protein_id, mrna_id in protein_to_mrna.items():
    gene_id = mrna_to_gene.get(mrna_id)
    if gene_id is None:
        missing_mrna += 1
        continue
    gene_to_proteins.setdefault(gene_id, []).append(protein_id)

print(f"Genes com >=1 proteina mapeada: {len(gene_to_proteins)} | proteinas sem mRNA->gene resolvido: {missing_mrna}", file=sys.stderr)

# Passo 4: comprimento de cada proteina, a partir do FASTA baixado
protein_lengths = {}
protein_records = {}
for rec in SeqIO.parse(PROTEIN_FAA, "fasta"):
    acc = rec.id
    protein_lengths[acc] = len(rec.seq)
    protein_records[acc] = rec

n_proteins_in_faa = len(protein_records)
print(f"Proteinas no FASTA baixado: {n_proteins_in_faa}", file=sys.stderr)

# Passo 5: para cada gene, escolher a isoforma mais longa presente no FASTA
representative = {}
genes_sem_faa = 0
for gene_id, proteins in gene_to_proteins.items():
    candidates = [p for p in proteins if p in protein_lengths]
    if not candidates:
        genes_sem_faa += 1
        continue
    best = max(candidates, key=lambda p: protein_lengths[p])
    representative[gene_id] = best

print(f"Genes com proteina representativa escolhida: {len(representative)} | genes sem proteina no FASTA: {genes_sem_faa}", file=sys.stderr)

# Passo 6: escrever FASTA reduzido (1 seq/gene) + tabela de mapeamento
with open(OUT_FAA, "w") as out_fa, open(OUT_MAP, "w") as out_map:
    out_map.write("gene_id\tprotein_id\tprotein_length\tn_isoformas_totais\n")
    for gene_id, protein_id in sorted(representative.items()):
        rec = protein_records[protein_id]
        rec.id = protein_id
        rec.description = f"gene={gene_id}"
        SeqIO.write(rec, out_fa, "fasta")
        n_iso = len(gene_to_proteins[gene_id])
        out_map.write(f"{gene_id}\t{protein_id}\t{protein_lengths[protein_id]}\t{n_iso}\n")

print(f"Escrito: {OUT_FAA} ({len(representative)} sequencias)", file=sys.stderr)
print(f"Escrito: {OUT_MAP}", file=sys.stderr)
