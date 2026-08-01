# Anticarsia-GORE3

Pós-doutorado de **Eulálio Gutemberg.** — UFV
(Departamento de Bioquímica e Biologia Molecular, BIOAGRO/INCT-IPP),
supervisão da Profa. Maria Goreti de Almeida Oliveira.

**Pergunta central:** o peptídeo inibidor de protease GORE3 (pentapeptídeo,
derivado da própria pró-região da tripsina digestiva do inseto)
altera o transcriptoma do intestino médio de *Anticarsia gemmatalis*
(lagarta-praga da soja) de forma diferente dos inibidores clássicos já
conhecidos (Benzamidina, SKTI)? E onde/como o GORE3 se torna mais
letal/eficaz frente a eles?

Este repositório contém a análise de RNA-Seq (4 grupos × 3 réplicas:
Controle, Benzamidina, SKTI, GORE3) do começo ao fim — QC, alinhamento,
quantificação, expressão diferencial, anotação funcional e enriquecimento
— construída de forma incremental e documentada, com todo número/figura
rastreável até o script e o dado-fonte que o gerou.

## Por onde começar

| Se você quer... | Vá para |
|---|---|
| Ler o artigo por completo (inglês, canônico) | [`artigo.md`](artigo.md) |
| Ler em português (tradução fiel, não resumo) | [`artigo_pt.md`](artigo_pt.md) |
| Entender o plano completo do pipeline (todas as 10 fases) | [`docs/07_analise_rnaseq.md`](docs/07_analise_rnaseq.md) |
| Encontrar qual script/dado gerou uma figura ou tabela específica | [`INDICE_MATERIAL.md`](INDICE_MATERIAL.md) |
| Ver a base bibliográfica (125+ artigos revisados, fichados) | [`literatura/`](literatura/) |
| Reproduzir uma etapa específica | `codigo/fase{N}_bloco{X}/` |

`artigo.md`/`artigo_pt.md` são **documentos vivos**: cada seção só contém
o que foi de fato executado e confirmado, nunca projeção ou "resultado
esperado". Quando uma análise ainda não rodou, o documento diz isso
explicitamente.

## Status do projeto

| Fase | O quê | Status |
|---|---|---|
| 1 | QC bruto + trimagem (fastp) | ✅ completa |
| 2 | Alinhamento genoma-guiado (STAR + Subread) | ✅ completa |
| 3 | Quantificação (featureCounts + Salmon/tximport) | ✅ completa |
| 4 | Decisão de correção de lote | ✅ decidida (sem correção, justificado) |
| 5 | Expressão diferencial (DESeq2 + PyDESeq2, dois motores) | ✅ completa |
| 6 | Splicing alternativo/isoforma | ⏳ não iniciada |
| 7 | Anotação funcional multi-fonte + enriquecimento GO/KEGG | ✅ completa |
| 8 | Coexpressão (WGCNA) | ⏳ não iniciada |
| 9 | Curadoria dirigida da família de serino-proteases | ⏳ não iniciada |
| 10 | Montagem *de novo* secundária (Trinity) | ⏳ não iniciada |

Detalhe completo de cada bloco em [`docs/07_analise_rnaseq.md`](docs/07_analise_rnaseq.md)
e no histórico de commits (cada commit fecha uma fase ou bloco inteiro,
com o resumo do que foi verificado).

## Achados principais até aqui

- **GORE3 e SKTI convergem** numa assinatura transcricional e funcional
  ampla e específica (3.053 genes DE compartilhados; 86% dos termos GO
  significativos de GORE3 também são significativos em SKTI) — enquanto
  **Benzamidina é sistematicamente menor e mais genérico**.
- **O contraste Benzamidina×Controle é frágil**: removendo uma única
  amostra (ID-8, sequenciada em corrida separada), os genes
  diferencialmente expressos caem de 255 para 6 — não é um efeito robusto
  de grupo, e isso qualifica qualquer interpretação futura desse
  contraste.
- **Anotação funcional cobre 80,1%** dos 14.238 genes protein_coding
  (união eggNOG-mapper + InterProScan6, dois métodos independentes com
  Jaccard 0,692 de concordância).
- Toda análise estatística central (expressão diferencial e
  enriquecimento GO/KEGG) foi rodada em **dois motores independentes**
  (R e Python), com a concordância/discordância entre eles reportada como
  resultado, não assumida.

## Estrutura do repositório

```
artigo.md / artigo_pt.md   documento vivo do artigo (EN canônico / PT-BR)
docs/                       plano mestre do pipeline (10 fases) + bibliografia (.bib)
literatura/                 125+ artigos revisados e fichados, por tema
codigo/fase{N}_bloco{X}/    todo script usado, organizado por fase e bloco
resultados/fase{N}_bloco{X}/  saídas (CSV/TSV) pequenas o bastante para versionar
figuras/                    figuras finais (PDF + PNG 300 dpi), prontas para Word/PPT
INDICE_MATERIAL.md          mapa figura↔tabela↔código↔dado-fonte↔seção do artigo
qc/                         logs de QC/alinhamento pequenos, versionados para reprodutibilidade
report-rnaseq-macrogen/     relatório de QC original do fornecedor de sequenciamento
```

**O que não está aqui, por design:** FASTQ brutos/trimados, BAMs, índices
de alinhador e bancos de anotação (dezenas de GB) ficam só no servidor de
processamento — grandes demais para git. Cada um desses casos está
documentado em [`INDICE_MATERIAL.md`](INDICE_MATERIAL.md) (seção "Dados
grandes NÃO versionados"), com o caminho exato no servidor e como
reconstruir a partir do que *está* versionado aqui.

## Reprodutibilidade

Todo número e toda figura no artigo vêm de um script versionado neste
repositório — nunca digitados à mão. A análise estatística central roda
em dois motores independentes (R e Python) desde a FASE 5, e a
concordância entre eles é reportada como resultado verificado, não
assumida. `INDICE_MATERIAL.md` mapeia cada figura/tabela ao script exato
que a gerou e ao CSV/TSV de dado-fonte.

Pipeline roda em ambiente próprio no servidor de processamento (Debian,
GPU RTX 5070 Ti), com ambientes conda/mamba dedicados por ferramenta
(`r-analysis`, `pydeseq2-env`, `annotation`, `ngs`, etc.) — não há
requirements.txt único porque as ferramentas (DESeq2, PyDESeq2,
clusterProfiler, gseapy, STAR, Salmon, featureCounts, eggNOG-mapper,
InterProScan6, HMMER) vivem em ambientes separados, cada um documentado
no bloco de código correspondente.

## Citação e afiliação

Trabalho de pós-doutorado vinculado ao **INCT-IPP** (Instituto Nacional
de Ciência e Tecnologia em Interações Planta-Praga) e ao **BIOAGRO/UFV**.
Ver `docs/referencias.bib` para a bibliografia completa em formato
BibTeX (150+ entradas, todas com DOI/PMID verificado).
