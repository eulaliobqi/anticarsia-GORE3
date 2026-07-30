# Análise de RNA-Seq — pipeline calibrado ao desenho real

Especificação executável, passo a passo, de como processar os dados do
experimento GORE3. Cada decisão tem citação em `docs/referencias.bib` ou em
`literatura/`; isto é o que a base teórica (`03_metodologia_padrao_ouro.md`)
descrevia em nível de decisão, agora escrito em nível de execução.

**Atualização 28/07/2026:** o relatório de QC bruto da Macrogen (pedido
`HN00280302`) chegou — ver §13.1 para o diagnóstico. Os FASTQ em si (13
arquivos pareados, ~2 GB cada) ainda **não foram baixados** para o servidor;
só o relatório HTML/PDF de controle de qualidade está disponível localmente
em `report-rnaseq-macrogen/`. Nenhuma fase abaixo de FASE 2 em diante foi
executada — apenas a FASE 1 (QC/trimagem) pode ser calibrada com dado real
agora; o resto continua descrito em nível de decisão.

---

## 0. Parâmetros do desenho (confirmados em 27/07/2026)

| Parâmetro | Valor |
|---|---|
| Grupos | Controle · Benzamidina (controle positivo) · SKTI (inibidor natural) · GORE3 |
| Réplicas biológicas | 3 por grupo (desenho) |
| Amostras totais (desenho) | 12 |
| **Amostras entregues (HN00280302, 24/07/2026)** | **13** — ver §13.1, mismatch não resolvido |
| Leitura | Paired-end, 151 nt (confirmado no relatório Macrogen; "150 nt" do desenho é o valor nominal do kit) |
| Profundidade obtida | 8,2–11,9 Gbp / 54,2–78,9 M reads por amostra (alvo de ~40M reads era conservador — todas as amostras excederam) |
| Espécie | *Anticarsia gemmatalis* |
| Genoma de referência | `GCF_050436995.1` (ilAntGemm2) — nível cromossomo, 32 cromossomos, N50 12,19 Mb, **BUSCO 99,36% completo** |
| Anotação | NCBI RS_2026_04 — 15.773 genes, 14.238 codificantes de proteína |

**⚠️ Do par de informações pendentes na versão anterior deste documento, uma
foi resolvida pelo relatório da Macrogen, a outra continua em aberto:**

1. **Tamanho de fragmento/inserto da biblioteca — AINDA NÃO CONFIRMADO.** O
   relatório de raw data da Macrogen não reporta tamanho de inserto (isso
   normalmente vem de QC de biblioteca via Bioanalyzer/TapeStation, não do
   relatório de sequenciamento). "151 nt" continua sendo o comprimento de
   *leitura*, não de *fragmento* — a diferença afeta a identificabilidade de
   isoforma (`ferrerbonsoms2022identifiability`, PMID 34978563), relevante
   para a família de tripsinas (H1). **Ação: pedir à Macrogen o tamanho médio
   de inserto**, ou estimar via `picard CollectInsertSizeMetrics` depois do
   alinhamento genoma-guiado (FASE 2) — não assumir.
2. **Orientação da biblioteca — RESOLVIDO.** A página "Order Information" do
   relatório Macrogen registra `Library Kit: Illumina Stranded mRNA Prep,
   Ligation Reference Guide`. É um kit **stranded** (seleção por poli-A +
   marcação de segunda fita, protocolo de ligação) — não é o caso "não
   registrado" que o documento anterior apontava. Consequência prática: usar
   `--libType ISR` no Salmon e `-s 2` (reverse) no featureCounts/Subread como
   ponto de partida; **confirmar empiricamente com `salmon --libType A`** ou
   `RSeQC infer_experiment.py` nas primeiras amostras alinhadas antes de
   fixar o parâmetro em todo o lote — kits "stranded" da Illumina são
   tipicamente reverse-stranded, mas o relatório não declara o sentido
   explicitamente.

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

**Atualização 30/07/2026 — CONCLUÍDA (Blocos A e B, servidor
`~/rnaseq-Anticarsia-GORE3/`):**

**Bloco A (piloto, decisão STAR vs. HISAT2) — concluído.** Testado em 5
amostras (ID-1, ID-7, ID-8, ID-9, ID-10) com índice anotado, sem escrever BAM
(`--outSAMtype None`). Resultado (`resultados/fase2_blocoA_star_vs_hisat2.csv`,
script `codigo/fase2_blocoA/analyze_fase2_blocoA.py`): STAR venceu HISAT2 nas
5/5 amostras por 9,33–13,02pp (83,49–90,86% STAR vs. 74,15–78,59% HISAT2
anotado); **STAR atinge o critério de aprovação de >80% (§2) em todas, HISAT2
em nenhuma.** Critério combinado com o usuário (diferença ≥2pp decide o
alinhador único): **decisão = rodar só STAR** nas 13 bibliotecas completas,
não os dois.

**Bloco B (13 bibliotecas completas) — concluído nas duas vias.**

- *Via STAR* (`codigo/fase2_blocoB/run_alignment_full.sh`): **13/13
  concluídas**, todas acima do limiar de 80% (combinado único+multi:
  83,12–91,79%; menor valor ID-2, maior ID-12).
  `resultados/fase2_blocoB_star_mapping_summary.csv`. Primeira tentativa
  teve 5 amostras com "Falha de segmentação" por concorrência de
  threads — este script e o de Subread foram lançados juntos, cada um
  pedindo 16 threads; script reescrito para pular amostras já concluídas
  (`Log.final.out` como marcador) e não usar `set -e`, para que uma falha
  isolada não interrompa as demais (retomado via screen
  `fase2_blocoB_star_retry`, que terminou sozinho ao concluir a última
  amostra).
- *Via Subread* (`codigo/fase2_blocoB/run_subread_align_full.sh`, splicing,
  §3b): **13/13 concluídas com sucesso**, incluindo ID-1, que falhou na
  1ª tentativa (mesma causa de concorrência — BAM de 0 bytes) e foi
  rerodada isoladamente com sucesso depois que o STAR já tinha terminado
  (3,1 min, 26.065.883 reads únicos, 62.066 indels, BAM íntegro e
  indexado). Taxa de mapeamento único do Subread (multi-mapping
  desabilitado por desenho, ver script) fica entre 75,6% e 83,1% — **4
  amostras abaixo do limiar de 80%** (Control_R2, e as 3 réplicas de
  Benzamidine): esperado, não é falha, porque o limiar de 80% foi
  declarado para a via de expressão gênica (STAR); o Subread aqui serve
  só à acurácia de junção de splicing (§3b), não à contagem máxima de
  reads mapeados. `resultados/fase2_blocoB_subread_stats.csv`.

**Verificação de consistência entre fases:** `codigo/fase2_blocoB/analyze_blocoB2_alignment.py`
cruzou o "Number of input reads" do STAR contra `reads_after` da FASE 1
Bloco B (`resultados/blocoB_trim_summary.csv`) — bate exatamente
(`reads_after = 2 × input_reads`) nas 13 amostras, confirmando que o
alinhamento rodou sobre o FASTQ trimado correto de cada amostra. Também
confirma os 13 logs do Subread com o marcador "Completed successfully.",
sem nenhuma string de erro. Estatísticas completas de splice junction e
mismatch rate do STAR (`resultados/fase2_blocoB_star_full_stats.csv`):
99,0–99,7% das junções anotadas contra a RS_2026_04, mismatch rate
uniforme (1,26–1,53%), sem outlier por amostra. Figura de comparação
STAR×Subread: `figuras/Figure5_fase2_blocoB_mapping_rates.png`.

**Pendência declarada (não a impede de prosseguir para FASE 3):** a
orientação de fita (forward/reverse) segue apenas inferida do nome do
kit (§0) — `codigo/fase2_blocoB/check_strandedness.sh` e
`analyze_strandedness.py` já existem para confirmar isso empiricamente
sobre os BAMs agora disponíveis, mas ainda não foram executados.

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

**⚠️ Enquadramento (30/07/2026, direto do usuário):** o objetivo desta fase é
alimentar os contrastes de grupo GORE3×Controle/Benzamidina/SKTI (§6.1) —
o resultado central do projeto. A via de gene (featureCounts) é a
**prioritária**; a via de transcrito/isoforma (Salmon+tximport) é apoio à
hipótese secundária H1 (troca de isoformas de tripsina), não o objetivo em
si.

| Nível | Ferramenta | Alimenta |
|---|---|---|
| Gene | featureCounts sobre BAM do STAR/HISAT2 | DESeq2 (FASE 5) |
| Transcrito/isoforma | Salmon em modo `--alignment-mode` sobre o mesmo BAM, ou pseudoalinhamento direto | tximport → DESeq2/EBSeq (FASE 5–6) |

**Atualização 30/07/2026 — execução (Blocos A-C concluídos):**

**Bloco A — strandedness confirmado + defeito de GTF corrigido.**
`check_strandedness.sh`/`analyze_strandedness.py` (escritos na FASE 2,
executados agora): **reverse (`-s 2` / `--libType ISR`) vence de forma
consistente** em ID-1 (75,03% assigned) e ID-8 (73,62%) vs. 0,29%/0,33% no
forward — decisão sem ambiguidade, ao contrário da inferência provisória
do nome do kit. `codigo/fase3_blocoA/decide_libtype.py` formaliza isso em
`resultados/fase3_blocoA_strand_decision.csv`, fonte única lida por todo
script seguinte.

**Achado não previsto, corrigido:** a primeira tentativa de rodar
featureCounts falhou com "failed to find the gene identifier attribute" —
330 das 515.035 linhas do GTF (118 genes, todos loci "LOC" não
caracterizados, sem mRNA no GFF3 original) não tinham `gene_id`, só
`transcript_id` (o gffread da FASE 2 não propaga `gene_id` quando não há
hierarquia gene→mRNA→exon explícita no GFF3). Confirmado 100% consistente:
o valor de `transcript_id` nessas linhas já era exatamente o que `gene_id`
deveria ser. `codigo/fase3_blocoA/fix_gtf_missing_geneid.sh` gera
`GCF_050436995.1_RS_2026_04.fixed.gtf` (mesmas 515.035 linhas, 0 sem
`gene_id`) — nenhum dos 118 genes afetados é tripsina/serino-protease
conhecida. FASE 2 (STAR) não precisa ser refeita (não depende de
`gene_id`); Blocos C-E desta fase usam o GTF corrigido.

**Bloco B — ferramentas.** `gffread` 0.12.7 e `featureCounts` v2.1.1 já no
env `ngs`; `salmon` 1.10.3 já no env `rnaseq-tools` — nenhuma instalação
necessária (`resultados/fase3_blocoB_env_check.txt`).

**Bloco C — featureCounts de produção (prioritário).** 13 BAMs do STAR,
GTF corrigido, `-s 2`, **sem `-M -O --fraction`** (decisão deliberada, ver
`zytnicki2017mmquant`, PMID 28915787, abaixo). 70,15–84,40% dos reads
atribuídos a genes por amostra (`resultados/fase3_blocoC_featurecounts_summary.csv`,
`figuras/Figure6_fase3_blocoC_featurecounts_assigned.png`), matriz completa
em `resultados/fase3_blocoC_gene_counts.txt` (8,3 MB, versionado — pequeno
o bastante, ao contrário dos BAMs/FASTQ).

**Bloco D — Salmon decoy-aware (apoio a H1).** Índice construído com
genoma inteiro como decoy (`gffread` transcriptoma + `genome_annotation/decoys.txt`
+ `gentrome.fa`, `k=31` default), `salmon quant` nas 13 amostras,
`--libType ISR` (Bloco A), `--validateMappings --gcBias`. Taxa de
mapeamento 80,3–91,2%, dentro de ±5,7pp da taxa combinada do STAR em toda
amostra (`resultados/fase3_blocoD_salmon_mapping_summary.csv`,
`figuras/Figure7_fase3_blocoD_salmon_vs_star_mapping.png`).

**Bloco E — tximport adaptado.** `tx2gene.tsv` extraído direto do GTF real
(25.840 transcritos, 15.773 genes únicos — bate exatamente com a contagem
de genes já conhecida da anotação RS_2026_04). Duas descobertas reais
durante a execução, ambas corrigidas:

1. **Índice Salmon sem `--keepDuplicates`:** 811 dos 25.840 transcritos
   têm sequência idêntica byte-a-byte a outro transcrito e foram
   colapsados pelo próprio indexador do Salmon (comportamento padrão, não
   erro) — resultado: 14.973 dos 15.773 genes ficam com pelo menos um
   transcrito diretamente quantificável na tabela do tximport; os ~800
   restantes tiveram seu único transcrito absorvido por outro gene.
   Afeta só a via de apoio (Salmon/tximport), não o featureCounts
   (Bloco C, prioritário), que conta sobreposição de éxon genômico
   diretamente.
2. **Armadilha de parsing do R:** a primeira rodada do tximport reportou
   "3.263 transcripts missing from tx2gene" — rastreado até o
   `read.table()` do R interpretar um apóstrofo literal no gene RefSeq
   `gene-beta'COP` como abertura de aspas nunca fechada, truncando
   silenciosamente 25.840 para 22.305 linhas lidas (só um aviso "EOF
   within quoted string", sem erro). Corrigido com `quote = ""` em
   `codigo/fase3_blocoE/00_tximport_gore3.R` — confirmado 0 transcritos
   ausentes depois da correção.

Saída: `resultados/fase3_blocoE_salmon_gene_counts.tsv`,
`fase3_blocoE_salmon_gene_tpm.tsv` (14.973 genes × 13 amostras).

**Bloco F — verificação cruzada entre quantificadores.** Três checagens,
todas OK (`codigo/fase3_blocoF/analyze_fase3_consistency.py` →
`resultados/fase3_blocoF_crosscheck.csv`): (1) `Assigned` do featureCounts
nunca supera o estimado de reads unicamente mapeados do STAR, em nenhuma
amostra; (2) Salmon×STAR dentro da banda de ±10pp pré-declarada nas 13
amostras; (3) concordância Spearman gene-a-gene entre featureCounts e
Salmon+tximport de **0,983–0,988 nas 13 amostras** (`figuras/Figure8_fase3_blocoF_featurecounts_vs_salmon_concordance.png`)
— forte concordância entre duas vias de quantificação estruturalmente
diferentes, apesar da diferença de cobertura gênica entre elas (item 1
acima).

**FASE 3 concluída (Blocos A-F).** Próximo passo: FASE 4 (correção de
lote, condicional — decidir se necessária quando confirmado o desenho de
corridas de sequenciamento) e FASE 5 (DESeq2, matriz de 4 grupos, 6
contrastes já listados em §6.1) — essas sim usam a matriz de contagem do
Bloco C como entrada principal.

`soneson2015differential` (PMID 26925227, lido do abstract — corrigido
30/07/2026, ver `NOTAS_DE_AUDITORIA.md`): estimativa
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

**Tensão declarada, não resolvida: featureCounts padrão vs. família
multigênica de tripsinas.** `zytnicki2017mmquant` (PMID 28915787, lido em
texto completo, "mmquant: how to count multi-mapping reads?") declara
textualmente que habilitar `-M -O --fraction` para resgatar reads
multi-mapeados/multi-sobrepostos "quase sempre produz resultados
enviesados" — por isso o featureCounts de produção (Bloco C) **não** usa
essas flags. Isso é relevante especificamente para a hipótese secundária
H1 (troca de isoformas de tripsina): a família de serino-proteases é
multigênica, e reads de parálogos próximos podem mapear ambiguamente —
o featureCounts padrão vai descartar/subcontar esses reads exatamente nos
genes de interesse mecanístico de H1. **Não resolvido aqui** — não afeta o
resultado principal desta fase (contrastes de grupo inteiros), fica para
revisitar na FASE 9 (curadoria manual da família de serino-proteases,
§10) especificamente para esses poucos genes, se necessário. Busca
dirigida por um benchmark equivalente em inseto/família multigênica não
encontrou nada (busca honesta, sem forçar citação); o mais próximo é Kwon
2015 (PMID 26112470, *Xenopus*, genes duplicados, só abstract acessado) —
não citado formalmente aqui, decisão em aberto.

**Indexação decoy-aware do Salmon (Bloco D).** `srivastava2020alignment`
(PMID 32894187, lido em texto completo) mostrou que indexar o Salmon com
decoy (genoma inteiro como decoy, modo "selective alignment"/SAF) reduz
atribuição espúria de reads vs. o modo `--type quasi` sem decoy usado no
módulo reaproveitável `RNA-Seq-not-model/modules/quantification.nf`
(desatualizado) — validado em 109 datasets reais humanos + simulações de
camundongo. **Ressalva de transferência, no mesmo padrão já usado para
`coxe2024benchmarking`:** nenhum genoma de inseto ou não-modelo foi
testado nesse benchmark — a estrutura do achado (decoy reduz atribuição
errada) é uma extrapolação razoável para *A. gemmatalis*, não um fato
estabelecido para esta espécie.

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

**Decisão final (30/07/2026) — NÃO rodar ComBat-seq, confundimento
declarado, verificação de robustez planejada para a FASE 5.** A condição
acima de fato se aplica: 12 das 13 amostras foram sequenciadas na mesma
corrida/flowcell (`LH00129`), e **ID-8 (Benzamidine_R3) sozinha numa
corrida separada** (`LH00688`, §13.1) — mas o desbalanceamento é extremo
(lote B = 1 única amostra), não um lote multi-amostra balanceado. Decisão
baseada em três tipos de fonte (não só artigo, conforme escopo ampliado
de "literatura" deste projeto — inclui código-fonte/documentação técnica
e fóruns de bioinformática confiáveis):

1. **Fato de código-fonte, decisivo:** o próprio `ComBat_seq.R`
   (`github.com/zhangyuqing/ComBat-seq`, espelhado no Bioconductor)
   contém a guarda `if(any(table(batch)<=1)) stop("ComBat-seq doesn't
   support 1 sample per batch yet")` — a ferramenta **recusa rodar**
   neste desenho. Não é uma escolha de parâmetro; é um limite estrutural
   da ferramenta já citada no projeto (`zhang2020combat`).
2. **Literatura revisada por pares:** `nygaard2016methods` (PMID
   26272994, lido em texto completo) mostra que métodos de correção de
   lote que tentam preservar diferença de grupo **podem inflar falsos
   positivos especificamente sob desbalanceamento** entre lote e
   grupo — reforça não forçar correção aqui. `leek2010tackling` (PMID
   20838408, lido em texto completo) recomenda, como piso mínimo quando
   correção formal não é aplicável, **declarar explicitamente** o grupo
   de processamento de cada amostra junto com as variáveis biológicas —
   é o que este parágrafo faz.
3. **Consenso de prática (fórum Bioconductor, não citável como artigo mas
   fonte tecnicamente autorizada — Gordon Smyth, coautor limma/edgeR):**
   para lotes pequenos/desbalanceados, recomenda covariável no modelo GLM
   em vez de ComBat. **Rejeitado aqui também:** com 1 amostra no lote B,
   incluir "corrida" como covariável no `design` do DESeq2 se comportaria
   como um intercepto individual para ID-8 — absorveria toda a variação
   daquela amostra (técnica **e** biológica) de forma não transparente,
   reduzindo o grupo Benzamidina a n=2 disfarçado de "correção."

**Decisão:** nenhuma correção formal de lote. O confundimento fica
declarado explicitamente (não escondido) em `artigo.md`/`artigo_pt.md`
§5 (Limitações). **Ação concreta para a FASE 5:** rodar os contrastes que
envolvem Benzamidina (#2 GORE3×Benzamidina, #5 Benzamidina×Controle) duas
vezes — com e sem ID-8 — e reportar se a conclusão (genes DE, direção do
efeito) muda. Isto é prática estatística geral razoável (verificação de
robustez/sensibilidade), **não um protocolo específico validado na
literatura para este cenário exato** — busca dirigida não encontrou
nenhum artigo prescrevendo isso nominalmente para confundimento de
amostra única; divulgado como decisão analítica própria, não como
citação.

**Reverificação da assimetria de profundidade entre grupos (prometida em
`artigo.md` §4, agora feita com dado real da FASE 3, não só read count
bruto da FASE 1):** somando reads atribuídos a genes (featureCounts,
Bloco C) por grupo —

| Grupo | Reads atribuídos (soma, n=3) | Média/amostra |
|---|---:|---:|
| Controle | 133.724.241 | 44,6M |
| Benzamidina | 103.235.368 | 34,4M |
| SKTI | 123.806.115 | 41,3M |
| GORE3 | 131.731.502 | 43,9M |

**A assimetria não desaparece no pós-alinhamento/pós-quantificação** —
Benzamidina segue ~23% abaixo do Controle em reads efetivamente
utilizáveis (não só na sobrevivência bruta da trimagem, FASE 1 §3.7).
Confirma que os contrastes #2 e #5 (os que envolvem Benzamidina) carregam
risco real de poder estatístico reduzido, consistente com — e agora
verificado além de — o que a FASE 1 já tinha sinalizado. Item 2 do plano
original (`artigo.md` §4: "inspecionar dispersão por gene do DESeq2
separadamente para esses contrastes") permanece para a FASE 5, já que
depende do modelo ajustado.

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
   escolha fina de parâmetros de Salmon/tximport para isoforma. Ainda não
   confirmado mesmo após o relatório de raw data (§13.1).
2. ~~**Strandedness**~~ — **resolvido em 28/07/2026** via `Library Kit:
   Illumina Stranded mRNA Prep, Ligation` no relatório Macrogen (§0, §13.1).
   Falta só confirmar o sentido (forward/reverse) empiricamente pós-alinhamento.
3. **O que constitui uma réplica biológica** (nº de intestinos agrupados por
   amostra) — não documentado em nenhum lugar do projeto ainda
   (`03_metodologia_padrao_ouro.md` §8).
4. **Se haverá mais de uma corrida/lane de sequenciamento** — decide se a
   FASE 4 (ComBat-seq) é necessária.
5. **GTF/GFF exato** a baixar do RefSeq para RS_2026_04 (link em
   `NOTAS_DE_AUDITORIA.md` §10) — confirmar formato compatível com
   STAR/HISAT2/Subread/featureCounts antes de escrever os módulos.
6. ~~**Mapeamento `ID-N` → grupo/réplica biológica**~~ — **resolvido em
   28/07/2026** via `identificacao-amostras.xlsx` + confirmação do Eulálio
   (`ID-18` = corpo gorduroso, fora do desenho de 4 grupos). Ver §13.1. Cada
   grupo fecha em n=3; o defeito de qualidade da FASE 1 concentra-se em
   Benzamidine (2/3 réplicas) e SKTI (1/3) — ponto de atenção que passa para
   a FASE 5, não mais pendência de mapeamento.

## 13.1 Diagnóstico do QC bruto — pedido HN00280302 (recebido 24/07/2026, lido 28/07/2026)

Fonte: `report-rnaseq-macrogen/20260724_HN00280302_TRR_Report/` (HTML + PDF
`assets/spgs/HN00280302.pdf`, 14 páginas, e 26 imagens per-base-quality em
`assets/images/quality_images/`). Nenhum FASTQ foi baixado ainda — este
diagnóstico é só sobre o relatório de QC que a Macrogen gera antes da
entrega dos arquivos.

### Estatísticas por amostra (raw data)

| ID | Bases (Gbp) | Reads (M) | GC% | Q20% | Q30% |
|---|---|---|---|---|---|
| 1 | 9.8 | 65.1 | 51.8 | 98.8 | 95.6 |
| 2 | 10.1 | 67.0 | 53.4 | 98.5 | 94.5 |
| 3 | 8.8 | 58.2 | 49.1 | 98.4 | 94.4 |
| 5 | 8.3 | 55.0 | 52.3 | 98.5 | 94.7 |
| **7** | 8.7 | 57.9 | **59.7** | 97.0 | **90.4** |
| **8** | 11.9 | 78.9 | **63.1** | **94.5** | **84.1** |
| 9 | 9.4 | 62.3 | 54.7 | 98.4 | 94.1 |
| **10** | 9.3 | 61.8 | **60.8** | 97.0 | **90.5** |
| 12 | 10.1 | 67.1 | 49.1 | 98.8 | 95.5 |
| 14 | 8.2 | 54.2 | 48.4 | 98.6 | 95.0 |
| 15 | 9.4 | 62.2 | 48.8 | 98.5 | 94.8 |
| 16 | 9.0 | 59.8 | 50.3 | 98.6 | 94.9 |
| 18 | 10.1 | 67.0 | 49.5 | 98.7 | 95.2 |

10 de 13 amostras estão dentro do esperado para mRNA-seq de inseto: GC
48–54%, Q20 ≥98,4%, Q30 ≥94,1%. Três amostras destoam — **ID-7, ID-8, ID-10**
— com GC elevado (59,7–63,1%) e Q30 reduzido (84,1–90,5%). ID-8 é o pior
caso: maior profundidade nominal (11,9 Gbp) e pior qualidade (Q30 84,1%,
Q20 94,5%).

### Causa raiz (identificada nas imagens per-base-quality, não só na tabela)

Inspecionadas as 26 imagens `ID-X_R{1,2}_per_base_quality.png`:

- **ID-7, ID-8 e ID-10 têm, no R1, o mesmo defeito localizado**: qualidade
  cai abruptamente do patamar normal (~39–40) para a faixa 24–28 (com
  mínimos a ~9) especificamente entre os **ciclos ~44–90**, e volta ao normal
  depois do ciclo ~90. A forma e a posição do vale são quase idênticas nas
  três amostras — não é o padrão esperado de degradação gradual de qualidade
  em direção à extremidade 3' (o que se vê em todas as outras 10 amostras).
- **ID-8 tem um segundo problema, independente e mais grave, no R2**: ruído
  difuso ao longo de quase toda a leitura (não localizado), o que explica por
  que ID-8 é a única amostra com Q20 abaixo de 98% e a pior de todas em Q30.
- R2 de ID-7 e ID-10 está limpo (só variação pontual normal) — o problema
  compartilhado é específico do R1 dessas duas.

**⚠️ CORREÇÃO (28/07/2026, FASE 1 Bloco A — ver `artigo.md` §3.3):** a frase
original aqui dizia que o padrão apontava para "causa técnica compartilhada
da corrida (lane/tile do flowcell...)". **Isso foi verificado contra os
headers reais dos FASTQ e não se sustenta.** ID-7 e ID-10 dividem
lane/flowcell (`LH00129`, `23NNGLLT4:4`) com as **10 amostras limpas** —
"mesma corrida" não explica por que só essas duas têm o defeito ali. ID-8
está numa corrida **inteiramente separada** (`LH00688`, `253LHLLT4:5`) —
não pode compartilhar causa de corrida com as outras duas por definição. Um
teste de Per Tile Sequence Quality (FastQC) foi inconclusivo: as 13
amostras, incluindo as limpas, mostram `warn`/`fail` com magnitude
comparável — não discrimina causa técnica localizada de ruído de fundo
normal do flowcell. **A causa do defeito está em aberto, não resolvida.**
Ver diagnóstico completo e critério objetivo de confirmação (ΔQ > 5 Phred,
aplicado às 13 amostras) em `artigo.md` §3.2–3.3 e `resultados/blocoA_results.csv`.

### Ação recomendada na FASE 1

Não excluir as 3 amostras a priori — o defeito é localizado (região de
~46 nt dentro de uma leitura de 151 nt) e recuperável por trimagem/masking
padrão do fastp. Mas:

1. Rodar FastQC/MultiQC pós-`fastp` **separadamente para ID-7/ID-8/ID-10** e
   comparar taxa de sobrevivência de reads e comprimento médio pós-trim
   contra as outras 10 amostras antes de prosseguir para FASE 2.
2. Tratar a taxa de mapeamento da FASE 2 (critério de aprovação já definido
   em §2, >80%) como o veredito real para essas 3 — se cair muito abaixo das
   demais, considerar exclusão apenas então, com justificativa registrada.
3. Marcar ID-8 como a amostra de maior risco do lote inteiro.
4. Guardar a hipótese de causa técnica de corrida (não biológica) para não
   confundir esse artefato com efeito de tratamento na FASE 5 — se ID-7,
   ID-8 e ID-10 caírem no mesmo grupo experimental, o artefato de qualidade
   pode se sobrepor a um efeito real de grupo e precisa ser desacoplado.

### Mapeamento ID → grupo/réplica — RESOLVIDO (28/07/2026)

Fonte: `identificacao-amostras.xlsx` (planilha de submissão à Macrogen, 17
tubos) + confirmação direta do Eulálio sobre `ID-18`.

| Grupo | Tubos submetidos | Entregues (raw data) | Ausentes na entrega |
|---|---|---|---|
| Control | ID-1,2,3,4 | ID-1,2,3 (**n=3**) | ID-4 |
| Benzamidine | ID-5,6,7,8 | ID-5,**7,8** (**n=3**) | ID-6 |
| SKTI | ID-9,10,11,12,13 | ID-9,**10**,12 (**n=3**) | ID-11, ID-13 |
| GORE3 | ID-14,15,16,17 | ID-14,15,16 (**n=3**) | ID-17 |
| — (fora do desenho) | não consta na planilha | **ID-18** | — |

**`ID-18` = corpo gorduroso da lagarta** (confirmado pelo Eulálio) — não é
réplica de nenhum dos 4 grupos de intestino médio, é outro tecido, amostra
única sem réplica. **Não entra na matriz de contrastes da FASE 5**
(DESeq2 precisa de réplicas por grupo, e não há grupo/tratamento definido
para ela). Uso potencial a decidir depois: referência de expressão
tecido-específica (ex.: checar se genes candidatos da família de
serino-proteases, FASE 9, também são expressos em corpo gorduroso, o que
ajudaria a interpretar especificidade tecidual) — não usar para nada que
exija DE ou WGCNA com essa amostra sozinha.

**O mismatch 13×12 está explicado:** cada um dos 4 grupos fechou
exatamente em **n=3**, como o desenho confirmado pede — os 4 tubos que não
vieram (ID-4, ID-6, ID-11, ID-13, mais ID-17 = **5 tubos**, não 4; SKTI
submeteu 5 tubos para render 3) ficaram de fora desta entrega, mais o
corpo gorduroso (ID-18) que nunca fez parte da contagem de 12. Se os
5 tubos ausentes forem réplicas de contingência (para o caso de alguma
falhar no QC da própria Macrogen) ou pertencem a uma entrega futura,
segue sem confirmação — mas não bloqueia mais a FASE 5, porque n=3 por
grupo já está garantido nesta entrega.

**⚠️ Achado que muda a leitura do diagnóstico de qualidade (§ acima): o
defeito técnico compartilhado não está espalhado entre grupos — está
concentrado.** Das 3 amostras com o vale de qualidade nos ciclos ~44–90 do
R1:
- **Benzamidine perde 2 de suas 3 réplicas** (ID-7 e ID-8) para o defeito —
  incluindo ID-8, a pior amostra do lote inteiro (ruído difuso adicional no
  R2).
- **SKTI perde 1 de 3** (ID-10).
- **Control e GORE3 estão limpos** — nenhuma das 3 réplicas de cada tem o
  defeito.

Consequência direta para a FASE 5: os contrastes que envolvem Benzamidine
(#2 GORE3 vs. Benzamidina, #5 Benzamidina vs. Controle, #6 GORE3 vs.
SKTI+Benzamidina agrupados) carregam risco de ruído técnico concentrado
num grupo inteiro, não distribuído — poder estatístico e taxa de
falso-positivo desse grupo especificamente devem ser tratados com mais
cautela que os demais. Registrar isso explicitamente no relatório de DE,
não só na FASE 1.

### Urgência operacional — RESOLVIDA (28/07/2026)

Os 26 arquivos (47 GB) foram baixados para
`eulalio@200.235.143.10:~/rnaseq-Anticarsia-GORE3/raw_fastq/` via
`screen -S rnaseq_download`, com retry automático por arquivo. **Os 26
md5sum conferem 100% contra `HN00280302_13samples_md5sum_DownloadLink.txt`**
(verificado com `md5sum -c`, todos `SUCESSO`) — a integridade dos dados
brutos está confirmada, não é mais suposição. Log completo em
`~/rnaseq-Anticarsia-GORE3/raw_fastq/download.log` e
`md5sum_check.log` no servidor.

FASE 1 (QC/trimagem) pode começar assim que o mapeamento de grupos (acima)
for usado para nomear as amostras no samplesheet do pipeline.

## 13.2 Teste de equilíbrio de trimagem (Bloco C, 29/07/2026)

**Pergunta:** afrouxar os parâmetros de trimagem do fastp (qualidade ou
sensibilidade de detecção de overlap/adapter-dimer) recupera reads úteis
nas 4 amostras problemáticas (ID-7, ID-8, ID-9, ID-10) sem custo de
qualidade, em relação ao Set B de produção (§13.1/Bloco B)?

**Desenho:** sub-amostras determinísticas de 2.000.000 pares
(`seqtk sample -s100`) de ID-1 (controle limpo) + ID-7/8/9/10, testando 4
configurações de fastp (`codigo/fase1_blocoC/run_fastp_paramsweep.sh`):

| Set | Parâmetro variado |
|---|---|
| **B** (baseline) | produção atual — `--qualified_quality_phred 20`, overlap default |
| **C1** | `--qualified_quality_phred 15` (afrouxar qualidade) |
| **C2** | overlap-analysis mais permissivo (`--overlap_len_require 20 --overlap_diff_limit 8 --overlap_diff_percent_limit 30`) |
| **C3** | overlap-analysis mais restritivo (contraprova) |

Critério de decisão pré-declarado: um Set só substitui o Set B se, nas 4
amostras problemáticas, simultaneamente (1) sobrevivência sobe ≥5 pontos
percentuais, (2) Q30 pós-trim continua ≥95%, (3) a taxa de mapeamento
HISAT2 (piloto, ver abaixo) não piora, e (4) o controle limpo (ID-1) não é
prejudicado.

**Piloto de alinhamento (não é a FASE 2 formal):** para arbitrar com dado
real — não só com métricas do próprio fastp — os reads trimados de cada
config foram alinhados com HISAT2 contra um índice **piloto** de
`GCF_050436995.1` (`codigo/fase1_blocoC/build_hisat2_index_pilot.sh`,
construído a partir do FASTA já baixado em outro projeto local,
`~/vg_search/genome/`, **sem** anotação de splice sites — suficiente para
taxa de mapeamento geral, não para quantificação de isoforma). Isso é
estritamente um teste piloto sobre a subamostra de 2M pares; a FASE 2 formal
segue não iniciada e vai precisar de índice próprio, com anotação, nas 13
amostras completas.

**Resultado (`resultados/blocoC_param_sweep.csv`, script
`codigo/fase1_blocoC/analyze_blocoC.py`): nenhuma das 3 variantes recuperou
qualquer read.** O %adapter-dimer ficou **idêntico** (até a 2ª casa decimal)
entre Set B e C1/C2 em todas as 4 amostras — ex. ID-7: 31,19% nos três; ID-8:
25,60% nos três; ID-9: 16,20% nos três; ID-10: 30,65% em B/C1, 30,65%/mesmo em
C2. A diferença de sobrevivência foi 0,00pp (ou -0,01pp, ruído de
arredondamento) em todos os casos. Set C3 (mais restritivo) piorou
ligeiramente a taxa de mapeamento em 3 das 4 amostras (ex. ID-7:
74,83%→74,81%), confirmando que a classificação *é* sensível ao parâmetro
na direção esperada, mas C1/C2 não geraram ganho na direção contrária.

**Interpretação:** a perda de reads nessas 4 amostras não é efeito de um
limiar de qualidade/overlap escolhido conservador demais — é uma
característica estrutural das próprias bibliotecas (par de leitura cujo
inserto biológico é curto o bastante para R1/R2 se sobreporem quase
totalmente com adaptador), invariante aos parâmetros testados. **Achado
adicional do piloto de alinhamento:** os reads que sobrevivem à trimagem
nas 4 amostras problemáticas mapeiam em taxa (74,8–79,4%) comparável à do
controle limpo (78,0%) — o que sobrevive é dado de qualidade equivalente ao
resto do lote; o problema é volume perdido, não degradação do que resta.

**⚠️ Nenhuma das taxas de mapeamento (mesmo em ID-1, controle limpo, 78,0%)
atinge o critério de aprovação oficial de >80% declarado em §2** — mas isso
é esperado e não comparável diretamente: o índice piloto não tem anotação
de splice sites, o que reduz a sensibilidade a reads que cruzam junções
éxon-éxon (justamente onde HISAT2 se beneficia mais de guia por anotação).
A taxa de mapeamento real da FASE 2, com índice anotado e as 13 amostras
completas, ainda precisa ser medida — este piloto não a substitui, só
compara as 4 amostras problemáticas entre si e contra o controle, o que é
válido independentemente do valor absoluto de mapeamento.

**Conclusão: Set B (produção) confirmado como equilíbrio ótimo por teste
empírico, não por suposição.** Nenhuma mudança no pipeline de trimagem;
`run_fastp_full_trim.sh` permanece como está. Pendência que persiste,
inalterada: a causa raiz de por que essas 4 bibliotecas especificamente
tiveram inserto curto na preparação (tamanho de inserto não reportado pela
Macrogen) segue sem explicação — o Bloco C mostrou que não é recuperável por
trimagem, não por que aconteceu.

---

## Fora de escopo deste documento

Não executa nada — os FASTQ não existem. Não escreve os módulos Nextflow
completos (`splicing.nf` é novo e `differential_expr.nf`/`quantification.nf`
precisam de adaptação estrutural, não só de parâmetro) — isso é o próximo
passo de engenharia, quando houver dado real ou sintético para validar contra.
Não resolve o bloco estrutural (AlphaFold/docking/MD), que segue em
`03_metodologia_padrao_ouro.md`.
