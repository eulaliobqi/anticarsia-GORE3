#!/bin/bash
# FASE 2, Bloco B - via de SPLICING: indice + alinhamento com Subread-align
# nas 13 bibliotecas completas trimadas.
#
# POR QUE UMA VIA SEPARADA (alem de STAR, que ja faz a via de expressao
# genica em run_alignment_full.sh): docs/07_analise_rnaseq.md cita
# coxe2024benchmarking (PMID 38475429), que comparou HISAT2, STAR, Subread
# e BBMap em Arabidopsis thaliana e achou que os alinhadores empatam em
# acuracia de RESOLUCAO DE BASE, mas Subread foi o mais promissor em
# RESOLUCAO DE JUNCAO - decisiva para atribuir corretamente um evento de
# splicing alternativo (o objetivo central deste projeto) a uma juncao
# exon-exon especifica. Por isso o "padrao ouro" do projeto usa Subread
# como via DEDICADA a splicing, em paralelo a STAR/HISAT2 (via de
# expressao genica), nao como substituto.
# Ressalva ja registrada no projeto: o benchmark citado e' em planta, nao
# inseto - o ranking absoluto pode nao se transferir, so a logica geral
# (base != juncao) foi usada para justificar ter as duas vias.
#
# Subread e' um pacote diferente do STAR/HISAT2: tem seu proprio formato
# de indice (subread-buildindex) e seu proprio alinhador (subread-align),
# ambos no env "rnaseq-tools" (confirmado antes de escrever este script).
# Diferente do STAR/HISAT2, o subread-buildindex NAO precisa do GTF - o
# subread-align detecta juncoes exon-exon por conta propria durante o
# alinhamento (modo "seed-and-vote"), guiado pela flag -t 0 abaixo.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

FASTA=$(cat genome_annotation/genome_fasta_path.txt)

mkdir -p genome_index_subread qc/fase2_blocoB_subread bam/subread

# ---------- indice Subread (uma vez so, reaproveitado por todas as amostras) ----------
if [ -f genome_index_subread/ilAntGemm2.reads ]; then
  echo "=== indice Subread ja existe, pulando construcao ==="
else
  echo "=== construindo indice Subread ==="
  subread-buildindex \
    -o genome_index_subread/ilAntGemm2 \
    "$FASTA"
fi

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16 ID-18"

for s in $SAMPLES; do
  # Retomabilidade: mesma logica dos outros scripts - se o BAM final ja
  # existe, a amostra ja foi processada com sucesso.
  if [ -f "bam/subread/${s}.bam" ]; then
    echo "=== Subread-align - $s: ja concluido, pulando ==="
    continue
  fi
  echo "=== Subread-align (biblioteca completa) - $s - $(date) ==="
  # -t 0: modo RNA-seq (habilita deteccao de reads que cruzam juncao
  # exon-exon). -t 1 seria modo DNA-seq/genomico, sem essa deteccao -
  # errado para o nosso caso.
  # -T 16: mesma logica de threads dos outros scripts (metade dos 32
  # nucleos do servidor por amostra).
  # --sortReadsByCoordinates: pede ao subread-align para ja entregar BAM
  # ordenado por posicao, equivalente ao --outSAMtype BAM SortedByCoordinate
  # do STAR - evita rodar samtools sort como passo separado.
  subread-align \
    -t 0 \
    -T 16 \
    -i genome_index_subread/ilAntGemm2 \
    -r trimmed/${s}_1.trimmed.fastq.gz \
    -R trimmed/${s}_2.trimmed.fastq.gz \
    --sortReadsByCoordinates \
    -o bam/subread/${s}.bam \
    > qc/fase2_blocoB_subread/${s}.subread_align.log 2>&1

  samtools index bam/subread/${s}.bam
done

echo FASE2_BLOCOB_SUBREAD_DONE_MARKER
