#!/bin/bash
# FASE 3, Bloco D2 - quantificacao Salmon (nivel transcrito/isoforma) nas 13
# bibliotecas completas, contra o indice decoy-aware do D1. Via de APOIO a
# H1 (troca de isoformas de tripsina) - nao e' o resultado principal desta
# fase (esse e' o featureCounts do Bloco C).
#
# --libType do Bloco A (fase3_blocoA_strand_decision.csv -> ISR, confirmado
# empiricamente, nao suposto do nome do kit).
# --validateMappings --gcBias: mesmos parametros ja usados no modulo
# reaproveitavel RNA-Seq-not-model/modules/quantification.nf (SALMON_QUANT),
# mantidos sem alteracao.
#
# Resumivel (marcador = salmon/{amostra}/quant.sf existir) e tolerante a
# falha isolada (set -uo pipefail, nao set -e) - mesmo padrao dos scripts
# de alinhamento da FASE 2, que ja sofreram falha de segmentacao por
# concorrencia de threads quando rodados junto com outro job de 16 threads.
# NAO lancar este script junto com outro job de 16 threads no servidor.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

LIBTYPE=$(awk -F',' 'NR==2{print $2}' resultados/fase3_blocoA_strand_decision.csv)

mkdir -p salmon

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16 ID-18"

for s in $SAMPLES; do
  if [ -f "salmon/${s}/quant.sf" ]; then
    echo "=== Salmon - $s: ja concluido, pulando ==="
    continue
  fi
  echo "=== Salmon quant - $s - $(date) ==="
  salmon quant \
    --index salmon_index_decoy \
    --libType "$LIBTYPE" \
    -1 "trimmed/${s}_1.trimmed.fastq.gz" \
    -2 "trimmed/${s}_2.trimmed.fastq.gz" \
    --threads 16 \
    --validateMappings --gcBias \
    --output "salmon/${s}"
done

echo "libType usado: $LIBTYPE"
echo FASE3_BLOCOD2_SALMON_QUANT_DONE_MARKER
