#!/usr/bin/env Rscript
# FASE 7, Bloco I (R) - comparacao GO entre os 3 tratamentos com
# clusterProfiler::compareCluster() + enrichplot::dotplot() (a figura
# moderna padrao para "biological theme comparison" entre grupos,
# yu2012clusterprofiler) + cnetplot (rede gene-conceito) por contraste.
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(ggplot2)
})

GO_MAP <- "resultados_server/fase7_blocoF/gene_to_go_consolidated.csv"
D_DIR <- "resultados_server/fase5_blocoD"
OUT_DIR <- "resultados_server/fase7_blocoI"
PVALUE_CUTOFF <- 0.05

dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

go_map <- read.csv(GO_MAP, stringsAsFactors = FALSE)
term2gene <- go_map[, c("go_id", "gene_id")]
go_names <- read.csv("resultados_server/fase7_blocoF/go_term_names.csv", stringsAsFactors = FALSE)
term2name <- data.frame(go_id = go_names$GOID, name = go_names$TERM)

CONTRASTS <- c("Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control")
LABELS <- c("Benzamidine", "SKTI", "GORE3")

gene_clusters <- list()
universe <- NULL
for (i in seq_along(CONTRASTS)) {
  sig <- read.csv(file.path(D_DIR, sprintf("deseq2_%s_sig.csv", CONTRASTS[i])))
  gene_clusters[[LABELS[i]]] <- sig$gene_id
  if (is.null(universe)) {
    universe <- read.csv(file.path(D_DIR, sprintf("deseq2_%s_all.csv", CONTRASTS[i])))$gene_id
  }
}
cat(sprintf("Genes DE por grupo: %s\n", paste(sprintf("%s=%d", names(gene_clusters), lengths(gene_clusters)), collapse = ", ")))

# --- compareCluster (GO), mesmo universo/TERM2GENE dos 3 contrastes ---
ck <- compareCluster(
  geneCluster = gene_clusters, fun = "enricher",
  universe = universe, TERM2GENE = term2gene, TERM2NAME = term2name,
  pvalueCutoff = PVALUE_CUTOFF, qvalueCutoff = 1, pAdjustMethod = "BH"
)
ck_df <- as.data.frame(ck)
write.csv(ck_df, file.path(OUT_DIR, "compareCluster_GO_results.csv"), row.names = FALSE)
cat(sprintf("compareCluster: %d linhas (grupo x termo) escritas\n", nrow(ck_df)))

# --- Figura: dotplot comparativo (top 15 termos por grupo) ---
p_dot <- dotplot(ck, showCategory = 15) +
  theme(axis.text.y = element_text(size = 7)) +
  ggtitle("Comparacao GO entre tratamentos (compareCluster, top 15/grupo)")
ggsave(file.path(OUT_DIR, "fig_compareCluster_dotplot.pdf"), p_dot, width = 10, height = 11)
ggsave(file.path(OUT_DIR, "fig_compareCluster_dotplot.png"), p_dot, width = 10, height = 11, dpi = 300)
cat("Escrito: fig_compareCluster_dotplot.*\n")

# --- cnetplot por contraste (rede gene-conceito, top 10 termos) ---
for (i in seq_along(CONTRASTS)) {
  rotulo <- CONTRASTS[i]
  ego <- tryCatch(
    enricher(gene = gene_clusters[[LABELS[i]]], universe = universe,
             TERM2GENE = term2gene, TERM2NAME = term2name,
             pvalueCutoff = PVALUE_CUTOFF, qvalueCutoff = 1, pAdjustMethod = "BH"),
    error = function(e) NULL
  )
  if (is.null(ego) || nrow(as.data.frame(ego)) == 0) next
  p_cnet <- cnetplot(ego, showCategory = 10, node_label = "category") +
    ggtitle(sprintf("Rede gene-conceito - %s (top 10 termos GO)", LABELS[i]))
  ggsave(file.path(OUT_DIR, sprintf("fig_cnetplot_%s.pdf", rotulo)), p_cnet, width = 10, height = 9)
  ggsave(file.path(OUT_DIR, sprintf("fig_cnetplot_%s.png", rotulo)), p_cnet, width = 10, height = 9, dpi = 300)
  cat(sprintf("Escrito: fig_cnetplot_%s.*\n", rotulo))
}

# --- Riqueza/diversidade funcional por contraste ---
richness <- data.frame(
  grupo = LABELS,
  n_genes_DE = lengths(gene_clusters),
  n_termos_GO_significativos = sapply(LABELS, function(l) sum(ck_df$Cluster == l))
)
write.csv(richness, file.path(OUT_DIR, "functional_richness_summary.csv"), row.names = FALSE)
cat("\nRiqueza funcional por grupo:\n")
print(richness)

cat("\nBloco I (R: compareCluster, dotplot, cnetplot, riqueza) concluido.\n")
