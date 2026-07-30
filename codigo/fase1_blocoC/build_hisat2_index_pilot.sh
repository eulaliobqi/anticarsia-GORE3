#!/bin/bash
# FASE 1, Bloco C - indice HISAT2 PILOTO, so para o teste de equilibrio de
# trimagem (alinhamento de subamostras de 2M pares, nao a FASE 2 formal).
# Genoma de referencia (GCF_050436995.1, ilAntGemm2) ja estava baixado no
# servidor em ~/vg_search/genome/ (projeto agemmatalis-vg-vgr), reaproveitado
# aqui em vez de baixar de novo. Indice construido sem anotacao de splice
# sites (--ss/--exon) porque o objetivo e' taxa de mapeamento geral como
# criterio de decisao do sweep, nao quantificacao de isoforma - a FASE 2
# formal deve reconstruir (ou reindexar com splice sites) separadamente.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3
mkdir -p genome_index_pilot

GENOME_FA=~/vg_search/genome/ncbi_dataset/data/GCF_050436995.1/GCF_050436995.1_ilAntGemm2_primary_genomic.fna

hisat2-build -p 16 "$GENOME_FA" genome_index_pilot/ilAntGemm2_pilot \
  > genome_index_pilot/build.log 2>&1

echo HISAT2BUILD_DONE_MARKER
