#!/bin/bash
# FASE 1, Bloco C - subamostragem deterministica (seqtk, seed -s100, 2M pares)
# das amostras usadas no sweep de parametros de trimagem: ID-1 (controle
# limpo, mesma amostra do teste A/B do Bloco B) + ID-7/ID-8/ID-9/ID-10
# (as 4 amostras com alto % de adapter_dimer_reads no Bloco B).
set -uo pipefail
cd ~/rnaseq-Anticarsia-GORE3
mkdir -p qc/blocoC_subsample

# seqtk nao esta no env "ngs" (confirmado 29/07/2026); esta instalado no env
# "busco" (seqtk 1.5, bioconda). Chamado por caminho completo para nao alterar
# nenhum env existente so por causa deste teste pontual.
SEQTK=~/miniforge3/envs/busco/bin/seqtk

N=2000000
for s in ID-1 ID-7 ID-8 ID-9 ID-10; do
  echo "=== subamostrando $s ($N pares, seed 100) ==="
  $SEQTK sample -s100 raw_fastq/${s}_1.fastq.gz $N | gzip > qc/blocoC_subsample/${s}_1.fastq.gz
  $SEQTK sample -s100 raw_fastq/${s}_2.fastq.gz $N | gzip > qc/blocoC_subsample/${s}_2.fastq.gz
done
echo SUBSAMPLE_DONE_MARKER
