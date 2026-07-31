#!/usr/bin/env Rscript
# FASE 5, Bloco D1 (R) - extrai os 3 contrastes vs. Controle do modelo ja
# ajustado (Bloco C1, dds_fit.rds) e aplica shrinkage de log2FC.
#
# POR QUE apeglm E NAO shrinkage="normal": Bloco A ja fichou zhu2019heavy
# (PMID 30395178) como a referencia para apeglm - reduz o viesamento de
# LFC de genes de baixa contagem sem inflar erro tipo I, e e' o metodo
# recomendado pela propria vingeta do DESeq2 desde que a fonte seja um
# coeficiente unico (nao contraste generico) - e' exatamente o caso aqui
# (Controle e' a referencia, os 3 coeficientes ja saem prontos de
# resultsNames(), sem precisar relevelar).
#
# LIMIAR log2FC = 0,25: decisao ja registrada em docs/07_analise_rnaseq.md
# §6.2 e no plano da FASE 5 (memoized-questing-whistle.md) - meio da faixa
# 0,1-0,5 discutida em schurch2016many (PMID 27022035) para desenhos com
# poucas replicas biologicas (n=3 aqui).
suppressMessages(library(DESeq2))

IN_RDS <- "resultados_server/fase5_blocoC/dds_fit.rds"
OUT_DIR <- "resultados_server/fase5_blocoD"

PADJ_CUTOFF <- 0.05
LFC_CUTOFF <- 0.25

CONTRASTS <- list(
  c("Benzamidine", "Benzamidine_vs_Control", "condition_Benzamidine_vs_Control"),
  c("SKTI",        "SKTI_vs_Control",        "condition_SKTI_vs_Control"),
  c("GORE3",       "GORE3_vs_Control",       "condition_GORE3_vs_Control")
)

dds <- readRDS(IN_RDS)
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

for (spec in CONTRASTS) {
  tratamento <- spec[1]
  rotulo <- spec[2]
  coef_name <- spec[3]

  cat(sprintf("\n=== %s ===\n", rotulo))

  # results() com o contraste explicito primeiro - confirma o numero de
  # genes testados e serve de checagem cruzada contra o lfcShrink (mesmo
  # baseMean/pvalue, so o log2FoldChange muda apos o shrink).
  res_raw <- results(dds, contrast = c("condition", tratamento, "Control"),
                      alpha = PADJ_CUTOFF)
  cat(sprintf("results() bruto: %d genes testados\n", sum(!is.na(res_raw$padj))))

  # coef= direto (nao contrast=) - apeglm exige um unico coeficiente do
  # modelo, ja exposto em resultsNames(dds) porque Controle e' a
  # referencia (sem releveling necessario, confirmado no Bloco C1).
  res <- lfcShrink(dds, coef = coef_name, type = "apeglm", quiet = TRUE)

  res_df <- as.data.frame(res)
  res_df$gene_id <- rownames(res_df)
  res_df <- res_df[, c("gene_id", setdiff(colnames(res_df), "gene_id"))]
  res_df <- res_df[order(res_df$padj, -abs(res_df$log2FoldChange)), ]

  res_df$regulation <- "ns"
  up <- !is.na(res_df$padj) & res_df$padj < PADJ_CUTOFF & res_df$log2FoldChange > LFC_CUTOFF
  down <- !is.na(res_df$padj) & res_df$padj < PADJ_CUTOFF & res_df$log2FoldChange < -LFC_CUTOFF
  res_df$regulation[up] <- "up"
  res_df$regulation[down] <- "down"

  res_sig <- res_df[res_df$regulation != "ns", ]

  out_all <- file.path(OUT_DIR, sprintf("deseq2_%s_all.csv", rotulo))
  out_sig <- file.path(OUT_DIR, sprintf("deseq2_%s_sig.csv", rotulo))
  write.csv(res_df, out_all, row.names = FALSE)
  write.csv(res_sig, out_sig, row.names = FALSE)

  cat(sprintf("Escrito: %s (%d genes)\n", out_all, nrow(res_df)))
  cat(sprintf("Escrito: %s (%d DE: %d up / %d down)\n", out_sig, nrow(res_sig),
              sum(res_sig$regulation == "up"), sum(res_sig$regulation == "down")))
}

cat("\nBloco D1 (R/DESeq2) concluido para os 3 contrastes.\n")
