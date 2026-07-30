#!/bin/bash
# FASE 2, Bloco B - alinhamento COMPLETO das 13 bibliotecas trimadas (FASE 1,
# Bloco B: trimmed/ID-X_{1,2}.trimmed.fastq.gz) com o vencedor do Bloco A.
#
# DECISAO DO BLOCO A (resultados/fase2_blocoA_star_vs_hisat2.csv): STAR
# venceu HISAT2 em todas as 5 amostras testadas por 9-13 pontos percentuais
# de taxa de mapeamento (83-91% STAR vs. 74-79% HISAT2, indice anotado nos
# dois casos) - diferenca >= 2pp, entao o criterio de decisao combinado com
# o usuario manda rodar SO o vencedor (STAR) nas 13 bibliotecas completas,
# em vez dos dois.
#
# DIFERENCA em relacao ao teste do Bloco A: aqui SIM escrevemos o BAM
# (--outSAMtype BAM SortedByCoordinate), porque o resultado desta etapa e'
# um entregavel real (input do Bloco C/featureCounts, que sera planejado
# depois) - no Bloco A so queriamos a taxa de mapeamento (--outSAMtype None),
# aqui precisamos dos alinhamentos de verdade.
# NAO usamos "set -e" aqui de proposito: numa corrida de varias horas
# processando 13 amostras, um crash transitorio (ex. concorrencia de
# memoria/CPU com outro processo pesado rodando ao mesmo tempo no
# servidor - foi exatamente o que aconteceu na primeira tentativa: 5 das
# 13 amostras deram "Falha de segmentacao"/"Instrucao ilegal" no STAR
# porque este script e o run_subread_align_full.sh foram lancados juntos,
# cada um pedindo 16 threads, e a concorrencia derrubou o STAR bem no
# inicio de varias amostras) nao deveria interromper o processamento das
# amostras seguintes, que podem rodar bem assim que a concorrencia passar.
# Em vez disso, cada amostra e' verificada explicitamente apos o STAR
# rodar (bloco "if [ ! -f Log.final.out ]" abaixo) - se falhou, a amostra
# e' pulada com uma mensagem de erro clara, sem mover um BAM corrompido
# para bam/star/ (o que aconteceu na tentativa anterior, ja que so tinhamos
# "set -uo pipefail", que NAO para o script quando um comando simples como
# STAR retorna erro - so protege contra variavel nao-definida e pipe
# quebrado).
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

mkdir -p qc/fase2_blocoB_star bam/star

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16 ID-18"

for s in $SAMPLES; do
  # Retomabilidade (mesma logica do Bloco A): o STAR so escreve
  # Log.final.out quando termina com sucesso, e o BAM sorted so fica
  # completo (arquivo .bam final, nao um .tmp) quando o processo termina -
  # como as bibliotecas completas demoram muito mais que a subamostra
  # (40-80 milhoes de pares vs. 2 milhoes), interrupcoes por queda de
  # VPN/rede sao um risco real que ja vimos acontecer no Bloco A.
  if [ -f "qc/fase2_blocoB_star/${s}_Log.final.out" ]; then
    echo "=== STAR - $s: ja concluido, pulando ==="
    continue
  fi
  echo "=== STAR (biblioteca completa) - $s - $(date) ==="
  # --outSAMtype BAM SortedByCoordinate: pede ao STAR para ja entregar o
  # BAM ordenado por posicao (equivalente a rodar samtools sort depois) -
  # evita um passo extra e um arquivo intermediario grande (SAM nao
  # comprimido) no disco.
  # --runThreadN 16: metade dos 32 nucleos do servidor por amostra, para
  # deixar espaco para o Subread (via de splicing, run_subread_align_full.sh)
  # rodar ao mesmo tempo se o usuario decidir paralelizar as duas vias.
  STAR \
    --runMode alignReads \
    --runThreadN 16 \
    --genomeDir genome_index_star \
    --readFilesIn trimmed/${s}_1.trimmed.fastq.gz trimmed/${s}_2.trimmed.fastq.gz \
    --readFilesCommand zcat \
    --outSAMtype BAM SortedByCoordinate \
    --twopassMode Basic \
    --outFileNamePrefix qc/fase2_blocoB_star/${s}_

  # CHECAGEM EXPLICITA (adicionada apos o incidente descrito no topo do
  # script): Log.final.out so existe se o STAR terminou com sucesso. Se
  # nao existir, o STAR crashou/foi morto no meio - NAO movemos nem
  # indexamos nada (evita repetir o erro de mover um BAM de 0 bytes/
  # corrompido para bam/star/, que so seria descoberto tarde, na hora do
  # samtools index ou pior, na hora da analise). A amostra fica pendente
  # e sera reprocessada da proxima vez que este script rodar, gracas a
  # checagem de retomabilidade no topo do loop.
  if [ ! -f "qc/fase2_blocoB_star/${s}_Log.final.out" ]; then
    echo "!!! ERRO: STAR nao completou $s com sucesso (Log.final.out ausente) - pulando, NAO movendo BAM"
    rm -f "qc/fase2_blocoB_star/${s}_Aligned.sortedByCoord.out.bam"
    continue
  fi

  # STAR grava o BAM como "${prefix}Aligned.sortedByCoord.out.bam" - movemos
  # para uma pasta dedicada (bam/star/) com nome mais simples, para os
  # proximos scripts (checagem de strandedness, futuro Bloco C) nao
  # precisarem lidar com esse sufixo longo.
  mv qc/fase2_blocoB_star/${s}_Aligned.sortedByCoord.out.bam bam/star/${s}.bam

  # samtools index: cria o arquivo .bai necessario para qualquer ferramenta
  # que acesse regioes especificas do BAM (ex. IGV, featureCounts em alguns
  # modos, RSeQC) em vez de ler o arquivo inteiro sequencialmente.
  samtools index bam/star/${s}.bam
done

echo FASE2_BLOCOB_STAR_DONE_MARKER
