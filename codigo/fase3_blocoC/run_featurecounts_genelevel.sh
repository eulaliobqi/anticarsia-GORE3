#!/bin/bash
# FASE 3, Bloco C - quantificacao de PRODUCAO em nivel de GENE: featureCounts
# sobre os 13 BAMs do STAR (via de expressao genica da FASE 2), usando o GTF
# real (corrigido - ver fase3_blocoA/fix_gtf_missing_geneid.sh) e o strand
# confirmado empiricamente (fase3_blocoA/decide_libtype.py -> -s 2).
#
# Este e' o bloco PRIORITARIO da FASE 3 - alimenta diretamente o DESeq2
# (FASE 5) e os contrastes GORE3 x Controle/Benzamidina/SKTI, que sao o
# resultado central do projeto (nao a via de transcrito/Salmon do Bloco D,
# que e' so apoio a H1/tripsinas).
#
# DECISAO DELIBERADA: NAO usar -M -O --fraction (resgate de reads
# multi-mapeados/multi-sobrepostos). Zytnicki 2017 (PMID 28915787,
# "mmquant: how to count multi-mapping reads?") declara textualmente que
# habilitar essas flags "quase sempre produz resultados enviesados" -
# NAO adicionar essas flags aqui achando que "melhora" a contagem. Isso
# cria uma tensao real e conhecida para os genes de tripsina (familia
# multigenica, parte da hipotese secundaria H1) - reads ambiguos entre
# paralogos proximos serao descartados por padrao. Essa tensao e'
# declarada explicitamente em docs/07_analise_rnaseq.md e artigo.md, nao
# resolvida aqui - fica para revisitar na FASE 9 (curadoria da familia de
# serino-proteases), especificamente para esses poucos genes, se
# necessario. Para o objetivo PRINCIPAL desta fase (contrastes de grupo
# inteiros), o comportamento padrao do featureCounts e' o correto.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ngs
cd ~/rnaseq-Anticarsia-GORE3

GTF=genome_annotation/GCF_050436995.1_RS_2026_04.fixed.gtf
STRAND=$(awk -F',' 'NR==2{print $1}' resultados/fase3_blocoA_strand_decision.csv)

mkdir -p resultados_server/fase3_blocoC

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16 ID-18"
BAMS=""
for s in $SAMPLES; do
  BAMS="$BAMS bam/star/${s}.bam"
done

# -T 8 (nao 16): deixa margem de threads no servidor compartilhado - a FASE
# 2 ja teve falha de segmentacao duas vezes por concorrencia de jobs de 16
# threads rodando juntos (STAR + Subread). Nao rodar este script junto com
# o build do indice Salmon (fase3_blocoD/build_salmon_decoy_index.sh).
# -p: dados pareados. -g gene_id -t exon: contagem por gene, nivel padrao
# para expressao genica (nao por transcrito/isoforma - isso e' o Bloco D).
featureCounts \
  -T 8 \
  -p \
  -s "$STRAND" \
  -a "$GTF" \
  -g gene_id \
  -t exon \
  -o resultados_server/fase3_blocoC/gene_counts.txt \
  $BAMS \
  > resultados_server/fase3_blocoC/featurecounts.log 2>&1

echo "Strand usado: -s $STRAND"
echo FASE3_BLOCOC_FEATURECOUNTS_DONE_MARKER
