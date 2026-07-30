#!/bin/bash
# FASE 1, Bloco B - trimagem completa das 13 amostras (26 arquivos) com fastp
# 1.3.0 (env "ngs"), parametros "Set B" (decidido no teste A/B: sobrevivencia
# identica ao Set A em ID-8, mas com seguranca extra de poly_g/poly_x/overrep
# a custo zero - ver artigo.md Bloco B). NovaSeq X (2-color) ja confirmado
# pelos headers reais (artigo.md 2.2), o que justifica --trim_poly_g.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3
mkdir -p trimmed qc/post_trim

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16 ID-18"

for s in $SAMPLES; do
  echo "=== $s : fastp Set B - $(date) ==="
  fastp \
    --in1 raw_fastq/${s}_1.fastq.gz --in2 raw_fastq/${s}_2.fastq.gz \
    --out1 trimmed/${s}_1.trimmed.fastq.gz --out2 trimmed/${s}_2.trimmed.fastq.gz \
    --detect_adapter_for_pe --length_required 50 --qualified_quality_phred 20 \
    --trim_poly_g --trim_poly_x --overrepresentation_analysis \
    --json qc/post_trim/${s}.fastp.json --html qc/post_trim/${s}.fastp.html \
    --report_title "${s}" --thread 12 2> qc/post_trim/${s}.fastp.log
done
echo "=== Trimagem concluida: $(date) ==="
echo FULLTRIM_DONE_MARKER
