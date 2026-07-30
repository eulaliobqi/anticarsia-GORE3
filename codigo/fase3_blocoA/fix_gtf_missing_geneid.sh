#!/bin/bash
# FASE 3, Bloco A - passo 0: corrigir um defeito real na conversao GFF3->GTF
# da FASE 2 (Bloco A, convert_gff_to_gtf.sh) descoberto ao rodar o teste de
# strandedness: featureCounts recusa o GTF inteiro com
#   "ERROR: failed to find the gene identifier attribute in the 9th column"
# porque 330 das 515.035 linhas (todas do tipo "exon", cobrindo 118 genes)
# nao tem o atributo gene_id.
#
# CAUSA RAIZ (confirmada, nao suposta): esses 118 genes sao todos loci
# nao-caracterizados (nome "LOC..."), sem registro de mRNA no GFF3 original
# da RefSeq (RS_2026_04) - so "gene" + "exon" direto, sem transcrito
# intermediario. O gffread (usado na FASE 2 Bloco A) so preenche gene_id
# quando ha' uma hierarquia gene->mRNA->exon explicita; sem o mRNA, ele usa
# o ID do proprio gene como transcript_id e nao duplica esse valor em
# gene_id. Confirmado 100% consistente nas 330 linhas: o valor de
# transcript_id (ex. "gene-LOC142972336") e' EXATAMENTE o que gene_id
# deveria ser (mesmo padrao "gene-<nome>" das linhas normais, ex.
# transcript_id "rna-XM_..."; gene_id "gene-Xpac"). Ou seja, para esses 118
# genes, transcrito e gene sao a mesma entidade (sem isoforma) - a correcao
# abaixo so torna isso explicito, nao inventa nenhum dado novo.
#
# Nenhum dos 118 genes afetados e' uma tripsina/serino-protease conhecida
# (todos sao "LOC" sem nome/produto caracterizado) - achado verificado
# antes de decidir que a correcao e' segura para os genes de interesse
# central do projeto (contrastes GORE3 x Controle/Benzamidina/SKTI).
#
# Este script GERA um GTF corrigido separado (nao sobrescreve o original -
# a FASE 2/STAR ja rodou com o original e nao precisa ser refeita, ja que
# STAR so usa a hierarquia exon/transcript para guiar splice sites, nao
# gene_id). A partir daqui, featureCounts (Bloco C), extracao de
# transcriptoma para o Salmon (Bloco D) e tximport (Bloco E) devem
# apontar para o GTF CORRIGIDO, nao o original.
set -uo pipefail
cd ~/rnaseq-Anticarsia-GORE3/genome_annotation

IN=GCF_050436995.1_RS_2026_04.gtf
OUT=GCF_050436995.1_RS_2026_04.fixed.gtf

# Para toda linha que tem transcript_id mas NAO tem gene_id: insere
# gene_id "<mesmo valor de transcript_id>"; logo depois do transcript_id -
# mesma posicao/ordem de atributo das linhas normais (transcript_id;
# gene_id; gene_name;).
awk '
  /gene_id/ { print; next }
  {
    if (match($0, /transcript_id "[^"]+"/)) {
      tid_full = substr($0, RSTART, RLENGTH)
      # extrai só o valor entre aspas
      split(tid_full, a, "\"")
      tid_val = a[2]
      sub(/transcript_id "[^"]+";/, "transcript_id \"" tid_val "\"; gene_id \"" tid_val "\";")
    }
    print
  }
' "$IN" > "$OUT"

echo "Linhas totais: $(wc -l < "$OUT")"
echo "Linhas AINDA sem gene_id (deve ser 0):"
grep -vc 'gene_id' "$OUT" || true
echo "Linhas antes vs depois (deve ser igual - so adicionamos atributo, nao linha):"
wc -l "$IN" "$OUT"

echo GTF_GENEID_FIX_DONE_MARKER
