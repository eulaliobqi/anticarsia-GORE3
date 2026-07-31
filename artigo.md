
> **Documento vivo — construído incrementalmente, bloco de análise por bloco de análise.**
> Cada seção só contém o que foi de fato executado e confirmado nesta sessão de
> trabalho. Nada aqui é projeção, expectativa típica de literatura, ou "resultado
> esperado" — quando um resultado não existe ainda, a seção diz isso
> explicitamente em vez de ser omitida ou preenchida por extrapolação.
> Status atual: **FASE 1 completa** (Blocos A, A.1, B e C — QC bruto,
> fechamento da lacuna per-tile, trimagem com fastp, teste de equilíbrio de
> parâmetros de trimagem). **FASE 2 (Blocos A e B) completa**: piloto STAR
> vs. HISAT2 decidiu por STAR (Bloco A), e as 13 bibliotecas completas
> foram alinhadas com sucesso nas duas vias — STAR (expressão gênica) e
> Subread (splicing), 13/13 cada uma, todas acima do limiar de 80% de
> mapeamento (§3.9). **FASE 3 (Blocos A-F) completa**: quantificação por
> gene (featureCounts, via prioritária) e por transcrito (Salmon
> decoy-aware + tximport, apoio à hipótese H1), verificadas cruzadamente
> (concordância Spearman 0,98–0,99, §3.11). **FASE 4 decidida** (30/07/2026):
> nenhuma correção formal de lote — o confundimento de amostra única
> (ID-8) torna o ComBat-seq inaplicável (a própria ferramenta recusa
> rodar), decisão justificada por literatura + código-fonte (§4); checagem
> de sensibilidade planejada para a FASE 5. **FASE 5 (Blocos A-G)
> concluída em 31/07/2026:** modelo DESeq2 (R) e PyDESeq2 (Python)
> ajustados sobre a mesma matriz tximport (11.833 genes pós-filtro),
> 3 contrastes vs. Controle extraídos com shrinkage apeglm (log2FC=0,25,
> §3.12), verificação cruzada R×Python com concordância alta de log2FC
> mas mais fraca na fronteira de significância para Benzamidina (§3.13),
> checagem de sensibilidade ID-8 mostrando o contraste Benzamidina como
> **frágil e dependente de uma única amostra** (255→6 DE genes sem ID-8,
> §3.14), e figuras (PCA+UMAP, volcano, MA, heatmap, UpSet — SKTI∩GORE3
> compartilham 3.053 genes DE, §3.15). Os contrastes cabeça-a-cabeça
> (GORE3×Benzamidina, GORE3×SKTI/H4, agrupado) e o Bloco H (commit)
> ficam para a próxima rodada.
>
> **Versão em português:** `artigo_pt.md` (mantida em paralelo, sincronizada
> a cada atualização — tradução fiel, não um resumo).
>
> **Índice-mestre de material (figuras/tabelas/código/dados, para geração
> futura de Word/PPTX):** `INDICE_MATERIAL.md`.

# Transcriptomic response of *Anticarsia gemmatalis* midgut to the peptide protease inhibitor GORE3

**Eulálio Gutemberg Bonfim dos Santos Jr.¹\*, [demais autores a definir]**

¹ Laboratory of Enzymology and Biochemistry of Proteins and Peptides,
Departamento de Bioquímica e Biologia Molecular, Universidade Federal de
Viçosa (UFV), BIOAGRO/INCT-IPP, Viçosa-MG, Brasil

\*Correspondência: eulalio.santos@ufv.br

---

## Abstract

*[PENDENTE — o abstract só será escrito quando houver resultados de expressão
diferencial (FASE 5) para resumir. Um abstract escrito agora, cobrindo só QC
de dados brutos, não resumiria um achado científico substantivo — seria
preenchimento de seção por completude, o que este documento evita
explicitamente.]*

---

## 1. Introduction

*[PENDENTE — a introdução deste artigo deve ser derivada de
`docs/01_fundamentacao_teorica.md`, `docs/02_estado_da_arte_GORE.md` e
`docs/05_lacunas_e_hipoteses.md`, já auditados e com citação verificada. Será
escrita como bloco próprio, não copiada diretamente desses documentos sem
revisão de contexto para formato de artigo.]*

---

## 2. Materials and Methods

### 2.1 Biological material and experimental design

Fifth-instar *Anticarsia gemmatalis* larvae were fed artificial diet
supplemented with one of four treatments: untreated control, benzamidine
(synthetic positive control), SKTI (natural Kunitz-type trypsin inhibitor)
or GORE3 (the peptide inhibitor under study), with three biological
replicates per treatment (midgut tissue, one replicate per larva pool). One
additional, non-replicated fat-body sample was included outside this
four-group design. Sample identity and treatment-group assignment were
resolved from the Macrogen submission manifest
(`identificacao-amostras.xlsx`) and confirmed against the raw-data
delivery; the correspondence is reported in Table S1
(`codigo/fase1_blocoA/samplesheet.tsv`).

### 2.2 RNA sequencing

Total RNA was sequenced by Macrogen Inc. (order HN00280302, delivered 24
July 2026) as paired-end, 2×151 bp reads using the Illumina Stranded mRNA
Prep, Ligation library kit. Sequencing instrument identity was not stated
explicitly in the vendor report ("Illumina platform"); it was inferred from
the instrument-ID prefix in the FASTQ read headers (`LH00xxx`, consistent
with the Illumina NovaSeq X series) — reported here as an inference from raw
header content, not as a vendor-confirmed specification. NovaSeq
instruments use two-colour sequencing-by-synthesis chemistry, in which the
absence of a light signal is basecalled as G; as sequencing progresses and
per-cluster signal weakens, this can miscall true T/C bases as G,
producing polyG tails (Chen et al., 2018) — the mechanistic basis for the
`--trim_poly_g` parameter adopted in §2.4. Thirteen libraries
were delivered as 26 raw FASTQ files (~47 GB). File integrity was verified
against the vendor-supplied MD5 checksums for all 26 files (100% match;
`codigo/fase1_blocoA/md5sum.txt`).

### 2.3 Raw-read quality control

Raw-read quality was assessed with FastQC v0.12.1 and aggregated with
MultiQC v1.33 (Ewels et al., 2016), run in a dedicated Conda/Mamba
environment on a Linux server (32 CPU cores, 188 GB RAM), independently of
the vendor's own QC report. Exact tool versions and the full environment
specification are recorded in `resultados/blocoA_ENV_VERSIONS.txt`.

Total per-file read counts from FastQC were cross-checked against the
vendor-reported totals for all 13 samples, and read counts between mates
(R1/R2) were checked for exact agreement within each pair.

To test whether the localized raw-read quality defect visible in the
vendor's per-base-quality plots for three libraries reflected a shared
sequencing-run artefact, we (i) extracted the sequencing instrument, flow
cell and lane identifiers from the first FASTQ read header of each library;
(ii) computed, from the FastQC "Per base sequence quality" module, the mean
Phred score in a read-1 cycle window declared *before* inspecting
per-sample identities (cycles 44–90, matching the position range visually
apparent in the vendor plots) versus the flanking region (cycles 1–43 and
91–151), flagging any library with a flanking-minus-window drop exceeding
5.0 Phred; and (iii) inspected the FastQC "Per tile sequence quality"
module for evidence of tile-localized defects. Analysis code:
`codigo/fase1_blocoA/analyze_blocoA.py`.

### 2.4 Read trimming (Phase 1, Block B)

Two candidate fastp v1.3.0 parameter sets were compared empirically before
committing to one for the full batch, because the project's cited
literature (Chen, 2025; Chen et al., 2018) justifies choosing fastp over
Trimmomatic/Cutadapt but gives no numeric threshold guidance (declared as
Limitation 2 in the previous version of this document): **Set A**
(`--detect_adapter_for_pe --length_required 36 --qualified_quality_phred 20`,
matching the value originally recorded in `docs/07_analise_rnaseq.md`) and
**Set B** (`--detect_adapter_for_pe --length_required 50
--qualified_quality_phred 20 --trim_poly_g --trim_poly_x
--overrepresentation_analysis`, matching the sibling `RNA-Seq-not-model`
pipeline's production module, adapted to fastp 1.3.0). Both sets were run
on two representative libraries — Control_R1 (clean) and Benzamidine_R3
(worst raw-QC profile) — comparing read survival, Q20/Q30 after filtering,
and the breakdown of the `filtering_result` categories fastp reports.
Code: `codigo/fase1_blocoB/run_fastp_ab_test.sh`,
`codigo/fase1_blocoB/compare_ab_test.py`; full comparison:
`resultados/blocoB_ab_test_comparison.csv`.

Based on the A/B result (§3.5), Set B was selected and applied to all 13
libraries (26 files) in a single batch run
(`codigo/fase1_blocoB/run_fastp_full_trim.sh`), producing trimmed FASTQ in
`trimmed/` and one fastp JSON/HTML report per library in `qc/post_trim/`.
Post-trim QC results are analysed in `codigo/fase1_blocoB/analyze_blocoB.py`.

Alignment and quantification (Phase 2 onward) had not been executed at the
time of writing this section and are not reported below.

### 2.4.1 Trimming-parameter equilibrium test (Phase 1, Block C)

Because four libraries (Benzamidine_R2/R3, SKTI_R1/R2) lost 17.6–37.5% of
reads to fastp's `adapter_dimer_reads` classification under Set B (§3.6),
we tested whether relaxing trimming parameters could recover reads without
a quality cost, rather than assuming Set B was already optimal. Deterministic
2,000,000-read-pair subsamples (`seqtk` 1.5, seed `-s100`) were drawn from
Control_R1 (clean reference) and the four affected libraries
(`codigo/fase1_blocoC/subsample_reads.sh`), then trimmed with four fastp
configurations (`codigo/fase1_blocoC/run_fastp_paramsweep.sh`): **Set B**
(production baseline); **Set C1** (`--qualified_quality_phred 15` instead
of 20); **Set C2** (more permissive overlap-analysis:
`--overlap_len_require 20 --overlap_diff_limit 8
--overlap_diff_percent_limit 30`, versus fastp defaults 30/5/20); **Set C3**
(more restrictive overlap-analysis, as a sanity-check counter-test:
`--overlap_len_require 40 --overlap_diff_limit 3
--overlap_diff_percent_limit 10`). `--length_required 50` and the
poly-G/poly-X/adapter-detection flags were held fixed across all sets,
since §3.5 already showed `--length_required` does not affect survival.

To arbitrate with data beyond fastp's own metrics, trimmed subsample reads
from every sample × set combination were aligned with HISAT2 2.2.2 against
a **pilot** index of `GCF_050436995.1` built without splice-site annotation
(`codigo/fase1_blocoC/build_hisat2_index_pilot.sh`, genome FASTA reused from
a separate local project, `~/vg_search/genome/`) — adequate for an overall
mapping-rate comparison across configurations, not for isoform-level
quantification; this pilot precedes and is independent of the formal
Phase 2 genome-guided alignment on the complete 13 libraries.
Pre-declared decision rule (`codigo/fase1_blocoC/analyze_blocoC.py`): a
candidate set would replace Set B in production only if, in all four
affected libraries simultaneously, (i) read survival increased by ≥5
percentage points versus Set B, (ii) post-trim Q30 remained ≥95%, (iii) the
HISAT2 pilot mapping rate did not decrease, and (iv) the clean control
library was not degraded. Full results:
`resultados/blocoC_param_sweep.csv`.

### 2.5 Genome-guided alignment (Phase 2)

**Block A — aligner selection pilot.** Because no single aligner is optimal
for both gene-level quantification and splice-junction detection (Coxe et
al., 2024), STAR 2.7.10b and HISAT2 2.2.2 were compared head-to-head on a
five-sample subset spanning all four treatment groups plus one additional
replicate (Control_R1/ID-1; Benzamidine_R2/ID-7, Benzamidine_R3/ID-8;
SKTI_R1/ID-9, SKTI_R2/ID-10), using the trimmed (Set B) full libraries
against a genome index built from `GCF_050436995.1` with the RS_2026_04
GTF as splice-junction guide (`--outSAMtype None`, no BAM written — this
step measures mapping rate only). Code:
`codigo/fase2_blocoA/run_star_hisat2_subsample.sh`,
`build_star_index.sh`/`build_hisat2_index_annotated.sh`,
`convert_gff_to_gtf.sh`; analysis: `codigo/fase2_blocoA/analyze_fase2_blocoA.py`;
full output: `resultados/fase2_blocoA_star_vs_hisat2.csv`. Decision rule,
agreed with the project supervisor before inspecting results: the aligner
with a ≥2 percentage-point mapping-rate advantage across the pilot samples
would be run alone on the full batch, rather than running both aligners on
all 13 libraries.

**Block B — full-batch alignment, two parallel tracks.** Following the
Block A decision (§3.9), the winning aligner (STAR) was run on all 13
trimmed libraries with BAM output (`--outSAMtype BAM SortedByCoordinate
--twopassMode Basic`), producing the deliverable used downstream for
gene-level quantification (Phase 3) — code:
`codigo/fase2_blocoB/run_alignment_full.sh`. In parallel, Subread-align
2.1.1 was run on the same 13 trimmed libraries as the dedicated
splice-junction-accuracy track (Coxe et al., 2024 report Subread as the
most promising tool for junction-level, as opposed to base-level, mapping
accuracy — the property Phase 6's alternative-splicing analysis (H1, H5)
depends on) — code: `codigo/fase2_blocoB/run_subread_align_full.sh`. Both
scripts are resumable (a per-sample completion marker is checked before
re-running) and tolerate an isolated per-sample failure without aborting
the remaining samples (`set -uo pipefail`, not `set -e`), because the
first execution attempt showed that running both 16-thread jobs
concurrently on the server caused segmentation faults in a subset of
samples for both tools (§3.9, §5 item 9) — an operational finding, not a
property of the sequence data.

### 2.6 Gene- and transcript-level quantification (Phase 3)

Phase 3's purpose is to feed the group-level contrasts (GORE3 vs. Control,
GORE3 vs. Benzamidine, GORE3 vs. SKTI — the study's central deliverable,
§6.1 of the planning document) with a production gene-count matrix; the
transcript/isoform-level track is a secondary, supporting analysis for
hypothesis H1 (trypsin-like isoform switching), not the primary aim of
this phase.

**Library-orientation confirmation.** The two scripts written but not yet
run at the time of the Phase 2 write-up (`codigo/fase2_blocoB/check_strandedness.sh`,
`analyze_strandedness.py`) were executed against the STAR BAMs of ID-1 and
ID-8: featureCounts was run twice per sample (`-s 1` vs. `-s 2`) against
the real GTF, and the configuration assigning the larger fraction of reads
to genes was taken as the winner. Reverse-stranded (`-s 2` / Salmon
`--libType ISR`) won decisively and consistently in both samples (§3.11),
superseding the provisional kit-name-based inference. Code:
`codigo/fase3_blocoA/decide_libtype.py` formalises this as the single
source of truth (`resultados/fase3_blocoA_strand_decision.csv`) read by
every downstream script.

**An unplanned GTF defect, found and fixed.** Running featureCounts for
the first time failed with "failed to find the gene identifier attribute
in the 9th column." Inspection found 330 of 515,035 GTF lines (118 genes,
all uncharacterised "LOC" loci with no mRNA record in the source GFF3)
carried a `transcript_id` but no `gene_id` — gffread (used in Phase 2) does
not propagate `gene_id` when a GFF3 gene has no explicit gene→mRNA→exon
hierarchy. The fix (`codigo/fase3_blocoA/fix_gtf_missing_geneid.sh`) is
exact, not approximate: for these 330 lines, the existing `transcript_id`
value already equals what `gene_id` should be (same `"gene-<name>"`
convention used throughout the rest of the file, confirmed with zero
exceptions across all 330 lines before applying the fix), so the fix adds
`gene_id` using data already present on the same line, not a fabricated
value. None of the 118 affected genes is a known trypsin/serine-protease
gene. Phase 2 (STAR) does not need to be re-run, since STAR's use of the
GTF (splice-site guidance) does not depend on `gene_id`; all Phase 3
onward uses the corrected GTF (`GCF_050436995.1_RS_2026_04.fixed.gtf`).

**Gene-level quantification (priority track).** featureCounts v2.1.1 was
run once across all 13 STAR BAMs, real corrected GTF, confirmed reverse
strand, `-p -g gene_id -t exon` — code:
`codigo/fase3_blocoC/run_featurecounts_genelevel.sh`. **Deliberately not
used: `-M -O --fraction`** (rescuing multi-mapping/multi-overlapping
reads). Zytnicki (2017, PMID 28915787, "mmquant: how to count
multi-mapping reads?") states directly that enabling these flags "almost
always provides biased results." This creates a real, undeclared-as-solved
tension specific to this project: the secondary hypothesis H1 concerns a
multigenic trypsin-like serine-protease family, where reads from close
paralogs may map ambiguously, and default featureCounts will
discard/undercount those ambiguous reads at exactly those genes. This does
not affect the phase's primary deliverable (whole-group contrasts); it is
left open for Phase 9 (manual serine-protease family curation) to revisit
specifically for that gene set, not solved here. A targeted search for an
equivalent benchmark in insects or multigene families found nothing
directly on point; the closest available evidence, Kwon (2015, PMID
26112470, duplicated-gene quantification in *Xenopus*, abstract-only
access), is not in insects and is not cited as resolving this gap — only
as the nearest available analog.

**Transcript-level quantification (Phase D-E, support to H1).** Salmon
1.10.3 was indexed in decoy-aware mode ("selective alignment", full genome
as decoy) rather than the outdated decoy-free `--type quasi` mode used in
the reusable sibling module (`RNA-Seq-not-model/modules/quantification.nf`).
Srivastava et al. (2020, PMID 32894187, *Genome Biology*) established that
decoy-aware indexing reduces spurious read assignment relative to
decoy-free mapping, validated on 109 real human RNA-seq datasets plus
mouse simulations — **no insect or non-model genome was tested in that
benchmark**; the structural finding (decoys reduce mis-assignment) is a
reasonable extrapolation to *A. gemmatalis*, not an established fact for
this species, on the same model as the Coxe et al. (2024) plant-to-insect
caveat already declared in §2.5. Index build:
`codigo/fase3_blocoD/build_salmon_decoy_index.sh` (`gffread`-extracted
transcriptome + whole-genome decoy, `k=31`, Salmon's own default, not
tuned for this genome). Quantification:
`codigo/fase3_blocoD/run_salmon_quant_full.sh` (`--libType ISR`,
`--validateMappings --gcBias`, unchanged from the sibling pipeline).
tximport adaptation (`codigo/fase3_blocoE/build_tx2gene.py`,
`00_tximport_gore3.R`): the only real change from
`RNA-Seq-not-model/scripts/00_tximport.R` is reading a `tx2gene.tsv` built
directly from the real GTF's `transcript_id`/`gene_id` attributes, instead
of a Trinity `gene_trans_map` that does not exist in this genome-guided
design; the `tximport()` call itself, justified by
`soneson2015differential` (already cited, §2.5), is unchanged.

### 2.7 Differential expression: import, model, and dual implementation (Phase 5, Blocks A–G complete)

**Import strategy revisits Phase 3's technical choice, not its emphasis.**
The tximport documentation is normative, not suggestive: *"Do not
manually pass the original gene-level counts to downstream methods
without an offset... Passing uncorrected gene-level counts without an
offset is not recommended by the tximport package authors."*
Consequently, DESeq2 import for this phase uses
`DESeqDataSetFromTximport` (Salmon+tximport counts with the
transcript-length offset), not raw featureCounts counts; featureCounts
remains a secondary robustness check (already ρ = 0.983–0.988 concordant
with tximport-based gene counts at the gene level, §3.11). This refines
the Phase 3 technical input, not its declared scientific emphasis
(group-level contrasts remain the primary target; the trypsin-family
angle remains secondary).

**A real coverage gap, closed.** The Phase 3 Salmon index was built
without `--keepDuplicates`, silently collapsing 811 of 25,840
transcripts with byte-identical sequence into a single representative,
leaving ~800 of 15,773 genes without any directly quantifiable
transcript in tximport's gene-level table. Rebuilding the index with
`--keepDuplicates` (same transcriptome/decoy inputs, ~7 minutes of
re-indexing) and re-quantifying all 13 libraries closed this gap
completely: **15,773/15,773 genes (100%)**, up from 14,973/15,773
(94.9%) in Phase 3 (Fig. 9). An automated consistency check
(`codigo/fase5_blocoB/analyze_keepdup_coverage.py`) confirmed coverage
did not regress and no count value is negative or NaN before this matrix
was used further.

**Dataset construction.** `DESeqDataSetFromTximport` was built from the
re-quantified `txi` object, `condition` as a 4-level factor
(`Control`/`Benzamidine`/`SKTI`/`GORE3`, Control as the reference level),
excluding ID-18 (fat body, no group/replicate — already established in
Phase 1 §13.1) from `colData` before construction, not after. Code:
`codigo/fase5_blocoB/build_dds_tximport.R`.

**Dual-implementation plan, and a disclosed asymmetry found while
preparing it.** Per explicit instruction not to rely on R alone, the
statistical model will be fit independently in R (DESeq2) and Python
(PyDESeq2 — Muzellec et al. 2023, PMID 37669147, actively maintained
under the scverse organisation). A synthetic-data pilot run (not real
project data) caught two real script errors before any real-data run:
PyDESeq2's `ref_level` argument is deprecated in the installed version
(0.5.4, "no longer has any effect" — reference level is instead
controlled by categorical factor level order, already correctly set),
and its shrinkage-coefficient naming convention is
`condition[T.Benzamidine]`-style (formulaic/patsy), not
`condition_Benzamidine_vs_Control` as in R — both fixed in
`codigo/fase5_blocoC/run_pydeseq2.py` before it is run on real data
(§3.12, once available). Separately, and disclosed rather than
smoothed over: **PyDESeq2 has no equivalent to tximport's
transcript-length offset** — confirmed directly in its source
(`pydeseq2/ds.py`: only a per-sample scalar `log(size_factors)` term
exists, not a gene-by-sample offset matrix). The Python run therefore
used the same tximport-derived gene counts as the R model, but without
the length-bias correction the R model applies — a real, disclosed
asymmetry between the two engines' inputs, kept in mind when interpreting
their concordance (§3.12), not treated as a like-for-like comparison.

**Model fitting and contrast extraction.** Both engines were fit on the
same low-count filter (`rowSums(counts) >= 10`, or the equivalent
per-gene sum in Python) over the three contrasts against Control
(Benzamidine, SKTI, GORE3). log2 fold-change shrinkage used **apeglm**
(Zhu, Ibrahim & Love 2019, PMID 30395178) via a direct model coefficient
(no releveling needed, Control being the reference level in both
engines), at the pre-declared threshold **log2FC = 0.25**, padj < 0.05
(independent filtering on by default — Bourgon, Gentleman & Huber 2010,
PMID 20460310). Code: `codigo/fase5_blocoD/extract_contrasts_deseq2.R`
(R) and `apply_threshold_pydeseq2.py` (Python, applied post-hoc to the
already-shrunk log2FC that `run_pydeseq2.py`, Block C2, wrote out).

**Cross-engine verification** (a dataset-specific empirical check, not a
literature-backed benchmark — the PyDESeq2 paper itself reports no
quantitative concordance figure against R/DESeq2): Pearson/Spearman
correlation of shrunk log2FC and Jaccard overlap of significant-gene sets
between the two engines, per contrast. Code:
`codigo/fase5_blocoE/compare_r_python.py`.

**ID-8 sensitivity check** (a commitment from Phase 4's batch-correction
decision, §4): the Benzamidine-vs-Control model was refit on the raw
tximport `DESeqDataSet` (Phase 5 Block B) subset to n=2 (ID-5, ID-7,
excluding ID-8), with unused factor levels dropped before refitting, and
compared against the full n=3 result on DE-gene overlap and effect-sign
concordance. Code: `codigo/fase5_blocoF/sensitivity_id8.R`.

**Figures.** Categorical palette validated with this environment's
`dataviz` skill validator (`validate_palette.js`, `--pairs all`, four
categories): Control = blue `#2a78d6`, Benzamidine = orange `#eb6834`,
SKTI = aqua `#1baf7a`, GORE3 = violet `#4a3aa7`. The palette's default
fourth categorical slot (yellow) fails the normal-vision-floor check
against orange under all-pairs comparison and was swapped for violet,
which passes every check for this four-category set. PCA (`plotPCA` on
VST, `blind=FALSE`) was paired with UMAP as a non-linear reinforcement,
not a replacement (Yang et al. 2021, PMID 34320340), computed on the
identical VST matrix exported from R. Set intersections across the three
contrasts' DE-gene lists were visualised with an UpSet plot (Conway, Lex
& Gehlenborg 2017, PMID 28645171) rather than a Venn diagram. Code:
`codigo/fase5_blocoG/figures_r.R` (PCA, dispersion diagnostic, volcano,
MA, annotated heatmap) and `figures_python.py` (UMAP, UpSet).

---

## 3. Results

### 3.1 Library yield and identity confirmed independently of the vendor report

FastQC-derived read counts matched the vendor-reported totals exactly for
all 13 samples (e.g., Control_R1: 32,550,688 × 2 = 65,101,376 reads,
identical to the vendor total; Benzamidine_R3: 39,460,179 × 2 = 78,920,358,
identical). R1/R2 mate counts were identical within every pair (13/13).
This is independent, read-content-level confirmation beyond the
checksum-level integrity check in §2.2.

### 3.2 A quality defect confined to three libraries, by a pre-declared criterion

Mean R1 quality dropped by more than 5 Phred in the cycles-44–90 window
relative to flanking cycles in exactly three of the 13 libraries —
Benzamidine_R2 (ΔQ = 5.48), Benzamidine_R3 (ΔQ = 5.75) and SKTI_R2
(ΔQ = 5.46) — and in none of the remaining ten (ΔQ range 0.08–1.81;
Fig. 1, Table 1). The criterion was applied uniformly to all 13 libraries,
not only to the three originally flagged from visual inspection of the
vendor report, and reproduced that original flagging exactly (no false
positives or negatives against the pre-declared threshold).

**Table 1 | Raw-read summary statistics and quality-window test, by sample.**

| Sample | Treatment / replicate | Reads (R1) | R1/R2 match | ΔQ (cycles 44–90) | Flagged |
|---|---|---:|:---:|---:|:---:|
| ID-1 | Control_R1 | 32,550,688 | yes | 0.08 | no |
| ID-2 | Control_R2 | 33,504,042 | yes | 0.89 | no |
| ID-3 | Control_R3 | 29,090,048 | yes | 1.08 | no |
| ID-5 | Benzamidine_R1 | 27,500,647 | yes | 0.73 | no |
| ID-7 | Benzamidine_R2 | 28,930,368 | yes | 5.48 | **yes** |
| ID-8 | Benzamidine_R3 | 39,460,179 | yes | 5.75 | **yes** |
| ID-9 | SKTI_R1 | 31,172,157 | yes | 1.81 | no |
| ID-10 | SKTI_R2 | 30,906,748 | yes | 5.46 | **yes** |
| ID-12 | SKTI_R3 | 33,545,221 | yes | 0.33 | no |
| ID-14 | GORE3_R1 | 27,090,197 | yes | 0.35 | no |
| ID-15 | GORE3_R2 | 31,079,636 | yes | 0.95 | no |
| ID-16 | GORE3_R3 | 29,902,657 | yes | 0.72 | no |
| ID-18 | FatBody | 33,478,105 | yes | 0.42 | no |

*Full machine-readable output: `resultados/blocoA_results.csv`.*

**Figure 1 | Raw-read quality drop is confined to three libraries, defined
by a pre-declared position window.** Mean Phred quality score in read-1
cycles 44–90 was subtracted from the flanking-region mean (cycles 1–43 and
91–151) for each of the 13 raw FASTQ libraries (FastQC v0.12.1). Red bars
denote the three libraries exceeding the threshold declared before the
sample set was inspected (ΔQ > 5.0 Phred, dashed line): Benzamidine_R2,
Benzamidine_R3 and SKTI_R2. All ten remaining libraries — spanning all
four treatment groups and the non-replicated fat-body sample — fall below
ΔQ = 1.8. Sample labels combine treatment group and biological replicate
number, resolved from the Macrogen sample submission manifest (Table S1).
File: `figuras/Figure1_blocoA_quality_dip.png`.

### 3.3 The defect does not track sequencing lane; the physical cause remains open

Read headers showed that 12 of the 13 libraries — including both clean and
defective samples — were sequenced on the same instrument, flow cell and
lane (`LH00129`, flow cell `23NNGLLT4`, lane 4). Only Benzamidine_R3
(ID-8) was sequenced separately, on a different instrument, flow cell and
lane altogether (`LH00688`, flow cell `253LHLLT4`, lane 5).

This directly constrains the possible explanations: because Benzamidine_R2
and SKTI_R2 share a lane with all ten unaffected libraries, a lane-wide
technical cause is excluded for those two specifically; because
Benzamidine_R3 was sequenced on an entirely separate run, it cannot share a
lane- or flow-cell-level cause with the other two. A first, coarse
tile-resolved test (whole-read FastQC "Per tile sequence quality" pass/warn/fail
flag) was inconclusive, as reported in the previous version of this
section: all 13 libraries showed warn/fail flags at comparable magnitude.

### 3.4 A position-resolved re-analysis closes the gap: tile heterogeneity is real, localized, and tracks GC content

The coarse test above collapsed the entire 151-cycle read into one
pass/warn/fail flag, which cannot detect an effect confined to a 46-cycle
window. We repeated the per-tile analysis restricted to the same
pre-declared window (cycles 44–90) used in §3.2, computing, for every
sample and every physical tile, the mean per-tile quality deviation inside
the window versus in the flanking cycles, then comparing the **spread
(population standard deviation) of these per-tile values across tiles**
between window and flank
(code: `codigo/fase1_blocoA/per_tile_analysis.py`; full output:
`resultados/blocoA1_pertile_results.csv`).

The logic of this test: if the window-specific quality drop reflects a
sample-wide chemistry/library effect acting equally on every cluster
regardless of its physical position, tiles should disagree with each other
about as much inside the window as outside it (ratio ≈ 1). If instead
specific physical tiles are disproportionately bad only within that cycle
range, inter-tile spread should be much larger inside the window than
outside it (ratio ≫ 1).

**Result: the ratio is elevated specifically in four libraries, and it
tracks vendor-reported GC content, not lane membership.**

| Sample | Label | GC% (vendor) | Std. dev. window | Std. dev. flank | Ratio (window/flank) |
|---|---|---:|---:|---:|---:|
| ID-8 | Benzamidine_R3 | 63.1 | 0.646 | 0.103 | **6.28** |
| ID-9 | SKTI_R1 | 54.7 | 0.587 | 0.266 | **2.21** |
| ID-7 | Benzamidine_R2 | 59.7 | 0.486 | 0.223 | **2.18** |
| ID-10 | SKTI_R2 | 60.8 | 0.509 | 0.250 | **2.04** |
| ID-16 | GORE3_R3 | 50.3 | 0.317 | 0.255 | 1.25 |
| remaining 8 samples | — | 48.4–53.4 | 0.13–0.24 | 0.18–0.28 | 0.72–0.94 |

Pearson correlation between vendor-reported GC% and the window/flank ratio
across all 13 samples: **r = 0.80**; Spearman rank correlation (robust to
the ID-8 outlier): **ρ = 0.49**. The four samples with ratio > 2 are
exactly the four samples with the highest GC content in the entire batch
(59.7–63.1%, versus 48.4–54.7% for the rest) — including **SKTI_R1
(ID-9)**, which had *not* been flagged by the mean-based criterion in §3.2
(ΔQ = 1.81, below the 5.0 threshold) but shows the second-highest
window/flank ratio in the dataset. This is disclosed as a graded,
GC-correlated effect, not a strictly binary three-library phenomenon as
§3.2 alone would suggest.

**Figure 2 | Quality loss in cycles 44–90 is tile-heterogeneous in the
worst-affected library and absent in a clean one.** Per-tile quality
deviation from the sample mean (FastQC "Per tile sequence quality", read 1),
plotted as tile (flow-cell physical position, y-axis, arbitrary order) by
sequencing cycle (binned, x-axis), for **(a)** Control_R1 (ID-1, clean;
window/flank ratio 0.72) and **(b)** Benzamidine_R3 (ID-8, worst-affected;
window/flank ratio 6.28). Dashed vertical lines mark the pre-declared
cycles-44–90 window. Colour scale: blue, tile better than the sample mean
at that cycle; red, tile worse than the sample mean (Phred units, clipped
at ±3). A conspicuous banded, alternating pattern of well- and
poorly-performing tiles appears only inside the marked window in ID-8, and
is absent throughout ID-1 and outside the window in ID-8 — a signature
inconsistent with either a whole-lane or a whole-library-uniform cause.
File: `figuras/Figure2_blocoA1_pertile_heatmap.png`.

**Interpretation, stated at the confidence the data actually support — no
further than that.** Three findings jointly constrain the explanation: (i)
a lane-wide physical cause is excluded (§3.3: unaffected libraries share
the same lane and tiles); (ii) a pure library-composition cause acting
uniformly on all clusters is also inconsistent with the data (it would
predict low, not high, inter-tile spread inside the window — the opposite
of Fig. 2b); (iii) the effect is nonetheless strongly GC-correlated, not
randomly distributed among libraries. The pattern most consistent with all
three observations is an **interaction**: a subtle, cycle-specific imaging
or focus artefact affecting the run broadly during cycles 44–90 (invisible
in low-GC libraries, which tolerate it without measurable quality loss),
that becomes visible specifically in the higher-GC libraries whose cluster
signal properties leave less margin to absorb it. This is our best-supported
account, not a proven mechanism — we did not, and could not from FastQC
output alone, test focus/illumination metrics directly. **The precise
physical root cause is characterized in more depth than in §3.3, but is
not fully solved, and we do not claim otherwise.**

### 3.5 The A/B trimming test reveals the true bottleneck, and it is not the tested parameter

Contrary to the premise of the A/B test, the choice between
`--length_required 36` and `50` made almost no difference to read survival
for either library (Control_R1: 97.53% vs. 97.48%; Benzamidine_R3: 62.53%
vs. 62.49%). What the test did reveal, from fastp's own
`filtering_result` breakdown, is the actual dominant cause of read loss in
Benzamidine_R3: **25.6% of its read pairs were classified as
`adapter_dimer_reads`** — pairs whose insert is so short that read 1 and
read 2 sequence into each other's adapter — versus a negligible fraction
in Control_R1. This category, not the length or quality filters under
test, accounts for the majority of Benzamidine_R3's read loss and was not
part of the original hypothesis space in §2.3. Because both parameter
sets performed identically on the metric that actually matters (survival),
and Set B adds adapter/poly-tail safety relevant to the confirmed NovaSeq
X (2-colour) chemistry (§2.2) at no measured cost, **Set B was adopted for
the full batch**.

### 3.6 Adapter-dimer contamination, not a flow-cell defect, explains the raw-read quality pattern

Applying Set B to all 13 libraries and tabulating `adapter_dimer_reads`
(Table 2; `resultados/blocoB_trim_summary.csv`) shows the same four
libraries flagged throughout §3.2–3.4 — Benzamidine_R2, Benzamidine_R3,
SKTI_R1, SKTI_R2 — carry 16–31% adapter-dimer reads, against 1–7% for the
remaining nine. This produces a strong correlation with vendor-reported GC
content (Pearson r = 0.92, Spearman ρ = 0.63, n = 13; Fig. 3b) — tighter
than the per-tile-variance correlation in §3.4 (r = 0.80, ρ = 0.49) — and
a correspondingly asymmetric read survival (62–82% for the four affected
libraries vs. 91–97% for the rest; Fig. 3a).

**Table 2 | Post-trimming outcome by sample, Set B parameters.**

| Sample | Label | GC% (vendor) | Adapter-dimer reads (%) | Survival (%) | Q30 before | Q30 after |
|---|---|---:|---:|---:|---:|---:|
| ID-1 | Control_R1 | 51.8 | 0.96 | 97.48 | 95.58 | 96.66 |
| ID-2 | Control_R2 | 53.4 | 5.79 | 92.93 | 94.47 | 96.34 |
| ID-3 | Control_R3 | 49.1 | 6.60 | 91.67 | 94.44 | 96.55 |
| ID-5 | Benzamidine_R1 | 52.3 | 4.60 | 93.92 | 94.73 | 96.41 |
| ID-7 | Benzamidine_R2 | 59.7 | **31.16** | **66.44** | 90.39 | 96.38 |
| ID-8 | Benzamidine_R3 | 63.1 | **25.58** | **62.49** | 84.14 | 96.80 |
| ID-9 | SKTI_R1 | 54.7 | **16.23** | 82.38 | 94.13 | 96.74 |
| ID-10 | SKTI_R2 | 60.8 | **30.65** | **67.56** | 90.49 | 96.57 |
| ID-12 | SKTI_R3 | 49.1 | 2.21 | 96.56 | 95.55 | 96.86 |
| ID-14 | GORE3_R1 | 48.4 | 2.21 | 95.45 | 95.04 | 96.82 |
| ID-15 | GORE3_R2 | 48.8 | 5.97 | 92.51 | 94.84 | 96.72 |
| ID-16 | GORE3_R3 | 50.3 | 6.47 | 92.12 | 94.87 | 96.62 |
| ID-18 | FatBody | 49.5 | 3.22 | 95.36 | 95.19 | 96.53 |

A second, encouraging result in the same table: **post-trim Q30 is
essentially uniform across all 13 libraries (96.3–96.9%)**, including the
four affected ones (Benzamidine_R2: 90.4%→96.4%; Benzamidine_R3:
84.1%→96.8%; SKTI_R2: 90.5%→96.6%). Trimming fully normalises base-call
quality; what it cannot recover is the lost yield from reads that were
never a usable biological fragment to begin with.

**Figure 3 | Read survival and adapter-dimer contamination separate the
same four libraries flagged by raw-QC metrics, and correlate with GC
content.** **(a)** Percentage of read pairs surviving fastp trimming
(Set B parameters, §2.4), by sample. **(b)** Adapter-dimer read percentage
(fastp `filtering_result.adapter_dimer_reads`) versus vendor-reported GC
content, per sample; Pearson r and Spearman ρ given in the panel title.
Red markers in both panels denote libraries with adapter-dimer rate >10%
(Benzamidine_R2, Benzamidine_R3, SKTI_R1, SKTI_R2); this is a
post-hoc visual cutoff chosen after inspecting the bimodal distribution
in (b), not a pre-declared threshold as in Fig. 1. File:
`figuras/Figure3_blocoB_trimming.png`.

**This revises, and largely supersedes, the interpretation offered in
§3.4.** The imaging-artefact-×-GC-sensitivity hypothesis was the
best-supported account *given only FastQC output*; adapter-dimer
contamination is a more direct, more strongly correlated (r = 0.92 vs.
0.80), and mechanistically simpler explanation that also naturally
accounts for the per-tile heterogeneity in Fig. 2 (short-insert molecules
reading into adapter sequence around cycle ~44–90 would behave differently
from normal-insert molecules in a way that need not be spatially uniform
across tiles) without requiring an additional, unobserved imaging effect.
We do not have a library-prep-level explanation for *why* these four
specific libraries carry more short-insert/adapter-dimer molecules (this
would require insert-size metrics from the library QC stage, which
Macrogen's raw-data report does not include — Limitation 3 in the previous
version of this document, now partially informed but not resolved by this
finding). A targeted PubMed search (four query variants: two-colour/2-channel
SBS chemistry artefacts; adapter-dimer/short-insert formation vs. GC
content or library composition) returned no directly relevant peer-reviewed
result at the time of writing. We report this as an empty search, not as
absence of any relationship in the literature — the GC–adapter-dimer
correlation in §3.6 is presented as this study's own empirical finding,
not as literature-confirmed.

### 3.7 Group- and contrast-level exposure to reduced depth

Aggregating Table 2 by treatment group makes the practical consequence of
§3.6 concrete (Table 3; group sums from `resultados/blocoB_trim_summary.csv`).

**Table 3 | Post-trimming depth by treatment group.**

| Group | Reads before (sum, n=3) | Reads after (sum) | Survival | Mean depth after (per sample) |
|---|---:|---:|---:|---:|
| Control | 190,289,556 | 179,065,714 | 94.10% | 59.7 M |
| Benzamidine | 191,782,388 | 139,419,904 | **72.70%** | 46.5 M |
| SKTI | 191,248,252 | 157,904,910 | 82.57% | 52.6 M |
| GORE3 | 176,144,980 | 164,311,914 | 93.28% | 54.8 M |

Both Benzamidine and SKTI lose 2 of 3 replicates to reduced depth (§3.6),
but the practical impact differs by contrast because the two groups play
different roles in the planned contrast matrix
(`docs/07_analise_rnaseq.md` §6.1):

**Table 4 | Depth asymmetry by planned Phase 5 contrast.**

| # | Contrast | Groups (survival) | Asymmetry | Role |
|---|---|---|---|---|
| 1 | GORE3 vs. Control | 93.3% vs. 94.1% | minimal | Main effect |
| 2 | GORE3 vs. Benzamidine | 93.3% vs. **72.7%** | **high** | 2nd priority — does GORE3 beat the classic S1-directed positive control? |
| 3 | GORE3 vs. SKTI | 93.3% vs. 82.6% | moderate–high | 3rd priority — **H4**, the proteolytic-compensation mechanistic test |
| 4 | SKTI vs. Control | 82.6% vs. 94.1% | moderate | Reproduces the known SKTI-compensation pattern |
| 5 | Benzamidine vs. Control | **72.7%** vs. 94.1% | **high** | Positive-control effect alone |
| 6 | GORE3 vs. (SKTI + Benzamidine pooled) | 93.3% vs. pooled reduced | **high** | Inherits both groups' depth loss |

Four of the six planned contrasts touch a reduced-depth group. Benzamidine
and SKTI carry the asymmetry into different parts of the scientific
argument: Benzamidine's loss weighs most on contrast #2, the head-to-head
efficacy comparison against the classical pharmacological standard;
SKTI's loss weighs most on contrast #3 (H4), the mechanistic test the
project's original hypotheses treat as central. Neither loss is severe
enough, in absolute depth (46.5–59.7 M reads/sample after trimming, all
above the original ~40 M target), to argue against proceeding — but it is
severe enough to require explicit reporting per-contrast, not folded into
a single dataset-wide caveat.

**Figure 4 | Trimming fully normalises base-call quality in every
affected library; it does not — and cannot — restore lost depth.**
Mean read-1 Phred quality by cycle, before (red) and after (dark blue)
fastp trimming (Set B parameters, §2.4), for Control_R1 (clean reference)
and the four libraries flagged in §3.2–3.6 (Benzamidine_R2,
Benzamidine_R3, SKTI_R1, SKTI_R2). Shaded band: the pre-declared cycles
44–90 window from Fig. 1. Both curves are computed by fastp from the same
input file (`read1_before_filtering`/`read1_after_filtering` quality
curves), avoiding cross-tool binning artefacts. Note SKTI_R1's visibly
milder pre-trim dip relative to the other three, consistent with it
falling below the binary threshold in §3.2 (Fig. 1) despite carrying the
second-highest adapter-dimer rate in the dataset (§3.6, Table 2). File:
`figuras/Figure4_blocoB_before_after.png`; code:
`codigo/fase1_blocoB/plot_before_after_trim.py`.

### 3.8 Loosening trimming parameters does not recover reads: Set B confirmed as an empirical equilibrium

None of the three candidate configurations (§2.4.1) recovered any reads in
any of the four affected libraries. The `adapter_dimer_reads` percentage
was **identical to two decimal places** between Set B and Sets C1/C2 in
every affected library (e.g., Benzamidine_R2: 31.19% under all three; SKTI_R2:
30.65% under Set B and C1, 30.65% under C2 as well), and survival differed
by 0.00 percentage points (one exception, SKTI_R2 under Set C2, at
−0.01 pp — within rounding noise). Set C3 (more restrictive overlap
detection) produced a small but directionally consistent *decrease* in
HISAT2 pilot mapping rate in three of the four libraries (e.g.,
Benzamidine_R2: 74.83%→74.81%), confirming the classification is sensitive
to this parameter in the expected direction — yet loosening it in the
opposite direction (Set C2) produced no corresponding gain. None of the
three candidates met the pre-declared decision criteria (§2.4.1); Set B
remains the production configuration
(`resultados/blocoC_param_sweep.csv`).

An incidental finding from the pilot alignment step: reads that do survive
trimming in the four affected libraries map at rates (74.8–79.4%)
comparable to the clean control library (78.0%) — the surviving data is
not degraded relative to the rest of the batch; what is lost is volume, not
quality of what remains. (Absolute mapping rates here, including the clean
control, fall below the project's declared >80% Phase 2 acceptance
threshold — expected and not directly comparable, since this pilot index
lacks splice-site annotation, which reduces sensitivity to exon-exon
junction-spanning reads; the real Phase 2 mapping rate, with an annotated
index on the complete 13 libraries, remains to be measured.)

**Interpretation:** read loss in these four libraries reflects a structural
property of the underlying molecules (biological insert short enough that
R1/R2 overlap almost entirely with adapter sequence) rather than an
overly conservative choice of quality or overlap-detection threshold — it is
invariant to the parameters tested here. The library-prep root cause
(§5, item 1) remains open, but is now further constrained: it is not an
artefact of a correctable trimming-parameter choice.

### 3.9 STAR outperforms HISAT2 in the aligner-selection pilot; full-batch alignment in progress at the time of writing

**Block A result (complete).** STAR outperformed HISAT2 in all five pilot
libraries by 9.33–13.02 percentage points, and was the only aligner to
clear the project's declared >80% mapping-rate acceptance threshold in any
sample (Table 5; `resultados/fase2_blocoA_star_vs_hisat2.csv`). Per the
pre-agreed decision rule (§2.5), **STAR alone was selected** for the
full-batch Block B run; HISAT2 was not run on the remaining eight
libraries.

**Table 5 | Aligner-selection pilot: STAR vs. HISAT2 (annotated index), five samples.**

| Sample | Label | STAR mapping (%) | HISAT2 mapping (%) | Difference (pp) | STAR ≥80%? | HISAT2 ≥80%? |
|---|---|---:|---:|---:|:---:|:---:|
| ID-1 | Control_R1 | 90.46 | 77.44 | 13.02 | yes | no |
| ID-9 | SKTI_R1 | 90.86 | 78.54 | 12.32 | yes | no |
| ID-10 | SKTI_R2 | 90.59 | 78.59 | 12.00 | yes | no |
| ID-8 | Benzamidine_R3 | 86.91 | 77.58 | 9.33 | yes | no |
| ID-7 | Benzamidine_R2 | 83.49 | 74.15 | 9.34 | yes | no |

**Block B result (complete, both tracks — 30 July 2026, 09:48).**

- **STAR track: 13/13 libraries complete.** Every sample's combined
  uniquely-mapped-plus-multi-mapped rate falls within 83.1–91.8%
  (Table 6) — **all 13 libraries clear the project's >80% acceptance
  threshold**, the lowest being ID-2 at 83.12%.
- **Subread track: 13/13 libraries complete**, including ID-1. The first
  execution attempt produced a segmentation fault on ID-1 (0-byte BAM)
  because this script and the STAR script were both requesting 16 threads
  concurrently on the server; ID-1 was re-run in isolation after the STAR
  track finished (no thread contention), completing in 3.1 minutes with
  26,065,883 uniquely mapped reads, 62,066 called indels, and a
  successfully indexed, non-corrupted BAM — resolving Limitation 9.

**Table 6 | STAR full-batch mapping rate, all 13 libraries (final).**

| Sample | Uniquely mapped (%) | Multi-mapped (%) | Combined (%) |
|---|---:|---:|---:|
| ID-12 | 87.23 | 4.56 | 91.79 |
| ID-18 | 86.78 | 3.90 | 90.68 |
| ID-16 | 86.96 | 3.53 | 90.49 |
| ID-1 | 82.35 | 7.90 | 90.25 |
| ID-14 | 85.93 | 4.14 | 90.07 |
| ID-9 | 83.44 | 6.51 | 89.95 |
| ID-10 | 82.78 | 6.98 | 89.76 |
| ID-15 | 84.59 | 4.17 | 88.76 |
| ID-3 | 83.11 | 4.84 | 87.95 |
| ID-5 | 81.88 | 5.42 | 87.30 |
| ID-8 | 78.83 | 7.41 | 86.24 |
| ID-7 | 78.48 | 5.37 | 83.85 |
| ID-2 | 74.59 | 8.53 | 83.12 |

*Machine-readable version: `resultados/fase2_blocoB_star_mapping_summary.csv`.
Full per-sample `Log.final.out` files: server,
`~/rnaseq-Anticarsia-GORE3/qc/fase2_blocoB_star/`.*

### 3.10 Cross-phase verification, full alignment statistics, and STAR–Subread comparison

Two automated checks were run before treating the Block B alignment as
verified, rather than relying on the mapping-rate summary alone (code:
`codigo/fase2_blocoB/analyze_blocoB2_alignment.py`). **(i)** STAR's
per-sample "Number of input reads" (read pairs) was cross-checked against
the independently recorded post-trimming read count from Phase 1 Block B
(`resultados/blocoB_trim_summary.csv`, `reads_after`, total R1+R2 reads):
`reads_after` equals `2 × input read pairs` exactly in all 13 libraries,
with no exceptions. This confirms STAR was run on the correct, matching
trimmed FASTQ file for every sample — a class of error (wrong or stale
input file) that would not be visible from the mapping-rate percentage
alone, since a mismatched-but-valid FASTQ would still produce a plausible
mapping rate. **(ii)** All 13 Subread log files contain the tool's own
"Completed successfully." marker, and none contain any error or warning
string (checked directly, not inferred from exit status).

**Splice-junction and error-rate statistics (STAR, Table 7; full data:
`resultados/fase2_blocoB_star_full_stats.csv`).** Total detected splice
junctions per sample range from 10,691,972 (Benzamidine_R2, the
lowest-depth library) to 29,884,406 (SKTI_R3); the fraction annotated
against the RS_2026_04 GTF is consistently high and narrow across all 13
libraries (98.9–99.6%), and the mismatch rate per base is uniform
(1.26–1.53%) — neither shows the kind of sample-specific outlier that
would indicate a contamination or reference-mismatch problem in any
individual library.

**Table 7 | STAR splice-junction and mismatch statistics, all 13 libraries.**

| Sample | Splices (total) | Splices annotated (%) | Mismatch rate (%) | Unmapped: too short (%) | Unmapped: other (%) |
|---|---:|---:|---:|---:|---:|
| ID-1 | 22,890,218 | 99.21 | 1.50 | 7.37 | 2.10 |
| ID-2 | 16,735,271 | 99.03 | 1.53 | 9.81 | 6.80 |
| ID-3 | 18,124,299 | 99.34 | 1.45 | 10.49 | 1.34 |
| ID-5 | 18,754,015 | 99.43 | 1.42 | 8.03 | 4.49 |
| ID-7 | 10,691,972 | 99.21 | 1.30 | 12.41 | 3.49 |
| ID-8 | 15,570,825 | 99.31 | 1.38 | 8.97 | 4.65 |
| ID-9 | 21,160,774 | 99.59 | 1.35 | 7.72 | 1.84 |
| ID-10 | 17,968,284 | 99.55 | 1.38 | 7.49 | 2.14 |
| ID-12 | 29,884,406 | 99.63 | 1.38 | 6.71 | 1.05 |
| ID-14 | 22,737,302 | 99.62 | 1.32 | 8.57 | 1.03 |
| ID-15 | 24,450,805 | 99.64 | 1.41 | 9.68 | 1.25 |
| ID-16 | 25,408,075 | 99.71 | 1.40 | 8.38 | 0.94 |
| ID-18 | 22,615,969 | 99.64 | 1.26 | 6.52 | 2.66 |

Unmapped reads are dominated by "too short" (6.5–12.4%) rather than
"other" (0.9–6.8%) in every library except ID-2 (9.81% too-short vs. 6.80%
other, its two largest unmapped categories being comparable in size,
unlike the rest of the batch) — "too short" is the STAR category expected
from residual short-insert/adapter-dimer molecules already characterized
in Phase 1 (§3.6), so this distribution is consistent with, not
additional to, the previously documented library-prep issue; it is not a
new finding.

**STAR vs. Subread — a real, expected gap, not smoothed over (Fig. 5).**
Subread's overall mapped rate (unique matches only; multi-mapping
explicitly disabled in `run_subread_align_full.sh`, matching the
production configuration's own documented rationale) is lower than STAR's
combined rate in every one of the 13 libraries, and falls **below the
project's 80% threshold in four samples**: Control_R2 (75.6%),
Benzamidine_R2 (78.3%), Benzamidine_R3 (79.1%) and Benzamidine_R1 (79.7%)
(full data: `resultados/fase2_blocoB_subread_stats.csv`). This is not
treated as a Subread alignment failure: the 80% acceptance threshold was
declared for the gene-expression quantification track (§2 — the role STAR
plays here), and Subread's lower rate is the direct, mechanistic
consequence of the tool being run without multi-mapping reporting, a
configuration chosen deliberately because Subread's role in this project
is exon-exon junction accuracy (§2.5), not maximizing the count of reads
assigned somewhere in the genome. Declared here rather than omitted,
because the numeric gap is real and reproducibly measured, even though
its explanation does not indicate a problem with the underlying sequence
data.

**Figure 5 | Full-batch mapping rate, STAR vs. Subread, all 13
libraries.** Grouped bar chart, STAR (blue; uniquely-mapped + multi-mapped
%) versus Subread (red; uniquely-mapped %, multi-mapping reporting
disabled by design), per library, ordered by treatment group and
biological replicate. Dashed line: the project's declared 80%
mapping-rate acceptance threshold. All 13 STAR bars clear the threshold;
four Subread bars (Control_R2, and all three Benzamidine replicates) fall
below it, for the reason stated above. File:
`figuras/Figure5_fase2_blocoB_mapping_rates.png`; code:
`codigo/fase2_blocoB/analyze_blocoB2_alignment.py`.

### 3.11 Gene- and transcript-level quantification: both tracks complete, mutually verified

**Gene-level counts (production track).** featureCounts assigned 70.2–84.4%
of reads to genes across all 13 libraries (Table 8;
`resultados/fase3_blocoC_featurecounts_summary.csv`), with no
sample-specific outlier — the range is consistent with the residual
unassigned categories already characterised in Phase 2 §3.10 (short/
adapter-dimer-derived reads that map but don't land cleanly within an
exon). This is the deliverable that feeds the group contrasts in Phase 5.

**Table 8 | featureCounts gene-assignment rate, all 13 libraries.**

| Sample | Assigned (%) |
|---|---:|
| GORE3_R3 | 84.40 |
| FatBody | 83.58 |
| GORE3_R1 | 82.88 |
| GORE3_R2 | 82.66 |
| SKTI_R3 | 81.48 |
| Benzamidine_R1 | 81.12 |
| Control_R3 | 80.40 |
| SKTI_R1 | 75.52 |
| Control_R1 | 75.03 |
| Benzamidine_R2 | 74.11 |
| SKTI_R2 | 74.01 |
| Benzamidine_R3 | 73.62 |
| Control_R2 | 70.15 |

**Figure 6 | featureCounts gene-level assignment rate, 13 libraries.**
Percentage of read pairs assigned to a gene by featureCounts (production
parameters, §2.6), by sample, ordered by treatment group and replicate.
File: `figuras/Figure6_fase3_blocoC_featurecounts_assigned.png`; code:
`codigo/fase3_blocoC/analyze_featurecounts.py`.

**Transcript-level quantification (support track for H1).** The
decoy-aware Salmon index quantified all 13 libraries with mapping rates
80.3–91.2%, within ±5.7 percentage points of STAR's combined mapping rate
in every sample (Table 9; `resultados/fase3_blocoD_salmon_mapping_summary.csv`)
— comfortably inside the ±10 pp consistency band declared in advance
(§2.6), given the two methods are structurally different (genome
alignment vs. decoy-aware selective alignment against transcriptome).

**Table 9 | Salmon vs. STAR mapping rate, all 13 libraries.**

| Sample | Salmon (%) | STAR (%) | Diff (pp) |
|---|---:|---:|---:|
| Control_R1 | 91.09 | 90.25 | +0.84 |
| Control_R2 | 88.83 | 83.12 | +5.71 |
| Control_R3 | 85.19 | 87.95 | −2.76 |
| Benzamidine_R1 | 91.18 | 87.30 | +3.88 |
| Benzamidine_R2 | 80.27 | 83.85 | −3.58 |
| Benzamidine_R3 | 88.26 | 86.24 | +2.02 |
| SKTI_R1 | 86.99 | 89.95 | −2.96 |
| SKTI_R2 | 87.31 | 89.76 | −2.45 |
| SKTI_R3 | 87.75 | 91.79 | −4.04 |
| GORE3_R1 | 86.80 | 90.07 | −3.27 |
| GORE3_R2 | 85.55 | 88.76 | −3.21 |
| GORE3_R3 | 86.73 | 90.49 | −3.76 |
| FatBody | 88.78 | 90.68 | −1.90 |

**Figure 7 | Salmon vs. STAR mapping rate, all 13 libraries.** Grouped bar
chart, STAR (blue) vs. Salmon decoy-aware (green), per library. File:
`figuras/Figure7_fase3_blocoD_salmon_vs_star_mapping.png`; code:
`codigo/fase3_blocoD/analyze_salmon_mapping.py`.

**tximport note (minor, disclosed):** the Salmon index was built without
`--keepDuplicates`, so 811 of 25,840 gffread-extracted transcripts with
byte-identical sequence to another transcript were collapsed to a single
representative during indexing (standard Salmon default behaviour, not a
project-specific error). This leaves 14,973 of 15,773 annotated genes with
at least one directly quantifiable transcript in the tximport gene-level
table (`resultados/fase3_blocoE_salmon_gene_counts.tsv`) — the remaining
~800 genes' sole transcript(s) were sequence-identical to another gene's
transcript and absorbed into that transcript's count. This affects only
the secondary transcript/isoform support track (§2.6), not the Phase 3
priority deliverable (Table 8, featureCounts gene counts, which counts
genomic exon overlap directly and is unaffected by transcript-sequence
duplication).

**An unrelated R parsing pitfall, found and fixed before this table was
generated:** the first `tximport` run reported "3,263 transcripts missing
from tx2gene" — traced to R's `read.table()` default quote-handling
treating a literal apostrophe in the RefSeq gene name `beta'COP` (coatomer
subunit, gene ID `gene-beta'COP`) as an unterminated opening quote,
silently truncating the 25,840-row `tx2gene.tsv` to 22,305 rows without an
error (only an easy-to-miss "EOF within quoted string" warning). Adding
`quote = ""` to the `read.table()` call (`codigo/fase3_blocoE/00_tximport_gore3.R`)
resolved it completely (0 missing transcripts, confirmed directly before
and after the fix).

**Cross-quantifier verification (Bloco F).** Three checks, all passing
(`resultados/fase3_blocoF_crosscheck.csv`;
`codigo/fase3_blocoF/analyze_fase3_consistency.py`): **(i)** featureCounts'
`Assigned` count never exceeds STAR's estimated uniquely-mapped read count
in any sample, consistent with featureCounts (no `-M`) only counting
single-alignment reads. **(ii)** Salmon and STAR mapping rates agree within
the pre-declared ±10 pp band in all 13 samples (Table 9). **(iii)**
Gene-level counts from the two independent quantification paths
(featureCounts, Table 8; Salmon+tximport, above) are strongly and
uniformly concordant — Spearman ρ = 0.983–0.988 across all 13 samples
(Table 10, Fig. 8), despite the two methods using structurally different
read-assignment logic (exon-overlap counting vs. probabilistic
transcript-level EM with GC-bias correction, aggregated to gene level).

**Table 10 | Gene-level concordance between featureCounts and Salmon+tximport, all 13 libraries.**

| Sample | Spearman ρ |
|---|---:|
| ID-1 | 0.987 |
| ID-2 | 0.985 |
| ID-3 | 0.986 |
| ID-5 | 0.988 |
| ID-7 | 0.983 |
| ID-8 | 0.985 |
| ID-9 | 0.986 |
| ID-10 | 0.984 |
| ID-12 | 0.986 |
| ID-14 | 0.985 |
| ID-15 | 0.986 |
| ID-16 | 0.985 |
| ID-18 | 0.988 |

**Figure 8 | Gene-level concordance: featureCounts vs. Salmon+tximport.**
Per-sample Spearman correlation between the two independent gene-count
matrices. File:
`figuras/Figure8_fase3_blocoF_featurecounts_vs_salmon_concordance.png`.

### 3.12 Differential expression: three contrasts, two independent engines

Both engines were fit on the same filtered gene set (15,773 → 11,833
genes, `rowSums(counts) >= 10`) and exposed the same three expected model
coefficients before any contrast was extracted (§2.7). Significant genes
(padj < 0.05, |log2FC| > 0.25, apeglm-shrunk) per contrast:

**Table 12 | Differentially expressed genes, R/DESeq2 vs. Python/PyDESeq2.**

| Contrast | DE — R/DESeq2 | DE — Python/PyDESeq2 |
|---|---:|---:|
| Benzamidine vs. Control | 255 (183 up / 72 down) | 185 (130 up / 55 down) |
| SKTI vs. Control | 3,985 (1,902 up / 2,083 down) | 3,986 (1,891 up / 2,095 down) |
| GORE3 vs. Control | 4,164 (2,020 up / 2,144 down) | 4,214 (2,037 up / 2,177 down) |

SKTI and GORE3 each move roughly a third of all testable genes (34–35%);
Benzamidine moves ~2%. This asymmetry is consistent with, but not proven
by, the read-depth asymmetry already established for Benzamidine (§3.7,
Table 11) — §3.14 tests this directly rather than asserting it.

### 3.13 Cross-engine concordance is high for effect size, lower for the significance boundary

**Table 13 | R×Python concordance of shrunk log2FC and DE-gene sets.**

| Contrast | Pearson *r* | Spearman *ρ* | Jaccard (DE sets) |
|---|---:|---:|---:|
| Benzamidine vs. Control | 0.989 | 0.992 | 0.692 |
| SKTI vs. Control | 0.998 | 0.999 | 0.932 |
| GORE3 vs. Control | 0.999 | 0.999 | 0.937 |

Effect-size correlation (log2FC) is excellent across all three contrasts.
Agreement on *which* genes cross the significance threshold is
noticeably weaker for Benzamidine (Jaccard 0.69) than for SKTI/GORE3
(≥0.93) — expected for the contrast with the fewest total DE genes, where
more calls sit near the significance boundary and are therefore more
sensitive to the disclosed offset asymmetry between engines (§2.7). This
is a dataset-specific empirical finding, not a published benchmark figure
(Muzellec et al. 2023 report no quantitative R-vs-Python concordance
number).

### 3.14 The Benzamidine result is disproportionately dependent on a single sample (ID-8)

Refitting Benzamidine-vs-Control at n=2 (excluding ID-8, the single-run
batch established in §3.3) collapses the DE-gene count from 255 to **6**
(intersection = 4 genes; Jaccard = 0.016). Effect-sign agreement on those
4 shared genes is complete (4/4). A drop from n=3 to n=2 is expected to
reduce power, but a >95% loss of DE calls is far larger than typical
power loss from one fewer replicate, and the PCA/UMAP visualisation
(Fig. 10–11, §3.15) shows ID-8 sitting apart from ID-5 and ID-7 within
the Benzamidine group itself in both projections. Taken together, this is
consistent with a large share of the "Benzamidine vs. Control" (n=3)
signal being driven specifically by ID-8, rather than by the group as a
whole — **not** proof that ID-8 is a pure technical artefact (it may
reflect genuine single-individual biological variation), but a real
fragility of this specific contrast that must qualify any downstream
interpretation of it, not be silently absorbed into the n=3 result.

### 3.15 Sample-level structure and DE-set overlap (Figures 10–13)

**Figure 10 | PCA of VST-normalised counts (`blind=FALSE`).** PC1 (51%
variance) separates Control (negative) from SKTI+GORE3 (positive);
Benzamidine splits, with ID-7 closer to Control and ID-5/ID-8 more
central. ID-8 is outlined in black. File: `figuras/fase5_blocoG/fig_pca.png`.

**Figure 11 | UMAP (non-linear reinforcement of the PCA, same VST
matrix).** ID-8 sits apart from ID-5/ID-7, which cluster together near
Control — direct visual support for §3.14. File:
`figuras/fase5_blocoG/fig_umap.png`.

**Figure 12 | Volcano and MA plots per contrast (apeglm-shrunk log2FC).**
Files: `figuras/fase5_blocoG/fig_volcano_*.png`,
`figuras/fase5_blocoG/fig_ma_*.png`.

**Figure 13 | UpSet plot of the three contrasts' DE-gene sets.** The
largest set (3,053 genes) is the SKTI∩GORE3-exclusive intersection
(Benzamidine excluded) — SKTI (a known inducer of proteolytic
compensation) and GORE3 share a broad transcriptional signature that
Benzamidine, with far fewer total DEGs, contributes little to. This is a
gene-set-overlap pattern, not evidence of a shared mechanism — functional
enrichment (Phase 7, not yet run) is required before any pathway-level
claim. File: `figuras/fase5_blocoG/fig_upset_de_genes.png`. A real
software-compatibility bug was found and worked around while building
this figure: `upsetplot` 0.9.0's `show_counts=True` raises a `TypeError`
under `matplotlib` 3.11.1 (isolated in a dedicated test this session);
count labels were instead added with matplotlib's native `bar_label()`.

An annotated heatmap of the union of each contrast's top 30 DE genes (77
unique genes, Grupo + Lote/batch annotation tracks) and a
`plotDispEsts` dispersion diagnostic are also available
(`figuras/fase5_blocoG/fig_heatmap_top_de.pdf`,
`fig_dispersion_estimates.pdf`) but are not reproduced inline here.

---

## 4. Discussion

*[Parcial — restrito ao que o Bloco A permite discutir; retomado quando a
FASE 2 (mapeamento) e FASE 5 (expressão diferencial) estiverem disponíveis.]*

The original observation (§3.2–3.3) was that the Benzamidine treatment
group is the most exposed to a raw-read quality defect (two of three
biological replicates affected, including the single worst library in the
dataset by both Q20 and Q30), while Control and GORE3 appeared unaffected
and SKTI had one of three replicates affected. §3.6 refines the group-level
picture: once adapter-dimer contamination is used as the operative metric
instead of the original mean-quality threshold, **SKTI is equally affected
(2 of 3 replicates: SKTI_R1 and SKTI_R2)**, not the 1-of-3 picture §3.2's
binary criterion suggested.

§3.4 upgraded this from "unresolved" to "characterized, GC-correlated,
still not fully explained mechanistically," identifying SKTI_R1 (ID-9) as
a fourth, graded-risk library alongside Benzamidine_R2, Benzamidine_R3 and
SKTI_R2. §3.6 sharpens this further: the risk is not primarily one of
*base-call quality* (which trimming fully corrects, Table 2) but of
**yield** — Benzamidine and SKTI each lose 2 of 3 replicates to
substantially reduced read depth (62–68% and 67–82% survival,
respectively) driven by adapter-dimer contamination correlated with GC
content, while Control and GORE3 keep close to full depth (91–97%) in all
replicates. For Phase 5 contrasts, this reframes the caveat from "quality
risk" to "statistical power asymmetry": Benzamidine-vs-Control and
SKTI-vs-Control contrasts will run on libraries with systematically lower
usable read depth in the treatment arm, which should be reported alongside
any differential expression result from those specific contrasts, not
folded silently into the general n=3 power limitation already declared in
`docs/04_viabilidade.md` §1.1.

§3.7 sharpens this once more, from a group-level to a contrast-level
statement: the two most consequential comparisons in the entire contrast
matrix — #2 (GORE3 vs. Benzamidine, the head-to-head test against the
pharmacological standard) and #3 (GORE3 vs. SKTI, hypothesis H4) — are
exactly the two carrying the largest depth asymmetry, for different
reasons tied to each group's role in the study's argument (Table 4).

**Planned next steps to actually resolve this, not merely flag it
(Phase 2 onward):**
1. ~~Re-verify per-contrast depth asymmetry after alignment, using mapping
   rate...~~ — **Done (Phase 3, Table 11).** Using featureCounts'
   gene-assigned read counts (the actually-usable quantity, not raw
   trimmed-read survival), the asymmetry **persists after alignment and
   quantification**: Benzamidine's mean assigned-read count is 77.2% of
   Control's, essentially unchanged in relative terms from the
   pre-alignment picture (§3.7). This is not a new finding reversing
   §3.7 — it is the promised confirmation that the risk is real at the
   quantity that actually matters for DESeq2 (usable counts), not an
   artefact of the trimming-survival proxy.

**Table 11 | Group-level assigned-read depth, post-quantification (Phase 3 recheck).**

| Group | Assigned reads (sum, n=3) | Mean/sample | % of Control mean |
|---|---:|---:|---:|
| Control | 133,724,241 | 44,574,747 | 100.0% |
| Benzamidine | 103,235,368 | 34,411,789 | 77.2% |
| SKTI | 123,806,115 | 41,268,705 | 92.6% |
| GORE3 | 131,731,502 | 43,910,501 | 98.5% |

*Code: `codigo/fase3_blocoF/recheck_depth_asymmetry.py`; data:
`resultados/fase3_blocoF_depth_asymmetry_recheck.csv`.*

2. When DESeq2 runs (Phase 5), inspect per-gene dispersion estimates
   separately for contrasts #2/#3/#5/#6 versus #1/#4, to check whether the
   depth asymmetry measurably degrades detection power for
   moderate-to-low-expression genes in the affected arms, rather than
   assuming it does from read counts alone. **Not yet done — depends on
   the fitted DESeq2 model (Phase 5).**
3. Decide, informed by (1)–(2) and not before, whether any
   depth-compensating step (e.g., down-weighting, or flagging genes with
   contrast-specific low power) is warranted for contrasts #2 and #3
   specifically.

**Batch/run confound (ID-8, Benzamidine_R3) — resolved decision, not a
correction.** §3.3 already established that ID-8 was sequenced on a
separate flow cell/lane (`LH00688`) from the other 12 libraries
(`LH00129`). This is a single-sample "batch" (n=1), not a balanced
multi-sample batch, and three independent lines of evidence converge on
**not applying formal batch correction**: **(i)** a source-code fact, not
a paper — the project's own cited ComBat-seq tool
(`zhang2020combat`, and verified directly in its source,
`github.com/zhangyuqing/ComBat-seq`) contains the guard `if(any(table(batch)<=1))
stop("ComBat-seq doesn't support 1 sample per batch yet")` — it refuses
to run on this design outright. **(ii)** `nygaard2016methods` (PMID
26272994) shows batch-correction methods that try to preserve group
differences can inflate false positives specifically under batch/group
imbalance — reinforcing that forcing correction here would be a risk,
not a fix. **(iii)** Including run/lane as a DESeq2 design covariate
instead (a common alternative) is also rejected: with one sample in the
minority level, that covariate coefficient would behave as an individual
intercept for ID-8, silently absorbing all of that sample's variation
(technical *and* biological) and reducing the effective Benzamidine
group to n=2 under the appearance of a correction. **Decision:** no
formal batch adjustment; the confound is disclosed here rather than
hidden, per `leek2010tackling`'s (PMID 20838408) minimum standard of
reporting processing group alongside biological variables. **Verification
run (Phase 5, §3.14):** re-running Benzamidine-vs-Control with and
without ID-8 shows conclusions change drastically — DE genes collapse
from 255 (n=3) to 6 (n=2), Jaccard 0.016 — confirming this confound is not
a minor caveat for this specific contrast. The head-to-head contrasts
that also involve Benzamidine (#2, GORE3 vs. Benzamidine) inherit this
fragility and have not yet been run — a reasonable general
sensitivity-analysis practice was applied here, not a named,
literature-validated protocol for this exact single-sample-batch scenario
(a targeted search found no such paper — reported as an analytical
decision, not a citation).

---

## 5. Limitations (declared explicitly, not smoothed over)

1. **Cause of the quality defect is now best explained by adapter-dimer
   contamination (§3.6), correlated with GC content, but the library-prep
   root cause is still not established.** We do not know *why* these four
   libraries produced more short-insert molecules — this would require
   insert-size / molarity QC data from the library-prep stage, which
   Macrogen's raw-data delivery does not include (see item 3 below). §3.8
   further constrains this: the read loss is not an artefact of the chosen
   fastp trimming/overlap-detection thresholds (an empirical parameter
   sweep found zero recoverable reads under three alternative
   configurations), so the root cause is upstream of trimming, in the
   library molecules themselves.
2. ~~**fastp trimming parameters are undecided.**~~ — **Resolved (§3.5,
   §2.4).** An empirical A/B test on two representative libraries showed
   the tested parameter (`--length_required 36` vs. `50`) makes negligible
   difference to survival; Set B (50, plus poly-G/poly-X trimming and
   overrepresentation analysis) was adopted for the full batch because it
   is strictly no worse and adds safety relevant to the confirmed NovaSeq
   X chemistry, at zero measured cost.
3. **Library insert/fragment size is not confirmed.** This is required for
   isoform-level analyses (Phase 6) and is not reported by Macrogen's raw
   data QC; it must be requested from the vendor or estimated
   post-alignment (`picard CollectInsertSizeMetrics`).
4. **Library strandedness direction (forward vs. reverse) is inferred, not
   confirmed.** The vendor-stated kit name indicates a stranded protocol,
   but the read orientation must still be confirmed empirically
   post-alignment (`salmon --libType A` or `RSeQC infer_experiment.py`).
5. **Five of the 17 tubes submitted to Macrogen were not delivered in this
   batch** (Control ID-4; Benzamidine ID-6; SKTI ID-11, ID-13; GORE3
   ID-17). Each treatment group still resolves to n=3 in this delivery, so
   this does not block analysis, but the reason for the gap (contingency
   replicates never sequenced, or a pending future delivery) is
   unconfirmed.
6. **A FastQC command-line deviation occurred and is disclosed for the
   record:** the `-d qc/tmp` flag failed ("Option d is ambiguous") during
   execution and the tool fell back to its default temp-file behaviour.
   All 26 outputs were nonetheless produced successfully and no stray or
   corrupted files were found on inspection (`codigo/fase1_blocoA/run_fastqc_multiqc.sh`
   carries this note inline).
7. **Statistical power is now asymmetric across treatment groups AND across
   planned contrasts, not just across the dataset as a whole (§3.7,
   Tables 3–4).** Benzamidine and SKTI each retain only 2 of 3 replicates
   at close-to-full read depth after trimming; Control and GORE3 do not
   have this problem. Four of six planned Phase 5 contrasts touch a
   reduced-depth group, and the two highest-impact ones (#2 GORE3 vs.
   Benzamidine; #3 GORE3 vs. SKTI/H4) are exactly the two carrying the
   largest asymmetry. This compounds, rather than duplicates, the general
   n=3 power limitation already declared in `docs/04_viabilidade.md` §1.1.
   **Not yet resolved — resolution plan stated in §4** (re-check with
   mapping rate and DESeq2 dispersion once Phases 2 and 5 run, not
   inferred from read counts alone).
8. **The >10% adapter-dimer colour cutoff in Fig. 3 is a post-hoc visual
   choice**, made after inspecting the bimodal distribution in panel (b),
   not a threshold declared before the data were seen (unlike the ΔQ > 5.0
   Phred threshold in Fig. 1). It is disclosed as such and should not be
   read as having the same evidentiary weight.
9. ~~**Phase 2 Block B is incomplete at the time of writing.**~~ —
   **Resolved (§3.9).** All 13 STAR samples and all 13 Subread samples
   (including the ID-1 re-run) completed successfully. The concurrency
   issue that caused the original segmentation faults (two 16-thread
   alignment jobs launched at once on the same server) was operational,
   not a property of the sequencing data, and did not recur once the
   ID-1 re-run was launched after the STAR track had already finished.
   Per-sample STAR mapping rates (Table 6) are exported to
   `resultados/fase2_blocoB_star_mapping_summary.csv`.
10. **Default featureCounts (no `-M -O --fraction`) will
    discard/undercount ambiguous reads at the trypsin-like
    serine-protease gene family specifically (Phase 3, §2.6).** Zytnicki
    (2017, PMID 28915787) reports that enabling multi-mapping/
    multi-overlap rescue "almost always provides biased results," so it
    is not used — but the family this project's secondary hypothesis H1
    concerns is exactly the one most exposed to this default's
    conservatism (close paralogs, ambiguous read assignment). **Not
    solved here** — deferred to Phase 9 (manual serine-protease family
    curation) for this specific gene set. No insect- or multigene-family
    benchmark was found in a targeted literature search; Kwon (2015, PMID
    26112470, *Xenopus*, abstract-only) is the nearest available
    evidence, not a resolution.
11. **Decoy-aware Salmon indexing (Phase 3, §2.6) is validated only in
    human and mouse.** Srivastava et al. (2020, PMID 32894187) tested 109
    real human datasets plus mouse simulations — no insect or
    non-model genome. The expected benefit (reduced spurious read
    assignment) is a reasonable extrapolation to *A. gemmatalis*, not an
    established fact for this species — same caveat structure as the
    Coxe et al. (2024) plant-to-insect transfer already declared above.
12. **No formal batch correction is applied for the ID-8 (Benzamidine_R3)
    single-sample sequencing-run confound (§4), and the sensitivity check
    now shows this matters a great deal.** ComBat-seq — this project's
    own cited batch-correction tool — refuses to run on a design with one
    sample in a batch level (verified directly in its source code); the
    alternative of a design covariate would silently behave as an
    individual intercept for that one sample. No formal correction is
    applied; the confound is disclosed here rather than hidden. The
    planned sensitivity check (§3.14) has now run: excluding ID-8 collapses
    Benzamidine-vs-Control DE genes from 255 to 6 (Jaccard 0.016). This
    does not prove ID-8 is a technical artefact rather than genuine
    biological variation, but it means the Benzamidine result as reported
    (n=3) should be read as **fragile and disproportionately
    single-sample-driven**, not as a robust group-level effect — this
    qualifies every downstream use of the Benzamidine contrast, including
    any future head-to-head comparison against GORE3 (#2 in the contrast
    matrix, §6.1).
13. **Cross-engine (R/DESeq2 vs. Python/PyDESeq2) agreement on log2 fold
    change is excellent (Pearson/Spearman ≥ 0.989 in all three contrasts,
    §3.13), but agreement on which genes cross the significance threshold
    is visibly weaker for Benzamidine (Jaccard 0.69) than for SKTI/GORE3
    (≥0.93).** This is expected given Benzamidine's much smaller total
    DE-gene count (more borderline calls) combined with the disclosed
    offset asymmetry between engines (§2.7) — not a contradiction of the
    high effect-size concordance, but a reminder that "the two engines
    agree" is a graded statement, not a binary one, and is weakest exactly
    where Limitation 12 already flags fragility.
14. **The SKTI∩GORE3 shared DE-gene signature (3,053 genes, Fig. 13) is a
    gene-set overlap, not evidence of a shared pathway or mechanism.** No
    functional enrichment has been run yet (Phase 7); attributing this
    overlap to any specific biological process before that analysis would
    be speculation, not a result.

---

## References

Andrews, S. *FastQC: A Quality Control Tool for High Throughput Sequence
Data* (Babraham Bioinformatics, 2010); https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

Chen, S. fastp 1.0: an ultra-fast all-round tool for FASTQ data quality
control and preprocessing. *iMeta* **4**, e70078 (2025).

Chen, S., Zhou, Y., Chen, Y. & Gu, J. fastp: an ultra-fast all-in-one FASTQ
preprocessor. *Bioinformatics* **34**, i884–i890 (2018).

Ewels, P., Magnusson, M., Lundin, S. & Käller, M. MultiQC: summarize
analysis results for multiple tools and samples in a single report.
*Bioinformatics* **32**, 3047–3048 (2016).

Coxe, K. et al. Benchmarking short-read RNA-seq alignment and assembly
tools for splicing analysis. (2024). PMID 38475429.

Srivastava, A., Malik, L., Sarkar, H., Zakeri, M., Almodaresi, F., Soneson,
C., Love, M. I., Kingsford, C. & Patro, R. Alignment and mapping
methodology influence transcript abundance estimation. *Genome Biology*
**21**, 239 (2020).

Zytnicki, M. mmquant: how to count multi-mapping reads? *BMC
Bioinformatics* **18**, 411 (2017).

Nygaard, V., Rødland, E. A. & Hovig, E. Methods that remove batch effects
while retaining group differences may lead to exaggerated confidence in
downstream analyses. *Biostatistics* **17**, 29–39 (2016).

Leek, J. T. et al. Tackling the widespread and critical impact of batch
effects in high-throughput data. *Nat. Rev. Genet.* **11**, 733–739
(2010).

Zhu, A., Ibrahim, J. G. & Love, M. I. Heavy-tailed prior distributions for
sequence count data: removing the noise and preserving large differences.
*Bioinformatics* **35**, 2084–2092 (2019). PMID 30395178.

Bourgon, R., Gentleman, R. & Huber, W. Independent filtering increases
detection power for high-throughput experiments. *PNAS* **107**,
9546–9551 (2010). PMID 20460310.

Muzellec, B., Teleńczuk, M., Cabeli, V. & Andreux, M. PyDESeq2: a python
package for bulk RNA-seq differential expression analysis.
*Bioinformatics* **39**, btad547 (2023). PMID 37669147.

Yang, Y. et al. Dimensionality reduction by UMAP reinforces sample
heterogeneity analysis in bulk transcriptomic data. *Cell Rep.* **36**,
109442 (2021). PMID 34320340.

Conway, J. R., Lex, A. & Gehlenborg, N. UpSetR: an R package for the
visualization of intersecting sets and their properties. *Bioinformatics*
**33**, 2938–2940 (2017). PMID 28645171.

---

## Reproducibility — code and data locations

| Item | Path |
|---|---|
| Sample mapping / replace-names table | `codigo/fase1_blocoA/samplesheet.tsv`, `samplesheet_replace_names.tsv` |
| FASTQ download + MD5 verification | `codigo/fase1_blocoA/download_and_verify.sh`, `md5sum.txt` |
| FastQC + MultiQC execution | `codigo/fase1_blocoA/run_fastqc_multiqc.sh` |
| QC analysis + figure generation (Fig. 1) | `codigo/fase1_blocoA/analyze_blocoA.py` |
| Position-resolved per-tile analysis + figure generation (Fig. 2) | `codigo/fase1_blocoA/per_tile_analysis.py` |
| fastp A/B parameter test | `codigo/fase1_blocoB/run_fastp_ab_test.sh`, `compare_ab_test.py` |
| Full-batch fastp trimming (13 samples, Set B) | `codigo/fase1_blocoB/run_fastp_full_trim.sh` |
| Post-trim summary + Fig. 3 generation | `codigo/fase1_blocoB/analyze_blocoB.py` |
| Before/after quality curves + Fig. 4 generation | `codigo/fase1_blocoB/plot_before_after_trim.py`, `extract_fig4_data.py` |
| Results (CSV, machine-readable) | `resultados/blocoA_results.csv`, `resultados/blocoA1_pertile_results.csv`, `resultados/blocoB_ab_test_comparison.csv`, `resultados/blocoB_trim_summary.csv`, `resultados/figure4_quality_curves.csv` |
| Exact tool/environment versions | `resultados/blocoA_ENV_VERSIONS.txt` |
| Figure 1 (300 dpi PNG) | `figuras/Figure1_blocoA_quality_dip.png` |
| Figure 2 (300 dpi PNG) | `figuras/Figure2_blocoA1_pertile_heatmap.png` |
| Figure 3 (300 dpi PNG) | `figuras/Figure3_blocoB_trimming.png` |
| Figure 4 (300 dpi PNG) | `figuras/Figure4_blocoB_before_after.png` |
| Trimmed FASTQ (26 files) | server: `~/rnaseq-Anticarsia-GORE3/trimmed/` (não versionado — dado grande, não vai ao git) |
| Full FastQC/MultiQC/fastp HTML reports | server: `~/rnaseq-Anticarsia-GORE3/qc/{pre_trim,post_trim,ab_test}/` (não versionado) |
| Aligner-selection pilot (STAR vs. HISAT2) scripts | `codigo/fase2_blocoA/` (`run_star_hisat2_subsample.sh`, `build_star_index.sh`, `build_hisat2_index_annotated.sh`, `convert_gff_to_gtf.sh`, `analyze_fase2_blocoA.py`) |
| Aligner-selection pilot results (Table 5) | `resultados/fase2_blocoA_star_vs_hisat2.csv` |
| Full-batch STAR mapping-rate summary (Table 6) | `resultados/fase2_blocoB_star_mapping_summary.csv` |
| Cross-phase verification, full STAR/Subread stats, Fig. 5 generation (Table 7) | `codigo/fase2_blocoB/analyze_blocoB2_alignment.py` → `resultados/fase2_blocoB_star_full_stats.csv`, `resultados/fase2_blocoB_subread_stats.csv` |
| Figure 5 (300 dpi PNG) | `figuras/Figure5_fase2_blocoB_mapping_rates.png` |
| Full-batch alignment scripts (STAR + Subread) | `codigo/fase2_blocoB/` (`run_alignment_full.sh`, `run_subread_align_full.sh`, `check_strandedness.sh`, `analyze_strandedness.py`) |
| STAR/Subread BAMs, logs (13 libraries, complete) | server: `~/rnaseq-Anticarsia-GORE3/{bam/star,bam/subread,qc/fase2_blocoB_star,qc/fase2_blocoB_subread}/` (não versionado — dado grande) |
| GTF gene_id fix + strand decision (Phase 3 Block A) | `codigo/fase3_blocoA/fix_gtf_missing_geneid.sh`, `decide_libtype.py` → `resultados/fase3_blocoA_strand_decision.csv` |
| Tool audit (Phase 3 Block B) | `codigo/fase3_blocoB/check_tools.sh` → `resultados/fase3_blocoB_env_check.txt` |
| Production gene-level counts (Phase 3 Block C) | `codigo/fase3_blocoC/run_featurecounts_genelevel.sh`, `analyze_featurecounts.py` → `resultados/fase3_blocoC_featurecounts_summary.csv`, `resultados/fase3_blocoC_gene_counts.txt` |
| Figure 6 (300 dpi PNG) | `figuras/Figure6_fase3_blocoC_featurecounts_assigned.png` |
| Decoy-aware Salmon index + quant (Phase 3 Block D) | `codigo/fase3_blocoD/build_salmon_decoy_index.sh`, `run_salmon_quant_full.sh`, `analyze_salmon_mapping.py` |
| tximport adaptation (Phase 3 Block E) | `codigo/fase3_blocoE/build_tx2gene.py`, `build_samplesheet.py`, `00_tximport_gore3.R` |
| Cross-quantifier verification (Phase 3 Block F) | `codigo/fase3_blocoF/analyze_fase3_consistency.py` → `resultados/fase3_blocoF_crosscheck.csv` |
| Depth-asymmetry post-quantification recheck (Table 11) | `codigo/fase3_blocoF/recheck_depth_asymmetry.py` → `resultados/fase3_blocoF_depth_asymmetry_recheck.csv` |
| Salmon index/quant, tximport outputs (large) | server: `~/rnaseq-Anticarsia-GORE3/{salmon_index_decoy,salmon}/` (não versionado — dado grande) |
| Phase 5 keepDuplicates index rebuild + requant (Block B) | `codigo/fase5_blocoB/build_salmon_index_keepdup.sh`, `run_salmon_quant_keepdup.sh` |
| Phase 5 tximport rebuild + DESeqDataSet construction (Block B) | `codigo/fase5_blocoB/build_dds_tximport.R` |
| Coverage consistency check + Figure 9 | `codigo/fase5_blocoB/analyze_keepdup_coverage.py` → `resultados/fase5_blocoB_keepdup_coverage.csv` |
| Figure 9 (300 dpi PNG) | `figuras/Figure9_fase5_blocoB_keepdup_coverage.png` |
| R DESeq2 model (Block C1) | `codigo/fase5_blocoC/run_deseq2.R` |
| Python PyDESeq2 model (Block C2) | `codigo/fase5_blocoC/run_pydeseq2.py` |
| Salmon keepDuplicates index/quant, tximport gene counts export (large) | server: `~/rnaseq-Anticarsia-GORE3/{salmon_index_decoy_keepdup,salmon_keepdup}/` (não versionado — dado grande) |
| Contrast extraction, apeglm shrinkage (Block D) | `codigo/fase5_blocoD/extract_contrasts_deseq2.R`, `apply_threshold_pydeseq2.py` → `resultados/fase5_blocoD/*_sig.csv` |
| Cross-engine comparison (Block E) | `codigo/fase5_blocoE/compare_r_python.py` → `resultados/fase5_blocoE/cross_engine_comparison.csv` |
| ID-8 sensitivity check (Block F) | `codigo/fase5_blocoF/sensitivity_id8.R` → `resultados/fase5_blocoF/sensitivity_id8_summary.csv` |
| Figures — PCA, dispersion, volcano, MA, heatmap (Block G, R) | `codigo/fase5_blocoG/figures_r.R` |
| Figures — UMAP, UpSet (Block G, Python) | `codigo/fase5_blocoG/figures_python.py` |
| Figures 10–13 (PDF + 300 dpi PNG) | `figuras/fase5_blocoG/` |
