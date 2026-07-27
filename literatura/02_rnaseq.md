# Tema 2 — RNA-Seq

31 referências | 21 com texto completo em disco | **21 fichadas** | busca de 27/07/2026

Todos os metadados (DOI, volume, páginas) foram verificados no
Europe PMC. O campo **Lido de** declara o que foi efetivamente lido
**ao escrever a ficha** — ter o texto completo salvo em disco não
significa tê-lo lido. Ficha marcada `abstract` não contém número ou
detalhe de protocolo que só apareceria no corpo do artigo; onde o
dado falta e importa, a ressalva diz isso em vez de preencher.

Ver [protocolo de busca](00_PROTOCOLO_BUSCA.md) e
[PDFs pendentes](PDFS_PENDENTES.md).

---

## 2A — Artigos-fonte das ferramentas prescritas na metodologia

### `soneson2015differential` — Tier 1
**Soneson C, Love MI, Robinson MD.** (2015). Differential analyses for RNA-seq: transcript-level estimates improve gene-level inferences. `F1000Res` 2015;4:1521.

DOI: [10.12688/f1000research.7563.2](https://doi.org/10.12688/f1000research.7563.2) · PMID: [26925227](https://pubmed.ncbi.nlm.nih.gov/26925227/) · PMC: PMC4712774
**Lido de:** **abstract** · arquivo: `fulltext/soneson2015differential.txt`

**O que estabelece:** Demonstra que estimativas de abundância em nível de gene têm vantagem sobre análise em nível de transcrito em desempenho e interpretabilidade, e — o ponto central para este projeto — que a **presença de uso diferencial de isoformas infla a taxa de falsas descobertas** em análise de expressão diferencial de genes feita sobre matriz de contagem simples. O problema é corrigido incorporando offsets derivados das estimativas em nível de transcrito.

**Onde entra:** Metodologia §11 — é a justificativa formal do `tximport` entre Salmon e DESeq2, etapa que o `.docx` omite. E é o argumento metodológico da **hipótese H1**: se a troca de isoformas de tripsina existe, a análise só em nível de gene distorce o resultado.

**Ressalva:** O próprio artigo registra que o problema é relativamente pequeno em vários conjuntos de dados reais — não presumir que será grande aqui sem verificar.

### `wang2024rmats` — Tier 1
**Wang Y, Xie Z, Kutschera E, Adams JI, Kadash-Edmondson KE, Xing Y.** (2024). rMATS-turbo: an efficient and flexible computational tool for alternative splicing analysis of large-scale RNA-seq data. `Nat Protoc` 2024;19(4):1083-1104.

DOI: [10.1038/s41596-023-00944-2](https://doi.org/10.1038/s41596-023-00944-2) · PMID: [38396040](https://pubmed.ncbi.nlm.nih.gov/38396040/)
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `langfelder2008wgcna` — Tier 2
**Langfelder P, Horvath S.** (2008). WGCNA: an R package for weighted correlation network analysis. `BMC Bioinformatics` 2008;9:559.

DOI: [10.1186/1471-2105-9-559](https://doi.org/10.1186/1471-2105-9-559) · PMID: [19114008](https://pubmed.ncbi.nlm.nih.gov/19114008/) · PMC: PMC2631488
**Lido de:** **abstract** · arquivo: `fulltext/langfelder2008wgcna.txt`

**O que estabelece:** WGCNA, pacote R para análise de rede de correlação ponderada.

**Onde entra:** Metodologia §11 — módulos de coexpressão e identificação de hubs, etapa ausente do `.docx`.

**Ressalva:** Exige número de amostras adequado; com poucas réplicas os módulos ficam instáveis. Verificar o n antes de prometer WGCNA no projeto.

### `fu2012accelerated` — Tier 2
**Fu L, Niu B, Zhu Z, Wu S, Li W.** (2012). CD-HIT: accelerated for clustering the next-generation sequencing data. `Bioinformatics` 2012;28(23):3150-3152.

DOI: [10.1093/bioinformatics/bts565](https://doi.org/10.1093/bioinformatics/bts565) · PMID: [23060610](https://pubmed.ncbi.nlm.nih.gov/23060610/) · PMC: PMC3516142
**Lido de:** **abstract** · arquivo: `fulltext/fu2012accelerated.txt`

**O que estabelece:** CD-HIT acelerado para agrupamento de dados de sequenciamento de nova geração.

**Onde entra:** Metodologia §11 — remoção de redundância na via Trinity secundária.

**Ressalva:** Só metadados e título conferidos; abstract curto, sem números extraídos.

### `dobin2013star` — Tier 2
**Dobin A, Davis CA, Schlesinger F, Drenkow J, Zaleski C, Jha S, Batut P, Chaisson M, Gingeras TR.** (2013). STAR: ultrafast universal RNA-seq aligner. `Bioinformatics` 2013;29(1):15-21.

DOI: [10.1093/bioinformatics/bts635](https://doi.org/10.1093/bioinformatics/bts635) · PMID: [23104886](https://pubmed.ncbi.nlm.nih.gov/23104886/) · PMC: PMC3530905
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `love2014moderated` — Tier 2
**Love MI, Huber W, Anders S.** (2014). Moderated estimation of fold change and  dispersion for RNA-seq data with DESeq2. `Genome Biol` 2014;15(12):550.

DOI: [10.1186/s13059-014-0550-8](https://doi.org/10.1186/s13059-014-0550-8) · PMID: [25516281](https://pubmed.ncbi.nlm.nih.gov/25516281/) · PMC: PMC4302049
**Lido de:** **abstract** · arquivo: `fulltext/love2014moderated.txt`

**O que estabelece:** Apresenta o DESeq2, que usa **estimação por encolhimento** (*shrinkage*) de dispersões e de log-fold-changes para melhorar estabilidade e interpretabilidade das estimativas. O problema declarado é o de contagens com número pequeno de réplicas, discretude, grande faixa dinâmica e presença de outliers — que é exatamente o regime deste projeto.

**Onde entra:** Metodologia §11 — citação canônica do DESeq2. Também é a referência que corrige o erro C7 de `06_correcoes_projeto.md`, onde o `.docx` cita 'DESeq2 versão 3.15' (3.15 é versão do Bioconductor, não do pacote).

**Ressalva:** O encolhimento melhora estabilidade mas pressupõe que a maioria dos genes não é diferencialmente expressa — premissa a declarar.

### `jones2014interproscan` — Tier 2
**Jones P, Binns D, Chang HY, Fraser M, Li W, McAnulla C, McWilliam H, Maslen J, Mitchell A, Nuka G, Pesseat S, Quinn AF, Sangrador-Vegas A, Scheremetjew M, Yong SY, Lopez R, Hunter S.** (2014). InterProScan 5: genome-scale protein function classification. `Bioinformatics` 2014;30(9):1236-1240.

DOI: [10.1093/bioinformatics/btu031](https://doi.org/10.1093/bioinformatics/btu031) · PMID: [24451626](https://pubmed.ncbi.nlm.nih.gov/24451626/) · PMC: PMC3998142
**Lido de:** **abstract** · arquivo: `fulltext/jones2014interproscan.txt`

**O que estabelece:** InterProScan 5, classificação funcional de proteínas em escala genômica.

**Onde entra:** Metodologia §11 — anotação de domínios, complementar ao eggNOG-mapper.

**Ressalva:** Só metadados e título conferidos.

### `liao2014featurecounts` — Tier 2
**Liao Y, Smyth GK, Shi W.** (2014). featureCounts: an efficient general purpose program for assigning sequence reads to genomic features. `Bioinformatics` 2014;30(7):923-930.

DOI: [10.1093/bioinformatics/btt656](https://doi.org/10.1093/bioinformatics/btt656) · PMID: [24227677](https://pubmed.ncbi.nlm.nih.gov/24227677/)
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `ewels2016multiqc` — Tier 2
**Ewels P, Magnusson M, Lundin S, Käller M.** (2016). MultiQC: summarize analysis results for multiple tools and samples in a single report. `Bioinformatics` 2016;32(19):3047-3048.

DOI: [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354) · PMID: [27312411](https://pubmed.ncbi.nlm.nih.gov/27312411/) · PMC: PMC5039924
**Lido de:** **abstract** · arquivo: `fulltext/ewels2016multiqc.txt`

**O que estabelece:** MultiQC agrega resultados de múltiplas ferramentas e múltiplas amostras num relatório único.

**Onde entra:** Metodologia §11 — etapa de QC agregado.

**Ressalva:** Ferramenta de relatório; não substitui inspeção do QC por amostra.

### `patro2017salmon` — Tier 2
**Patro R, Duggal G, Love MI, Irizarry RA, Kingsford C.** (2017). Salmon provides fast and bias-aware quantification of transcript expression. `Nat Methods` 2017;14(4):417-419.

DOI: [10.1038/nmeth.4197](https://doi.org/10.1038/nmeth.4197) · PMID: [28263959](https://pubmed.ncbi.nlm.nih.gov/28263959/) · PMC: PMC5600148
**Lido de:** **abstract** · arquivo: `fulltext/patro2017salmon.txt`

**O que estabelece:** Apresenta o Salmon, método leve de quantificação de abundância de transcritos, combinando algoritmo de inferência paralela em duas fases, modelos de viés e mapeamento ultrarrápido. É descrito como **o primeiro quantificador transcriptoma-amplo a corrigir viés de conteúdo GC do fragmento**, o que segundo os autores melhora substancialmente a acurácia das estimativas e a sensibilidade da análise de expressão diferencial subsequente.

**Onde entra:** Metodologia §11 — citação canônica da troca de Kallisto 0.44 por Salmon. A correção de viés de GC é o argumento técnico da troca.

**Ressalva:** Artigo-fonte de 2017; a justificativa de escolha *hoje* deve vir de benchmark recente (`sarantopoulou2021comparative`), não deste.

### `chen2018fastp` — Tier 2
**Chen S, Zhou Y, Chen Y, Gu J.** (2018). fastp: an ultra-fast all-in-one FASTQ preprocessor. `Bioinformatics` 2018;34(17):i884-i890.

DOI: [10.1093/bioinformatics/bty560](https://doi.org/10.1093/bioinformatics/bty560) · PMID: [30423086](https://pubmed.ncbi.nlm.nih.gov/30423086/) · PMC: PMC6129281
**Lido de:** **abstract** · arquivo: `fulltext/chen2018fastp.txt`

**O que estabelece:** Artigo original do fastp, pré-processador de FASTQ que integra controle de qualidade, filtragem, corte e correção numa passagem.

**Onde entra:** Metodologia §11 — etapa de trimagem, citação canônica.

**Ressalva:** Superado pelo fastp 1.0 (`chen2025fastp`) como descrição da ferramenta atual; citar os dois quando a versão importar.

### `kim2019graph` — Tier 2
**Kim D, Paggi JM, Park C, Bennett C, Salzberg SL.** (2019). Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype. `Nat Biotechnol` 2019;37(8):907-915.

DOI: [10.1038/s41587-019-0201-4](https://doi.org/10.1038/s41587-019-0201-4) · PMID: [31375807](https://pubmed.ncbi.nlm.nih.gov/31375807/) · PMC: PMC7605509
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `ewels2020core` — Tier 2
**Ewels PA, Peltzer A, Fillinger S, Patel H, Alneberg J, Wilm A, Garcia MU, Di Tommaso P, Nahnsen S.** (2020). The nf-core framework for community-curated bioinformatics pipelines. `Nat Biotechnol` 2020;38(3):276-278.

DOI: [10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x) · PMID: [32055031](https://pubmed.ncbi.nlm.nih.gov/32055031/)
**Lido de:** nada ainda (só metadados)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `manni2021busco` — Tier 2
**Manni M, Berkeley MR, Seppey M, Zdobnov EM.** (2021). BUSCO: Assessing Genomic Data Quality and Beyond. `Curr Protoc` 2021;1(12):e323.

DOI: [10.1002/cpz1.323](https://doi.org/10.1002/cpz1.323) · PMID: [34936221](https://pubmed.ncbi.nlm.nih.gov/34936221/)
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `wu2021clusterprofiler` — Tier 2
**Wu T, Hu E, Xu S, Chen M, Guo P, Dai Z, Feng T, Zhou L, Tang W, Zhan L, Fu X, Liu S, Bo X, Yu G.** (2021). clusterProfiler 4.0: A universal enrichment tool for interpreting omics data. `Innovation (Camb)` 2021;2(3):100141.

DOI: [10.1016/j.xinn.2021.100141](https://doi.org/10.1016/j.xinn.2021.100141) · PMID: [34557778](https://pubmed.ncbi.nlm.nih.gov/34557778/) · PMC: PMC8454663
**Lido de:** **abstract** · arquivo: `fulltext/wu2021clusterprofiler.txt`

**O que estabelece:** clusterProfiler 4.0: interface universal de análise de enriquecimento funcional **para milhares de organismos**, com ontologias e vias internas mais dados de anotação fornecidos pelo usuário ou obtidos de bases online, e interfaces no estilo *dplyr*/*ggplot2*.

**Onde entra:** Metodologia §11 — enriquecimento GO/KEGG. O suporte a anotação fornecida pelo usuário é o que viabiliza o uso em organismo sem pacote `org.*.db` dedicado, que é o caso de *A. gemmatalis*.

**Ressalva:** Para organismo não-modelo o mapeamento GO vem do eggNOG-mapper; a qualidade do enriquecimento fica limitada pela qualidade dessa anotação, não pelo pacote.

### `cantalapiedra2021eggnog` — Tier 2
**Cantalapiedra CP, Hernández-Plaza A, Letunic I, Bork P, Huerta-Cepas J.** (2021). eggNOG-mapper v2: Functional Annotation, Orthology Assignments, and Domain Prediction at the Metagenomic Scale. `Mol Biol Evol` 2021;38(12):5825-5829.

DOI: [10.1093/molbev/msab293](https://doi.org/10.1093/molbev/msab293) · PMID: [34597405](https://pubmed.ncbi.nlm.nih.gov/34597405/) · PMC: PMC8662613
**Lido de:** **abstract** · arquivo: `fulltext/cantalapiedra2021eggnog.txt`

**O que estabelece:** Atualização maior do eggNOG-mapper, anotação funcional baseada em atribuições de ortologia pré-computadas, agora otimizada para conjuntos (meta)genômicos grandes. A v2 traz genomas e bases funcionais atualizados para o eggNOG v5 e acrescenta: predição gênica *de novo* a partir de contigs brutos, predição de ortologia par-a-par embutida, descoberta rápida de domínios proteicos e decoração automática de GFF.

**Onde entra:** Metodologia §11 — substitui TRAPID/Blast2GO/KOBAS 2.0 (este último descontinuado). A predição a partir de contigs é útil para a via Trinity secundária, de transcritos ausentes da anotação.

**Ressalva:** Anotação por ortologia herda os limites da cobertura do eggNOG para Lepidoptera — não verificado quão bem *A. gemmatalis* está representada.

### `chen2025fastp` — Tier 2
**Chen S.** (2025). fastp 1.0: An ultra-fast all-round tool for FASTQ data quality control and preprocessing. `Imeta` 2025;4(5):e70078.

DOI: [10.1002/imt2.70078](https://doi.org/10.1002/imt2.70078) · PMID: [41112039](https://pubmed.ncbi.nlm.nih.gov/41112039/) · PMC: PMC12527978
**Lido de:** **abstract** · arquivo: `fulltext/chen2025fastp.txt`

**O que estabelece:** Primeira grande atualização do fastp. Apresenta as novidades da versão 1.0 e os princípios de implementação, e **compara com Trimmomatic e Cutadapt** em simplicidade, eficiência e versatilidade.

**Onde entra:** Metodologia §11 — é a referência recente que justifica manter fastp em vez do Trimmomatic que o `.docx` propõe.

**Ressalva:** A comparação é feita pelos próprios autores da ferramenta, não é benchmark independente. Tratar como descrição, não como evidência de superioridade.

### `langer2025empowering` — Tier 2
**Langer BE, Amaral A, Baudement MO, Bonath F, Charles M, Chitneedi PK, Clark EL, Di Tommaso P, Djebali S, Ewels PA, Eynard S, Fellows Yates JA, Fischer D, Floden EW, Foissac S, Gabernet G, Garcia MU, Gillard G, Gundappa MK, Guyomar C, Hakkaart C, Hanssen F, Harrison PW, Hörtenhuber M, Kurylo C, Kühn C, Lagarrigue S, Lallias D, Macqueen DJ, Miller E, Mir-Pedrol J, Moreira GCM, Nahnsen S, Patel H, Peltzer A, Pitel F, Ramayo-Caldas Y, Ribeiro-Dantas MDC, Rocha D, Salavati M, Sokolov A, Espinosa-Carrasco J, Notredame C, Community TN.** (2025). Empowering bioinformatics communities with Nextflow and nf-core. `Genome Biol` 2025;26(1):228.

DOI: [10.1186/s13059-025-03673-9](https://doi.org/10.1186/s13059-025-03673-9) · PMID: [40731283](https://pubmed.ncbi.nlm.nih.gov/40731283/) · PMC: PMC12309086
**Lido de:** **abstract** · arquivo: `fulltext/langer2025empowering.txt`

**O que estabelece:** Reporta desenvolvimentos recentes do framework nf-core com a DSL2 do Nextflow, apresentando uma biblioteca extensa de módulos e subworkflows que permite adoção progressiva de padrões comuns, e o enquadra no paradigma **FAIR** (localizável, acessível, interoperável, reutilizável). Mostra a adoção por comunidades de pesquisa, incluindo seis consórcios EuroFAANG.

**Onde entra:** Metodologia — é a referência **recente** (2025) que justifica adotar padrão nf-core, e conversa com os pipelines Nextflow DSL2 já existentes localmente.

**Ressalva:** Artigo de comunidade/adoção, não benchmark de desempenho. Não sustenta afirmação de que nf-core produz resultado melhor, só de que padroniza e favorece reprodutibilidade.

## 2B — Benchmarks e boas praticas (recencia exigida: 2023+)

### `sarantopoulou2021comparative` — Tier 1
**Sarantopoulou D, Brooks TG, Nayak S, Mrčela A, Lahens NF, Grant GR.** (2021). Comparative evaluation of full-length isoform quantification from RNA-Seq. `BMC Bioinformatics` 2021;22(1):266.

DOI: [10.1186/s12859-021-04198-1](https://doi.org/10.1186/s12859-021-04198-1) · PMID: [34034652](https://pubmed.ncbi.nlm.nih.gov/34034652/) · PMC: PMC8145802
**Lido de:** **abstract** · arquivo: `fulltext/sarantopoulou2021comparative.txt`

**O que estabelece:** Benchmark de quantificação de isoformas de comprimento completo com dado simulado que reproduz propriedades do dado real (polimorfismo, sinal de íntron, cobertura não uniforme), cobrindo métodos baseados em genoma, em transcriptoma e em pseudoalinhamento, com uma abordagem simples como controle. Salmon, kallisto, RSEM e Cufflinks têm a maior acurácia em dado idealizado, mas **em dado realista não superam dramaticamente a abordagem simples**. Os parâmetros estruturais de maior impacto na acurácia são comprimento e complexidade de compressão da sequência, **não o número de isoformas**.

**Onde entra:** Metodologia — calibra a expectativa sobre quantificação por isoforma, que é a base operacional da H1, e é a ressalva honesta a declarar junto com a escolha do Salmon.

**Ressalva:** Dado simulado. O efeito de anotação incompleta é investigado no artigo, mas não extraí a conclusão específica sobre esse ponto — que é justamente o mais relevante aqui. Requer leitura do texto completo antes de citar como justificativa nesse aspecto.

### `chisanga2022impact` — Tier 1
**Chisanga D, Liao Y, Shi W.** (2022). Impact of gene annotation choice on the quantification of RNA-seq data. `BMC Bioinformatics` 2022;23(1):107.

DOI: [10.1186/s12859-022-04644-8](https://doi.org/10.1186/s12859-022-04644-8) · PMID: [35354358](https://pubmed.ncbi.nlm.nih.gov/35354358/) · PMC: PMC8969366
**Lido de:** **abstract** · arquivo: `fulltext/chisanga2022impact.txt`

**O que estabelece:** Compara as anotações Ensembl e RefSeq sobre um conjunto de referência do consórcio SEQC e conclui que **a anotação RefSeq levou a melhor acurácia de quantificação**, avaliada por correlação com verdades de referência que incluem mais de 800 genes validados por PCR em tempo real.

**Onde entra:** Metodologia — sustenta usar a anotação RefSeq `RS_2025_08` do `GCF_050436995.1`, e é a referência que faltava para declarar que a escolha de anotação afeta o resultado da quantificação.

**Ressalva:** Dados humanos, com anotação madura e curada nas duas bases. **Não testa o caso deste projeto**, que é anotação automática de um genoma de não-modelo depositado há pouco — o risco de erro em famílias multigênicas como as serino-proteases permanece, e a curadoria manual segue necessária.

### `coxe2024benchmarking` — Tier 1
**Coxe T, Burks DJ, Singh U, Mittler R, Azad RK.** (2024). Benchmarking RNA-Seq Aligners at Base-Level and Junction Base-Level Resolution Using the <i>Arabidopsis thaliana</i> Genome. `Plants (Basel)` 2024;13(5):582.

DOI: [10.3390/plants13050582](https://doi.org/10.3390/plants13050582) · PMID: [38475429](https://pubmed.ncbi.nlm.nih.gov/38475429/) · PMC: PMC10935055
**Lido de:** **abstract** · arquivo: `fulltext/coxe2024benchmarking.txt`

**O que estabelece:** Benchmark de cinco alinhadores de RNA-Seq muito usados, com dado simulado de *Arabidopsis thaliana* e SNPs anotados do TAIR, medindo acurácia em resolução de base e de base de junção. A motivação declarada é que as ferramentas são tipicamente pré-ajustadas com dados humanos ou procarióticos e **podem não ser adequadas a outros organismos**.

**Onde entra:** Metodologia — é o argumento publicado de que benchmark feito em humano não transfere automaticamente para outro clado, que sustenta declarar a escolha de alinhador como decisão e não como padrão herdado.

**Ressalva:** É planta, não inseto. O argumento sobre transferência entre clados vale; o ranking numérico específico não se transfere para *A. gemmatalis*. Não extraí qual alinhador venceu.

### `jauhal2021assessing` — Tier 2
**Jauhal AA, Newcomb RD.** (2021). Assessing genome assembly quality prior to downstream analysis: N50 versus BUSCO. `Mol Ecol Resour` 2021;21(5):1416-1421.

DOI: [10.1111/1755-0998.13364](https://doi.org/10.1111/1755-0998.13364) · PMID: [33629477](https://pubmed.ncbi.nlm.nih.gov/33629477/)
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `fenn2023alternative` — Tier 2
**Fenn A, Tsoy O, Faro T, Rößler FLM, Dietrich A, Kersting J, Louadi Z, Lio CT, Völker U, Baumbach J, Kacprowski T, List M.** (2023). Alternative splicing analysis benchmark with DICAST. `NAR Genom Bioinform` 2023;5(2):lqad044.

DOI: [10.1093/nargab/lqad044](https://doi.org/10.1093/nargab/lqad044) · PMID: [37260511](https://pubmed.ncbi.nlm.nih.gov/37260511/) · PMC: PMC10227362
**Lido de:** **abstract** · arquivo: `fulltext/fenn2023alternative.txt`

**O que estabelece:** DICAST, framework modular que integra **onze mapeadores splice-aware e oito ferramentas de detecção de eventos** de splicing, com benchmark em dado simulado e em RNA-seq de sangue total. Aponta que os benchmarks anteriores focaram em quantificação de isoformas e mapeamento, negligenciando detecção de eventos. Dois resultados: **STAR e HISAT2 mostraram o melhor equilíbrio entre desempenho e tempo de execução**, e o desempenho das ferramentas de detecção de eventos **varia muito, sem nenhuma superar todas as outras**.

**Onde entra:** Metodologia §11 — sustenta a escolha de STAR ou HISAT2 para o alinhamento genoma-guiado, e é a ressalva honesta a declarar ao escolher rMATS ou DEXSeq para a **hipótese H5** (splicing alternativo): a escolha de ferramenta não é neutra e nenhuma domina.

**Ressalva:** Dado humano (sangue total) e simulado. A conclusão sobre variabilidade entre ferramentas transfere como cautela; o ranking específico não.

## 2C — Transcriptomica de intestino de inseto sob estresse

### `pezenti2021transcriptional` — Tier 1
**Pezenti LF, Sosa-Gómez DR, de Souza RF, Vilas-Boas LA, Gonçalves KB, da Silva CRM, Vilas-Bôas GT, Baranoski A, Mantovani MS, da Rosa R.** (2021). Transcriptional profiling analysis of susceptible and resistant strains of Anticarsia gemmatalis and their response to Bacillus thuringiensis. `Genomics` 2021;113(4):2264-2275.

DOI: [10.1016/j.ygeno.2021.05.012](https://doi.org/10.1016/j.ygeno.2021.05.012) · PMID: [34022342](https://pubmed.ncbi.nlm.nih.gov/34022342/)
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `chen2020differences` — Tier 2
**Chen G, Wang Y, Liu Y, Chen F, Han L.** (2020). Differences in midgut transcriptomes between resistant and susceptible strains of Chilo suppressalis to Cry1C toxin. `BMC Genomics` 2020;21(1):634.

DOI: [10.1186/s12864-020-07051-6](https://doi.org/10.1186/s12864-020-07051-6) · PMID: [32928099](https://pubmed.ncbi.nlm.nih.gov/32928099/) · PMC: PMC7490912
**Lido de:** **abstract** · arquivo: `fulltext/chen2020differences.txt`

**O que estabelece:** Compara transcriptomas de intestino médio de cepas resistente e suscetível de *Chilo suppressalis* frente à toxina Cry1C, com montagem *de novo* de **139.206 unigenes** a partir de 373 milhões de leituras Illumina HiSeq e Roche 454.

**Onde entra:** Tema 2, eixo 2C — desenho análogo ao deste projeto (transcriptoma de intestino médio, resistente × suscetível), útil como referência de escala e de estrutura de comparação.

**Ressalva:** Espécie diferente, e o estressor é toxina Bt, não inibidor de protease. Montagem *de novo*, que é justamente a abordagem que este projeto abandona por ter genoma de referência. Só o abstract foi lido; não extraí quais genes saíram diferencialmente expressos.

### `pezenti2023transposable` — Tier 2 ✅ ja em docs/referencias.bib
**Pezenti LF, Dionisio JF, Sosa-Gómez DR, de Souza RF, da Rosa R.** (2023). Transposable elements in the transcriptome of the velvetbean caterpillar <i>Anticarsia gemmatalis</i> Hübner, 1818 (Lepidoptera: Erebidae). `Genome` 2023;66(6):116-130.

DOI: [10.1139/gen-2022-0066](https://doi.org/10.1139/gen-2022-0066) · PMID: [36971261](https://pubmed.ncbi.nlm.nih.gov/36971261/)
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

### `pejendino2026expression` — Tier 2
**Pejendino BJM, Cadena VEM, Rodríguez MCD, Gonzalez CS, Velasquez-Vasconez PA.** (2026). RNA-seq Co-Expression Analysis Reveals a Midgut-Associated Digestive Gene Module in &lt;i&gt;Helicoverpa armigera&lt;/i&gt;. `BioTech (Basel)` 2026;15(3):53.

DOI: [10.3390/biotech15030053](https://doi.org/10.3390/biotech15030053) · PMID: [42496569](https://pubmed.ncbi.nlm.nih.gov/42496569/)
**Lido de:** nada ainda (abstract disponível)

**O que estabelece:** ⚠️ PENDENTE DE FICHAMENTO
**Onde entra:** ⚠️ PENDENTE

## 2D — Fronteira 2024-2026

### `pardopalacios2024systematic` — Tier 1
**Pardo-Palacios FJ, Wang D, Reese F, Diekhans M, Carbonell-Sala S, Williams B, Loveland JE, De María M, Adams MS, Balderrama-Gutierrez G, Behera AK, Gonzalez Martinez JM, Hunt T, Lagarde J, Liang CE, Li H, Meade MJ, Moraga Amador DA, Prjibelski AD, Birol I, Bostan H, Brooks AM, Çelik MH, Chen Y, Du MRM, Felton C, Göke J, Hafezqorani S, Herwig R, Kawaji H, Lee J, Li JL, Lienhard M, Mikheenko A, Mulligan D, Nip KM, Pertea M, Ritchie ME, Sim AD, Tang AD, Wan YK, Wang C, Wong BY, Yang C, Barnes I, Berry AE, Capella-Gutierrez S, Cousineau A, Dhillon N, Fernandez-Gonzalez JM, Ferrández-Peral L, Garcia-Reyero N, Götz S, Hernández-Ferrer C, Kondratova L, Liu T, Martinez-Martin A, Menor C, Mestre-Tomás J, Mudge JM, Panayotova NG, Paniagua A, Repchevsky D, Ren X, Rouchka E, Saint-John B, Sapena E, Sheynkman L, Smith ML, Suner MM, Takahashi H, Youngworth IA, Carninci P, Denslow ND, Guigó R, Hunter ME, Maehr R, Shen Y, Tilgner HU, Wold BJ, Vollmers C, Frankish A, Au KF, Sheynkman GM, Mortazavi A, Conesa A, Brooks AN.** (2024). Systematic assessment of long-read RNA-seq methods for transcript identification and quantification. `Nat Methods` 2024;21(7):1349-1363.

DOI: [10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3) · PMID: [38849569](https://pubmed.ncbi.nlm.nih.gov/38849569/) · PMC: PMC11543605
**Lido de:** **abstract** · arquivo: `fulltext/pardopalacios2024systematic.txt`

**O que estabelece:** Consórcio LRGASP: mais de 427 milhões de leituras longas de cDNA e de RNA direto, em humano, camundongo e peixe-boi, avaliando detecção de isoformas, quantificação e detecção *de novo*. Resultados centrais: **bibliotecas com leituras mais longas e mais acuradas produzem transcritos mais acurados do que bibliotecas com maior profundidade**, enquanto maior profundidade melhora a acurácia de quantificação; em genomas bem anotados as ferramentas baseadas em referência têm o melhor desempenho; e recomenda-se dado ortogonal adicional e réplicas quando o alvo são transcritos raros ou novos, ou quando se usa abordagem sem referência.

**Onde entra:** Metodologia, eixo de fronteira — é a referência para decidir se vale acrescentar long-read para resolver isoformas de tripsina, e a base do trade-off comprimento × profundidade.

**Ressalva:** Espécies com anotação madura. A recomendação do próprio artigo sobre abordagens sem referência e dado ortogonal é o que mais se aproxima do caso de *A. gemmatalis*, cuja anotação é automática e recente.

### `yan2026comprehensive` — Tier 1
**Yan F, Baldoni PL, Lancaster J, Ritchie ME, Lewsey MG, Gouil Q, Davidson NM.** (2026). A comprehensive evaluation of long-read de novo transcriptome assembly. `Genome Biol` 2026;27(1):102.

DOI: [10.1186/s13059-026-04001-5](https://doi.org/10.1186/s13059-026-04001-5) · PMID: [41709347](https://pubmed.ncbi.nlm.nih.gov/41709347/) · PMC: PMC13020369
**Lido de:** **abstract** · arquivo: `fulltext/yan2026comprehensive.txt`

**O que estabelece:** Avalia os montadores *de novo* de leitura longa RATTLE, RNA-Bloom2 e isONform contra o Trinity (leitura curta), em dado simulado com transcritos sequin e dado real de humano e ervilha, em profundidades de 6 a 60 milhões de leituras, cobrindo ONT cDNA, ONT RNA direto e PacBio.

**Onde entra:** Metodologia — informa se a via Trinity secundária, prevista para transcritos ausentes da anotação, deveria migrar para long-read.

**Ressalva:** ⚠️ Li apenas objetivos e desenho no abstract. **Não extraí qual ferramenta teve melhor desempenho nem sob quais condições** — não citar como justificativa de escolha antes de ler os resultados. O texto completo está em `fulltext/yan2026comprehensive.txt`.

### `morabito2023hdwgcna` — Tier 2
**Morabito S, Reese F, Rahimzadeh N, Miyoshi E, Swarup V.** (2023). hdWGCNA identifies co-expression networks in high-dimensional transcriptomics data. `Cell Rep Methods` 2023;3(6):100498.

DOI: [10.1016/j.crmeth.2023.100498](https://doi.org/10.1016/j.crmeth.2023.100498) · PMID: [37426759](https://pubmed.ncbi.nlm.nih.gov/37426759/) · PMC: PMC10326379
**Lido de:** **abstract** · arquivo: `fulltext/morabito2023hdwgcna.txt`

**O que estabelece:** hdWGCNA, framework para redes de coexpressão em dados transcriptômicos de alta dimensão (single-cell e espacial), com inferência de rede, identificação de módulos, enriquecimento, testes estatísticos e visualização. Notavelmente, é **capaz de fazer análise de rede em nível de isoforma** usando single-cell de leitura longa.

**Onde entra:** Tema 2, fronteira — a análise de rede **em nível de isoforma** é conceitualmente o que a hipótese H1 pede, ainda que aqui aplicada a single-cell.

**Ressalva:** Foi feito para single-cell e espacial; este projeto é bulk RNA-Seq. Aplicabilidade direta **não verificada** — não citar como ferramenta escolhida, apenas como direção.

### `athavudeen2026pervasive` — Tier 2
**Athavudeen S, Issac N, Norris A.** (2026). Pervasive non-triplet alternative splicing drives functional isoform diversity. `Nat Commun` 2026;17(1):5112.

DOI: [10.1038/s41467-026-71615-5](https://doi.org/10.1038/s41467-026-71615-5) · PMID: [41963350](https://pubmed.ncbi.nlm.nih.gov/41963350/) · PMC: PMC13247117
**Lido de:** **abstract** · arquivo: `fulltext/athavudeen2026pervasive.txt`

**O que estabelece:** Investiga a prevalência global, a regulação e a função do **splicing alternativo não-triplete** (em que as isoformas não mantêm o mesmo quadro de leitura) *in vivo* em *C. elegans*, usando RNA-Seq de tipo selvagem e de mutantes deficientes em NMD. Registra que o splicing não-triplete é às vezes tratado como evidência de erro ou ruído, e classifica suas consequências moleculares em três classes, incluindo isoformas sensíveis a NMD.

**Onde entra:** Tema 2, fronteira — relevante para a **hipótese H5**: se aparecer splicing alternativo em tripsinas, este trabalho é o argumento de que nem todo evento não-triplete é ruído, e o alerta de que NMD precisa ser considerado na interpretação.

**Ressalva:** *C. elegans*, não inseto. Só o abstract foi lido; não extraí as três classes nem a prevalência quantificada.
