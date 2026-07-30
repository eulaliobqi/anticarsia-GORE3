#!/bin/bash
# FASE 1, Bloco C - alinhamento PILOTO (HISAT2) dos reads trimados de cada
# combinacao amostra x set do sweep, contra o indice piloto de
# GCF_050436995.1 (build_hisat2_index_pilot.sh). So para arbitrar o sweep de
# trimagem com taxa de mapeamento real (criterio de aprovacao oficial do
# projeto e' mapeamento >80%, docs/07_analise_rnaseq.md); NAO e' a FASE 2
# formal (que roda nas 13 amostras completas, nao nas subamostras de 2M).
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3

INDEX=genome_index_pilot/ilAntGemm2_pilot

for s in ID-1 ID-7 ID-8 ID-9 ID-10; do
  for set in setB setC1 setC2 setC3; do
    echo "=== HISAT2 piloto - $s $set ==="
    hisat2 -p 8 -x "$INDEX" \
      -1 qc/blocoC_test/${s}_${set}_1.fastq.gz \
      -2 qc/blocoC_test/${s}_${set}_2.fastq.gz \
      -S /dev/null \
      --summary-file qc/blocoC_test/${s}_${set}.hisat2_summary.txt \
      2> qc/blocoC_test/${s}_${set}.hisat2.log
  done
done
echo HISAT2PILOT_DONE_MARKER
