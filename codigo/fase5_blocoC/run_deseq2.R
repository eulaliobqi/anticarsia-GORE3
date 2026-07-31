#!/usr/bin/env Rscript
# FASE 5, Bloco C1 (R) - roda o modelo DESeq2 sobre o DESeqDataSet
# construido via tximport (Bloco B). Adaptado de
# RNA-Seq-not-model/scripts/01_deseq2.R, generalizado de um par binario
# control/treatment para os 4 niveis deste desenho (docs/07_analise_
# rnaseq.md §6.1 ja pedia essa generalizacao).
#
# Defaults confirmados no manual de referencia do DESeq2 (nao supostos):
# DESeq() usa test="Wald", fitType="parametric", betaPrior=FALSE (default
# desde a v1.16) - por isso lfcShrink() roda depois, separado, como no
# script original.
suppressMessages(library(DESeq2))

IN_RDS <- "resultados_server/fase5_blocoB/dds_raw.rds"
OUT_RDS <- "resultados_server/fase5_blocoC/dds_fit.rds"

dds <- readRDS(IN_RDS)

# Filtro de baixa contagem: rowSums(counts) >= 10 - mesmo do script
# reaproveitavel original, e' a recomendacao padrao da propria vinheta do
# DESeq2 (nao achamos artigo dedicado so para esse limiar - declarado como
# tal, nao como citacao de paper).
n_before <- nrow(dds)
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep, ]
cat(sprintf("Filtro baixa contagem: %d -> %d genes (rowSums >= 10)\n", n_before, nrow(dds)))

dds <- DESeq(dds)

cat("resultsNames(dds):\n")
print(resultsNames(dds))

# Confirmacao explicita de que os 3 coeficientes esperados (vs. Controle,
# a referencia) existem antes de qualquer extracao de contraste - nao
# assumir, checar.
expected <- c("condition_Benzamidine_vs_Control",
              "condition_SKTI_vs_Control",
              "condition_GORE3_vs_Control")
missing_coef <- setdiff(expected, resultsNames(dds))
if (length(missing_coef) > 0) {
  stop("Coeficientes esperados ausentes em resultsNames(dds): ",
       paste(missing_coef, collapse = ", "))
}
cat("OK: os 3 coeficientes esperados estao presentes.\n")

dir.create(dirname(OUT_RDS), showWarnings = FALSE, recursive = TRUE)
saveRDS(dds, OUT_RDS)
cat("Escrito:", OUT_RDS, "\n")
