#!/usr/bin/env Rscript
# FASE 5, Bloco G (R) - figuras padrao ouro + moderno (PCA, dispersao,
# volcano, MA, heatmap). Paleta categorica validada via skill `dataviz`
# deste ambiente (script scripts/validate_palette.js, --pairs all, 4
# categorias): Control=azul #2a78d6, Benzamidine=laranja #eb6834,
# SKTI=aqua #1baf7a, GORE3=violeta #4a3aa7 - ordem escolhida porque o
# 4o slot padrao da paleta (amarelo) falha o piso de visao normal contra o
# laranja (slot 2) sob --pairs all (documentado no proprio references/
# palette.md da skill); violeta (slot 7) passa todos os checks nessa
# combinacao de 4 (ver validacao rodada nesta sessao).
suppressMessages({
  library(DESeq2)
  library(ggplot2)
  library(ggrepel)
  library(pheatmap)
  library(RColorBrewer)
  library(EnhancedVolcano)
})

DDS_FIT <- "resultados_server/fase5_blocoC/dds_fit.rds"
D_DIR <- "resultados_server/fase5_blocoD"
OUT_DIR <- "resultados_server/fase5_blocoG"
LFC_CUTOFF <- 0.25
PADJ_CUTOFF <- 0.05

PAL <- c(Control = "#2a78d6", Benzamidine = "#eb6834", SKTI = "#1baf7a", GORE3 = "#4a3aa7")

dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

dds <- readRDS(DDS_FIT)
vsd <- vst(dds, blind = FALSE)

# ── PCA ──────────────────────────────────────────────────────────
# ID-8 (Benzamidine_R3) e' o unico membro do lote separado (LH00688,
# ver FASE 4/artigo.md) - marcado com contorno preto na PCA, nao cor
# separada (a cor continua codificando so `condition`, por decisao
# de acessibilidade: nao misturar 2 variaveis categoricas na mesma
# escala de cor).
pca_data <- plotPCA(vsd, intgroup = "condition", returnData = TRUE)
pca_var <- round(100 * attr(pca_data, "percentVar"))
pca_data$is_id8 <- rownames(pca_data) == "ID-8"

p_pca <- ggplot(pca_data, aes(PC1, PC2, color = condition)) +
  geom_point(aes(size = is_id8, stroke = ifelse(is_id8, 1.4, 0)),
             shape = 21, fill = NA) +
  geom_point(size = 3.2, alpha = 0.9) +
  geom_text_repel(aes(label = rownames(pca_data)), size = 3, max.overlaps = 20,
                   show.legend = FALSE) +
  scale_color_manual(values = PAL, name = "Grupo") +
  scale_size_manual(values = c(`TRUE` = 5.5, `FALSE` = 0), guide = "none") +
  labs(title = "PCA - Anticarsia gemmatalis (VST, blind=FALSE)",
       subtitle = "Contorno preto = ID-8 (lote unico, LH00688)",
       x = sprintf("PC1 (%d%%)", pca_var[1]),
       y = sprintf("PC2 (%d%%)", pca_var[2])) +
  theme_bw(base_size = 12) +
  theme(panel.grid.minor = element_blank(), plot.title = element_text(face = "bold"))
ggsave(file.path(OUT_DIR, "fig_pca.pdf"), p_pca, width = 7.5, height = 6)
ggsave(file.path(OUT_DIR, "fig_pca.png"), p_pca, width = 7.5, height = 6, dpi = 300)

# Exporta a matriz VST normalizada + metadados para o Bloco G (Python)
# calcular UMAP sobre os MESMOS dados da PCA (nao uma matriz recomputada
# a parte) - garante que os dois pontos de vista (linear/nao-linear)
# descrevem exatamente a mesma heterogeneidade amostral.
vst_mat <- assay(vsd)
write.csv(as.data.frame(vst_mat), file.path(OUT_DIR, "vst_normalized_matrix.csv"))
write.csv(data.frame(sample = colnames(vsd), condition = as.character(vsd$condition),
                      is_id8 = colnames(vsd) == "ID-8"),
          file.path(OUT_DIR, "sample_metadata.csv"), row.names = FALSE)
cat("Escrito: vst_normalized_matrix.csv + sample_metadata.csv (para UMAP em Python)\n")

# ── Diagnostico de dispersao (plotDispEsts) ─────────────────────
pdf(file.path(OUT_DIR, "fig_dispersion_estimates.pdf"), width = 7, height = 6)
plotDispEsts(dds, main = "Estimativas de dispersao - DESeq2")
dev.off()
cat("Escrito: fig_dispersion_estimates.pdf\n")

# ── Volcano + MA por contraste ───────────────────────────────────
CONTRASTS <- c("Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control")

for (rotulo in CONTRASTS) {
  res_df <- read.csv(file.path(D_DIR, sprintf("deseq2_%s_all.csv", rotulo)))

  p_vol <- EnhancedVolcano(res_df,
    lab = res_df$gene_id, x = "log2FoldChange", y = "padj",
    pCutoff = PADJ_CUTOFF, FCcutoff = LFC_CUTOFF,
    pointSize = 1.3, labSize = 0, # sem rotulo de gene individual (15.7k LOC ids, ilegivel)
    title = sub("_", " ", rotulo), subtitle = "DESeq2 (log2FC encolhido, apeglm)",
    col = c("#c3c2b7", "#1baf7a", "#2a78d6", "#e34948"),
    colAlpha = 0.6, legendPosition = "bottom", drawConnectors = FALSE
  )
  ggsave(file.path(OUT_DIR, sprintf("fig_volcano_%s.pdf", rotulo)), p_vol, width = 8, height = 7)
  ggsave(file.path(OUT_DIR, sprintf("fig_volcano_%s.png", rotulo)), p_vol, width = 8, height = 7, dpi = 300)

  p_ma <- ggplot(res_df[!is.na(res_df$padj), ],
                 aes(log10(baseMean + 1), log2FoldChange, color = regulation)) +
    geom_point(alpha = 0.35, size = 0.8) +
    geom_hline(yintercept = c(-LFC_CUTOFF, LFC_CUTOFF), linetype = "dashed", color = "#52514e") +
    geom_hline(yintercept = 0, color = "#0b0b0b") +
    scale_color_manual(values = c(up = "#eb6834", down = "#2a78d6", ns = "#c3c2b7"),
                        name = sprintf("FDR<%.2f, |LFC|>%.2f", PADJ_CUTOFF, LFC_CUTOFF)) +
    labs(title = sprintf("MA plot - %s", sub("_", " ", rotulo)),
         x = "log10(baseMean + 1)", y = "log2 Fold Change (apeglm)") +
    theme_bw(base_size = 12) + theme(panel.grid.minor = element_blank())
  ggsave(file.path(OUT_DIR, sprintf("fig_ma_%s.pdf", rotulo)), p_ma, width = 7.5, height = 6)
  ggsave(file.path(OUT_DIR, sprintf("fig_ma_%s.png", rotulo)), p_ma, width = 7.5, height = 6, dpi = 300)

  cat(sprintf("Escrito: fig_volcano_%s.* + fig_ma_%s.*\n", rotulo, rotulo))
}

# ── Heatmap anotado (uniao dos top DE de cada contraste) ─────────
top_n_per_contrast <- 30
top_genes <- c()
for (rotulo in CONTRASTS) {
  sig <- read.csv(file.path(D_DIR, sprintf("deseq2_%s_sig.csv", rotulo)))
  sig <- sig[order(sig$padj), ]
  top_genes <- union(top_genes, head(sig$gene_id, top_n_per_contrast))
}
cat(sprintf("Heatmap: uniao de top %d por contraste = %d genes unicos\n",
            top_n_per_contrast, length(top_genes)))

mat_h <- vst_mat[intersect(top_genes, rownames(vst_mat)), , drop = FALSE]
mat_h <- t(scale(t(mat_h)))  # z-score por gene

annot_col <- data.frame(
  Grupo = as.character(vsd$condition),
  Lote = ifelse(colnames(vsd) == "ID-8", "LH00688 (unico)", "LH00129"),
  row.names = colnames(vsd)
)
annot_colors <- list(
  Grupo = PAL,
  Lote = c(`LH00688 (unico)` = "#e34948", `LH00129` = "#c3c2b7")
)

pheatmap(mat_h,
  annotation_col = annot_col, annotation_colors = annot_colors,
  show_rownames = nrow(mat_h) <= 60, fontsize_row = 6, fontsize_col = 9,
  clustering_method = "ward.D2",
  color = colorRampPalette(c("#2a78d6", "#fcfcfb", "#eb6834"))(100),
  border_color = NA,
  main = sprintf("Heatmap - uniao top %d DE/contraste (z-score VST)", top_n_per_contrast),
  filename = file.path(OUT_DIR, "fig_heatmap_top_de.pdf"), width = 9, height = 11
)
cat("Escrito: fig_heatmap_top_de.pdf\n")

cat("\nBloco G (R: PCA, dispersao, volcano, MA, heatmap) concluido.\n")
