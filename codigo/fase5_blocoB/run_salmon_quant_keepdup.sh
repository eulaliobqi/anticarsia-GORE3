#!/bin/bash
# FASE 5, Bloco B - requantifica as 13 amostras contra o indice
# salmon_index_decoy_keepdup (FASE 5 Bloco B), saida em salmon_keepdup/ -
# NAO sobrescreve salmon/ da FASE 3 (indice antigo, sem --keepDuplicates).
# Mesmos parametros ja validados na FASE 3 (--libType ISR, confirmado
# empiricamente no Bloco A daquela fase; --validateMappings --gcBias).
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

LIBTYPE=$(awk -F',' 'NR==2{print $2}' resultados/fase3_blocoA_strand_decision.csv)

mkdir -p salmon_keepdup

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16 ID-18"

for s in $SAMPLES; do
  if [ -f "salmon_keepdup/${s}/quant.sf" ]; then
    echo "=== Salmon (keepDup) - $s: ja concluido, pulando ==="
    continue
  fi
  echo "=== Salmon quant (keepDup) - $s - $(date) ==="
  salmon quant \
    --index salmon_index_decoy_keepdup \
    --libType "$LIBTYPE" \
    -1 "trimmed/${s}_1.trimmed.fastq.gz" \
    -2 "trimmed/${s}_2.trimmed.fastq.gz" \
    --threads 16 \
    --validateMappings --gcBias \
    --output "salmon_keepdup/${s}"
done

echo "libType usado: $LIBTYPE"
echo FASE5_BLOCOB_SALMON_QUANT_KEEPDUP_DONE_MARKER
