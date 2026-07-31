#!/usr/bin/env Rscript
# FASE 5, Bloco F - checagem de sensibilidade ID-8, compromisso assumido na
# FASE 4 (commit 3a44b37) quando decidimos NAO aplicar ComBat-seq (ID-8 e'
# lote de amostra unica, LH00688, ComBat_seq.R recusa rodar com 1 amostra
# por lote).
#
# O QUE ESTE SCRIPT TESTA: se o contraste Benzamidina x Controle muda de
# forma relevante ao remover ID-8 (Benzamidine_R3) do desenho - n=3
# (ID-5,7,8, o resultado ja no Bloco D) vs. n=2 (ID-5,7). NAO e' um
# protocolo validado na literatura para este cenario exato (busca na FASE 4
# nao achou nada especifico) - e' uma decisao analitica propria do projeto,
# ja divulgada como tal.
suppressMessages(library(DESeq2))

IN_RDS <- "resultados_server/fase5_blocoB/dds_raw.rds"
OUT_DIR <- "resultados_server/fase5_blocoF"
FULL_SIG <- "resultados_server/fase5_blocoD/deseq2_Benzamidine_vs_Control_sig.csv"

PADJ_CUTOFF <- 0.05
LFC_CUTOFF <- 0.25

dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

dds_full <- readRDS(IN_RDS)

# Subconjunto n=2: remove ID-8 (Benzamidine_R3), mantem so Control (3) +
# Benzamidine sem ID-8 (2) - dropar os niveis SKTI/GORE3 do factor, senao
# DESeq() tenta estimar dispersao para grupos vazios.
keep_samples <- colnames(dds_full)[colnames(dds_full) %in% c("ID-1", "ID-2", "ID-3", "ID-5", "ID-7")]
cat("Amostras no subconjunto n=2 (sem ID-8):", paste(keep_samples, collapse = ", "), "\n")

dds_n2 <- dds_full[, keep_samples]
dds_n2$condition <- droplevels(dds_n2$condition)
cat("Niveis apos droplevels:", paste(levels(dds_n2$condition), collapse = ", "), "\n")

n_before <- nrow(dds_n2)
keep_genes <- rowSums(counts(dds_n2)) >= 10
dds_n2 <- dds_n2[keep_genes, ]
cat(sprintf("Filtro baixa contagem (n=2): %d -> %d genes\n", n_before, nrow(dds_n2)))

dds_n2 <- DESeq(dds_n2)
coef_name <- resultsNames(dds_n2)[grep("Benzamidine", resultsNames(dds_n2))]
cat("Coeficiente usado:", coef_name, "\n")

res_n2 <- lfcShrink(dds_n2, coef = coef_name, type = "apeglm", quiet = TRUE)
res_n2_df <- as.data.frame(res_n2)
res_n2_df$gene_id <- rownames(res_n2_df)

res_n2_df$regulation <- "ns"
up <- !is.na(res_n2_df$padj) & res_n2_df$padj < PADJ_CUTOFF & res_n2_df$log2FoldChange > LFC_CUTOFF
down <- !is.na(res_n2_df$padj) & res_n2_df$padj < PADJ_CUTOFF & res_n2_df$log2FoldChange < -LFC_CUTOFF
res_n2_df$regulation[up] <- "up"
res_n2_df$regulation[down] <- "down"

out_all <- file.path(OUT_DIR, "deseq2_Benzamidine_vs_Control_n2_all.csv")
write.csv(res_n2_df, out_all, row.names = FALSE)
cat(sprintf("Escrito: %s (%d genes)\n", out_all, nrow(res_n2_df)))

# Compara contra o resultado n=3 ja gerado no Bloco D - concordancia de
# direcao do efeito (sinal do log2FC) e sobreposicao dos genes
# significativos, nao so contagem bruta.
sig_n3 <- read.csv(FULL_SIG, stringsAsFactors = FALSE)
sig_n2 <- res_n2_df[res_n2_df$regulation != "ns", ]

cat(sprintf("\nDE significativos: n=3 (com ID-8) = %d | n=2 (sem ID-8) = %d\n",
            nrow(sig_n3), nrow(sig_n2)))

set_n3 <- sig_n3$gene_id
set_n2 <- sig_n2$gene_id
intersect_genes <- intersect(set_n3, set_n2)
union_genes <- union(set_n3, set_n2)
jac <- length(intersect_genes) / length(union_genes)
cat(sprintf("Intersecao: %d | Uniao: %d | Jaccard: %.4f\n",
            length(intersect_genes), length(union_genes), jac))

# Concordancia de direcao nos genes DE em ambos os cenarios.
merged <- merge(
  sig_n3[, c("gene_id", "log2FoldChange")],
  res_n2_df[, c("gene_id", "log2FoldChange")],
  by = "gene_id", suffixes = c("_n3", "_n2")
)
merged_all <- merged[merged$gene_id %in% intersect_genes, ]
concord_dir <- sum(sign(merged_all$log2FoldChange_n3) == sign(merged_all$log2FoldChange_n2))
cat(sprintf("Concordancia de direcao do efeito (genes DE em ambos): %d/%d\n",
            concord_dir, nrow(merged_all)))

summary_out <- data.frame(
  n_sig_n3_com_ID8 = nrow(sig_n3),
  n_sig_n2_sem_ID8 = nrow(sig_n2),
  intersecao = length(intersect_genes),
  uniao = length(union_genes),
  jaccard = jac,
  concordancia_direcao = concord_dir,
  n_avaliado_direcao = nrow(merged_all)
)
write.csv(summary_out, file.path(OUT_DIR, "sensitivity_id8_summary.csv"), row.names = FALSE)
cat("\nEscrito:", file.path(OUT_DIR, "sensitivity_id8_summary.csv"), "\n")
cat("\nBloco F (checagem de sensibilidade ID-8) concluido.\n")
