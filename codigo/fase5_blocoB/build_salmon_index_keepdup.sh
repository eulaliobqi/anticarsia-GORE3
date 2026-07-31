#!/bin/bash
# FASE 5, Bloco B - reconstroi o indice Salmon decoy-aware da FASE 3 (Bloco
# D1) ADICIONANDO --keepDuplicates.
#
# POR QUE: o manual do tximport (bioconductor.org/.../tximport.html) e'
# normativo, nao sugestivo - "Do not manually pass the original gene-level
# counts to downstream methods without an offset... Passing uncorrected
# gene-level counts without an offset is not recommended by the tximport
# package authors." Isso significa usar DESeqDataSetFromTximport (com o
# offset de comprimento de transcrito) como entrada do DESeq2 na FASE 5,
# em vez do featureCounts bruto. Mas o indice Salmon da FASE 3 foi
# construido SEM --keepDuplicates, o que colapsou 811 dos 25.840
# transcritos (sequencia identica byte-a-byte a outro transcrito) num
# unico representante - deixando ~800 dos 15.773 genes sem nenhum
# transcrito diretamente quantificavel no tximport. --keepDuplicates
# resolve isso (mantem todos os transcritos como entradas separadas no
# indice, mesmo os identicos), fechando a lacuna de cobertura a custo
# minimo (mesmo transcriptoma/decoy ja extraidos na FASE 3, so a etapa de
# indexacao precisa rodar de novo - ja levou so ~7 min da primeira vez).
#
# transcripts.fa, decoys.txt e gentrome.fa ja existem da FASE 3 Bloco D1 -
# reaproveitados sem alteracao (mesmo transcriptoma, mesmo genoma-decoy).
# Indice novo em diretorio separado (salmon_index_decoy_keepdup) - NAO
# sobrescreve o indice da FASE 3 (salmon_index_decoy), que fica disponivel
# para comparacao se necessario.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

if [ -f salmon_index_decoy_keepdup/info.json ]; then
  echo "=== indice com --keepDuplicates ja existe, pulando construcao ==="
else
  echo "=== salmon index (decoy-aware, --keepDuplicates, k=31 default) ==="
  salmon index \
    --threads 8 \
    --transcripts genome_annotation/gentrome.fa \
    --decoys genome_annotation/decoys.txt \
    --index salmon_index_decoy_keepdup \
    --keepDuplicates \
    -k 31
fi

echo FASE5_BLOCOB_SALMON_INDEX_KEEPDUP_DONE_MARKER
