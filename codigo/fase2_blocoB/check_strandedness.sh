#!/bin/bash
# FASE 2, Bloco B - confirmar EMPIRICAMENTE o sentido (forward/reverse) da
# biblioteca stranded, usando os BAMs do STAR ja alinhados.
#
# CONTEXTO (docs/07_analise_rnaseq.md secao 0/13): o relatorio da Macrogen
# so confirma QUE a biblioteca e' stranded (kit "Illumina Stranded mRNA
# Prep, Ligation"), nao qual sentido (a maioria dos kits Illumina
# "stranded" e' reverse-stranded, mas isso e' uma expectativa, nao uma
# confirmacao lida no relatorio) - por isso o ponto de partida do projeto
# ("-s 2" no featureCounts/Subread) precisa ser CONFIRMADO com dado real
# antes de ser usado em producao (na futura quantificacao gênica, ainda
# nao planejada - Bloco C).
#
# COMO TESTAMOS: em vez de instalar RSeQC (que exigiria converter o GTF
# para BED12 com uma ferramenta que nao estava disponivel no servidor),
# usamos o proprio featureCounts (ja instalado, env "ngs") para rodar a
# MESMA contagem de genes duas vezes no mesmo BAM - uma assumindo "-s 1"
# (forward-stranded), outra assumindo "-s 2" (reverse-stranded). A
# configuracao CORRETA e' a que atribui a fracao muito maior de reads a
# genes (a errada atribui a maioria como "Unassigned_NoFeature", porque
# esta' testando o sentido oposto ao real da biblioteca).
#
# Amostras escolhidas: ID-1 (controle limpo) e ID-8 (pior amostra do lote
# em qualidade, FASE 1) - se o sentido correto for consistente nas duas,
# nao depende da amostra ter qualidade boa ou ruim.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3

mkdir -p qc/fase2_blocoB_strandcheck

# GTF CORRIGIDO (FASE 3 Bloco A, fix_gtf_missing_geneid.sh): o GTF original
# tinha 330 linhas (118 genes "LOC" nao-caracterizados, sem mRNA no GFF3
# original) sem o atributo gene_id, o que faz featureCounts recusar o
# arquivo inteiro ("failed to find the gene identifier attribute").
GTF=genome_annotation/GCF_050436995.1_RS_2026_04.fixed.gtf
SAMPLES="ID-1 ID-8"

for s in $SAMPLES; do
  for strand in 1 2; do
    echo "=== featureCounts - $s - teste -s $strand ==="
    # -p: dados pareados (paired-end) - sem isso featureCounts trataria
    # cada mate como uma leitura independente, inflando/distorcendo a
    # contagem.
    # -g gene_id -t exon: agrupa por gene (soma todos os exons do mesmo
    # gene_id), o nivel de contagem padrao para expressao genica (nao
    # por transcrito/isoforma).
    featureCounts \
      -T 8 \
      -p \
      -s $strand \
      -a "$GTF" \
      -g gene_id \
      -t exon \
      -o qc/fase2_blocoB_strandcheck/${s}_s${strand}.txt \
      bam/star/${s}.bam \
      > qc/fase2_blocoB_strandcheck/${s}_s${strand}.log 2>&1
  done
done

echo FASE2_BLOCOB_STRANDCHECK_DONE_MARKER
