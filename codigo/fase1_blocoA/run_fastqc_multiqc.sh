#!/bin/bash
# FASE 1, Bloco A - QC bruto (FastQC + MultiQC) sobre os 26 FASTQ do pedido
# Macrogen HN00280302. Executado em eulalio@200.235.143.10, dentro de
# `screen -S fase1-blocoA`, env mamba "ngs" (fastqc 0.12.1, multiqc 1.33).
# Executado em 28/07/2026.
set -uo pipefail

source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3

mkdir -p qc/pre_trim qc/tmp

echo "=== FastQC iniciado: $(date) ==="
# NOTA: a flag -d qc/tmp abaixo FALHOU em execucao real ("Option d is
# ambiguous") nesta versao do FastQC; o diretorio de temp caiu no padrao
# da ferramenta. Mantido aqui como registro fiel do comando rodado, nao
# como comando validado.
fastqc --threads 12 --memory 2048 -d qc/tmp --outdir qc/pre_trim raw_fastq/*.fastq.gz
echo "=== FastQC concluido: $(date) ==="

echo "=== MultiQC iniciado: $(date) ==="
multiqc qc/pre_trim -o qc/pre_trim --filename multiqc_pre_trim -f \
  --replace-names samplesheet_replace_names.tsv
echo "=== MultiQC concluido: $(date) ==="
