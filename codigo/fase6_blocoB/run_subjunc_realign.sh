#!/bin/bash
# FASE 6, Bloco B (pre-requisito) - REALINHAMENTO com subjunc, corrigindo um
# erro real da FASE 2.
#
# ACHADO TECNICO REAL (01/08/2026), nao suavizado: o BAM do "Subread" gerado
# na FASE 2 Bloco B (codigo/fase2_blocoB/run_subread_align_full.sh) foi
# feito com `subread-align -t 0`. O comentario original desse script dizia
# que -t 0 "habilita deteccao de reads que cruzam juncao exon-exon" - isso
# esta ERRADO na pratica, confirmado checando o CIGAR real do BAM
# (samtools view): ZERO reads em todo o arquivo tem operador 'N' no CIGAR
# (a marca padrao de alinhamento com gap/splice que rMATS, STAR e qualquer
# ferramenta de deteccao de evento espera). Os CIGARs mostram só soft-clip
# pesado (ex. "16S135M", "33S118M") - subread-align faz o "seed-and-vote"
# generico e SOFT-CLIPA a porcao que nao alinha, em vez de reportar um
# alinhamento com gap atraves do intron. E' por isso que o rMATS-turbo
# (FASE 6 Bloco B, primeira tentativa) produziu 0 eventos com contagem em
# TODOS os 5 tipos x 3 contrastes - nao e' um resultado biologico "sem
# splicing", e' as leituras nunca tendo sido alinhadas de forma
# spliced-aware para comecar.
#
# O pacote Subread tem DOIS alinhadores: subread-align (uso geral, sem
# deteccao de juncao confiavel) e subjunc (dedicado a RNA-Seq/deteccao de
# juncao exon-exon, mesmo indice, mesma familia "seed-and-vote", mas
# reporta juncoes com 'N' no CIGAR). coxe2024benchmarking (a citacao que
# justificou "usar Subread para splicing" na FASE 2) quase certamente
# testou subjunc, nao subread-align, para a metrica de "acuracia de
# juncao" - o benchmark nao teria sentido com um alinhador que nao reporta
# juncao nenhuma. A decisao da FASE 2 de citar "Subread" ficou ambigua
# entre os dois binarios; corrigido aqui, nao la (o BAM da FASE 2 continua
# valido/usado para o que ja foi feito com ele, que nao dependia de
# juncao - so este bloco precisa do dado spliced-aware).
#
# Mesmo indice ja construido na FASE 2 (subread-buildindex nao depende do
# alinhador escolhido depois) - nao precisa reconstruir.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

mkdir -p qc/fase6_blocoB_subjunc bam/subjunc

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16 ID-18"

for s in $SAMPLES; do
  if [ -f "bam/subjunc/${s}.bam" ]; then
    echo "=== subjunc - $s: ja concluido, pulando ==="
    continue
  fi
  echo "=== subjunc (biblioteca completa) - $s - $(date) ==="
  # Mesmos parametros de proposito do subread-align original (-T 16,
  # --sortReadsByCoordinates) - unica mudanca real e' o binario (subjunc
  # em vez de subread-align), que e' o que resolve o problema. subjunc
  # nao tem flag -t (esse modo e' exclusivo do subread-align) - ele já é
  # sempre "modo RNA-seq"/splice-aware por definicao.
  subjunc \
    -T 16 \
    -i genome_index_subread/ilAntGemm2 \
    -r trimmed/${s}_1.trimmed.fastq.gz \
    -R trimmed/${s}_2.trimmed.fastq.gz \
    --sortReadsByCoordinates \
    -o bam/subjunc/${s}.bam \
    > qc/fase6_blocoB_subjunc/${s}.subjunc.log 2>&1

  samtools index bam/subjunc/${s}.bam
done

echo FASE6_BLOCOB_SUBJUNC_DONE_MARKER
