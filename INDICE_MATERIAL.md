---
Documento vivo — atualizado a cada bloco de análise concluído.
Função: mapa único de tudo que existe hoje (figuras, tabelas, texto,
código, dado-fonte), para uso na geração futura do artigo em Word e da
apresentação em PowerPoint. Nada aqui substitui `artigo.md`/`artigo_pt.md`
— é o índice de orquestração que aponta pra eles.
Última atualização: 01/08/2026 (FASE 6 A-F concluída, ainda não commitada).
---

# Índice de material — Pós-doc GORE3 / RNA-Seq

## Status

| Fase | Bloco | Status | Seção no artigo |
|---|---|---|---|
| FASE 1 | A — QC bruto (FastQC+MultiQC) | ✅ concluído | §2.3, §3.1–3.3 |
| FASE 1 | A.1 — fechamento da lacuna per-tile | ✅ concluído | §3.4 |
| FASE 1 | B — trimagem (fastp, teste A/B + lote completo) | ✅ concluído | §2.4, §3.5–3.7 |
| FASE 1 | C — equilíbrio de trimagem (sweep de parâmetros + piloto HISAT2) | ✅ concluído | §2.4.1, §3.8 |
| FASE 1 | Abstract / Introdução do artigo | ⏳ pendente | aguarda FASE 5 (não preenchido por projeção) |
| FASE 2 | A — piloto de seleção de alinhador (STAR vs. HISAT2, 5 amostras) | ✅ concluído | §2.5, §3.9 |
| FASE 2 | B — alinhamento completo, via STAR (13/13 amostras) | ✅ concluído | §2.5, §3.9 |
| FASE 2 | B — alinhamento completo, via Subread/splicing (13/13 amostras) | ✅ concluído | §2.5, §3.9 |
| FASE 2 | Verificação entre fases + estatísticas completas + Fig. 5 | ✅ concluído | §3.10 |
| FASE 2 | Confirmação empírica de strandedness (forward/reverse) | ✅ concluído (executado na FASE 3 Bloco A) | §4 |
| FASE 3 | A — strandedness confirmado (reverse/ISR) + correção de GTF (gene_id ausente) | ✅ concluído | §4 |
| FASE 3 | B — auditoria de ferramentas (gffread/featureCounts/salmon) | ✅ concluído | §4 |
| FASE 3 | C — featureCounts produção (gene-level, prioritário) | ✅ concluído | §4 |
| FASE 3 | D — Salmon decoy-aware (índice + quant, apoio a H1) | ✅ concluído | §4, §3.11 |
| FASE 3 | E — tximport adaptado (tx2gene do GTF real) | ✅ concluído | §4, §3.11 |
| FASE 3 | F — verificação cruzada entre quantificadores | ✅ concluído (ρ=0,983–0,988) | §4, §3.11 |
| FASE 4 | Decisão de correção de lote — NÃO aplicar ComBat-seq (lote de amostra única) | ✅ decidido | §4 (Discussão), §5 item 12 |
| FASE 5 | A — bibliografia + Zotero (7 citações, antes da execução) | ✅ concluído | §2.7 |
| FASE 5 | B — rebuild Salmon --keepDuplicates + tximport (cobertura 100%) | ✅ concluído | §2.7 |
| FASE 5 | C — modelo DESeq2 (R) + PyDESeq2 (Python) | ✅ concluído (11.833 genes pós-filtro, 3 coeficientes confirmados) | §2.7, §3.12 |
| FASE 5 | D — extrair 3 contrastes vs. Controle, R+Python (apeglm, log2FC=0,25) | ✅ concluído | §2.7, §3.12 |
| FASE 5 | E — verificação cruzada R×Python | ✅ concluído (Pearson/Spearman ≥0,989; Jaccard DE 0,69–0,94) | §2.7, §3.13 |
| FASE 5 | F — checagem de sensibilidade ID-8 | ✅ concluído (⚠️ Benzamidina 255→6 DE sem ID-8) | §2.7, §3.14, §5 item 12 |
| FASE 5 | G — figuras modernas (PCA+UMAP, volcano, MA, heatmap, UpSet) | ✅ concluído | §2.7, §3.15 |
| FASE 5 | H — documentação + commit | ✅ concluído (commit `1daaf72`) | — |
| FASE 5 | Cabeça-a-cabeça (#2 GORE3×Benzamidina, #3 GORE3×SKTI/H4, #6 agrupado) | ⏳ escopo movido para outro artigo (decisão do usuário) | §6.1 |
| FASE 7 | A — bibliografia + Zotero (8 citações, antes da execução) | ✅ concluído (PHILHARMONIC identificado como preprint) | §2.8 |
| FASE 7 | B — proteoma representativo + Pfam/HMMER | ✅ concluído (14.238 genes, 83,1% com domínio) | §2.8, §3.16 |
| FASE 7 | C — eggNOG-mapper (GO/KEGG) | ✅ concluído (94,8% hit, 60,7% GO, 56,8% KEGG) | §2.8, §3.16 |
| FASE 7 | D — InterProScan 6 (Nextflow, Docker) | ✅ concluído (95,2% hit, 74,9% GO) | §2.8, §3.16 |
| FASE 7 | E — PHILHARMONIC (opcional) | ⏳ não rodado (preprint, escopo/tempo) | §5 item 17 |
| FASE 7 | F — consolidação multi-fonte (união GO) | ✅ concluído (80,1% cobertura combinada, Jaccard 0,692) | §2.8, §3.16 |
| FASE 7 | G — enriquecimento GO/KEGG/Pfam, dois motores | ✅ concluído | §2.8, §3.17 |
| FASE 7 | H — verificação cruzada R×Python (GO) | ✅ concluído (⚠️ gseapy sistematicamente mais permissivo) | §2.8, §3.17 |
| FASE 7 | I — comparação entre tratamentos (compareCluster, Venn, UpSet) | ✅ concluído (86% termos GORE3 também em SKTI) | §2.8, §3.18 |
| FASE 7 | J — figuras finais | ✅ concluído (geradas junto ao Bloco I) | §3.18 |
| FASE 7 | K — documentação + commit | ✅ concluído (esta sessão) | — |
| FASE 6 | A — bibliografia (4 citações, antes da execução) | ✅ concluído (já tinham bib+ficha, faltava só Zotero) | §2.9 |
| FASE 6 | B — rMATS-turbo, 3 contrastes | ✅ concluído (⚠️ 1ª tentativa deu 0 eventos — BAM Subread sem splice, corrigido com `subjunc`) | §2.9, §3.19 |
| FASE 6 | C — MAJIQ build+psi-coverage+deltapsi, 3 contrastes | ✅ concluído (instalação exigiu 5 correções reais; `majiq weights` não existe na v3, `moccasin` não aplicado) | §2.9, §3.19 |
| FASE 6 | D — convergência rMATS×MAJIQ | ✅ concluído (Jaccard 0,05-0,10, baixa) | §3.19 |
| FASE 6 | E — cruzamento splicing×DE(FASE5)×Pfam-tripsina(FASE7) | ✅ concluído (sobreposição sig. p<3,4e-4, mas maioria do splicing não é DE) | §3.19 |
| FASE 6 | F — figuras (UpSet genes splicing, splicing×DE) | ✅ concluído | §3.19 |
| FASE 8–10 | Ver `docs/07_analise_rnaseq.md` | não iniciado | — |

## Figuras

| # | Arquivo | O que mostra | Seção | Código-fonte | Dado-fonte (CSV) |
|---|---|---|---|---|---|
| 1 | `figuras/Figure1_blocoA_quality_dip.png` | Queda de qualidade (ΔQ ciclos 44–90) por amostra, raw | §3.2 | `codigo/fase1_blocoA/analyze_blocoA.py` | `resultados/blocoA_results.csv` |
| 2 | `figuras/Figure2_blocoA1_pertile_heatmap.png` | Heatmap tile×ciclo, ID-1 (limpa) vs. ID-8 (pior) | §3.4 | `codigo/fase1_blocoA/per_tile_analysis.py` | `resultados/blocoA1_pertile_results.csv` |
| 3 | `figuras/Figure3_blocoB_trimming.png` | (a) sobrevivência pós-trim; (b) adapter-dimer % vs. GC% | §3.6 | `codigo/fase1_blocoB/analyze_blocoB.py` | `resultados/blocoB_trim_summary.csv` |
| 4 | `figuras/Figure4_blocoB_before_after.png` | Curvas de qualidade antes/depois da trimagem, 5 amostras | §3.7 | `codigo/fase1_blocoB/plot_before_after_trim.py` | `resultados/figure4_quality_curves.csv` |
| 5 | `figuras/Figure5_fase2_blocoB_mapping_rates.png` | Taxa de mapeamento STAR vs. Subread, 13 bibliotecas, agrupado por tratamento | §3.10 | `codigo/fase2_blocoB/analyze_blocoB2_alignment.py` | `resultados/fase2_blocoB_star_full_stats.csv`, `resultados/fase2_blocoB_subread_stats.csv` |
| 6 | `figuras/Figure6_fase3_blocoC_featurecounts_assigned.png` | % de reads atribuídos a genes (featureCounts), 13 bibliotecas | §3.11 | `codigo/fase3_blocoC/analyze_featurecounts.py` | `resultados/fase3_blocoC_featurecounts_summary.csv` |
| 7 | `figuras/Figure7_fase3_blocoD_salmon_vs_star_mapping.png` | Taxa de mapeamento Salmon vs. STAR, 13 bibliotecas | §3.11 | `codigo/fase3_blocoD/analyze_salmon_mapping.py` | `resultados/fase3_blocoD_salmon_mapping_summary.csv` |
| 8 | `figuras/Figure8_fase3_blocoF_featurecounts_vs_salmon_concordance.png` | Concordância Spearman gene-a-gene, featureCounts vs. Salmon+tximport | §3.11 | `codigo/fase3_blocoF/analyze_fase3_consistency.py` | `resultados/fase3_blocoF_crosscheck.csv` |
| 9 | `figuras/Figure9_fase5_blocoB_keepdup_coverage.png` | Cobertura gênica do tximport antes/depois de --keepDuplicates (94,9%→100%) | §2.7 | `codigo/fase5_blocoB/analyze_keepdup_coverage.py` | `resultados/fase5_blocoB_keepdup_coverage.csv` |
| 10 | `figuras/fase5_blocoG/fig_pca.png` | PCA (VST, blind=FALSE), 4 grupos, ID-8 marcado | §3.15 | `codigo/fase5_blocoG/figures_r.R` | `resultados_server/fase5_blocoG/vst_normalized_matrix.csv` (servidor) |
| 11 | `figuras/fase5_blocoG/fig_umap.png` | UMAP, mesma matriz VST, reforço não-linear da PCA | §3.15 | `codigo/fase5_blocoG/figures_python.py` | idem |
| 12 | `figuras/fase5_blocoG/fig_volcano_*.png` + `fig_ma_*.png` (3 contrastes cada) | Volcano e MA plot por contraste, log2FC encolhido | §3.15 | `codigo/fase5_blocoG/figures_r.R` | `resultados/fase5_blocoD/deseq2_*_all.csv` |
| 13 | `figuras/fase5_blocoG/fig_upset_de_genes.png` | Interseção dos 3 conjuntos de DEGs (SKTI∩GORE3=3.053) | §3.15 | `codigo/fase5_blocoG/figures_python.py` | `resultados/fase5_blocoD/deseq2_*_sig.csv` |
| — | `figuras/fase5_blocoG/fig_heatmap_top_de.pdf`, `fig_dispersion_estimates.pdf` | Heatmap top DE anotado (Grupo+Lote) e diagnóstico de dispersão DESeq2 | §3.15 | `codigo/fase5_blocoG/figures_r.R` | idem |
| 14 | `figuras/fase7_blocoI/fig_compareCluster_dotplot.png` | Dotplot GO comparativo entre os 3 tratamentos (compareCluster) | §3.18 | `codigo/fase7_blocoI/compare_clusters_r.R` | `resultados/fase7_blocoI/compareCluster_GO_results.csv` |
| 15 | `figuras/fase7_blocoI/fig_upset_go_terms.png` | UpSet dos termos GO significativos por contraste (não genes) | §3.18 | `codigo/fase7_blocoI/venn_upset_go_python.py` | `resultados/fase7_blocoG/clusterprofiler_GO_*.csv` |
| 16 | `figuras/fase7_blocoI/fig_venn3_de_genes.png` | Venn de 3 vias dos genes DE (checagem cruzada com UpSet da FASE 5) | §3.18 | `codigo/fase7_blocoI/venn_upset_go_python.py` | `resultados/fase5_blocoD/deseq2_*_sig.csv` |
| — | `figuras/fase7_blocoI/fig_cnetplot_*.png` (3 contrastes) | Rede gene-conceito, top 10 termos GO por contraste | §3.18 | `codigo/fase7_blocoI/compare_clusters_r.R` | idem |
| 17 | `figuras/fase6_blocoF/fig_upset_splicing_genes.png` | UpSet dos genes com splicing significativo (rMATS∪MAJIQ) entre os 3 contrastes | §3.19 | `codigo/fase6_blocoF/figures_splicing.py` | `resultados/fase6_blocoD/{rmats,majiq}_sig_*.csv` |
| 18 | `figuras/fase6_blocoF/fig_splicing_vs_de_overlap.png` | Sobreposição splicing×DE por contraste (barras empilhadas) | §3.19 | `codigo/fase6_blocoF/figures_splicing.py` | `resultados/fase6_blocoE/cross_reference_summary.csv` |

Todas em PNG 300 dpi, legenda 100% em inglês no `artigo.md` (padrão
Nature: `**Figure N |** frase-título...`), traduzida fielmente no
`artigo_pt.md`. Prontas para inserção direta em Word/PowerPoint sem
reprocessamento.

## Tabelas

| # | Título | Seção | Dado-fonte |
|---|---|---|---|
| 1 | Raw-read summary statistics and quality-window test, by sample | §3.2 | `resultados/blocoA_results.csv` |
| 2 | Post-trimming outcome by sample, Set B parameters | §3.6 | `resultados/blocoB_trim_summary.csv` |
| 3 | Post-trimming depth by treatment group | §3.7 | `resultados/blocoB_trim_summary.csv` (agregado por grupo) |
| 4 | Depth asymmetry by planned Phase 5 contrast | §3.7 | `resultados/blocoB_trim_summary.csv` (agregado) + `docs/07_analise_rnaseq.md` §6.1 (lista de contrastes) |
| 5 | Aligner-selection pilot: STAR vs. HISAT2 (5 amostras) | §3.9 | `resultados/fase2_blocoA_star_vs_hisat2.csv` |
| 6 | STAR full-batch mapping rate, 13 bibliotecas | §3.9 | `resultados/fase2_blocoB_star_mapping_summary.csv` |
| 7 | STAR splice-junction and mismatch statistics, 13 bibliotecas | §3.10 | `resultados/fase2_blocoB_star_full_stats.csv` |
| 8 | featureCounts gene-assignment rate, 13 bibliotecas | §3.11 | `resultados/fase3_blocoC_featurecounts_summary.csv` |
| 9 | Salmon vs. STAR mapping rate, 13 bibliotecas | §3.11 | `resultados/fase3_blocoD_salmon_mapping_summary.csv` |
| 10 | Gene-level concordance featureCounts vs. Salmon+tximport, 13 bibliotecas | §3.11 | `resultados/fase3_blocoF_crosscheck.csv` |
| 11 | Group-level assigned-read depth, post-quantification recheck | §4 (Discussion) | `resultados/fase3_blocoF_depth_asymmetry_recheck.csv` |
| 12 | Differentially expressed genes, R/DESeq2 vs. Python/PyDESeq2, 3 contrastes | §3.12 | `resultados/fase5_blocoD/{deseq2,pydeseq2}_*_sig.csv` |
| 13 | Cross-engine (R×Python) concordance: Pearson/Spearman de log2FC, Jaccard de DE | §3.13 | `resultados/fase5_blocoE/cross_engine_comparison.csv` |
| 14 | Cobertura de anotação funcional por fonte (Pfam, eggNOG, InterProScan6, união) | §3.16 | `resultados/fase7_blocoB/pfam_coverage_summary.csv`, `resultados/fase7_blocoC/eggnog_coverage_summary.csv`, `resultados/fase7_blocoF/annotation_coverage_summary.csv` |
| 15 | Enriquecimento GO/KEGG/Pfam significativo por contraste e método | §3.17 | `resultados/fase7_blocoG/*.csv` |
| 16 | Concordância cruzada R×Python (GO), Jaccard por contraste | §3.17 | `resultados/fase7_blocoH/cross_engine_go_comparison.csv` |
| 17 | Eventos de splicing significativos por contraste, rMATS-turbo vs. MAJIQ | §3.19 | `resultados/fase6_blocoD/{rmats,majiq}_sig_*.csv` |

Todas as tabelas do artigo são texto Markdown gerado a partir dos CSVs
acima — nenhum número foi digitado à mão sem conferência contra a fonte
(checagem de veracidade feita em 28/07/2026, ver histórico da sessão).

## Texto

| Arquivo | Idioma | Papel |
|---|---|---|
| `artigo.md` | Inglês | Canônico — versão a ser usada como base do Word/PPTX final |
| `artigo_pt.md` | Português | Tradução fiel, sincronizada a cada atualização — não é resumo |

## Código (reprodutibilidade)

| Diretório | Conteúdo |
|---|---|
| `codigo/fase1_blocoA/` | Download+md5 (`download_and_verify.sh`, `md5sum.txt`), samplesheets, FastQC+MultiQC (`run_fastqc_multiqc.sh`), análise+Fig.1 (`analyze_blocoA.py`), per-tile+Fig.2 (`per_tile_analysis.py`) |
| `codigo/fase1_blocoB/` | Teste A/B fastp (`run_fastp_ab_test.sh`, `compare_ab_test.py`), trimagem completa (`run_fastp_full_trim.sh`), resumo+Fig.3 (`analyze_blocoB.py`), curvas antes/depois+Fig.4 (`plot_before_after_trim.py`, `extract_fig4_data.py`) |
| `codigo/fase1_blocoC/` | Subamostragem (`subsample_reads.sh`), sweep de parâmetros fastp Sets B/C1/C2/C3 (`run_fastp_paramsweep.sh`), índice HISAT2 piloto (`build_hisat2_index_pilot.sh`), alinhamento piloto (`run_hisat2_pilot.sh`), análise+critério de decisão (`analyze_blocoC.py` → `resultados/blocoC_param_sweep.csv`) |
| `codigo/fase2_blocoA/` | Índices anotados STAR/HISAT2 (`build_star_index.sh`, `build_hisat2_index_annotated.sh`, `convert_gff_to_gtf.sh`), piloto STAR×HISAT2 nas 5 amostras (`run_star_hisat2_subsample.sh`), análise+critério de decisão+Tabela 5 (`analyze_fase2_blocoA.py` → `resultados/fase2_blocoA_star_vs_hisat2.csv`) |
| `codigo/fase2_blocoB/` | Alinhamento completo STAR, 13 amostras, resumível (`run_alignment_full.sh`), alinhamento completo Subread/splicing, 13 amostras, resumível (`run_subread_align_full.sh`), verificação entre fases + estatísticas completas + Fig.5 + Tabelas 6-7 (`analyze_blocoB2_alignment.py`), confirmação de strandedness pós-alinhamento (`check_strandedness.sh`, `analyze_strandedness.py`) — **executado na FASE 3 Bloco A** |
| `codigo/fase3_blocoA/` | Correção de GTF sem gene_id (`fix_gtf_missing_geneid.sh`), formalização da decisão de strand (`decide_libtype.py` → `resultados/fase3_blocoA_strand_decision.csv`) |
| `codigo/fase3_blocoB/` | Auditoria de ferramentas (`check_tools.sh` → `resultados/fase3_blocoB_env_check.txt`) |
| `codigo/fase3_blocoC/` | featureCounts produção sem `-M -O --fraction` (`run_featurecounts_genelevel.sh`), resumo+Fig.6 (`analyze_featurecounts.py`) |
| `codigo/fase3_blocoD/` | Índice Salmon decoy-aware (`build_salmon_decoy_index.sh`), quant resumível 13 amostras (`run_salmon_quant_full.sh`), resumo+Fig.7 (`analyze_salmon_mapping.py`) |
| `codigo/fase3_blocoE/` | tx2gene do GTF real (`build_tx2gene.py`), samplesheet (`build_samplesheet.py`), tximport adaptado (`00_tximport_gore3.R`) |
| `codigo/fase3_blocoF/` | Verificação cruzada featureCounts×Salmon+tximport+STAR, 3 checagens+Fig.8 (`analyze_fase3_consistency.py`); reverificação de assimetria de profundidade pós-quantificação, Tabela 11 (`recheck_depth_asymmetry.py`) |
| `codigo/fase5_blocoB/` | Rebuild do índice Salmon com `--keepDuplicates` (`build_salmon_index_keepdup.sh`), requant 13 amostras (`run_salmon_quant_keepdup.sh`), rebuild tximport + `DESeqDataSetFromTximport` (`build_dds_tximport.R`), checagem de consistência+Fig.9 (`analyze_keepdup_coverage.py`) |
| `codigo/fase5_blocoC/` | Modelo DESeq2 em R (`run_deseq2.R`) e PyDESeq2 em Python (`run_pydeseq2.py`) — rodados sobre dado real (11.833 genes pós-filtro, 3 coeficientes confirmados) |
| `codigo/fase5_blocoD/` | Extração dos 3 contrastes com shrinkage apeglm (`extract_contrasts_deseq2.R`) e aplicação do mesmo limiar (log2FC=0,25) sobre o log2FC já encolhido do PyDESeq2 (`apply_threshold_pydeseq2.py`) |
| `codigo/fase5_blocoE/` | Verificação cruzada R×Python — Pearson/Spearman + Jaccard (`compare_r_python.py`) |
| `codigo/fase5_blocoF/` | Checagem de sensibilidade ID-8, refit n=2 vs. n=3 (`sensitivity_id8.R`) |
| `codigo/fase5_blocoG/` | Figuras: PCA+dispersão+volcano+MA+heatmap em R (`figures_r.R`), UMAP+UpSet em Python (`figures_python.py`) — paleta validada via skill `dataviz` |
| `codigo/fase7_blocoB/` | Seleção de proteína representativa por gene (`select_representative_protein.py`), hmmscan+cobertura Pfam (`analyze_pfam_coverage.py`) |
| `codigo/fase7_blocoC/` | Cobertura GO/KEGG do eggNOG-mapper (`analyze_eggnog_coverage.py`) |
| `codigo/fase7_blocoF/` | Consolidação multi-fonte da anotação GO (`consolidate_annotation.py`) |
| `codigo/fase7_blocoG/` | Enriquecimento GO/KEGG em R (`run_enrichment_clusterprofiler.R`) e Python (`run_enrichment_gseapy.py`), Fisher exato de domínios Pfam (`run_pfam_enrichment.py`) |
| `codigo/fase7_blocoH/` | Verificação cruzada R×Python do enriquecimento GO (`compare_enrichment_r_python.py`) |
| `codigo/fase7_blocoI/` | compareCluster+dotplot+cnetplot em R (`compare_clusters_r.R`), Venn+UpSet em Python (`venn_upset_go_python.py`) |
| `codigo/fase6_blocoB/` | Realinhamento `subjunc` corrigindo a via Subread sem splice da FASE 2 (`run_subjunc_realign.sh`), rMATS-turbo 3 contrastes (`run_rmats_turbo.sh`) |
| `codigo/fase6_blocoC/` | Samplesheet MAJIQ (`experiments.tsv`), build do splicegraph (`run_majiq_build.sh`), psi-coverage+deltapsi 3 contrastes (`run_majiq_psi_deltapsi.sh`) |
| `codigo/fase6_blocoD/` (via `extract_sig_genes_fase6.py`, servidor) | Extração de genes significativos por contraste (rMATS/MAJIQ) + convergência (Jaccard) |
| `codigo/fase6_blocoE/` | Cruzamento splicing×DE(FASE5)×Pfam-tripsina(FASE7), com teste hipergeométrico de enriquecimento (`cross_reference_splicing_de.py`) |
| `codigo/fase6_blocoF/` | Figuras UpSet + splicing×DE, paleta reaproveitada da FASE 5/7 (`figures_splicing.py`) |

Todo comando, incluindo os que falharam parcialmente (flag `-d` do
FastQC na FASE 1; falha de segmentação por concorrência de threads na
FASE 2, Bloco B — ver `run_alignment_full.sh`/`run_subread_align_full.sh`),
está documentado inline nos próprios scripts — não só na prosa do
artigo. Os scripts da FASE 2 em diante seguem convenção própria de
comentário mais verboso (o quê **e** por quê, não só o quê) — ver
`feedback-codigo-didatico-posdoc` na memória do projeto — porque estes
scripts ainda vão ser reaproveitados/adaptados nas fases seguintes
(quantificação, splicing) por quem não estava presente na decisão
original.

## Dados grandes NÃO versionados (ficam só no servidor, por design)

| O quê | Onde | Tamanho | Por quê fora do repo |
|---|---|---|---|
| FASTQ brutos | `eulalio@200.235.143.10:~/rnaseq-Anticarsia-GORE3/raw_fastq/` | 47 GB | grande demais para git |
| FASTQ trimados | `~/rnaseq-Anticarsia-GORE3/trimmed/` | ~40 GB estimado | idem |
| Relatórios HTML completos (FastQC/MultiQC/fastp) | `~/rnaseq-Anticarsia-GORE3/qc/{pre_trim,post_trim,ab_test}/` | ~45 MB só os JSON do fastp | grande, e os números relevantes já foram extraídos para os CSVs acima |
| Índice HISAT2 piloto (Bloco C, sem anotação de splice sites) | `~/rnaseq-Anticarsia-GORE3/genome_index_pilot/` | ~590 MB | específico do teste de equilíbrio de trimagem; a FASE 2 formal precisa de índice próprio, com anotação |
| BAMs STAR + Subread (13 amostras cada, FASE 2 Bloco B) | `~/rnaseq-Anticarsia-GORE3/bam/{star,subread}/` | ~35–70 GB estimado | grande demais para git — os logs-texto (`Log.final.out`, `.subread_align.log`) que sustentam as Tabelas 6-7 **foram copiados e versionados** em `qc/fase2_blocoB_{star,subread}/` (260 KB total), suficiente para reproduzir a análise sem acesso ao servidor |
| Índice Salmon decoy-aware + saídas `quant.sf` (13 amostras, FASE 3 Bloco D) | `~/rnaseq-Anticarsia-GORE3/{salmon_index_decoy,salmon}/` | índice ~1–2 GB estimado | grande demais para git — os logs de mapeamento (`salmon_quant.log`) que sustentam a Tabela 9/Fig.7 **foram copiados e versionados** em `qc/fase3_blocoD_salmon_logs/`, e as tabelas de contagem/TPM do tximport (pequenas, ~2,4 MB) já estão versionadas em `resultados/fase3_blocoE_salmon_gene_{counts,tpm}.tsv` |
| Índice Salmon `--keepDuplicates` + `quant.sf` (13 amostras, FASE 5 Bloco B) | `~/rnaseq-Anticarsia-GORE3/{salmon_index_decoy_keepdup,salmon_keepdup}/` | índice ~1–2 GB estimado | grande demais para git — a matriz de contagens completa (100% cobertura, 15.773 genes × 12 amostras) já está versionada em `resultados/fase5_blocoB_txi_counts_for_python.csv` (~870 KB), suficiente para reproduzir o modelo estatístico sem acesso ao servidor |
| `DESeqDataSet` ajustado (R, `.rds`) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase5_blocoB/dds_raw.rds` | pequeno mas binário/R-específico | não versionado por ser objeto R serializado, não CSV portável — reconstruível a partir de `resultados/fase5_blocoB_txi_counts_for_python.csv` + `codigo/fase5_blocoB/build_dds_tximport.R` |
| `DESeqDataSet` já rodado (`DESeq()`, R, `.rds`) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase5_blocoC/dds_fit.rds` | pequeno mas binário/R-específico | idem — reconstruível a partir de `dds_raw.rds` + `codigo/fase5_blocoC/run_deseq2.R` |
| Matriz VST normalizada (genes×amostras) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase5_blocoG/vst_normalized_matrix.csv` | ~2,6 MB | não versionada por tamanho, mas pequena o bastante para copiar se necessário; reconstruível a partir de `dds_fit.rds` (`vst(dds, blind=FALSE)`) |
| Todos os `_all.csv` (genes não-significativos incluídos, 3 contrastes × 2 motores) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase5_blocoD/*_all.csv` | ~2,7 MB total | só os `_sig.csv` (genes DE) foram versionados em `resultados/fase5_blocoD/` — os `_all.csv` completos (11.833 genes cada) ficam no servidor, reconstruíveis via `codigo/fase5_blocoD/` |
| Banco de dados InterPro/member-databases (FASE 7 Bloco D) | `~/rnaseq-Anticarsia-GORE3/genome_annotation/interproscan6_data/` | ~28 GB | baixado automaticamente pelo pipeline Nextflow via lookup por checksum + download; reobtível rerodando `nextflow run ebi-pf-team/interproscan6 -r 6.0.1` |
| Saída completa do InterProScan6 (TSV/GFF3/JSON/JSONL/XML) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase7_blocoD/protein_representative.faa.*` | ~590 MB total (JSON sozinho 247 MB) | grande demais para git — a extração relevante (cobertura, pares gene-GO) já está em `resultados/fase7_blocoB/`, `resultados_server/fase7_blocoF/gene_to_go_consolidated.csv` |
| Anotações completas do eggNOG-mapper (`.emapper.annotations`) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase7_blocoC/pfam_eggnog_out.emapper.annotations` | 17,4 MB | só o resumo de cobertura + `gene_to_kegg.csv` foram versionados; `gene_to_go.csv` (27,8 MB, todos os pares gene-GO do eggNOG isolado) fica só no servidor |
| Mapeamento gene→GO consolidado (união eggNOG+InterProScan6) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase7_blocoF/gene_to_go_consolidated.csv` | 36,8 MB | só o resumo de cobertura (`annotation_coverage_summary.csv`) foi versionado; reconstruível via `codigo/fase7_blocoF/consolidate_annotation.py` |
| BAMs `subjunc` (13 amostras, FASE 6 Bloco B, substitui o Subread sem splice da FASE 2) | `~/rnaseq-Anticarsia-GORE3/bam/subjunc/` | 32 GB | grande demais para git — os `*.MATS.JC.txt` (rMATS) e `.sj`/splicegraph (MAJIQ) que sustentam a Tabela 17/Figs. 17-18 **foram copiados e resumidos** em `resultados/fase6_blocoD/`; reobtível rerodando `codigo/fase6_blocoB/run_subjunc_realign.sh` a partir dos FASTQ trimados (se ainda existirem no servidor) |
| Saída completa MAJIQ build (splicegraph + `.sj` por experimento) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase6_blocoC/build/` | 33 MB | reobtível via `codigo/fase6_blocoC/run_majiq_build.sh` a partir dos BAMs `subjunc` |
| Saída zero-evento da 1ª tentativa rMATS (Subread sem splice, achado técnico preservado por transparência) | `~/rnaseq-Anticarsia-GORE3/resultados_server/fase6_blocoB_ATTEMPT1_subread_zero_events/` | 35 MB | não apagada de propósito — evidência do achado declarado em `artigo.md` §2.9/Limitação 18 |

**Risco declarado, não escondido:** os links de download da Macrogen já
expiraram (`docs/07_analise_rnaseq.md` §13.1) — se o servidor for limpo,
os FASTQ brutos e trimados **não podem ser regerados**, e os BAMs da
FASE 2 (Bloco B) também não, já que dependem deles. Os CSVs em
`resultados/` (incluindo os novos da FASE 2) bastam para reproduzir todas
as figuras/tabelas do artigo, mas não para continuar a análise (FASE 3 em
diante — quantificação por gene precisa dos BAMs em si, não só das
estatísticas resumo) se `raw_fastq/`/`trimmed/`/`bam/` do servidor forem
perdidos.

## Pendências e lacunas conhecidas (não fabricadas, ver `artigo.md` §5 / `artigo_pt.md` §5 para o texto completo)

1. Causa raiz da contaminação por adapter-dimer (por que essas 4 bibliotecas) — não estabelecida, precisa dado de tamanho de inserto que a Macrogen não forneceu. Bloco C (§3.8) descarta que seja artefato de parâmetro de trimagem: sweep empírico não recuperou nenhum read.
2. Tamanho de inserto/fragmento da biblioteca — não confirmado.
3. Orientação de fita (forward/reverse) — inferida do nome do kit, não confirmada empiricamente.
4. 5 dos 17 tubos submetidos não vieram nesta entrega — motivo não confirmado.
5. Desvio de comando do FastQC (`-d` falhou) — documentado, sem consequência nos resultados.
6. Assimetria de poder estatístico por contraste (Tabela 4) — caracterizada, plano de resolução declarado, **ainda não resolvida**.
7. Corte de cor >10% na Fig. 3 é escolha visual post-hoc, não limiar pré-declarado como na Fig. 1.
8. `majiq weights` (ponderação de outlier, planejada na FASE 4/6 para o confundimento ID-8) não existe no MAJIQ v3 instalado — sucessor aparente `majiq moccasin` ainda não aplicado.
9. Candidatos de splicing em genes de tripsina (FASE 6, §3.19) são leitura direta de limiar, não curadoria — curadoria formal é a FASE 9, não iniciada.
10. Causa raiz de por que `subread-align` (não `subjunc`) foi usado na FASE 2 original não é maliciosa nem negligente — era a leitura razoável do comentário do próprio Subread na época, só corrigida ao ver o resultado zero-evento do rMATS na FASE 6.

## Para quando for gerar o Word/PowerPoint

- As legendas em `artigo.md` já seguem o padrão `Figure N | frase-título. Detalhe.` — usar como legenda de figura diretamente.
- As tabelas em Markdown convertem para tabela nativa do Word/PPTX sem reformatação de conteúdo (só de estilo).
- **Não inventar Abstract/Introdução para preencher o documento** — se o Word precisar dessas seções antes da FASE 5 terminar, marcar explicitamente como rascunho/pendente no arquivo gerado, do jeito que já está marcado aqui.
- Skills disponíveis para a geração: `docx` (edição/criação de Word), `pptx`/`scientific-slides` (apresentação), `dataviz`/`scientific-visualization` (se figuras novas forem necessárias).
