#!/bin/bash
# FASE 2, Bloco A - alinhar STAR e HISAT2 (ambos com indice ANOTADO) contra
# as MESMAS subamostras de 2 milhoes de pares ja geradas na FASE 1, Bloco C
# (codigo/fase1_blocoC/subsample_reads.sh) - nao regeramos as subamostras.
#
# CORRECAO IMPORTANTE (29/07/2026): a primeira versao deste script alinhava
# os FASTQ BRUTOS da subamostra (qc/blocoC_subsample/ID-X_{1,2}.fastq.gz).
# Isso deu taxas de mapeamento muito baixas e ate MENORES que o indice
# piloto sem anotacao do Bloco C (que usava reads TRIMADOS) - resultado
# implausivel (anotacao nunca deveria piorar o mapeamento), investigado e
# rastreado a essa causa: reads brutos ainda tem adaptador/poly-G/baixa
# qualidade nas pontas, o que reduz mapeamento independente do indice.
# CORRIGIDO: usar os reads da subamostra JA TRIMADOS pelo Set B do Bloco C
# (qc/blocoC_test/ID-X_setB_{1,2}.fastq.gz - fastp Set B ja rodou nessas
# subamostras no Bloco C, nao precisa retrimar).
#
# OBJETIVO: decidir entre STAR e HISAT2 (o "padrao ouro" do projeto aceita
# qualquer um dos dois para a via de expressao genica) usando taxa de
# mapeamento REAL, na mesma subamostra, em vez de escolher por preferencia.
# Como bonus, comparamos tambem contra o indice PILOTO sem anotacao do
# Bloco C (que so tinha HISAT2) - isso mostra quanto a anotacao real ajuda.
set -uo pipefail
cd ~/rnaseq-Anticarsia-GORE3
mkdir -p qc/fase2_blocoA_test

SAMPLES="ID-1 ID-7 ID-8 ID-9 ID-10"
# Reads de entrada: TRIMADOS (Set B, ja gerados no Bloco C), nao os brutos.
TRIMMED_DIR=qc/blocoC_test

# ---------- STAR ----------
# STAR vive no env "rnaseq-tools" (ver build_star_index.sh).
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools

for s in $SAMPLES; do
  # Retomabilidade: se Log.final.out ja existe, o STAR ja completou esta
  # amostra numa execucao anterior (ex. apos queda de conexao/VPN) - pula
  # para nao reprocessar do zero. Log.final.out so e' escrito quando o
  # STAR termina com sucesso, entao ele nunca existe para uma corrida
  # interrompida no meio.
  if [ -f "qc/fase2_blocoA_test/${s}_STAR_Log.final.out" ]; then
    echo "=== STAR - $s: ja concluido, pulando ==="
    continue
  fi
  echo "=== STAR - $s ==="
  # --outSAMtype None: nao escreve o BAM de alinhamento. Nesta etapa so
  # precisamos da taxa de mapeamento (fica em Log.final.out), nao dos
  # proprios alinhamentos - evita gastar tempo/disco com BAMs que serao
  # descartados assim que decidirmos o vencedor.
  # --readFilesCommand zcat: os FASTQ de entrada estao comprimidos (.gz);
  # sem isso o STAR tentaria ler o arquivo binario gzip como texto puro.
  # --twopassMode Basic: primeiro passe descobre juncoes de splice novas
  # (nao anotadas), segundo passe realinha usando essas juncoes recem-
  # descobertas alem das da anotacao. Melhora deteccao de juncao (relevante
  # para o objetivo de splicing alternativo do projeto) a um custo de
  # tempo modesto (roda o alinhamento duas vezes) - decisao tomada aqui
  # porque nenhum documento do projeto tinha fixado este parametro antes.
  STAR \
    --runMode alignReads \
    --runThreadN 8 \
    --genomeDir genome_index_star \
    --readFilesIn ${TRIMMED_DIR}/${s}_setB_1.fastq.gz ${TRIMMED_DIR}/${s}_setB_2.fastq.gz \
    --readFilesCommand zcat \
    --outSAMtype None \
    --twopassMode Basic \
    --outFileNamePrefix qc/fase2_blocoA_test/${s}_STAR_
done

# ---------- HISAT2 (indice anotado) ----------
conda activate ngs

for s in $SAMPLES; do
  # Mesma logica de retomabilidade do loop do STAR acima: o
  # --summary-file so fica completo quando o HISAT2 termina com sucesso.
  if [ -f "qc/fase2_blocoA_test/${s}_HISAT2_annotated.hisat2_summary.txt" ]; then
    echo "=== HISAT2 (anotado) - $s: ja concluido, pulando ==="
    continue
  fi
  echo "=== HISAT2 (anotado) - $s ==="
  # -S /dev/null: mesma logica do STAR --outSAMtype None - descartamos o
  # SAM de alinhamento, so queremos o --summary-file com a taxa de
  # mapeamento, para comparar contra o STAR e contra o piloto sem
  # anotacao do Bloco C.
  # --dta ("downstream transcriptome assembly"): flag recomendada pelo
  # proprio manual do HISAT2 quando o BAM vai alimentar um montador de
  # transcritos ou uma ferramenta de quantificacao por transcrito depois -
  # reporta alinhamentos de forma mais compativel com essas ferramentas.
  hisat2 -p 8 \
    -x genome_index_annotated/ilAntGemm2_annotated \
    -1 ${TRIMMED_DIR}/${s}_setB_1.fastq.gz \
    -2 ${TRIMMED_DIR}/${s}_setB_2.fastq.gz \
    --dta \
    -S /dev/null \
    --summary-file qc/fase2_blocoA_test/${s}_HISAT2_annotated.hisat2_summary.txt \
    2> qc/fase2_blocoA_test/${s}_HISAT2_annotated.log
done

echo FASE2_BLOCOA_ALIGN_DONE_MARKER
