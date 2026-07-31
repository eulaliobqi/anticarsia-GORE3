#!/usr/bin/env Rscript
# FASE 7, Bloco G1 (R) - enriquecimento GO (via TERM2GENE consolidado,
# Bloco F) e KEGG (via KO do eggNOG-mapper, organism="ko" - modo
# universal do clusterProfiler, nao precisa de banco especifico de
# especie, o caso de A. gemmatalis que nao tem entrada dedicada no KEGG).
suppressMessages({
  library(clusterProfiler)
  library(GO.db)
})

GO_MAP <- "resultados_server/fase7_blocoF/gene_to_go_consolidated.csv"
KEGG_MAP <- "resultados_server/fase7_blocoC/gene_to_kegg.csv"
D_DIR <- "resultados_server/fase5_blocoD"
D_DIR_ALL <- "resultados_server/fase5_blocoD"
OUT_DIR <- "resultados_server/fase7_blocoG"

CONTRASTS <- c("Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control")
PVALUE_CUTOFF <- 0.05

dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

# --- TERM2GENE / TERM2NAME (GO), construido uma vez, reusado nos 3 ---
go_map <- read.csv(GO_MAP, stringsAsFactors = FALSE)
term2gene <- go_map[, c("go_id", "gene_id")]

all_go_ids <- unique(go_map$go_id)
go_terms <- suppressWarnings(AnnotationDbi::select(
  GO.db, keys = all_go_ids, columns = c("TERM", "ONTOLOGY"), keytype = "GOID"
))
go_terms <- go_terms[!duplicated(go_terms$GOID), ]
term2name <- data.frame(go_id = go_terms$GOID, name = go_terms$TERM)
go_ontology <- setNames(go_terms$ONTOLOGY, go_terms$GOID)
cat(sprintf("TERM2GENE: %d pares gene-GO | %d termos GO unicos (%d sem nome resolvido no GO.db)\n",
            nrow(term2gene), length(all_go_ids), sum(is.na(term2name$name))))

# --- TERM2GENE (KEGG KO), gene->KO do eggNOG-mapper ---
kegg_map <- read.csv(KEGG_MAP, stringsAsFactors = FALSE)
kegg_map$ko <- sub("^ko:", "", kegg_map$kegg_ko)
kegg_gene_to_ko <- split(kegg_map$ko, kegg_map$gene_id)

for (rotulo in CONTRASTS) {
  cat(sprintf("\n=== %s ===\n", rotulo))
  sig <- read.csv(file.path(D_DIR, sprintf("deseq2_%s_sig.csv", rotulo)))
  all_genes <- read.csv(file.path(D_DIR_ALL, sprintf("deseq2_%s_all.csv", rotulo)))

  de_genes <- sig$gene_id
  universe <- all_genes$gene_id
  cat(sprintf("DE: %d genes | universo testado: %d genes\n", length(de_genes), length(universe)))

  # --- GO (enricher generico, TERM2GENE/TERM2NAME proprios - via ja
  # documentada em docs/07_analise_rnaseq.md §8 para organismo sem org.db) ---
  ego <- tryCatch(
    enricher(gene = de_genes, universe = universe,
             TERM2GENE = term2gene, TERM2NAME = term2name,
             pvalueCutoff = PVALUE_CUTOFF, qvalueCutoff = 1, pAdjustMethod = "BH"),
    error = function(e) { message("GO enricher() falhou: ", conditionMessage(e)); NULL }
  )
  if (!is.null(ego) && nrow(as.data.frame(ego)) > 0) {
    ego_df <- as.data.frame(ego)
    ego_df$ontology <- go_ontology[ego_df$ID]
    out_go <- file.path(OUT_DIR, sprintf("clusterprofiler_GO_%s.csv", rotulo))
    write.csv(ego_df, out_go, row.names = FALSE)
    cat(sprintf("GO: %d termos significativos (padj<%.2f) -> %s\n", nrow(ego_df), PVALUE_CUTOFF, out_go))
  } else {
    cat("GO: nenhum termo significativo (ou enricher() vazio)\n")
    write.csv(data.frame(), file.path(OUT_DIR, sprintf("clusterprofiler_GO_%s.csv", rotulo)), row.names = FALSE)
  }

  # --- KEGG (organism="ko", modo universal - sem banco especifico da especie) ---
  de_ko <- unique(unlist(kegg_gene_to_ko[de_genes[de_genes %in% names(kegg_gene_to_ko)]]))
  universe_ko <- unique(unlist(kegg_gene_to_ko[universe[universe %in% names(kegg_gene_to_ko)]]))
  cat(sprintf("KO mapeados: %d de DE (de %d DE totais), %d do universo\n",
              length(de_ko), length(de_genes), length(universe_ko)))

  ekegg <- tryCatch(
    enrichKEGG(gene = de_ko, universe = universe_ko, organism = "ko",
               pvalueCutoff = PVALUE_CUTOFF, qvalueCutoff = 1, pAdjustMethod = "BH"),
    error = function(e) { message("enrichKEGG() falhou: ", conditionMessage(e)); NULL }
  )
  if (!is.null(ekegg) && nrow(as.data.frame(ekegg)) > 0) {
    ekegg_df <- as.data.frame(ekegg)
    out_kegg <- file.path(OUT_DIR, sprintf("clusterprofiler_KEGG_%s.csv", rotulo))
    write.csv(ekegg_df, out_kegg, row.names = FALSE)
    cat(sprintf("KEGG: %d vias significativas (padj<%.2f) -> %s\n", nrow(ekegg_df), PVALUE_CUTOFF, out_kegg))
  } else {
    cat("KEGG: nenhuma via significativa (ou enrichKEGG() vazio/API indisponivel)\n")
    write.csv(data.frame(), file.path(OUT_DIR, sprintf("clusterprofiler_KEGG_%s.csv", rotulo)), row.names = FALSE)
  }
}

cat("\nBloco G1 (R/clusterProfiler: GO + KEGG) concluido para os 3 contrastes.\n")
