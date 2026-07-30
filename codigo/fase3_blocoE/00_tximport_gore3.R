#!/usr/bin/env Rscript
# FASE 3, Bloco E - adaptacao de RNA-Seq-not-model/scripts/00_tximport.R para
# este projeto genoma-guiado. UNICA mudanca real em relacao ao script
# original: le --tx2gene (Bloco E, extraido do GTF real da RS_2026_04) em
# vez de --gene_trans_map (formato Trinity, que nao existe aqui - esse
# projeto nao tem montagem de novo). A chamada tximport() em si nao muda -
# continua justificada por soneson2015differential (ja em docs/referencias.bib,
# PMID 26925227), que mostra que estimativas de gene sem os offsets de
# tximport inflam a FDR quando ha' uso diferencial de isoforma (o cenario
# que a hipotese H1 propoe existir entre isoformas de tripsina).
#
# tx2gene.tsv (Bloco E, build_tx2gene.py) ja vem no formato
# transcript_id<TAB>gene_id - ordem que o tximport espera - diferente do
# gene_trans_map do Trinity (gene<TAB>transcript, ordem invertida), que o
# script original precisava reordenar. Essa etapa de reordenar colunas
# some aqui.
suppressMessages(library(tximport))
suppressMessages(library(optparse))

option_list <- list(
  make_option("--salmon_dir", type = "character"),
  make_option("--samplesheet", type = "character"),
  make_option("--tx2gene", type = "character"),
  make_option("--outdir", type = "character")
)
opt <- parse_args(OptionParser(option_list = option_list))

samplesheet <- read.csv(opt$samplesheet, stringsAsFactors = FALSE)
quant_files <- file.path(opt$salmon_dir, samplesheet$sample, "quant.sf")
names(quant_files) <- samplesheet$sample

missing <- quant_files[!file.exists(quant_files)]
if (length(missing) > 0) {
  stop("quant.sf ausente para: ", paste(names(missing), collapse = ", "))
}

# quote = "" (nao o default "\"'"): pelo menos um gene_id do RefSeq contem
# apostrofo literal no nome (ex. "gene-beta'COP", subunidade beta' do
# complexo COPI) - o parser default do read.table interpreta isso como
# abertura de string entre aspas que nunca fecha ate o fim do arquivo,
# truncando silenciosamente a leitura de 25.840 para 22.305 linhas (sem
# erro, so um aviso "EOF within quoted string" facil de nao notar).
# Confirmado o efeito antes de corrigir: sem quote="", tximport reportava
# "3.263 transcripts missing from tx2gene"; com quote="", 0 ausentes.
tx2gene <- read.table(opt$tx2gene, header = FALSE, sep = "\t", quote = "",
                      col.names = c("transcript_id", "gene_id"))

txi <- tximport(quant_files, type = "salmon", tx2gene = tx2gene,
                ignoreTxVersion = FALSE, ignoreAfterBar = FALSE)

dir.create(opt$outdir, showWarnings = FALSE, recursive = TRUE)
write.table(round(txi$counts), file.path(opt$outdir, "fase3_blocoE_salmon_gene_counts.tsv"),
            sep = "\t", quote = FALSE, col.names = NA)
write.table(txi$abundance, file.path(opt$outdir, "fase3_blocoE_salmon_gene_tpm.tsv"),
            sep = "\t", quote = FALSE, col.names = NA)
write.csv(samplesheet, file.path(opt$outdir, "fase3_blocoE_sample_metadata.tsv"), row.names = FALSE)

cat("tximport concluido:", nrow(txi$counts), "genes x", ncol(txi$counts), "amostras\n")
