#!/bin/bash
# FASE 3, Bloco D1 - constroi um indice DECOY-AWARE do Salmon (modo "selective
# alignment"/SAF: genoma inteiro como decoy), nao o modo "--type quasi" sem
# decoy usado no script reaproveitavel RNA-Seq-not-model/modules/
# quantification.nf (que era o estado da arte quando aquele modulo foi
# escrito, mas ja foi superado).
#
# POR QUE DECOY-AWARE: Srivastava et al. 2020 (Genome Biology, PMID
# 32894187) mostrou que reads originarios de loci genomicos nao-anotados
# mas parecidos com transcritos anotados sao frequentemente atribuidos
# erradamente ao transcrito anotado quando o indice NAO tem decoy - incluir
# o genoma inteiro como decoy deixa o Salmon rejeitar esses reads em vez de
# atribui-los errado. Validado em 109 datasets reais humanos + simulacoes
# de camundongo - NAO testado em inseto/genoma nao-modelo (ressalva
# declarada em docs/07_analise_rnaseq.md e artigo.md, mesmo padrao da
# ressalva ja usada para coxe2024benchmarking).
#
# k=31 e' o default do proprio Salmon (nao inventado/otimizado para
# inseto - nao existe benchmark de k especifico para este genoma).
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

GTF=genome_annotation/GCF_050436995.1_RS_2026_04.fixed.gtf
FASTA=$(cat genome_annotation/genome_fasta_path.txt)

if [ -f salmon_index_decoy/info.json ]; then
  echo "=== indice Salmon decoy-aware ja existe, pulando construcao ==="
else
  echo "=== extraindo transcriptoma (gffread) ==="
  conda activate ngs
  gffread -w genome_annotation/transcripts.fa -g "$FASTA" "$GTF"
  conda activate rnaseq-tools

  echo "=== construindo lista de decoys (nomes dos cromossomos/scaffolds do genoma) ==="
  grep "^>" "$FASTA" | sed 's/^>//; s/ .*//' > genome_annotation/decoys.txt

  echo "=== concatenando transcriptoma + genoma (gentrome) ==="
  cat genome_annotation/transcripts.fa "$FASTA" > genome_annotation/gentrome.fa

  echo "=== salmon index (decoy-aware, k=31 default) ==="
  salmon index \
    --threads 8 \
    --transcripts genome_annotation/gentrome.fa \
    --decoys genome_annotation/decoys.txt \
    --index salmon_index_decoy \
    -k 31
fi

echo FASE3_BLOCOD1_SALMON_INDEX_DONE_MARKER
