# Análise de RNA-Seq — pipeline calibrado ao desenho real

Especificação executável, passo a passo, de como processar os dados do
experimento GORE3 quando os FASTQ chegarem da Macrogen. Cada decisão tem
citação em `docs/referencias.bib` ou em `literatura/`. Nada aqui foi
executado — os FASTQ não existem ainda; isto é o que a base teórica
(`03_metodologia_padrao_ouro.md`) descrevia em nível de decisão, agora escrito
em nível de execução.

---

## 0. Parâmetros do desenho (confirmados em 27/07/2026)

| Parâmetro | Valor |
|---|---|
| Grupos | Controle · Benzamidina (controle positivo) · SKTI (inibidor natural) · GORE3 |
| Réplicas biológicas | 3 por grupo |
| Amostras totais | 12 |
| Leitura | Paired-end, 150 nt |
| Profundidade alvo | ~40 milhões de reads/amostra |
| Espécie | *Anticarsia gemmatalis* |
| Genoma de referência | `GCF_050436995.1` (ilAntGemm2) — nível cromossomo, 32 cromossomos, N50 12,19 Mb, **BUSCO 99,36% completo** |
| Anotação | NCBI RS_2026_04 — 15.773 genes, 14.238 codificantes de proteína |

**⚠️ Duas informações ainda não confirmadas com a Macrogen, e que este pipeline
não pode ser fechado sem elas:**

1. **Tamanho de fragmento/inserto da biblioteca.** "150 nt" é o comprimento de
   *leitura*, não de *fragmento* — são parâmetros distintos, e a diferença
   afeta diretamente a identificabilidade de isoforma
   (`ferrerbonsoms2022identifiability`, PMID 34978563: o comprimento de
   fragmento ótimo depende do gene; genes com muitas isoformas — como a
   família de tripsinas, o alvo central da H1 — precisam de fragmento maior
   para deconvolução confiável). **Ação: pedir à Macrogen o tamanho médio de
   inserto da biblioteca**, não assumir.
2. **Orientação da biblioteca (strand-specific ou não)** e protocolo de
   seleção de RNA (polyA ou depleção de rRNA) — nenhum dos dois está
   registrado em `04_viabilidade.md`. Afeta o parâmetro `--libType` do Salmon
   e `strandedness` do featureCounts/Subread abaixo.

---

## 1. Visão geral do fluxo

```
FASTQ bruto (12 amostras, PE 150nt, ~40M reads)
   │
   ├─ FASE 1: QC + trimagem ──────────────────────────────────────
   │
   ├─ FASE 2: Alinhamento genoma-guiado (via primária) ───────────
   │      STAR ou HISAT2 (expressão gênica) + Subread (splicing)
   │
   ├─ FASE 3: Quantificação ───────────────────────────────────────
   │      featureCounts (gene) │ Salmon --alignment-mode + tximport
   │
   ├─ FASE 4: Correção de lote (se necessário) ────────────────────
   │      ComBat-seq
   │
   ├─ FASE 5: Expressão diferencial ───────────────────────────────
   │      DESeq2, 6 contrastes pairwise, limiar calibrado a n=3
   │
   ├─ FASE 6: Splicing alternativo / isoforma (H1, H5) ────────────
   │      rMATS-turbo + MAJIQ (paralelos) sobre alinhamento Subread
   │
   ├─ FASE 7: Anotação funcional e enriquecimento ─────────────────
   │      eggNOG-mapper v2 → clusterProfiler (GO/KEGG)
   │
   ├─ FASE 8: Coexpressão ──────────────────────────────────────────
   │      WGCNA
   │
   ├─ FASE 9: Família de serino-proteases (o teste mecanístico) ───
   │      curadoria manual + filogenia + expressão por isoforma
   │
   └─ FASE 10 (secundária, paralela): Trinity de novo ─────────────
          só para transcritos ausentes da anotação RS_2026_04
```

A via primária é **genoma-guiada** (FASES 1–9); Trinity é **secundária e
paralela** (FASE 10), não um pré-requisito — diferença central em relação ao
`.docx` original e ao pipeline `RNA-Seq-not-model` já existente (que é
*de novo*-primário, para *S. frugiperda*, espécie ainda sem genoma).

---

## 2. FASE 1 — QC e trimagem

| Etapa | Ferramenta | Citação |
|---|---|---|
| QC bruto | FastQC + MultiQC | `ewels2016multiqc` (PMID 27312411) |
| Trimagem | **fastp** | `chen2025fastp` (PMID 41112039 — fastp 1.0, comparado a Trimmomatic e Cutadapt) |
| QC pós-trimagem | FastQC + MultiQC | idem |

fastp em vez de Trimmomatic (proposto no `.docx`): mais rápido, controle de
qualidade e trimagem numa única ferramenta. `chen2025fastp` é a referência
atual (2025); `chen2018fastp` é o artigo original, citado junto por ser a
referência canônica.

**Parâmetros:** `--detect_adapter_for_pe` (a Illumina usa adaptadores
diferentes por leitura em PE), `--length_required 36`, `--qualified_quality_phred 20`.
Reaproveita o módulo `RNA-Seq-not-model/modules/trimming.nf` (`FASTP`)
praticamente sem alteração — já é PE-aware.

**Critério de aprovação:** taxa de mapeamento >80% na FASE 2 é o sinal de
saúde real; % de adaptador residual e duplicação de FastQC/MultiQC são
triagem inicial.

---

## 3. FASE 2 — Alinhamento genoma-guiado

**Duas vias, propositalmente redundantes**, porque nenhum alinhador único é
ótimo para os dois objetivos deste projeto (expressão gênica e detecção de
splicing):

### 3a. Via de expressão gênica — STAR ou HISAT2

`dobin2013star` (PMID 23104886) ou `kim2019graph`/HISAT2 (PMID 31375807).
Ambos adequados para contagem por gene. Reaproveitar o padrão de
`RNA-Seq-not-model/modules/quantification.nf` (`HISAT2_BUILD`/`HISAT2_ALIGN`),
com uma mudança estrutural: lá o índice é construído contra o **transcriptoma**
(via *de novo*); aqui precisa ser construído contra o **genoma**
(`GCF_050436995.1` FASTA) com o GTF/GFF da anotação RS_2026_04 como guia
(`--sjdbGTFfile` no STAR / `--ss`+`--exon` no `hisat2_extract_splice_sites.py`
no HISAT2).

### 3b. Via de splicing — Subread

`coxe2024benchmarking` (PMID 38475429, lido em texto completo): em benchmark
de HISAT2, STAR, Subread e BBMap contra *Arabidopsis*, os alinhadores
populares empatam em acurácia de **resolução de base**, mas na **resolução de
junção** — o que decide se um evento de splicing é atribuído ao lugar certo —
**Subread foi o mais promissor**, recomendado quando alta acurácia de junção
importa. Como a hipótese H5 (splicing alternativo) e a análise de isoformas
de tripsina (H1) dependem inteiramente de reads de junção corretamente
atribuídas, **usar Subread como via paralela dedicada a splicing**, mesmo
mantendo STAR/HISAT2 para a contagem gênica padrão.

**Ressalva declarada:** o benchmark é em planta (*Arabidopsis thaliana*), não
inseto — os próprios autores notam que é "talvez menos complexa" que outros
genomas vegetais. O ranking não se transfere automaticamente para
*A. gemmatalis*; a estrutura do achado (base ≠ junção) sim.

**Ferramenta secundária de completude:** BUSCO já não precisa ser rodado no
genoma (99,36% verificado, `NOTAS_DE_AUDITORIA.md` §10) — mas **deve** ser
rodado na montagem *de novo* secundária (FASE 10), onde a métrica ainda não
existe.

---

## 4. FASE 3 — Quantificação

| Nível | Ferramenta | Alimenta |
|---|---|---|
| Gene | featureCounts sobre BAM do STAR/HISAT2 | DESeq2 (FASE 5) |
| Transcrito/isoforma | Salmon em modo `--alignment-mode` sobre o mesmo BAM, ou pseudoalinhamento direto | tximport → DESeq2/EBSeq (FASE 5–6) |

`soneson2015differential` (PMID 26925227, lido em texto completo): estimativa
em nível de **gene** com `tximport` tem vantagem de desempenho e
interpretabilidade sobre nível de transcrito puro, mas **a presença de uso
diferencial de isoforma infla a FDR de uma análise só em nível de gene** — o
que a correção por offset do `tximport` resolve. É o argumento formal para
por que a etapa `tximport` (ausente do `.docx`) é obrigatória entre Salmon e
DESeq2, e por que ambos os níveis (gene e isoforma) precisam ser reportados,
não só um.

**Ressalva crítica, direto de `sarantopoulou2021comparative`** (PMID 34034652,
lido em texto completo): quando a isoforma mais expressa de um gene
desaparece — exatamente o cenário que H1 propõe existir entre isoformas de
tripsina sensíveis e insensíveis ao GORE3 — **a acurácia de todos os métodos
de quantificação testados cai drasticamente**, e a FDR real de DE em nível de
isoforma **excede muito a nominal** (a 0,01 de FDR reportada, ≥1.000 isoformas
foram chamadas DE indevidamente no benchmark). Consequência prática:

- Quantificação por isoforma via Salmon/tximport alimentando DESeq2 mede
  sensibilidade da expressão gênica *a* troca de isoforma — não é o mesmo
  que uma ferramenta de DE em nível de transcrito desenhada para isso.
- Se for reportar DE em nível de isoforma como resultado principal (não só
  como insumo do splicing), **declarar explicitamente que a FDR nominal pode
  estar subestimada**, e usar um controle negativo interno (genes sem
  expressão detectável em nenhuma réplica) quando a profundidade permitir.

Reaproveitar `RNA-Seq-not-model/scripts/00_tximport.R` como base — a lógica
de leitura de `quant.sf` por amostra não muda; muda a origem do índice
(genoma-guiado, não transcriptoma *de novo*) e o mapeamento gene↔transcrito
(vem do GTF da RefSeq, não do `gene_trans_map` do Trinity).

---

## 5. FASE 4 — Correção de lote (condicional)

**ComBat-seq** (`zhang2020combat`, PMID
33015620, lido em texto completo): regressão binomial negativa, mantém
contagens inteiras (compatível com DESeq2/edgeR, ao contrário de métodos
gaussianos que geram valores negativos artificiais). Em simulação com efeito
de lote realista, TPR de 0,89 contra 0,85–0,87 dos métodos alternativos
(ComBat em logCPM, RUV-seq, SVA-seq, ou simplesmente incluir lote como
covariável).

**Ressalva do próprio artigo:** se não houver diferença real de dispersão
entre lotes, ComBat-seq fica redundante e **mais conservador** que incluir
lote como covariável simples no modelo — não aplicar cegamente.

**Decisão condicional:** só rodar esta fase se o sequenciamento da Macrogen
sair em mais de uma corrida/lane com confundimento potencial entre lote e
tratamento. Módulo já existe: `RNA-Seq-not-model/modules/differential_expr.nf`
(`COMBAT_SEQ`) + `RNA-Seq-not-model/scripts/05_batch_correction.R`, ativado
por `params.run_combat_seq`.

---

## 6. FASE 5 — Expressão diferencial

**Ferramenta:** DESeq2 (`love2014moderated`, PMID 25516281, lido em texto
completo). Justificado duas vezes: (1) `froussios2019well` confirma que
medidas de RNA-Seq seguem distribuição binomial negativa mesmo em eucarioto
complexo, o que é a premissa do DESeq2; (2) para o n=3 real deste desenho,
`schurch2016many` recomenda especificamente **DESeq2 ou edgeR (exact)** como
melhor combinação de verdadeiro/falso-positivo abaixo de 12 réplicas.

### 6.1 Contrastes (não é um único controle × tratamento)

Diferente do módulo `DESEQ2` de `RNA-Seq-not-model`, que aceita só um par
`--control`/`--treatment`, este desenho tem **4 grupos** e precisa de **matriz
de contrastes**, não de um único par. Contrastes mínimos, em ordem de
prioridade para responder às hipóteses do projeto:

| # | Contraste | Responde |
|---|---|---|
| 1 | GORE3 vs. Controle | Efeito principal do peptídeo |
| 2 | GORE3 vs. Benzamidina | GORE3 supera o controle positivo farmacológico clássico (S1-dirigido)? |
| 3 | GORE3 vs. SKTI | **H4** — GORE3 evita a compensação proteolítica que SKTI induz (Mendonça et al. 2020) |
| 4 | SKTI vs. Controle | Reproduz o padrão conhecido de compensação (validação do desenho) |
| 5 | Benzamidina vs. Controle | Efeito do controle positivo isolado |
| 6 | GORE3 vs. (SKTI + Benzamidina) agrupados | Poder extra via agrupamento, só se 1–5 forem consistentes entre si |

**Ação de construção:** generalizar `scripts/01_deseq2.R` para receber a
fórmula `~ group` com `group` de 4 níveis e extrair os `results()` com
`contrast = c("group", nível_A, nível_B)` para cada par acima, em vez do
parâmetro binário atual.

### 6.2 Limiar de significância, calibrado ao n real

O `.docx` propõe padj < 0,01; a versão anterior deste documento recomendava
0,05 "com qualquer um servindo, desde que declarado". **Isso muda com o n=3
confirmado:** `schurch2016many` recomenda escalonar o limiar de fold-change
pelo número de réplicas (0,1 ≤ T ≤ 0,5 em log2 para poucas réplicas, não
|log2FC| ≥ 1 fixo). Usar padj < 0,05 **e** declarar o limiar de fold-change
como decisão explícita, não copiado de outro desenho.

---

## 7. FASE 6 — Splicing alternativo e isoforma (hipóteses H1 e H5)

Este é o núcleo metodológico do projeto — a pergunta que nenhum trabalho
anterior da série GORE respondeu.

| Ferramenta | Papel | Citação |
|---|---|---|
| **rMATS-turbo** | Detecção de eventos clássicos (SE, A5SS, A3SS, MXE, RI) | `wang2024rmats` (PMID 38396040) |
| **MAJIQ** | Captura *local splicing variations* (LSVs), incluindo eventos complexos além dos clássicos | `vaquerogarcia2016view` (PMID 26829591, lido em texto completo) |
| Detecção de outlier | Pondera/desconta réplica atípica sem descartá-la | `norton2018outlier` (PMID 29236961) |

**Por que rodar os dois em paralelo, não escolher um:** `fenn2023alternative`
(DICAST, PMID 37260511) faz benchmark de 11 mapeadores splice-aware × 8
ferramentas de detecção de evento, e conclui que **o desempenho de detecção
de evento varia muito, sem nenhuma ferramenta superar todas as outras**. Não
há vencedor único a citar — a mitigação é rodar rMATS-turbo (clássico,
consolidado, scripts já existem no grupo) e MAJIQ (mais sensível a eventos
complexos, o tipo de resposta que a hipótese H6 já mostrou existir na
estrutura do GORE3) em paralelo, e reportar convergência/divergência.

**Alinhamento de entrada:** o BAM de **Subread** (FASE 2b), não o de
STAR/HISAT2 — é o alinhador com melhor acurácia de junção segundo
`coxe2024benchmarking`.

**Controle de outlier obrigatório dado o n=3:** `norton2018outlier` é
particularmente relevante aqui porque, com apenas 3 réplicas, uma única
amostra atípica pode dominar o resultado de splicing diferencial. Aplicar o
esquema de ponderação do MAJIQ (`majiq weights`) em vez de decidir
manualmente incluir/excluir uma réplica.

**Isto ainda não existe como módulo** em `RNA-Seq-not-model` — é a peça
genuinamente nova a construir, sem precedente local direto. Estrutura
proposta: `modules/splicing.nf` com processos `RMATS_TURBO`, `MAJIQ_BUILD`,
`MAJIQ_PSI`, `MAJIQ_DELTAPSI`.

---

## 8. FASE 7 — Anotação funcional e enriquecimento

Sem mudança de decisão em relação a `03_metodologia_padrao_ouro.md` — apenas
apontando as citações já verificadas: **eggNOG-mapper v2**
(`cantalapiedra2021eggnog`, PMID 34597405) para anotação funcional a partir de
contigs/proteínas preditas, **clusterProfiler 4.0** (`wu2021clusterprofiler`,
PMID 34557778) para enriquecimento GO/KEGG com interface para organismos sem
`org.*.db` dedicado — o caso de *A. gemmatalis*. Reaproveitar
`RNA-Seq-not-model/modules/annotation.nf` (`EGGNOG_MAPPER`,
`GENE2GO_BUILD`) e `modules/enrichment.nf` (`GO_ENRICHMENT`,
`KEGG_ENRICHMENT`, `GSEA`) quase sem alteração — a entrada muda (proteínas
preditas da anotação RS_2026_04 em vez de TransDecoder sobre Trinity), a
lógica não.

---

## 9. FASE 8 — Coexpressão (WGCNA)

`langfelder2008wgcna` (PMID 19114008). Módulo `WGCNA` de
`RNA-Seq-not-model/modules/enrichment.nf` é reaproveitável diretamente.

⚠️ **Ressalva de poder, dado o n confirmado:** WGCNA tipicamente precisa de
**≥15–20 amostras** para módulos estáveis; este desenho tem 12. Não
descartar a etapa, mas **declarar explicitamente a limitação** e tratar os
módulos resultantes como exploratórios, não confirmatórios. `hdWGCNA`
(`morabito2023hdwgcna`, PMID 37426759) foi desenhado para single-cell/dado de
alta dimensão — **não testado para bulk RNA-Seq com n baixo**, não citar como
solução para esta limitação sem verificação adicional.

---

## 10. FASE 9 — Análise dirigida da família de serino-proteases

O teste mecanístico central do projeto, ausente do `.docx` original
(`03_metodologia_padrao_ouro.md` §9 já apontava a lacuna). Sequência:

1. **Identificação:** extrair da anotação RS_2026_04 todos os genes anotados
   como tripsina/serino-protease (busca por domínio Pfam/InterPro, não só por
   nome de produto gênico — nomes automáticos erram em famílias
   multigênicas, ver `05_lacunas_e_hipoteses.md` §5).
2. **Curadoria manual:** conferir cada hit contra a tríade catalítica
   His57/Asp102/Ser195 e o motivo GDSGGP — critério estrutural, não
   confiar só na anotação automática (BUSCO 99,36% mede completude da
   montagem, não acerto por gene individual, ver `NOTAS_DE_AUDITORIA.md`
   §10).
3. **Filogenia:** árvore da família identificada, para diferenciar
   parálogos verdadeiros de erro de anotação.
4. **Expressão por isoforma:** cruzar com a FASE 6 — quais isoformas de
   tripsina mudam entre GORE3 e controle, e se a mudança é de nível
   (gene) ou de identidade (splicing).
5. **Ponte com o bloco estrutural:** as isoformas induzidas por GORE3 aqui
   identificadas são as que entram na modelagem AlphaFold/docking do bloco
   estrutural (`03_metodologia_padrao_ouro.md`, fluxo estrutural) — este é o
   elo de integração que dá originalidade ao projeto.

---

## 11. FASE 10 (secundária, paralela) — Trinity *de novo*

Só para **transcritos ausentes da anotação RS_2026_04**, não como via
principal. Reaproveitar `RNA-Seq-not-model/modules/assembly.nf` quase
integralmente (`TRINITY`, `CDHIT_EST`, `BUSCO`, `ASSEMBLY_STATS`).

**Calibração de expectativa, com número real:** `sergio2024comprehensive`
(PMID 39649541, lido em texto completo) mostra que **o grau de splicing
alternativo é a variável que mais prejudica reconstrução por montagem
*de novo*** — sem splicing, reconstrução de 62,8–96,3% dos transcritos; no
grau máximo de splicing simulado, cai para 11,6–48,7%. Como a família de
serino-proteases é justamente multigênica e com splicing candidato (H5), **a
montagem *de novo* secundária tende a ser mais fraca exatamente nos genes de
maior interesse** — argumento quantitativo, não só qualitativo, para manter
o genoma-guiado como via primária.

---

## 12. Infraestrutura reaproveitável — caminhos reais

| Recurso | Caminho | Reuso |
|---|---|---|
| Pipeline Nextflow DSL2 completo (de novo) | `C:\Users\eulal\.claude\RNA-Seq-not-model\` | Estrutura de módulos, QC, trimagem, DESeq2 (a generalizar p/ 4 grupos), ComBat-seq, enriquecimento, WGCNA, relatório Quarto |
| Ambientes conda já testados | `RNA-Seq-not-model\envs\*.yml` | Reaproveitar e estender com Subread, rMATS-turbo, MAJIQ |
| `tximport` já em R | `RNA-Seq-not-model\scripts\00_tximport.R` | Adaptar fonte do índice (genoma-guiado) |
| `DESeq2` já em R | `RNA-Seq-not-model\scripts\01_deseq2.R` | Generalizar para matriz de 4 grupos / 6 contrastes |
| `batch_correction.R` (ComBat-seq) | `RNA-Seq-not-model\scripts\05_batch_correction.R` | Reaproveitar sem alteração |
| `WGCNA` em R | `RNA-Seq-not-model\scripts\04_wgcna.R` | Reaproveitar, com ressalva de n declarada |
| Pipeline transcriptoma→estrutura | `C:\Users\eulal\.claude\caracterization-trypsin\nextflow\` | Ponto de entrada da FASE 9.5 (integração com bloco estrutural) |
| Sequências de tripsina locais | `Desktop\LEBPP\Dsign-racional-peptid-inib\anticarsia_gemmatalis_trypsins.fasta` | Ponto de partida da curadoria manual (FASE 9) |
| RNA-Seq anterior do grupo | BioProject **PRJNA1494060** (controle/SKTI/GORE2, 8 SRR) | Dado de validação cruzada — mesma espécie, desenho anterior |

---

## 13. O que falta confirmar antes de fechar o pipeline

1. **Tamanho de fragmento/inserto** da biblioteca Macrogen (§0) — bloqueia a
   escolha fina de parâmetros de Salmon/tximport para isoforma.
2. **Strandedness** e protocolo de seleção de RNA — bloqueia `--libType`
   (Salmon) e `-s` (featureCounts/Subread).
3. **O que constitui uma réplica biológica** (nº de intestinos agrupados por
   amostra) — não documentado em nenhum lugar do projeto ainda
   (`03_metodologia_padrao_ouro.md` §8).
4. **Se haverá mais de uma corrida/lane de sequenciamento** — decide se a
   FASE 4 (ComBat-seq) é necessária.
5. **GTF/GFF exato** a baixar do RefSeq para RS_2026_04 (link em
   `NOTAS_DE_AUDITORIA.md` §10) — confirmar formato compatível com
   STAR/HISAT2/Subread/featureCounts antes de escrever os módulos.

## Fora de escopo deste documento

Não executa nada — os FASTQ não existem. Não escreve os módulos Nextflow
completos (`splicing.nf` é novo e `differential_expr.nf`/`quantification.nf`
precisam de adaptação estrutural, não só de parâmetro) — isso é o próximo
passo de engenharia, quando houver dado real ou sintético para validar contra.
Não resolve o bloco estrutural (AlphaFold/docking/MD), que segue em
`03_metodologia_padrao_ouro.md`.
