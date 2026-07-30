---
Documento vivo — atualizado a cada bloco de análise concluído.
Função: mapa único de tudo que existe hoje (figuras, tabelas, texto,
código, dado-fonte), para uso na geração futura do artigo em Word e da
apresentação em PowerPoint. Nada aqui substitui `artigo.md`/`artigo_pt.md`
— é o índice de orquestração que aponta pra eles.
Última atualização: 30/07/2026 (FASE 3 completa, Blocos A-F).
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
| FASE 4–10 | Ver `docs/07_analise_rnaseq.md` | não iniciado | — |

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
| `codigo/fase3_blocoF/` | Verificação cruzada featureCounts×Salmon+tximport+STAR, 3 checagens+Fig.8 (`analyze_fase3_consistency.py`) |

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

## Para quando for gerar o Word/PowerPoint

- As legendas em `artigo.md` já seguem o padrão `Figure N | frase-título. Detalhe.` — usar como legenda de figura diretamente.
- As tabelas em Markdown convertem para tabela nativa do Word/PPTX sem reformatação de conteúdo (só de estilo).
- **Não inventar Abstract/Introdução para preencher o documento** — se o Word precisar dessas seções antes da FASE 5 terminar, marcar explicitamente como rascunho/pendente no arquivo gerado, do jeito que já está marcado aqui.
- Skills disponíveis para a geração: `docx` (edição/criação de Word), `pptx`/`scientific-slides` (apresentação), `dataviz`/`scientific-visualization` (se figuras novas forem necessárias).
