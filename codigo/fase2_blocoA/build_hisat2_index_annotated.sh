#!/bin/bash
# FASE 2, Bloco A - construir o indice HISAT2 anotado (com splice sites reais).
#
# CONTEXTO: este indice SUBSTITUI o indice piloto do Bloco C da FASE 1
# (codigo/fase1_blocoC/build_hisat2_index_pilot.sh), que foi construido
# de proposito SEM anotacao, so para comparar taxa de mapeamento bruta
# entre configuracoes de trimagem. Agora, com a anotacao real (RS_2026_04)
# disponivel, construimos o indice completo - a diferenca de taxa de
# mapeamento entre este indice e o piloto quantifica o quanto a anotacao
# ajuda o alinhamento (pergunta em aberto desde o Bloco C).
#
# HISAT2 (Kim et al. 2019, PMID 31375807) e' o segundo candidato para a
# via de expressao genica, junto com STAR (ver build_star_index.sh). Vive
# no env "ngs" (mesmo do fastp/featureCounts), diferente do STAR.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3

GTF=genome_annotation/GCF_050436995.1_RS_2026_04.gtf
FASTA=$(cat genome_annotation/genome_fasta_path.txt)

mkdir -p genome_index_annotated

# hisat2_extract_splice_sites.py / hisat2_extract_exons.py sao scripts
# Python que vem junto com o HISAT2 (nao sao programas separados a
# instalar). Eles leem o GTF e escrevem duas tabelas simples que o
# hisat2-build usa para saber onde ficam os introns/exons conhecidos:
#
# - splicesites.txt: uma linha por juncao conhecida (cromossomo, posicao
#   inicial/final do intron, fita) - usado pelo HISAT2 para alinhar reads
#   que cruzam uma juncao mesmo quando a juncao em si e' rara/pouco coberta.
# - exons.txt: uma linha por exon conhecido - complementa a informacao de
#   juncoes com os limites exatos de cada exon anotado.
hisat2_extract_splice_sites.py "$GTF" > genome_index_annotated/splicesites.txt
hisat2_extract_exons.py "$GTF" > genome_index_annotated/exons.txt

echo "Juncoes de splice extraidas:"
wc -l genome_index_annotated/splicesites.txt
echo "Exons extraidos:"
wc -l genome_index_annotated/exons.txt

# --ss / --exon: passam as duas tabelas acima para o hisat2-build, para
# que o indice resultante "conheca" a anotacao (equivalente em efeito ao
# --sjdbGTFfile do STAR, so que em dois arquivos separados em vez de um).
# -p 16: mesma logica de paralelismo do build_star_index.sh (16 de 32
# nucleos, deixando espaco para o STAR rodar ao mesmo tempo).
hisat2-build \
  -p 16 \
  --ss genome_index_annotated/splicesites.txt \
  --exon genome_index_annotated/exons.txt \
  "$FASTA" \
  genome_index_annotated/ilAntGemm2_annotated

echo HISAT2_INDEX_ANNOTATED_DONE_MARKER
