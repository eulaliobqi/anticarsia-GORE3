#!/bin/bash
# FASE 2, Bloco A - construir o indice STAR do genoma anotado.
#
# CONTEXTO: STAR (Dobin et al. 2013, PMID 23104886) e' um dos dois
# alinhadores splice-aware candidatos para a via de expressao genica
# (o outro e' HISAT2, ver build_hisat2_index_annotated.sh). O "padrao
# ouro" do projeto (docs/03_metodologia_padrao_ouro.md) aceita qualquer
# um dos dois; este Bloco A testa ambos numa subamostra pequena para
# decidir com dado real, nao por preferencia a priori.
#
# STAR esta instalado no env "rnaseq-tools" (nao no "ngs", onde vivem
# fastp/HISAT2/featureCounts) - confirmado por checagem direta no
# servidor antes de escrever este script.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

GTF=genome_annotation/GCF_050436995.1_RS_2026_04.gtf
FASTA=$(cat genome_annotation/genome_fasta_path.txt)

mkdir -p genome_index_star

# Explicacao de cada flag nao-obvia:
#
# --sjdbGTFfile <gtf>
#     Passa a anotacao para o STAR construir a "sjdb" (splice junction
#     database) - a lista de juncoes exon-exon conhecidas. Sem isso, o
#     STAR ainda alinha, mas so descobre juncoes de novo durante o
#     alinhamento, com menos sensibilidade/precisao. Como o objetivo do
#     projeto inclui expressao por isoforma e splicing alternativo, usar
#     a anotacao real (RS_2026_04) e' importante.
#
# --sjdbOverhang 150
#     Controla o tamanho da sequencia de cada lado de uma juncao que o
#     STAR usa para construir os "splice junction reads" indexados.
#     Regra pratica recomendada pelo proprio manual do STAR:
#     comprimento_da_leitura - 1. As leituras deste projeto tem 151 nt
#     (confirmado no relatorio da Macrogen e no FASE 1 §0 do artigo),
#     entao 151 - 1 = 150. Esse parametro nunca tinha sido decidido em
#     nenhum documento do projeto antes deste script.
#
# --genomeSAindexNbases 13
#     O STAR recomenda reduzir esse valor (padrao 14) para genomas
#     menores que o humano, pela formula min(14, log2(tamanho_genoma)/2 - 1).
#     Este genoma (~397 Mb, GCF_050436995.1) da log2(397e6)/2 - 1 ~= 13.3,
#     entao usamos 13 (arredondado para baixo). Um valor errado aqui nao
#     quebra o alinhamento, mas desperdica memoria/tempo de indexacao.
#
# --runThreadN 16
#     Servidor tem 32 nucleos / 188 GB RAM (confirmado via `nproc`/`free -h`
#     antes deste script) - 16 threads deixa metade da maquina livre para
#     outros processos (ex. o HISAT2 anotado pode rodar em paralelo).
STAR \
  --runMode genomeGenerate \
  --runThreadN 16 \
  --genomeDir genome_index_star \
  --genomeFastaFiles "$FASTA" \
  --sjdbGTFfile "$GTF" \
  --sjdbOverhang 150 \
  --genomeSAindexNbases 13

echo STAR_INDEX_DONE_MARKER
