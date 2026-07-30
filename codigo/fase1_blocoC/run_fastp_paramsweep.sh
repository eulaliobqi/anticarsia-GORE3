#!/bin/bash
# FASE 1, Bloco C - sweep de parametros de trimagem nas subamostras (2M pares)
# de ID-1/7/8/9/10. Testa se afrouxar qualidade (C1) ou a sensibilidade de
# overlap-analysis do fastp (C2/C3) recupera reads sem custo de qualidade,
# em relacao ao Set B de producao (Bloco B, ja decidido para as 13 amostras
# completas). --length_required 50 e --detect_adapter_for_pe/trim_poly_g/
# trim_poly_x ficam fixos em todos os sets: o teste A/B do Bloco B ja mostrou
# que --length_required nao move a agulha (diferenca <0.1pp).
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3
mkdir -p qc/blocoC_test

run_fastp () {
  local s=$1 set=$2 extra=$3
  fastp \
    --in1 qc/blocoC_subsample/${s}_1.fastq.gz --in2 qc/blocoC_subsample/${s}_2.fastq.gz \
    --out1 qc/blocoC_test/${s}_${set}_1.fastq.gz --out2 qc/blocoC_test/${s}_${set}_2.fastq.gz \
    --detect_adapter_for_pe --length_required 50 --trim_poly_g --trim_poly_x \
    --overrepresentation_analysis \
    $extra \
    --json qc/blocoC_test/${s}_${set}.json --html qc/blocoC_test/${s}_${set}.html \
    --report_title "${s} ${set}" --thread 8 2> qc/blocoC_test/${s}_${set}.log
}

for s in ID-1 ID-7 ID-8 ID-9 ID-10; do
  echo "=== $s - Set B (baseline: qq_phred 20, overlap default) ==="
  run_fastp "$s" setB "--qualified_quality_phred 20"

  echo "=== $s - Set C1 (qq_phred 15, overlap default) ==="
  run_fastp "$s" setC1 "--qualified_quality_phred 15"

  echo "=== $s - Set C2 (qq_phred 20, overlap permissivo) ==="
  run_fastp "$s" setC2 "--qualified_quality_phred 20 --overlap_len_require 20 --overlap_diff_limit 8 --overlap_diff_percent_limit 30"

  echo "=== $s - Set C3 (qq_phred 20, overlap restritivo - contraprova) ==="
  run_fastp "$s" setC3 "--qualified_quality_phred 20 --overlap_len_require 40 --overlap_diff_limit 3 --overlap_diff_percent_limit 10"
done
echo PARAMSWEEP_DONE_MARKER
