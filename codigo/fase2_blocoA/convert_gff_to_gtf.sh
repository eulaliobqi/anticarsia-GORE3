#!/bin/bash
# FASE 2, Bloco A - passo 1: converter a anotacao do genoma de GFF3 para GTF.
#
# POR QUE ISSO E' NECESSARIO:
# O RefSeq (NCBI) distribui anotacoes em formato GFF3. STAR e HISAT2 tambem
# aceitam GFF3, mas exigem que a gente informe manualmente quais tags do
# GFF3 correspondem a "gene" e "transcrito pai" de cada exon (ex.
# --sjdbGTFtagExonParentTranscript Parent no STAR). Isso e' propenso a erro
# e cada ferramenta tem uma sintaxe diferente para isso. Convertendo uma
# unica vez para GTF (formato mais simples e padronizado: cada linha de
# exon ja vem com gene_id/transcript_id explicitos), tanto o STAR quanto o
# HISAT2 (via hisat2_extract_splice_sites.py/hisat2_extract_exons.py, que
# so aceitam GTF) conseguem ler o mesmo arquivo sem gambiarra de flags.
#
# gffread (do pacote Cufflinks/GFFread, ja instalado no env "ngs",
# versao 0.12.7) faz essa conversao preservando gene_id/transcript_id.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3

# Genoma e anotacao (GFF3) ja baixados por outro projeto local (vg_search),
# confirmados como a anotacao RS_2026_04 correta (checado pelo cabecalho
# "#!annotation-source NCBI RefSeq GCF_050436995.1-RS_2026_04" do proprio
# arquivo GFF) - por isso reaproveitamos em vez de baixar de novo.
GENOME_DIR=~/vg_search/genome/ncbi_dataset/data/GCF_050436995.1
GFF=$GENOME_DIR/genomic.gff
FASTA=$GENOME_DIR/GCF_050436995.1_ilAntGemm2_primary_genomic.fna

mkdir -p genome_annotation

# -T = forca saida em formato GTF (em vez do GFF3 padrao do gffread).
# -o  = arquivo de saida.
gffread "$GFF" -T -o genome_annotation/GCF_050436995.1_RS_2026_04.gtf

# Guarda tambem o caminho do FASTA num arquivo texto simples, para os
# proximos scripts (build_star_index.sh, build_hisat2_index_annotated.sh)
# nao precisarem repetir o caminho completo do outro projeto.
echo "$FASTA" > genome_annotation/genome_fasta_path.txt

# Contagem rapida de linhas de "exon" no GTF gerado - serve so como
# checagem visual de sanidade (nao e' um teste automatizado, so um numero
# para conferir que a conversao nao gerou um arquivo vazio ou truncado).
echo "Linhas de exon no GTF gerado:"
grep -c $'\texon\t' genome_annotation/GCF_050436995.1_RS_2026_04.gtf

echo GFF_TO_GTF_DONE_MARKER
