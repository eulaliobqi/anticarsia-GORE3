#!/bin/bash
# FASE 1, Bloco B - teste A/B empirico de parametros do fastp, em 2 amostras
# representativas (ID-8 = pior amostra do lote / GC alto; ID-1 = limpa).
# Decide entre --length_required 36 (docs/07_analise_rnaseq.md original) e
# --length_required 50 + trim_poly_g/poly_x/overrepresentation (modulo de
# producao do RNA-Seq-not-model), com fastp 1.3.0 (env "ngs").
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3
mkdir -p qc/ab_test

for s in ID-1 ID-8; do
  echo "=== $s - Set A (length_required 36) ==="
  fastp \
    --in1 raw_fastq/${s}_1.fastq.gz --in2 raw_fastq/${s}_2.fastq.gz \
    --out1 qc/ab_test/${s}_setA_1.fastq.gz --out2 qc/ab_test/${s}_setA_2.fastq.gz \
    --detect_adapter_for_pe --length_required 36 --qualified_quality_phred 20 \
    --json qc/ab_test/${s}_setA.json --html qc/ab_test/${s}_setA.html \
    --report_title "${s} setA" --thread 8 2> qc/ab_test/${s}_setA.log

  echo "=== $s - Set B (length_required 50 + poly_g/poly_x + overrep) ==="
  fastp \
    --in1 raw_fastq/${s}_1.fastq.gz --in2 raw_fastq/${s}_2.fastq.gz \
    --out1 qc/ab_test/${s}_setB_1.fastq.gz --out2 qc/ab_test/${s}_setB_2.fastq.gz \
    --detect_adapter_for_pe --length_required 50 --qualified_quality_phred 20 \
    --trim_poly_g --trim_poly_x --overrepresentation_analysis \
    --json qc/ab_test/${s}_setB.json --html qc/ab_test/${s}_setB.html \
    --report_title "${s} setB" --thread 8 2> qc/ab_test/${s}_setB.log
done
echo AB_TEST_DONE_MARKER
