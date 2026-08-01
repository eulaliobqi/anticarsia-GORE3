#!/bin/bash
# FASE 9, Bloco C, passo 2 - MSA (MAFFT --auto) das regioes de dominio
# PF00089 dos 168 candidatos + 2 referencias conhecidas (build_domain_input.py).
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate phylo
cd ~/rnaseq-Anticarsia-GORE3

mafft --auto --thread 16 \
  resultados_server/fase9_blocoC_domain_input.faa \
  > resultados_server/fase9_blocoC_domain_aligned.fasta \
  2> resultados_server/fase9_blocoC_mafft.log

echo "mafft exit=$?"
echo "sequencias no alinhamento: $(grep -c '>' resultados_server/fase9_blocoC_domain_aligned.fasta)"
