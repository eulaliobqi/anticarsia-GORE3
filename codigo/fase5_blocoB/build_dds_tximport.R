#!/usr/bin/env Rscript
# FASE 5, Bloco B (passo 4) - constroi o DESeqDataSet via tximport, NAO via
# featureCounts bruto.
#
# POR QUE tximport E NAO A TABELA JA EXPORTADA NA FASE 3 (fase3_blocoE_
# salmon_gene_counts.tsv): aquela tabela so tem contagens+TPM - perdeu a
# matriz de comprimento medio de transcrito por amostra que o tximport
# calcula internamente. E' exatamente essa matriz de comprimento que vira
# o "offset" documentado (vinheta do tximport, bioconductor.org/.../
# tximport.html): "Do not manually pass the original gene-level counts to
# downstream methods without an offset... is not recommended by the
# tximport package authors." Por isso este script chama tximport()
# diretamente sobre os quant.sf (indice com --keepDuplicates, FASE 5
# Bloco B passo 1-3), nao reaproveita a tabela ja exportada.
#
# tx2gene.tsv e' o MESMO da FASE 3 (nao muda - so o indice/quant.sf
# mudaram, a relacao transcript_id->gene_id continua a mesma).
suppressMessages(library(tximport))
suppressMessages(library(DESeq2))

SALMON_DIR <- "salmon_keepdup"
TX2GENE <- "genome_annotation/tx2gene.tsv"
SAMPLESHEET <- "resultados/fase3_blocoE_samplesheet.csv"
OUT_RDS <- "resultados_server/fase5_blocoB/dds_raw.rds"

samplesheet <- read.csv(SAMPLESHEET, stringsAsFactors = FALSE)
# ID-18 (FatBody) nao entra no desenho de 4 grupos/3 replicas (ja
# declarado em docs/07_analise_rnaseq.md §13.1) - remover antes de montar
# o colData, nao depois (evitar um nivel de fator "FatBody" com n=1).
samplesheet <- samplesheet[samplesheet$condition != "FatBody", ]

quant_files <- file.path(SALMON_DIR, samplesheet$sample, "quant.sf")
names(quant_files) <- samplesheet$sample
missing <- quant_files[!file.exists(quant_files)]
if (length(missing) > 0) {
  stop("quant.sf ausente para: ", paste(names(missing), collapse = ", "))
}

tx2gene <- read.table(TX2GENE, header = FALSE, sep = "\t", quote = "",
                      col.names = c("transcript_id", "gene_id"))

# type="salmon", tx2gene fornecido -> tximport agrega a nivel de gene E
# calcula a matriz de comprimento medio ponderado por abundancia por
# amostra (o "offset" em si) - e' isso que falta na tabela ja exportada.
txi <- tximport(quant_files, type = "salmon", tx2gene = tx2gene,
                ignoreTxVersion = FALSE, ignoreAfterBar = FALSE)

cat(nrow(txi$counts), "genes x", ncol(txi$counts), "amostras (txi)\n")

# Controle como nivel de referencia - expoe direto em resultsNames() os 3
# coeficientes vs. Controle que a FASE 5 precisa (Benzamidina/SKTI/GORE3),
# sem releveling (confirmado no manual/foruns do DESeq2, ver docs/07 §6).
condition <- factor(samplesheet$condition,
                     levels = c("Control", "Benzamidine", "SKTI", "GORE3"))
colData <- data.frame(row.names = samplesheet$sample, condition = condition)

dds <- DESeqDataSetFromTximport(txi, colData = colData, design = ~condition)

dir.create(dirname(OUT_RDS), showWarnings = FALSE, recursive = TRUE)
saveRDS(dds, OUT_RDS)
cat("Escrito:", OUT_RDS, "\n")
cat("Amostras:", paste(colnames(dds), collapse = ", "), "\n")
cat("Niveis de condition:", paste(levels(dds$condition), collapse = ", "), "\n")

# Exporta txi$counts (contagens brutas, arredondadas p/ inteiro - mesma
# convencao do script reaproveitavel original) para o PyDESeq2 (Bloco C2)
# usar como entrada. IMPORTANTE, declarado explicitamente: o PyDESeq2 NAO
# tem equivalente ao offset de comprimento de transcrito do tximport -
# verificado direto no codigo-fonte (pydeseq2/ds.py) que so existe
# log(size_factors), um escalar por amostra, nao uma matriz gene x
# amostra. Ou seja, a via Python roda sobre as MESMAS contagens de gene
# (Salmon+tximport, cobertura completa) mas SEM a correcao de vies de
# comprimento que a via R aplica via DESeqDataSetFromTximport - assimetria
# real entre os dois motores, declarada aqui e no artigo, nao escondida.
counts_out <- t(round(txi$counts))  # amostras nas linhas, genes nas colunas (convencao do pydeseq2)
write.csv(counts_out, "resultados_server/fase5_blocoB/txi_counts_for_python.csv")
cat("Escrito: resultados_server/fase5_blocoB/txi_counts_for_python.csv\n")
