#!/bin/bash
# FASE 6, Bloco B - deteccao de splicing alternativo classico (SE, A5SS,
# A3SS, MXE, RI) com rMATS-turbo, sobre o alinhamento Subread (FASE 2,
# Bloco B) - Subread foi escolhido ali por ter a melhor acuracia de
# juncao exon-exon (coxe2024benchmarking), o criterio que mais importa
# para splicing, diferente da via STAR/expressao genica usada nas
# FASES 3/5/7.
#
# Escopo (confirmado com o usuario, mesmo recorte da FASE 5/7): 3
# contrastes pareados contra o Controle - Benzamidina, SKTI, GORE3. Os
# cabeca-a-cabeca ficam para outro artigo, igual nas fases anteriores.
#
# rMATS ja vem instalado no ambiente rnaseq-tools (v4.3.0, confirmado
# nesta sessao, nao precisou instalar nada) - o mesmo ambiente que tem o
# Subread usado para gerar os BAMs de entrada.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

GTF=genome_annotation/GCF_050436995.1_RS_2026_04.fixed.gtf
# ATENCAO - correcao real (01/08/2026): a primeira tentativa apontava para
# bam/subread (gerado por subread-align -t 0), que NUNCA reporta juncao
# exon-exon com 'N' no CIGAR - confirmado com samtools view, 0 reads em
# todo o BAM. Isso fez o rMATS produzir 0 eventos em TODOS os 5 tipos x 3
# contrastes na primeira rodada. Corrigido: bam/subjunc (gerado por
# codigo/fase6_blocoB/run_subjunc_realign.sh, usando o binario subjunc do
# mesmo pacote Subread - o dedicado a deteccao de juncao) - confirmado
# via samtools view que agora existem reads com 'N' real no CIGAR
# (ex. "133M1126N18M").
BAMDIR=bam/subjunc
OUTBASE=resultados_server/fase6_blocoB
mkdir -p "$OUTBASE"

# Grupos delivered (13/13 amostras, confirmado na FASE 1 - 5 tubos dos 17
# submetidos nao vieram nesta entrega: ID-4,6,11,13,17). ID-18 (corpo
# gorduroso) fica fora, nao entra na matriz de contraste.
CONTROL="ID-1 ID-2 ID-3"
BENZAMIDINE="ID-5 ID-7 ID-8"
SKTI="ID-9 ID-10 ID-12"
GORE3="ID-14 ID-15 ID-16"

# Leitura: relatorio da Macrogen (FASE 1) fala em "~150nt", mas o campo
# SEQ do BAM real (checado nesta sessao, samtools view + length do
# campo 10, 3 reads de ID-1) mostra 151nt exatos - usar o dado real, nao
# o nominal do fornecedor. Strand: reverse (-s 2 no featureCounts, ISR
# no Salmon, decisao empirica registrada em
# resultados/fase3_blocoA_strand_decision.csv) -> equivalente declarado
# aqui a fr-firststrand na convencao do rMATS (biblioteca dUTP/
# reverse-stranded padrao: read1 e' antisenso ao transcrito). Nao e'
# uma suposicao nova, e' o mesmo dado ja usado nas FASES 3/5, so
# traduzido para a nomenclatura que o rMATS espera.
READ_LEN=151
LIBTYPE=fr-firststrand
NTHREAD=16   # deixa metade dos 32 cores livres p/ outros jobs no servidor
             # compartilhado (mesma cautela ja aprendida na FASE 2, onde
             # concorrencia de threads causou falha de segmentacao).

# make_bam_list <nome_saida> <lista de IDs>: escreve o .txt que o rMATS
# espera (caminhos separados por virgula, uma linha so), a partir dos
# BAMs ja indexados (.bai confirmados presentes nesta sessao).
make_bam_list() {
  local outfile="$1"; shift
  local paths=()
  for id in "$@"; do
    paths+=("$BAMDIR/${id}.bam")
  done
  local IFS=,
  echo "${paths[*]}" > "$outfile"
}

run_contrast() {
  local name="$1"; shift
  local treat_ids="$1"; shift
  local outdir="$OUTBASE/${name}_vs_Control"
  local tmpdir="$OUTBASE/${name}_vs_Control_tmp"

  # Retomabilidade: se o marcador de sucesso ja existe, pula (mesmo
  # padrao dos scripts das fases anteriores).
  if [ -f "$outdir/rmats_done.marker" ]; then
    echo "SKIP $name: ja concluido"
    return 0
  fi

  mkdir -p "$outdir" "$tmpdir"
  make_bam_list "$outdir/b1.txt" $treat_ids
  make_bam_list "$outdir/b2.txt" $CONTROL

  # b1 = tratamento, b2 = Controle: IncLevelDifference do rMATS sai como
  # media(IncLevel_b1) - media(IncLevel_b2), ou seja positivo = mais
  # inclusao no tratamento em relacao ao Controle - convencao mantida
  # igual a FASE 5 (log2FC sempre tratamento vs. Controle).
  rmats.py \
    --b1 "$outdir/b1.txt" \
    --b2 "$outdir/b2.txt" \
    --gtf "$GTF" \
    --od "$outdir" \
    --tmp "$tmpdir" \
    -t paired \
    --readLength $READ_LEN \
    --variable-read-length \
    --libType $LIBTYPE \
    --nthread $NTHREAD \
    > "$outdir/rmats.log" 2>&1

  if [ $? -eq 0 ]; then
    touch "$outdir/rmats_done.marker"
    echo "OK $name"
  else
    echo "FALHOU $name - ver $outdir/rmats.log"
  fi
}

run_contrast "Benzamidine" "$BENZAMIDINE"
run_contrast "SKTI"        "$SKTI"
run_contrast "GORE3"       "$GORE3"

echo FASE6_BLOCOB_RMATS_DONE_MARKER
