#!/bin/bash
# FASE 6, Bloco C - construcao do splicegraph MAJIQ + cobertura PSI, sobre
# os mesmos BAMs subjunc corrigidos do Bloco B (MAJIQ tem a mesma exigencia
# de alinhamento spliced-aware com 'N' no CIGAR que o rMATS).
#
# 12 amostras (mesmos grupos n=3 da FASE 5/rMATS) - ID-18 (corpo gorduroso)
# fica de fora, fora da matriz de contraste.
#
# GFF3 (nao GTF - majiq build exige GFF3): reaproveitado de
# ~/vg_search/genome/ncbi_dataset/data/GCF_050436995.1/genomic.gff, ja
# confirmado em sessao anterior (FASE 7) como a anotacao RS_2026_04 exata.
#
# Strand: reverse (mesma decisao empirica da FASE 3/rMATS, --strandness
# REVERSE eh o nome que o MAJIQ usa para o mesmo protocolo).
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate majiq-env
cd ~/rnaseq-Anticarsia-GORE3

LICENSE=~/majiq_license_academic_official.lic
GFF3=~/vg_search/genome/ncbi_dataset/data/GCF_050436995.1/genomic.gff
OUTDIR=resultados_server/fase6_blocoC/build

mkdir -p resultados_server/fase6_blocoC

echo "=== majiq build - $(date) ==="
majiq build \
  "$GFF3" \
  codigo/fase6_blocoC/experiments.tsv \
  "$OUTDIR" \
  --strandness REVERSE \
  --nthreads 16 \
  --license "$LICENSE" \
  --overwrite \
  > resultados_server/fase6_blocoC/majiq_build.log 2>&1

echo "build exit=$?"
echo "--- conteudo de $OUTDIR ---"
ls -la "$OUTDIR"

echo FASE6_BLOCOC_MAJIQ_BUILD_DONE_MARKER
