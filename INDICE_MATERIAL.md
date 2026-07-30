---
Documento vivo — atualizado a cada bloco de análise concluído.
Função: mapa único de tudo que existe hoje (figuras, tabelas, texto,
código, dado-fonte), para uso na geração futura do artigo em Word e da
apresentação em PowerPoint. Nada aqui substitui `artigo.md`/`artigo_pt.md`
— é o índice de orquestração que aponta pra eles.
Última atualização: 29/07/2026 (FASE 1, Blocos A + A.1 + B + C concluídos).
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
| FASE 2 | Alinhamento genoma-guiado (STAR/HISAT2 + Subread) | não iniciado | — |
| FASE 3–10 | Ver `docs/07_analise_rnaseq.md` | não iniciado | — |

## Figuras

| # | Arquivo | O que mostra | Seção | Código-fonte | Dado-fonte (CSV) |
|---|---|---|---|---|---|
| 1 | `figuras/Figure1_blocoA_quality_dip.png` | Queda de qualidade (ΔQ ciclos 44–90) por amostra, raw | §3.2 | `codigo/fase1_blocoA/analyze_blocoA.py` | `resultados/blocoA_results.csv` |
| 2 | `figuras/Figure2_blocoA1_pertile_heatmap.png` | Heatmap tile×ciclo, ID-1 (limpa) vs. ID-8 (pior) | §3.4 | `codigo/fase1_blocoA/per_tile_analysis.py` | `resultados/blocoA1_pertile_results.csv` |
| 3 | `figuras/Figure3_blocoB_trimming.png` | (a) sobrevivência pós-trim; (b) adapter-dimer % vs. GC% | §3.6 | `codigo/fase1_blocoB/analyze_blocoB.py` | `resultados/blocoB_trim_summary.csv` |
| 4 | `figuras/Figure4_blocoB_before_after.png` | Curvas de qualidade antes/depois da trimagem, 5 amostras | §3.7 | `codigo/fase1_blocoB/plot_before_after_trim.py` | `resultados/figure4_quality_curves.csv` |

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

Todo comando, incluindo os que falharam parcialmente (flag `-d` do
FastQC), está documentado inline nos próprios scripts — não só na prosa
do artigo.

## Dados grandes NÃO versionados (ficam só no servidor, por design)

| O quê | Onde | Tamanho | Por quê fora do repo |
|---|---|---|---|
| FASTQ brutos | `eulalio@200.235.143.10:~/rnaseq-Anticarsia-GORE3/raw_fastq/` | 47 GB | grande demais para git |
| FASTQ trimados | `~/rnaseq-Anticarsia-GORE3/trimmed/` | ~40 GB estimado | idem |
| Relatórios HTML completos (FastQC/MultiQC/fastp) | `~/rnaseq-Anticarsia-GORE3/qc/{pre_trim,post_trim,ab_test}/` | ~45 MB só os JSON do fastp | grande, e os números relevantes já foram extraídos para os CSVs acima |
| Índice HISAT2 piloto (Bloco C, sem anotação de splice sites) | `~/rnaseq-Anticarsia-GORE3/genome_index_pilot/` | ~590 MB | específico do teste de equilíbrio de trimagem; a FASE 2 formal precisa de índice próprio, com anotação |

**Risco declarado, não escondido:** se o servidor for limpo antes da
FASE 2 rodar, os FASTQ brutos e trimados precisam ser regerados a partir
dos links de download da Macrogen (que já expiraram, ver
`docs/07_analise_rnaseq.md` §13.1) — ou seja, **o dado bruto baixado é
neste momento insubstituível**. Os CSVs em `resultados/` bastam para
reproduzir todas as figuras/tabelas do artigo, mas não para continuar a
análise (FASE 2 em diante) se o `raw_fastq/`/`trimmed/` do servidor for
perdido.

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
