
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
> (concordância Spearman 0,98–0,99, §3.11). Ver `docs/07_analise_rnaseq.md`
> para o plano completo das fases seguintes (FASE 4/5, correção de lote
> condicional + DESeq2, ainda não iniciadas).
>
> **Versão em inglês:** `artigo.md` (mantida em paralelo, sincronizada a
> cada atualização — esta é a tradução fiel, não um resumo).
>
> **Índice-mestre de material (figuras/tabelas/código/dados, para geração
> futura de Word/PPTX):** `INDICE_MATERIAL.md`.

# Resposta transcriptômica do intestino médio de *Anticarsia gemmatalis* ao inibidor peptídico de protease GORE3

**Eulálio Gutemberg Bonfim dos Santos Jr.¹\*, [demais autores a definir]**

¹ Laboratory of Enzymology and Biochemistry of Proteins and Peptides,
Departamento de Bioquímica e Biologia Molecular, Universidade Federal de
Viçosa (UFV), BIOAGRO/INCT-IPP, Viçosa-MG, Brasil

\*Correspondência: eulalio.santos@ufv.br

---

## Resumo

*[PENDENTE — o resumo só será escrito quando houver resultados de expressão
diferencial (FASE 5) para sintetizar. Um resumo escrito agora, cobrindo só
QC de dados brutos, não resumiria um achado científico substantivo — seria
preenchimento de seção por completude, o que este documento evita
explicitamente.]*

---

## 1. Introdução

*[PENDENTE — a introdução deste artigo deve ser derivada de
`docs/01_fundamentacao_teorica.md`, `docs/02_estado_da_arte_GORE.md` e
`docs/05_lacunas_e_hipoteses.md`, já auditados e com citação verificada.
Será escrita como bloco próprio, não copiada diretamente desses documentos
sem revisão de contexto para formato de artigo.]*

---

## 2. Material e Métodos

### 2.1 Material biológico e desenho experimental

Lagartas de *Anticarsia gemmatalis* em quinto ínstar foram alimentadas com
dieta artificial suplementada com um de quatro tratamentos: controle não
tratado, benzamidina (controle positivo sintético), SKTI (inibidor natural
de tripsina do tipo Kunitz) ou GORE3 (o peptídeo inibidor em estudo), com
três réplicas biológicas por tratamento (tecido de intestino médio, uma
réplica por pool de larvas). Uma amostra adicional, de corpo gorduroso, sem
réplica, foi incluída fora desse desenho de 4 grupos. A identidade das
amostras e a atribuição a grupo de tratamento foram resolvidas a partir da
planilha de submissão à Macrogen (`identificacao-amostras.xlsx`) e
confirmadas contra a entrega dos dados brutos; a correspondência está
registrada na Tabela S1 (`codigo/fase1_blocoA/samplesheet.tsv`).

### 2.2 Sequenciamento de RNA

O RNA total foi sequenciado pela Macrogen Inc. (pedido HN00280302, entregue
em 24/07/2026) em leituras pareadas de 2×151 pb, usando o kit de biblioteca
Illumina Stranded mRNA Prep, Ligation. A identidade do instrumento de
sequenciamento não foi declarada explicitamente no relatório do fornecedor
("Illumina platform"); foi inferida a partir do prefixo do ID do
instrumento nos headers dos reads FASTQ (`LH00xxx`, consistente com a série
Illumina NovaSeq X) — reportada aqui como inferência a partir do conteúdo
bruto do header, não como especificação confirmada pelo fornecedor.
Instrumentos NovaSeq usam química de sequenciamento-por-síntese de duas
cores, na qual a ausência de sinal de luz é lida como G; à medida que o
sequenciamento avança e o sinal por cluster enfraquece, isso pode fazer
bases T/C verdadeiras serem lidas erroneamente como G, produzindo caudas
poli-G (Chen et al., 2018) — a base mecanística do parâmetro
`--trim_poly_g` adotado no §2.4. Treze
bibliotecas foram entregues como 26 arquivos FASTQ brutos (~47 GB). A
integridade dos arquivos foi verificada contra os checksums MD5 fornecidos
pelo fornecedor para os 26 arquivos (100% de correspondência;
`codigo/fase1_blocoA/md5sum.txt`).

### 2.3 Controle de qualidade dos dados brutos

A qualidade dos reads brutos foi avaliada com FastQC v0.12.1 e agregada com
MultiQC v1.33 (Ewels et al., 2016), rodados num ambiente Conda/Mamba
dedicado num servidor Linux (32 núcleos de CPU, 188 GB de RAM),
independentemente do próprio relatório de QC do fornecedor. As versões
exatas das ferramentas e a especificação completa do ambiente estão
registradas em `resultados/blocoA_ENV_VERSIONS.txt`.

As contagens totais de reads por arquivo, obtidas do FastQC, foram
cruzadas contra os totais reportados pelo fornecedor para as 13 amostras, e
as contagens de reads entre pares (R1/R2) foram checadas quanto à
concordância exata dentro de cada par.

Para testar se o defeito de qualidade localizado, visível nos gráficos de
qualidade-por-base do fornecedor para três bibliotecas, refletia um
artefato compartilhado da corrida de sequenciamento, nós (i) extraímos os
identificadores de instrumento, flowcell e lane do primeiro header de read
FASTQ de cada biblioteca; (ii) calculamos, a partir do módulo "Per base
sequence quality" do FastQC, o escore Phred médio numa janela de ciclos do
read 1 declarada *antes* de inspecionar as identidades por amostra (ciclos
44–90, correspondendo à faixa de posição visualmente aparente nos gráficos
do fornecedor) versus a região de flanco (ciclos 1–43 e 91–151), marcando
como suspeita qualquer biblioteca com queda flanco-menos-janela superior a
5,0 Phred; e (iii) inspecionamos o módulo "Per tile sequence quality" do
FastQC em busca de evidência de defeitos localizados por tile. Código de
análise: `codigo/fase1_blocoA/analyze_blocoA.py`.

### 2.4 Trimagem de reads (FASE 1, Bloco B)

Dois conjuntos candidatos de parâmetros do fastp v1.3.0 foram comparados
empiricamente antes de fechar um deles para o lote completo, porque a
literatura citada do projeto (Chen, 2025; Chen et al., 2018) justifica
escolher fastp em vez de Trimmomatic/Cutadapt, mas não dá orientação
numérica de limiar (declarado como Limitação 2 na versão anterior deste
documento): **Set A** (`--detect_adapter_for_pe --length_required 36
--qualified_quality_phred 20`, batendo com o valor originalmente registrado
em `docs/07_analise_rnaseq.md`) e **Set B** (`--detect_adapter_for_pe
--length_required 50 --qualified_quality_phred 20 --trim_poly_g
--trim_poly_x --overrepresentation_analysis`, batendo com o módulo de
produção do pipeline irmão `RNA-Seq-not-model`, adaptado para fastp 1.3.0).
Os dois conjuntos foram rodados em duas bibliotecas representativas —
Control_R1 (limpa) e Benzamidine_R3 (pior perfil de QC bruto) —
comparando sobrevivência de reads, Q20/Q30 pós-filtragem, e a
decomposição das categorias de `filtering_result` que o fastp reporta.
Código: `codigo/fase1_blocoB/run_fastp_ab_test.sh`,
`codigo/fase1_blocoB/compare_ab_test.py`; comparação completa:
`resultados/blocoB_ab_test_comparison.csv`.

Com base no resultado do teste A/B (§3.5), o Set B foi selecionado e
aplicado às 13 bibliotecas (26 arquivos) numa única rodada em lote
(`codigo/fase1_blocoB/run_fastp_full_trim.sh`), produzindo FASTQ trimado
em `trimmed/` e um relatório JSON/HTML do fastp por biblioteca em
`qc/post_trim/`. Os resultados de QC pós-trimagem são analisados em
`codigo/fase1_blocoB/analyze_blocoB.py`.

Alinhamento e quantificação (FASE 2 em diante) ainda não tinham sido
executados no momento da redação desta seção e não são reportados abaixo.

### 2.4.1 Teste de equilíbrio de parâmetros de trimagem (FASE 1, Bloco C)

Como quatro bibliotecas (Benzamidine_R2/R3, SKTI_R1/R2) perderam 17,6–37,5%
dos reads para a classificação `adapter_dimer_reads` do fastp sob o Set B
(§3.6), testamos se afrouxar os parâmetros de trimagem recuperaria reads
sem custo de qualidade, em vez de assumir que o Set B já era ótimo.
Subamostras determinísticas de 2.000.000 pares (`seqtk` 1.5, seed `-s100`)
foram extraídas de Control_R1 (referência limpa) e das quatro bibliotecas
afetadas (`codigo/fase1_blocoC/subsample_reads.sh`), depois trimadas com
quatro configurações do fastp
(`codigo/fase1_blocoC/run_fastp_paramsweep.sh`): **Set B** (linha de base
de produção); **Set C1** (`--qualified_quality_phred 15` em vez de 20);
**Set C2** (overlap-analysis mais permissivo:
`--overlap_len_require 20 --overlap_diff_limit 8
--overlap_diff_percent_limit 30`, vs. padrão do fastp 30/5/20); **Set C3**
(overlap-analysis mais restritivo, como contraprova de sanidade:
`--overlap_len_require 40 --overlap_diff_limit 3
--overlap_diff_percent_limit 10`). `--length_required 50` e as flags de
poly-G/poly-X/detecção de adaptador ficaram fixas em todos os sets, já que
o §3.5 já mostrou que `--length_required` não afeta a sobrevivência.

Para arbitrar com dado além das métricas do próprio fastp, os reads
trimados de cada combinação amostra×set foram alinhados com HISAT2 2.2.2
contra um índice **piloto** de `GCF_050436995.1` construído sem anotação de
splice sites (`codigo/fase1_blocoC/build_hisat2_index_pilot.sh`, FASTA do
genoma reaproveitado de outro projeto local, `~/vg_search/genome/`) —
adequado para comparar taxa de mapeamento geral entre configurações, não
para quantificação em nível de isoforma; este piloto precede e é
independente do alinhamento genoma-guiado formal da FASE 2 nas 13
bibliotecas completas. Regra de decisão pré-declarada
(`codigo/fase1_blocoC/analyze_blocoC.py`): um set candidato só substituiria
o Set B na produção se, nas quatro bibliotecas afetadas simultaneamente,
(i) a sobrevivência de reads subisse ≥5 pontos percentuais em relação ao
Set B, (ii) o Q30 pós-trim permanecesse ≥95%, (iii) a taxa de mapeamento
do piloto HISAT2 não caísse, e (iv) a biblioteca controle limpa não fosse
prejudicada. Resultados completos:
`resultados/blocoC_param_sweep.csv`.

### 2.5 Alinhamento genoma-guiado (FASE 2)

**Bloco A — piloto de seleção de alinhador.** Como nenhum alinhador único é
ótimo tanto para quantificação em nível de gene quanto para detecção de
junção de splicing (Coxe et al., 2024), STAR 2.7.10b e HISAT2 2.2.2 foram
comparados lado a lado num subconjunto de cinco amostras cobrindo os quatro
grupos de tratamento mais uma réplica adicional (Control_R1/ID-1;
Benzamidine_R2/ID-7, Benzamidine_R3/ID-8; SKTI_R1/ID-9, SKTI_R2/ID-10),
usando as bibliotecas completas trimadas (Set B) contra um índice do genoma
construído a partir de `GCF_050436995.1` com o GTF da RS_2026_04 como guia
de junção de splicing (`--outSAMtype None`, sem escrever BAM — esta etapa
só mede taxa de mapeamento). Código:
`codigo/fase2_blocoA/run_star_hisat2_subsample.sh`,
`build_star_index.sh`/`build_hisat2_index_annotated.sh`,
`convert_gff_to_gtf.sh`; análise: `codigo/fase2_blocoA/analyze_fase2_blocoA.py`;
resultado completo: `resultados/fase2_blocoA_star_vs_hisat2.csv`. Regra de
decisão, combinada com o orientador do projeto antes de inspecionar os
resultados: o alinhador com vantagem de taxa de mapeamento ≥2 pontos
percentuais nas amostras-piloto seria rodado sozinho no lote completo, em
vez de rodar os dois alinhadores nas 13 bibliotecas.

**Bloco B — alinhamento do lote completo, duas vias paralelas.** Seguindo a
decisão do Bloco A (§3.9), o alinhador vencedor (STAR) foi rodado nas 13
bibliotecas trimadas com saída em BAM (`--outSAMtype BAM SortedByCoordinate
--twopassMode Basic`), produzindo o entregável usado depois para
quantificação em nível de gene (FASE 3) — código:
`codigo/fase2_blocoB/run_alignment_full.sh`. Em paralelo, o Subread-align
2.1.1 foi rodado nas mesmas 13 bibliotecas trimadas como a via dedicada de
acurácia de junção de splicing (Coxe et al., 2024 reportam o Subread como o
mais promissor em acurácia de mapeamento em nível de junção, em vez de em
nível de base — a propriedade de que depende a análise de splicing
alternativo da FASE 6, H1 e H5) — código:
`codigo/fase2_blocoB/run_subread_align_full.sh`. Os dois scripts são
retomáveis (um marcador de conclusão por amostra é checado antes de
rerodar) e toleram falha isolada de uma amostra sem abortar as demais
(`set -uo pipefail`, não `set -e`), porque a primeira tentativa de execução
mostrou que rodar os dois jobs de 16 threads simultaneamente no servidor
causou falhas de segmentação num subconjunto de amostras em ambas as
ferramentas (§3.9, §5 item 9) — um achado operacional/de agendamento, não
uma propriedade dos dados de sequenciamento.

### 2.6 Quantificação em nível de gene e transcrito (FASE 3)

O objetivo da FASE 3 é alimentar os contrastes de grupo (GORE3 vs.
Controle, GORE3 vs. Benzamidina, GORE3 vs. SKTI — o entregável central do
estudo, §6.1 do documento de planejamento) com uma matriz de contagem de
genes de produção; a via de transcrito/isoforma é uma análise secundária,
de apoio à hipótese H1 (troca de isoformas de tripsina), não o objetivo
principal desta fase.

**Confirmação da orientação da biblioteca.** Os dois scripts escritos mas
ainda não executados no momento da redação da FASE 2
(`codigo/fase2_blocoB/check_strandedness.sh`, `analyze_strandedness.py`)
foram executados contra os BAMs do STAR de ID-1 e ID-8: featureCounts foi
rodado duas vezes por amostra (`-s 1` vs. `-s 2`) contra o GTF real, e a
configuração que atribuiu a maior fração de reads a genes foi tomada como
vencedora. Reverse-stranded (`-s 2` / `--libType ISR` do Salmon) venceu de
forma decisiva e consistente nas duas amostras (§3.11), substituindo a
inferência provisória baseada no nome do kit. Código:
`codigo/fase3_blocoA/decide_libtype.py` formaliza isso como a fonte única
de verdade (`resultados/fase3_blocoA_strand_decision.csv`) lida por todo
script seguinte.

**Um defeito de GTF não planejado, encontrado e corrigido.** Rodar o
featureCounts pela primeira vez falhou com "failed to find the gene
identifier attribute in the 9th column." A inspeção encontrou 330 das
515.035 linhas do GTF (118 genes, todos loci "LOC" não caracterizados, sem
registro de mRNA no GFF3 de origem) com `transcript_id` mas sem `gene_id`
— o gffread (usado na FASE 2) não propaga `gene_id` quando um gene do
GFF3 não tem hierarquia explícita gene→mRNA→exon. A correção
(`codigo/fase3_blocoA/fix_gtf_missing_geneid.sh`) é exata, não
aproximada: para essas 330 linhas, o valor de `transcript_id` já existente
é exatamente o que `gene_id` deveria ser (mesma convenção
`"gene-<nome>"` usada no resto do arquivo, confirmada sem exceção nas 330
linhas antes de aplicar a correção), então a correção adiciona `gene_id`
usando dado já presente na mesma linha, não um valor fabricado. Nenhum
dos 118 genes afetados é uma tripsina/serino-protease conhecida. A FASE 2
(STAR) não precisa ser refeita, já que o uso do GTF pelo STAR (guia de
splice sites) não depende de `gene_id`; toda a FASE 3 em diante usa o GTF
corrigido (`GCF_050436995.1_RS_2026_04.fixed.gtf`).

**Quantificação em nível de gene (via prioritária).** featureCounts
v2.1.1 foi rodado uma única vez sobre os 13 BAMs do STAR, GTF real
corrigido, strand reverso confirmado, `-p -g gene_id -t exon` — código:
`codigo/fase3_blocoC/run_featurecounts_genelevel.sh`. **Deliberadamente
não usado: `-M -O --fraction`** (resgate de reads multi-mapeados/
multi-sobrepostos). Zytnicki (2017, PMID 28915787, "mmquant: how to count
multi-mapping reads?") declara diretamente que habilitar essas flags
"quase sempre produz resultados enviesados." Isso cria uma tensão real,
não declarada como resolvida, específica deste projeto: a hipótese
secundária H1 trata de uma família multigênica de serino-proteases tipo
tripsina, onde reads de parálogos próximos podem mapear ambiguamente, e o
featureCounts padrão vai descartar/subcontar esses reads exatamente
nesses genes. Isso não afeta o entregável principal da fase (contrastes
de grupo inteiros); fica em aberto para a FASE 9 (curadoria manual da
família de serino-proteases) revisitar especificamente para esse conjunto
de genes, não resolvido aqui. Uma busca dirigida por um benchmark
equivalente em insetos ou famílias multigênicas não encontrou nada
diretamente no ponto; a evidência mais próxima disponível, Kwon (2015,
PMID 26112470, quantificação de genes duplicados em *Xenopus*, acesso só
ao abstract), não é em insetos e não é citada como resolvendo essa
lacuna — só como o análogo mais próximo disponível.

**Quantificação em nível de transcrito (Blocos D-E, apoio a H1).** O
Salmon 1.10.3 foi indexado em modo decoy-aware ("selective alignment",
genoma inteiro como decoy), não no modo `--type quasi` sem decoy,
desatualizado, usado no módulo reaproveitável
(`RNA-Seq-not-model/modules/quantification.nf`). Srivastava et al. (2020,
PMID 32894187, *Genome Biology*) estabeleceram que a indexação
decoy-aware reduz atribuição espúria de reads em relação ao mapeamento
sem decoy, validado em 109 datasets reais humanos + simulações de
camundongo — **nenhum genoma de inseto ou não-modelo foi testado nesse
benchmark**; o achado estrutural (decoys reduzem atribuição errada) é uma
extrapolação razoável para *A. gemmatalis*, não um fato estabelecido para
esta espécie, no mesmo padrão da ressalva de Coxe et al. (2024,
planta→inseto) já declarada no §2.5. Construção do índice:
`codigo/fase3_blocoD/build_salmon_decoy_index.sh` (transcriptoma extraído
via `gffread` + decoy do genoma inteiro, `k=31`, default do próprio
Salmon, não ajustado para este genoma). Quantificação:
`codigo/fase3_blocoD/run_salmon_quant_full.sh` (`--libType ISR`,
`--validateMappings --gcBias`, sem alteração em relação ao pipeline
irmão). Adaptação do tximport (`codigo/fase3_blocoE/build_tx2gene.py`,
`00_tximport_gore3.R`): a única mudança real em relação a
`RNA-Seq-not-model/scripts/00_tximport.R` é ler um `tx2gene.tsv`
construído direto dos atributos `transcript_id`/`gene_id` do GTF real, em
vez de um `gene_trans_map` do Trinity que não existe neste desenho
genoma-guiado; a chamada `tximport()` em si, justificada por
`soneson2015differential` (já citada, §2.5), não muda.

---

## 3. Resultados

### 3.1 Rendimento e identidade das bibliotecas confirmados independentemente do relatório do fornecedor

As contagens de reads derivadas do FastQC bateram exatamente com os totais
reportados pelo fornecedor nas 13 amostras (ex.: Control_R1: 32.550.688 × 2
= 65.101.376 reads, idêntico ao total do fornecedor; Benzamidine_R3:
39.460.179 × 2 = 78.920.358, idêntico). As contagens de pares R1/R2 foram
idênticas em todos os pares (13/13). Esta é uma confirmação independente,
em nível de conteúdo de reads, além da checagem de integridade por
checksum do §2.2.

### 3.2 Um defeito de qualidade confinado a três bibliotecas, por um critério pré-declarado

A qualidade média do R1 caiu mais de 5 Phred na janela de ciclos 44–90 em
relação aos ciclos de flanco em exatamente três das 13 bibliotecas —
Benzamidine_R2 (ΔQ = 5,48), Benzamidine_R3 (ΔQ = 5,75) e SKTI_R2
(ΔQ = 5,46) — e em nenhuma das outras dez (faixa de ΔQ 0,08–1,81; Fig. 1,
Tabela 1). O critério foi aplicado uniformemente às 13 bibliotecas, não só
às três originalmente sinalizadas por inspeção visual do relatório do
fornecedor, e reproduziu exatamente essa sinalização original (nenhum
falso positivo ou negativo contra o limiar pré-declarado).

**Tabela 1 | Estatísticas resumidas de reads brutos e teste da janela de
qualidade, por amostra.**

| Amostra | Tratamento / réplica | Reads (R1) | Pares R1/R2 batem | ΔQ (ciclos 44–90) | Sinalizada |
|---|---|---:|:---:|---:|:---:|
| ID-1 | Control_R1 | 32.550.688 | sim | 0,08 | não |
| ID-2 | Control_R2 | 33.504.042 | sim | 0,89 | não |
| ID-3 | Control_R3 | 29.090.048 | sim | 1,08 | não |
| ID-5 | Benzamidine_R1 | 27.500.647 | sim | 0,73 | não |
| ID-7 | Benzamidine_R2 | 28.930.368 | sim | 5,48 | **sim** |
| ID-8 | Benzamidine_R3 | 39.460.179 | sim | 5,75 | **sim** |
| ID-9 | SKTI_R1 | 31.172.157 | sim | 1,81 | não |
| ID-10 | SKTI_R2 | 30.906.748 | sim | 5,46 | **sim** |
| ID-12 | SKTI_R3 | 33.545.221 | sim | 0,33 | não |
| ID-14 | GORE3_R1 | 27.090.197 | sim | 0,35 | não |
| ID-15 | GORE3_R2 | 31.079.636 | sim | 0,95 | não |
| ID-16 | GORE3_R3 | 29.902.657 | sim | 0,72 | não |
| ID-18 | FatBody | 33.478.105 | sim | 0,42 | não |

*Saída completa e legível por máquina: `resultados/blocoA_results.csv`.*

**Figura 1 | A queda de qualidade dos reads brutos está confinada a três
bibliotecas, definida por uma janela de posição pré-declarada.** O escore
médio de qualidade Phred nos ciclos 44–90 do read 1 foi subtraído da média
da região de flanco (ciclos 1–43 e 91–151) para cada uma das 13
bibliotecas FASTQ brutas (FastQC v0.12.1). Barras vermelhas indicam as três
bibliotecas que excedem o limiar declarado antes de o conjunto de amostras
ser inspecionado (ΔQ > 5,0 Phred, linha tracejada): Benzamidine_R2,
Benzamidine_R3 e SKTI_R2. As dez bibliotecas restantes — abrangendo os
quatro grupos de tratamento e a amostra de corpo gorduroso sem réplica —
ficam abaixo de ΔQ = 1,8. Os rótulos das amostras combinam grupo de
tratamento e número de réplica biológica, resolvidos a partir da planilha
de submissão de amostras da Macrogen (Tabela S1). Arquivo:
`figuras/Figure1_blocoA_quality_dip.png`.

### 3.3 O defeito não acompanha a lane de sequenciamento; a causa física continua em aberto

Os headers dos reads mostraram que 12 das 13 bibliotecas — incluindo tanto
amostras limpas quanto defeituosas — foram sequenciadas no mesmo
instrumento, flowcell e lane (`LH00129`, flowcell `23NNGLLT4`, lane 4).
Apenas Benzamidine_R3 (ID-8) foi sequenciada separadamente, num
instrumento, flowcell e lane inteiramente diferentes (`LH00688`, flowcell
`253LHLLT4`, lane 5).

Isso restringe diretamente as explicações possíveis: como Benzamidine_R2 e
SKTI_R2 dividem lane com as dez bibliotecas não afetadas, uma causa técnica
de toda a lane fica excluída para essas duas especificamente; como
Benzamidine_R3 foi sequenciada numa corrida inteiramente separada, ela não
pode compartilhar uma causa em nível de lane ou flowcell com as outras
duas. Um primeiro teste, grosseiro, resolvido por tile (a marca única
pass/warn/fail do módulo "Per tile sequence quality" do FastQC, agregada
sobre o read inteiro) foi inconclusivo, como relatado na versão anterior
desta seção: as 13 bibliotecas mostraram marcas warn/fail de magnitude
comparável.

### 3.4 Uma reanálise resolvida por posição fecha a lacuna: a heterogeneidade entre tiles é real, localizada, e acompanha o conteúdo de GC

O teste grosseiro acima colapsou o read inteiro de 151 ciclos numa única
marca pass/warn/fail, que não consegue detectar um efeito confinado a uma
janela de 46 ciclos. Repetimos a análise por tile restrita à mesma janela
pré-declarada (ciclos 44–90) usada no §3.2, calculando, para cada amostra e
cada tile físico, o desvio médio de qualidade por tile dentro da janela
versus nos ciclos de flanco, e então comparando a **dispersão (desvio-padrão
populacional) desses valores por tile entre tiles**, na janela versus no
flanco (código: `codigo/fase1_blocoA/per_tile_analysis.py`; saída
completa: `resultados/blocoA1_pertile_results.csv`).

A lógica deste teste: se a queda de qualidade específica da janela reflete
um efeito de química/biblioteca que age igualmente sobre cada cluster,
independentemente da sua posição física, os tiles deveriam discordar entre
si aproximadamente na mesma medida dentro da janela e fora dela (razão ≈
1). Se, em vez disso, tiles físicos específicos são desproporcionalmente
ruins só dentro dessa faixa de ciclos, a dispersão entre tiles deveria ser
muito maior dentro da janela do que fora dela (razão ≫ 1).

**Resultado: a razão está elevada especificamente em quatro bibliotecas, e
ela acompanha o %GC reportado pelo fornecedor, não a pertença à lane.**

| Amostra | Rótulo | %GC (fornecedor) | Desvio-padrão janela | Desvio-padrão flanco | Razão (janela/flanco) |
|---|---|---:|---:|---:|---:|
| ID-8 | Benzamidine_R3 | 63,1 | 0,646 | 0,103 | **6,28** |
| ID-9 | SKTI_R1 | 54,7 | 0,587 | 0,266 | **2,21** |
| ID-7 | Benzamidine_R2 | 59,7 | 0,486 | 0,223 | **2,18** |
| ID-10 | SKTI_R2 | 60,8 | 0,509 | 0,250 | **2,04** |
| ID-16 | GORE3_R3 | 50,3 | 0,317 | 0,255 | 1,25 |
| demais 8 amostras | — | 48,4–53,4 | 0,13–0,24 | 0,18–0,28 | 0,72–0,94 |

Correlação de Pearson entre %GC reportado pelo fornecedor e a razão
janela/flanco, nas 13 amostras: **r = 0,80**; correlação de postos de
Spearman (robusta ao valor extremo de ID-8): **ρ = 0,49**. As quatro
amostras com razão > 2 são exatamente as quatro amostras com maior
conteúdo de GC de todo o lote (59,7–63,1%, contra 48,4–54,7% para as
demais) — incluindo **SKTI_R1 (ID-9)**, que *não* tinha sido sinalizada
pelo critério baseado em média no §3.2 (ΔQ = 1,81, abaixo do limiar de
5,0) mas mostra a segunda maior razão janela/flanco do conjunto de dados.
Isso é reportado como um efeito gradual, correlacionado com GC, não como
um fenômeno estritamente binário de três bibliotecas, como o §3.2 sozinho
sugeriria.

**Figura 2 | A perda de qualidade nos ciclos 44–90 é heterogênea entre
tiles na biblioteca mais afetada e ausente numa biblioteca limpa.** Desvio
de qualidade por tile em relação à média da amostra (FastQC "Per tile
sequence quality", read 1), plotado como tile (posição física no flowcell,
eixo y, ordem arbitrária) por ciclo de sequenciamento (agrupado em bins,
eixo x), para **(a)** Control_R1 (ID-1, limpa; razão janela/flanco 0,72) e
**(b)** Benzamidine_R3 (ID-8, a mais afetada; razão janela/flanco 6,28).
Linhas verticais tracejadas marcam a janela pré-declarada de ciclos 44–90.
Escala de cor: azul, tile melhor que a média da amostra naquele ciclo;
vermelho, tile pior que a média da amostra (unidades Phred, com corte em
±3). Um padrão conspícuo, em faixas alternadas de tiles bons e ruins,
aparece só dentro da janela marcada em ID-8, e está ausente ao longo de
ID-1 e fora da janela em ID-8 — uma assinatura incompatível tanto com uma
causa de lane inteira quanto com uma causa uniforme por toda a biblioteca.
Arquivo: `figuras/Figure2_blocoA1_pertile_heatmap.png`.

**Interpretação, declarada no nível de confiança que o dado de fato
sustenta — nem mais que isso.** Três achados restringem juntos a
explicação: (i) uma causa física de toda a lane está excluída (§3.3: as
bibliotecas não afetadas dividem a mesma lane e os mesmos tiles); (ii) uma
causa pura de composição da biblioteca, agindo uniformemente sobre todos
os clusters, também é incompatível com o dado (previria dispersão baixa,
não alta, entre tiles dentro da janela — o oposto da Fig. 2b); (iii) o
efeito, mesmo assim, está fortemente correlacionado com GC, não distribuído
ao acaso entre bibliotecas. O padrão mais compatível com as três
observações é uma **interação**: um artefato sutil, específico de ciclo,
de imageamento ou foco, afetando a corrida de forma ampla durante os
ciclos 44–90 (invisível em bibliotecas de GC baixo, que toleram sem perda
de qualidade mensurável), que se torna visível especificamente nas
bibliotecas de GC mais alto, cujas propriedades de sinal do cluster deixam
menos margem para absorvê-lo. Este é o relato mais bem sustentado que
temos, não um mecanismo comprovado — não tivemos, e não poderíamos ter só
com a saída do FastQC, testado métricas de foco/iluminação diretamente.
**A causa física precisa está caracterizada com mais profundidade que no
§3.3, mas não está totalmente resolvida, e não afirmamos o contrário.**

### 3.5 O teste A/B de trimagem revela o verdadeiro gargalo, e não é o parâmetro testado

Ao contrário da premissa do teste A/B, a escolha entre
`--length_required 36` e `50` fez quase nenhuma diferença na sobrevivência
de reads em nenhuma das duas bibliotecas (Control_R1: 97,53% vs. 97,48%;
Benzamidine_R3: 62,53% vs. 62,49%). O que o teste de fato revelou, a partir
da decomposição `filtering_result` do próprio fastp, foi a causa real e
dominante da perda de reads em Benzamidine_R3: **25,6% dos pares de reads
foram classificados como `adapter_dimer_reads`** — pares cujo inserto é
tão curto que o read 1 e o read 2 sequenciam um dentro do adaptador do
outro — contra uma fração desprezível em Control_R1. Essa categoria, não
os filtros de comprimento ou qualidade sob teste, responde pela maioria
da perda de reads de Benzamidine_R3, e não fazia parte do espaço de
hipóteses original no §2.3. Como os dois conjuntos de parâmetros tiveram
desempenho idêntico na métrica que de fato importa (sobrevivência), e o
Set B adiciona segurança de poli-cauda/adaptador relevante para a química
NovaSeq X (2 cores) já confirmada (§2.2) sem custo medido, **o Set B foi
adotado para o lote completo**.

### 3.6 Contaminação por adapter-dimer, não um defeito de flowcell, explica o padrão de qualidade dos reads brutos

Aplicando o Set B às 13 bibliotecas e tabulando `adapter_dimer_reads`
(Tabela 2; `resultados/blocoB_trim_summary.csv`), as mesmas quatro
bibliotecas sinalizadas ao longo dos §3.2–3.4 — Benzamidine_R2,
Benzamidine_R3, SKTI_R1, SKTI_R2 — carregam 16–31% de reads
adapter-dimer, contra 1–7% para as outras nove. Isso produz uma correlação
forte com o conteúdo de GC reportado pelo fornecedor (Pearson r = 0,92,
Spearman ρ = 0,63, n = 13; Fig. 3b) — mais apertada que a correlação de
variância por tile do §3.4 (r = 0,80, ρ = 0,49) — e uma sobrevivência de
reads correspondentemente assimétrica (62–82% nas quatro bibliotecas
afetadas vs. 91–97% nas demais; Fig. 3a).

**Tabela 2 | Resultado pós-trimagem por amostra, parâmetros Set B.**

| Amostra | Rótulo | %GC (fornecedor) | Reads adapter-dimer (%) | Sobrevivência (%) | Q30 antes | Q30 depois |
|---|---|---:|---:|---:|---:|---:|
| ID-1 | Control_R1 | 51,8 | 0,96 | 97,48 | 95,58 | 96,66 |
| ID-2 | Control_R2 | 53,4 | 5,79 | 92,93 | 94,47 | 96,34 |
| ID-3 | Control_R3 | 49,1 | 6,60 | 91,67 | 94,44 | 96,55 |
| ID-5 | Benzamidine_R1 | 52,3 | 4,60 | 93,92 | 94,73 | 96,41 |
| ID-7 | Benzamidine_R2 | 59,7 | **31,16** | **66,44** | 90,39 | 96,38 |
| ID-8 | Benzamidine_R3 | 63,1 | **25,58** | **62,49** | 84,14 | 96,80 |
| ID-9 | SKTI_R1 | 54,7 | **16,23** | 82,38 | 94,13 | 96,74 |
| ID-10 | SKTI_R2 | 60,8 | **30,65** | **67,56** | 90,49 | 96,57 |
| ID-12 | SKTI_R3 | 49,1 | 2,21 | 96,56 | 95,55 | 96,86 |
| ID-14 | GORE3_R1 | 48,4 | 2,21 | 95,45 | 95,04 | 96,82 |
| ID-15 | GORE3_R2 | 48,8 | 5,97 | 92,51 | 94,84 | 96,72 |
| ID-16 | GORE3_R3 | 50,3 | 6,47 | 92,12 | 94,87 | 96,62 |
| ID-18 | FatBody | 49,5 | 3,22 | 95,36 | 95,19 | 96,53 |

Um segundo resultado, animador, na mesma tabela: **o Q30 pós-trimagem é
essencialmente uniforme nas 13 bibliotecas (96,3–96,9%)**, incluindo as
quatro afetadas (Benzamidine_R2: 90,4%→96,4%; Benzamidine_R3:
84,1%→96,8%; SKTI_R2: 90,5%→96,6%). A trimagem normaliza completamente a
qualidade de base-calling; o que ela não consegue recuperar é o
rendimento perdido de reads que nunca foram um fragmento biológico
utilizável, para começo de conversa.

**Figura 3 | Sobrevivência de reads e contaminação por adapter-dimer
separam as mesmas quatro bibliotecas sinalizadas pelas métricas de QC
bruto, e correlacionam com o conteúdo de GC.** **(a)** Porcentagem de
pares de reads sobreviventes à trimagem do fastp (parâmetros Set B,
§2.4), por amostra. **(b)** Porcentagem de reads adapter-dimer (fastp
`filtering_result.adapter_dimer_reads`) versus GC reportado pelo
fornecedor, por amostra; Pearson r e Spearman ρ dados no título do
painel. Marcadores vermelhos em ambos os painéis indicam bibliotecas com
taxa de adapter-dimer >10% (Benzamidine_R2, Benzamidine_R3, SKTI_R1,
SKTI_R2); este é um corte visual post-hoc escolhido depois de inspecionar
a distribuição bimodal em (b), não um limiar pré-declarado como na Fig. 1.
Arquivo: `figuras/Figure3_blocoB_trimming.png`.

**Isso revisa, e em boa parte substitui, a interpretação oferecida no
§3.4.** A hipótese de artefato-de-imageamento×sensibilidade-a-GC era o
relato mais bem sustentado *dado apenas a saída do FastQC*; a
contaminação por adapter-dimer é uma explicação mais direta, mais
fortemente correlacionada (r = 0,92 vs. 0,80), e mecanisticamente mais
simples, que também explica naturalmente a heterogeneidade por tile na
Fig. 2 (moléculas de inserto curto lendo para dentro da sequência do
adaptador por volta do ciclo ~44–90 se comportariam de forma diferente de
moléculas de inserto normal, de um jeito que não precisa ser
espacialmente uniforme entre tiles) sem exigir um efeito adicional, não
observado, de imageamento. Não temos uma explicação em nível de preparo
de biblioteca para *por que* essas quatro bibliotecas específicas
carregam mais moléculas de inserto curto/adapter-dimer (isso exigiria
métricas de tamanho de inserto da etapa de QC de biblioteca, que o
relatório de dados brutos da Macrogen não inclui — Limitação 3 na versão
anterior deste documento, agora parcialmente informada, mas não resolvida
por este achado). Uma busca dirigida no PubMed (quatro variantes de
consulta: artefatos de química SBS de duas cores/2 canais; formação de
adapter-dimer/inserto curto vs. conteúdo de GC ou composição da
biblioteca) não retornou nenhum resultado peer-reviewed diretamente
relevante no momento da redação. Reportamos isso como uma busca vazia, não
como ausência de qualquer relação na literatura — a correlação
GC–adapter-dimer do §3.6 é apresentada como achado empírico próprio deste
estudo, não como confirmada pela literatura.

### 3.7 Exposição em nível de grupo e de contraste à profundidade reduzida

Agregar a Tabela 2 por grupo de tratamento torna concreta a consequência
prática do §3.6 (Tabela 3; somas de grupo a partir de
`resultados/blocoB_trim_summary.csv`).

**Tabela 3 | Profundidade pós-trimagem por grupo de tratamento.**

| Grupo | Reads antes (soma, n=3) | Reads depois (soma) | Sobrevivência | Profundidade média depois (por amostra) |
|---|---:|---:|---:|---:|
| Control | 190.289.556 | 179.065.714 | 94,10% | 59,7 M |
| Benzamidine | 191.782.388 | 139.419.904 | **72,70%** | 46,5 M |
| SKTI | 191.248.252 | 157.904.910 | 82,57% | 52,6 M |
| GORE3 | 176.144.980 | 164.311.914 | 93,28% | 54,8 M |

Tanto Benzamidina quanto SKTI perdem 2 de 3 réplicas para profundidade
reduzida (§3.6), mas o impacto prático difere por contraste, porque os
dois grupos desempenham papéis diferentes na matriz de contrastes
planejada (`docs/07_analise_rnaseq.md` §6.1):

**Tabela 4 | Assimetria de profundidade por contraste planejado da FASE 5.**

| # | Contraste | Grupos (sobrevivência) | Assimetria | Papel |
|---|---|---|---|---|
| 1 | GORE3 vs. Controle | 93,3% vs. 94,1% | mínima | Efeito principal |
| 2 | GORE3 vs. Benzamidina | 93,3% vs. **72,7%** | **alta** | 2ª prioridade — GORE3 supera o controle positivo clássico S1-dirigido? |
| 3 | GORE3 vs. SKTI | 93,3% vs. 82,6% | moderada–alta | 3ª prioridade — **H4**, o teste mecanístico de compensação proteolítica |
| 4 | SKTI vs. Controle | 82,6% vs. 94,1% | moderada | Reproduz o padrão conhecido de compensação do SKTI |
| 5 | Benzamidina vs. Controle | **72,7%** vs. 94,1% | **alta** | Efeito do controle positivo isolado |
| 6 | GORE3 vs. (SKTI + Benzamidina agrupados) | 93,3% vs. pool reduzido | **alta** | Herda a perda de profundidade dos dois grupos |

Quatro dos seis contrastes planejados tocam um grupo de profundidade
reduzida. Benzamidina e SKTI carregam a assimetria para partes diferentes
do argumento científico: a perda da Benzamidina pesa mais sobre o
contraste #2, a comparação direta de eficácia contra o padrão
farmacológico clássico; a perda do SKTI pesa mais sobre o contraste #3
(H4), o teste mecanístico que as hipóteses originais do projeto tratam
como central. Nenhuma das duas perdas é severa o bastante, em
profundidade absoluta (46,5–59,7 M reads/amostra pós-trimagem, todas
acima do alvo original de ~40 M), para argumentar contra prosseguir — mas
é severa o bastante para exigir relato explícito por contraste, não
diluído numa única ressalva geral do conjunto de dados.

**Figura 4 | A trimagem normaliza completamente a qualidade de
base-calling em todas as bibliotecas afetadas; ela não recupera — e não
poderia recuperar — a profundidade perdida.** Qualidade Phred média do
read 1 por ciclo, antes (vermelho) e depois (azul-escuro) da trimagem com
fastp (parâmetros Set B, §2.4), para Control_R1 (referência limpa) e as
quatro bibliotecas sinalizadas nos §3.2–3.6 (Benzamidine_R2,
Benzamidine_R3, SKTI_R1, SKTI_R2). Faixa sombreada: a janela
pré-declarada de ciclos 44–90 da Fig. 1. As duas curvas são calculadas
pelo próprio fastp a partir do mesmo arquivo de entrada (curvas de
qualidade `read1_before_filtering`/`read1_after_filtering`), evitando
artefatos de binning entre ferramentas diferentes. Note o vale pré-trim
visivelmente mais brando de SKTI_R1 em relação às outras três, consistente
com ela ter ficado abaixo do limiar binário no §3.2 (Fig. 1) apesar de
carregar a segunda maior taxa de adapter-dimer do conjunto de dados
(§3.6, Tabela 2). Arquivo: `figuras/Figure4_blocoB_before_after.png`;
código: `codigo/fase1_blocoB/plot_before_after_trim.py`.

### 3.8 Afrouxar parâmetros de trimagem não recupera reads: Set B confirmado como equilíbrio empírico

Nenhuma das três configurações candidatas (§2.4.1) recuperou qualquer read
em nenhuma das quatro bibliotecas afetadas. A porcentagem de
`adapter_dimer_reads` ficou **idêntica até a segunda casa decimal** entre o
Set B e os Sets C1/C2 em todas as bibliotecas afetadas (ex.:
Benzamidine_R2: 31,19% nos três; SKTI_R2: 30,65% no Set B e C1, 30,65%
também no C2), e a sobrevivência diferiu 0,00 pontos percentuais (uma
exceção, SKTI_R2 sob o Set C2, em −0,01 pp — dentro do ruído de
arredondamento). O Set C3 (overlap-analysis mais restritivo) produziu uma
queda pequena, mas direcionalmente consistente, na taxa de mapeamento do
piloto HISAT2 em três das quatro bibliotecas (ex.: Benzamidine_R2:
74,83%→74,81%), confirmando que a classificação é sensível a esse
parâmetro na direção esperada — mas afrouxá-lo na direção oposta (Set C2)
não produziu ganho correspondente. Nenhuma das três candidatas atendeu aos
critérios de decisão pré-declarados (§2.4.1); o Set B permanece a
configuração de produção (`resultados/blocoC_param_sweep.csv`).

Um achado incidental da etapa de alinhamento piloto: os reads que
sobrevivem à trimagem nas quatro bibliotecas afetadas mapeiam em taxas
(74,8–79,4%) comparáveis à biblioteca controle limpa (78,0%) — o dado que
sobrevive não está degradado em relação ao resto do lote; o que se perde é
volume, não qualidade do que resta. (As taxas de mapeamento absolutas
aqui, incluindo o controle limpo, ficam abaixo do limiar de aprovação de
>80% da FASE 2 declarado no projeto — esperado e não diretamente
comparável, já que este índice piloto não tem anotação de splice sites, o
que reduz a sensibilidade a reads que cruzam junções éxon-éxon; a taxa de
mapeamento real da FASE 2, com índice anotado nas 13 bibliotecas
completas, ainda precisa ser medida.)

**Interpretação:** a perda de reads nessas quatro bibliotecas reflete uma
propriedade estrutural das próprias moléculas (inserto biológico curto o
bastante para R1/R2 se sobreporem quase inteiramente com sequência de
adaptador), não uma escolha de limiar de qualidade/overlap conservadora
demais — é invariante aos parâmetros testados aqui. A causa raiz de
preparo de biblioteca (§5, item 1) segue em aberto, mas agora mais
restrita: não é um artefato de uma escolha de parâmetro de trimagem
corrigível.

### 3.9 STAR supera o HISAT2 no piloto de seleção de alinhador; alinhamento do lote completo em andamento no momento da redação

**Resultado do Bloco A (concluído).** O STAR superou o HISAT2 nas cinco
bibliotecas-piloto por 9,33–13,02 pontos percentuais, e foi o único
alinhador a ultrapassar o limiar de aprovação de >80% de mapeamento
declarado pelo projeto em qualquer amostra (Tabela 5;
`resultados/fase2_blocoA_star_vs_hisat2.csv`). Pela regra de decisão
pré-acordada (§2.5), **o STAR sozinho foi selecionado** para a rodada do
Bloco B no lote completo; o HISAT2 não foi rodado nas outras oito
bibliotecas.

**Tabela 5 | Piloto de seleção de alinhador: STAR vs. HISAT2 (índice anotado), cinco amostras.**

| Amostra | Rótulo | Mapeamento STAR (%) | Mapeamento HISAT2 (%) | Diferença (pp) | STAR ≥80%? | HISAT2 ≥80%? |
|---|---|---:|---:|---:|:---:|:---:|
| ID-1 | Control_R1 | 90,46 | 77,44 | 13,02 | sim | não |
| ID-9 | SKTI_R1 | 90,86 | 78,54 | 12,32 | sim | não |
| ID-10 | SKTI_R2 | 90,59 | 78,59 | 12,00 | sim | não |
| ID-8 | Benzamidine_R3 | 86,91 | 77,58 | 9,33 | sim | não |
| ID-7 | Benzamidine_R2 | 83,49 | 74,15 | 9,34 | sim | não |

**Resultado do Bloco B (concluído, as duas vias — 30/07/2026, 09h48).**

- **Via STAR: 13/13 bibliotecas concluídas.** Em toda amostra, a taxa
  combinada de mapeamento único mais multi-mapeado cai entre 83,1–91,8%
  (Tabela 6) — **as 13 bibliotecas ultrapassam o limiar de aprovação de
  >80% do projeto**, a menor sendo ID-2 com 83,12%.
- **Via Subread: 13/13 bibliotecas concluídas**, incluindo ID-1. A
  primeira tentativa de execução produziu uma falha de segmentação em
  ID-1 (BAM de 0 bytes) porque este script e o do STAR pediam 16 threads
  simultaneamente no servidor; ID-1 foi rerodada isoladamente depois que a
  via STAR já tinha terminado (sem disputa de threads), concluindo em 3,1
  minutos, com 26.065.883 reads mapeados unicamente, 62.066 indels
  chamados, e um BAM indexado com sucesso, sem corrupção — resolvendo a
  Limitação 9.

**Tabela 6 | Taxa de mapeamento do STAR no lote completo, 13 bibliotecas (final).**

| Amostra | Mapeamento único (%) | Multi-mapeado (%) | Combinado (%) |
|---|---:|---:|---:|
| ID-12 | 87,23 | 4,56 | 91,79 |
| ID-18 | 86,78 | 3,90 | 90,68 |
| ID-16 | 86,96 | 3,53 | 90,49 |
| ID-1 | 82,35 | 7,90 | 90,25 |
| ID-14 | 85,93 | 4,14 | 90,07 |
| ID-9 | 83,44 | 6,51 | 89,95 |
| ID-10 | 82,78 | 6,98 | 89,76 |
| ID-15 | 84,59 | 4,17 | 88,76 |
| ID-3 | 83,11 | 4,84 | 87,95 |
| ID-5 | 81,88 | 5,42 | 87,30 |
| ID-8 | 78,83 | 7,41 | 86,24 |
| ID-7 | 78,48 | 5,37 | 83,85 |
| ID-2 | 74,59 | 8,53 | 83,12 |

*Versão legível por máquina: `resultados/fase2_blocoB_star_mapping_summary.csv`.
Arquivos `Log.final.out` completos por amostra: servidor,
`~/rnaseq-Anticarsia-GORE3/qc/fase2_blocoB_star/`.*

### 3.10 Verificação entre fases, estatísticas completas de alinhamento, e comparação STAR–Subread

Duas checagens automatizadas foram rodadas antes de tratar o alinhamento
do Bloco B como verificado, em vez de confiar só no resumo de taxa de
mapeamento (código: `codigo/fase2_blocoB/analyze_blocoB2_alignment.py`).
**(i)** O "Number of input reads" (pares de leitura) de cada amostra do
STAR foi cruzado contra a contagem de reads pós-trimagem registrada
independentemente na FASE 1 Bloco B
(`resultados/blocoB_trim_summary.csv`, `reads_after`, total R1+R2):
`reads_after` é igual a `2 × pares de leitura de entrada` exatamente nas
13 bibliotecas, sem exceção. Isso confirma que o STAR rodou sobre o FASTQ
trimado correto e correspondente de cada amostra — um tipo de erro
(arquivo de entrada errado ou desatualizado) que não seria visível pela
taxa de mapeamento sozinha, já que um FASTQ trocado mas válido ainda
produziria uma taxa de mapeamento plausível. **(ii)** Os 13 arquivos de
log do Subread contêm o marcador próprio da ferramenta "Completed
successfully.", e nenhum contém qualquer string de erro ou warning
(checado diretamente, não inferido do status de saída).

**Estatísticas de junção de splicing e taxa de erro (STAR, Tabela 7; dado
completo: `resultados/fase2_blocoB_star_full_stats.csv`).** O total de
junções de splicing detectadas por amostra varia de 10.691.972
(Benzamidine_R2, a biblioteca de menor profundidade) a 29.884.406
(SKTI_R3); a fração anotada contra o GTF da RS_2026_04 é consistentemente
alta e estreita nas 13 bibliotecas (98,9–99,6%), e a taxa de mismatch por
base é uniforme (1,26–1,53%) — nenhuma das duas mostra o tipo de outlier
específico de amostra que indicaria um problema de contaminação ou
incompatibilidade com a referência em alguma biblioteca individual.

**Tabela 7 | Estatísticas de junção de splicing e mismatch do STAR, 13 bibliotecas.**

| Amostra | Splices (total) | Splices anotadas (%) | Taxa de mismatch (%) | Não mapeado: curto demais (%) | Não mapeado: outro (%) |
|---|---:|---:|---:|---:|---:|
| ID-1 | 22.890.218 | 99,21 | 1,50 | 7,37 | 2,10 |
| ID-2 | 16.735.271 | 99,03 | 1,53 | 9,81 | 6,80 |
| ID-3 | 18.124.299 | 99,34 | 1,45 | 10,49 | 1,34 |
| ID-5 | 18.754.015 | 99,43 | 1,42 | 8,03 | 4,49 |
| ID-7 | 10.691.972 | 99,21 | 1,30 | 12,41 | 3,49 |
| ID-8 | 15.570.825 | 99,31 | 1,38 | 8,97 | 4,65 |
| ID-9 | 21.160.774 | 99,59 | 1,35 | 7,72 | 1,84 |
| ID-10 | 17.968.284 | 99,55 | 1,38 | 7,49 | 2,14 |
| ID-12 | 29.884.406 | 99,63 | 1,38 | 6,71 | 1,05 |
| ID-14 | 22.737.302 | 99,62 | 1,32 | 8,57 | 1,03 |
| ID-15 | 24.450.805 | 99,64 | 1,41 | 9,68 | 1,25 |
| ID-16 | 25.408.075 | 99,71 | 1,40 | 8,38 | 0,94 |
| ID-18 | 22.615.969 | 99,64 | 1,26 | 6,52 | 2,66 |

Reads não mapeados são dominados pela categoria "curto demais" (6,5–12,4%)
em vez de "outro" (0,9–6,8%) em toda biblioteca exceto ID-2 (9,81%
curto-demais vs. 6,80% outro, suas duas maiores categorias de não-mapeado
sendo comparáveis em tamanho, diferente do resto do lote) — "curto demais"
é a categoria do STAR esperada a partir de moléculas residuais de
inserto-curto/adapter-dimer já caracterizadas na FASE 1 (§3.6), então essa
distribuição é consistente com, não adicional a, o problema de preparo de
biblioteca já documentado; não é um achado novo.

**STAR vs. Subread — uma diferença real e esperada, não suavizada
(Fig. 5).** A taxa de mapeamento geral do Subread (só matches únicos;
multi-mapping explicitamente desabilitado em `run_subread_align_full.sh`,
batendo com a própria justificativa documentada da configuração de
produção) é menor que a taxa combinada do STAR em todas as 13
bibliotecas, e cai **abaixo do limiar de 80% do projeto em quatro
amostras**: Control_R2 (75,6%), Benzamidine_R2 (78,3%), Benzamidine_R3
(79,1%) e Benzamidine_R1 (79,7%) (dado completo:
`resultados/fase2_blocoB_subread_stats.csv`). Isso não é tratado como
falha de alinhamento do Subread: o limiar de aprovação de 80% foi
declarado para a via de quantificação de expressão gênica (§2 — o papel
que o STAR ocupa aqui), e a taxa menor do Subread é consequência direta e
mecanística de a ferramenta rodar sem reportar multi-mapping,
configuração escolhida deliberadamente porque o papel do Subread neste
projeto é acurácia de junção éxon-éxon (§2.5), não maximizar a contagem de
reads atribuídos a algum lugar do genoma. Declarado aqui em vez de
omitido, porque a diferença numérica é real e medida de forma
reprodutível, mesmo que sua explicação não indique um problema com os
dados de sequenciamento em si.

**Figura 5 | Taxa de mapeamento do lote completo, STAR vs. Subread, 13
bibliotecas.** Gráfico de barras agrupadas, STAR (azul; % único +
multi-mapeado) versus Subread (vermelho; % único, reporte de multi-mapping
desabilitado por desenho), por biblioteca, ordenado por grupo de
tratamento e réplica biológica. Linha tracejada: o limiar de aprovação de
80% de taxa de mapeamento declarado pelo projeto. As 13 barras do STAR
ultrapassam o limiar; quatro barras do Subread (Control_R2 e as três
réplicas de Benzamidine) ficam abaixo dele, pelo motivo declarado acima.
Arquivo: `figuras/Figure5_fase2_blocoB_mapping_rates.png`; código:
`codigo/fase2_blocoB/analyze_blocoB2_alignment.py`.

### 3.11 Quantificação em nível de gene e transcrito: as duas vias concluídas, verificadas mutuamente

**Contagens em nível de gene (via de produção).** O featureCounts atribuiu
70,2–84,4% dos reads a genes nas 13 bibliotecas (Tabela 8;
`resultados/fase3_blocoC_featurecounts_summary.csv`), sem outlier
específico de amostra — a faixa é consistente com as categorias residuais
de não-atribuídos já caracterizadas na FASE 2 §3.10 (reads derivados de
inserto curto/adapter-dimer que mapeiam mas não caem limpo dentro de um
éxon). Este é o entregável que alimenta os contrastes de grupo na FASE 5.

**Tabela 8 | Taxa de atribuição a genes pelo featureCounts, 13 bibliotecas.**

| Amostra | Atribuído (%) |
|---|---:|
| GORE3_R3 | 84,40 |
| FatBody | 83,58 |
| GORE3_R1 | 82,88 |
| GORE3_R2 | 82,66 |
| SKTI_R3 | 81,48 |
| Benzamidine_R1 | 81,12 |
| Control_R3 | 80,40 |
| SKTI_R1 | 75,52 |
| Control_R1 | 75,03 |
| Benzamidine_R2 | 74,11 |
| SKTI_R2 | 74,01 |
| Benzamidine_R3 | 73,62 |
| Control_R2 | 70,15 |

**Figura 6 | Taxa de atribuição a genes pelo featureCounts, 13 bibliotecas.**
Porcentagem de pares de reads atribuídos a um gene pelo featureCounts
(parâmetros de produção, §2.6), por amostra, ordenado por grupo de
tratamento e réplica. Arquivo:
`figuras/Figure6_fase3_blocoC_featurecounts_assigned.png`; código:
`codigo/fase3_blocoC/analyze_featurecounts.py`.

**Quantificação em nível de transcrito (via de apoio a H1).** O índice
decoy-aware do Salmon quantificou as 13 bibliotecas com taxas de
mapeamento de 80,3–91,2%, dentro de ±5,7 pontos percentuais da taxa
combinada do STAR em toda amostra (Tabela 9;
`resultados/fase3_blocoD_salmon_mapping_summary.csv`) — confortavelmente
dentro da banda de consistência de ±10pp declarada antecipadamente
(§2.6), dado que os dois métodos são estruturalmente diferentes
(alinhamento genômico vs. alinhamento seletivo decoy-aware contra
transcriptoma).

**Tabela 9 | Taxa de mapeamento Salmon vs. STAR, 13 bibliotecas.**

| Amostra | Salmon (%) | STAR (%) | Diferença (pp) |
|---|---:|---:|---:|
| Control_R1 | 91,09 | 90,25 | +0,84 |
| Control_R2 | 88,83 | 83,12 | +5,71 |
| Control_R3 | 85,19 | 87,95 | −2,76 |
| Benzamidine_R1 | 91,18 | 87,30 | +3,88 |
| Benzamidine_R2 | 80,27 | 83,85 | −3,58 |
| Benzamidine_R3 | 88,26 | 86,24 | +2,02 |
| SKTI_R1 | 86,99 | 89,95 | −2,96 |
| SKTI_R2 | 87,31 | 89,76 | −2,45 |
| SKTI_R3 | 87,75 | 91,79 | −4,04 |
| GORE3_R1 | 86,80 | 90,07 | −3,27 |
| GORE3_R2 | 85,55 | 88,76 | −3,21 |
| GORE3_R3 | 86,73 | 90,49 | −3,76 |
| FatBody | 88,78 | 90,68 | −1,90 |

**Figura 7 | Taxa de mapeamento Salmon vs. STAR, 13 bibliotecas.** Gráfico
de barras agrupadas, STAR (azul) vs. Salmon decoy-aware (verde), por
biblioteca. Arquivo:
`figuras/Figure7_fase3_blocoD_salmon_vs_star_mapping.png`; código:
`codigo/fase3_blocoD/analyze_salmon_mapping.py`.

**Nota sobre o tximport (menor, divulgada):** o índice do Salmon foi
construído sem `--keepDuplicates`, então 811 dos 25.840 transcritos
extraídos via gffread com sequência idêntica byte-a-byte a outro
transcrito foram colapsados num único representante durante a indexação
(comportamento padrão do Salmon, não um erro específico deste projeto).
Isso deixa 14.973 dos 15.773 genes anotados com pelo menos um transcrito
diretamente quantificável na tabela de genes do tximport
(`resultados/fase3_blocoE_salmon_gene_counts.tsv`) — os ~800 genes
restantes tinham seu(s) único(s) transcrito(s) idêntico(s) em sequência a
um transcrito de outro gene, absorvido na contagem desse outro
transcrito. Isso afeta só a via secundária de apoio de transcrito/
isoforma (§2.6), não o entregável prioritário da FASE 3 (Tabela 8,
contagens de gene do featureCounts, que conta sobreposição de éxon
genômico diretamente e não é afetado por duplicação de sequência de
transcrito).

**Uma armadilha de parsing do R, não relacionada, encontrada e corrigida
antes desta tabela ser gerada:** a primeira rodada do `tximport` reportou
"3.263 transcripts missing from tx2gene" — rastreado até o tratamento
padrão de aspas do `read.table()` do R interpretar um apóstrofo literal no
nome de um gene RefSeq (`beta'COP`, subunidade do complexo coatômero,
ID de gene `gene-beta'COP`) como abertura de aspas nunca fechada,
truncando silenciosamente as 25.840 linhas do `tx2gene.tsv` para 22.305
linhas sem erro (só um aviso "EOF within quoted string" fácil de não
notar). Adicionar `quote = ""` à chamada `read.table()`
(`codigo/fase3_blocoE/00_tximport_gore3.R`) resolveu completamente (0
transcritos ausentes, confirmado diretamente antes e depois da correção).

**Verificação entre quantificadores (Bloco F).** Três checagens, todas
passando (`resultados/fase3_blocoF_crosscheck.csv`;
`codigo/fase3_blocoF/analyze_fase3_consistency.py`): **(i)** a contagem
`Assigned` do featureCounts nunca supera a contagem estimada de reads
unicamente mapeados do STAR em nenhuma amostra, consistente com o
featureCounts (sem `-M`) só contando reads de alinhamento único. **(ii)**
As taxas de mapeamento do Salmon e do STAR concordam dentro da banda
pré-declarada de ±10pp nas 13 amostras (Tabela 9). **(iii)** As contagens
em nível de gene das duas vias de quantificação independentes
(featureCounts, Tabela 8; Salmon+tximport, acima) são forte e
uniformemente concordantes — Spearman ρ = 0,983–0,988 nas 13 amostras
(Tabela 10, Fig. 8), apesar dos dois métodos usarem lógica
estruturalmente diferente de atribuição de reads (contagem de
sobreposição de éxon vs. EM probabilístico em nível de transcrito com
correção de viés de GC, agregado a nível de gene).

**Tabela 10 | Concordância em nível de gene entre featureCounts e Salmon+tximport, 13 bibliotecas.**

| Amostra | Spearman ρ |
|---|---:|
| ID-1 | 0,987 |
| ID-2 | 0,985 |
| ID-3 | 0,986 |
| ID-5 | 0,988 |
| ID-7 | 0,983 |
| ID-8 | 0,985 |
| ID-9 | 0,986 |
| ID-10 | 0,984 |
| ID-12 | 0,986 |
| ID-14 | 0,985 |
| ID-15 | 0,986 |
| ID-16 | 0,985 |
| ID-18 | 0,988 |

**Figura 8 | Concordância em nível de gene: featureCounts vs. Salmon+tximport.**
Correlação de Spearman por amostra entre as duas matrizes independentes
de contagem de genes. Arquivo:
`figuras/Figure8_fase3_blocoF_featurecounts_vs_salmon_concordance.png`.

---

## 4. Discussão

*[Parcial — restrita ao que o Bloco A permite discutir; retomada quando a
FASE 2 (mapeamento) e a FASE 5 (expressão diferencial) estiverem
disponíveis.]*

A observação original (§3.2–3.3) foi que o grupo de tratamento Benzamidina
é o mais exposto a um defeito de qualidade de reads brutos (duas de três
réplicas biológicas afetadas, incluindo a pior biblioteca de todo o
conjunto de dados tanto em Q20 quanto em Q30), enquanto Controle e GORE3
pareciam livres do defeito e SKTI tinha uma de três réplicas afetada. O
§3.6 refina esse quadro em nível de grupo: uma vez usada a contaminação
por adapter-dimer como métrica operativa em vez do limiar de qualidade
média original, **o SKTI está igualmente afetado (2 de 3 réplicas:
SKTI_R1 e SKTI_R2)**, não o quadro de 1-em-3 que o critério binário do
§3.2 sugeria.

O §3.4 elevou isso de "não resolvido" para "caracterizado, correlacionado
com GC, ainda não totalmente explicado mecanisticamente", identificando
SKTI_R1 (ID-9) como uma quarta biblioteca de risco gradual, junto com
Benzamidine_R2, Benzamidine_R3 e SKTI_R2. O §3.6 aprofunda isso ainda
mais: o risco não é primariamente de *qualidade de base-calling* (que a
trimagem corrige por completo, Tabela 2), mas de **rendimento** —
Benzamidina e SKTI perdem cada uma 2 de 3 réplicas para profundidade de
reads substancialmente reduzida (62–68% e 67–82% de sobrevivência,
respectivamente), impulsionada por contaminação de adapter-dimer
correlacionada com GC, enquanto Controle e GORE3 mantêm profundidade
próxima de completa (91–97%) em todas as réplicas. Para os contrastes da
FASE 5, isso reformula a ressalva de "risco de qualidade" para "assimetria
de poder estatístico": os contrastes Benzamidina-vs-Controle e
SKTI-vs-Controle vão rodar sobre bibliotecas com profundidade de reads
utilizável sistematicamente menor no braço de tratamento, o que deve ser
reportado junto com qualquer resultado de expressão diferencial desses
contrastes específicos, não diluído silenciosamente na limitação geral de
poder com n=3 já declarada em `docs/04_viabilidade.md` §1.1.

O §3.7 aprofunda isso mais uma vez, de uma afirmação em nível de grupo
para uma em nível de contraste: as duas comparações mais consequentes de
toda a matriz de contrastes — #2 (GORE3 vs. Benzamidina, o teste direto
contra o padrão farmacológico) e #3 (GORE3 vs. SKTI, hipótese H4) — são
exatamente as duas que carregam a maior assimetria de profundidade, por
razões diferentes ligadas ao papel de cada grupo no argumento do estudo
(Tabela 4).

**Próximos passos planejados para de fato resolver isso, não só
sinalizar (FASE 2 em diante):**
1. Reverificar a assimetria de profundidade por contraste depois do
   alinhamento, usando taxa de mapeamento e o número de genes que passam
   no limiar de filtragem independente do DESeq2 por amostra, não a
   contagem de reads sozinha — contagem de reads é um proxy, a contagem
   mapeada/utilizável é a quantidade real que importa.
2. Quando o DESeq2 rodar (FASE 5), inspecionar as estimativas de
   dispersão por gene separadamente para os contrastes #2/#3/#5/#6 versus
   #1/#4, para checar se a assimetria de profundidade de fato degrada o
   poder de detecção para genes de expressão moderada-a-baixa nos braços
   afetados, em vez de assumir que degrada só a partir da contagem de
   reads.
3. Decidir, informado por (1)–(2) e não antes, se alguma etapa de
   compensação de profundidade (ex.: ponderação, ou sinalização de genes
   com poder específico-de-contraste baixo) se justifica especificamente
   para os contrastes #2 e #3.

---

## 5. Limitações (declaradas explicitamente, não suavizadas)

1. **A causa do defeito de qualidade agora é mais bem explicada por
   contaminação de adapter-dimer (§3.6), correlacionada com GC, mas a
   causa raiz em nível de preparo de biblioteca ainda não está
   estabelecida.** Não sabemos *por que* essas quatro bibliotecas
   produziram mais moléculas de inserto curto — isso exigiria dados de QC
   de tamanho de inserto/molaridade da etapa de preparo de biblioteca, que
   a entrega de dados brutos da Macrogen não inclui (ver item 3 abaixo). O
   §3.8 restringe isso ainda mais: a perda de reads não é um artefato dos
   limiares de trimagem/detecção de overlap escolhidos (um sweep empírico
   de parâmetros encontrou zero reads recuperáveis sob três configurações
   alternativas) — a causa raiz é anterior à trimagem, nas próprias
   moléculas da biblioteca.
2. ~~**Os parâmetros de trimagem do fastp estão indefinidos.**~~ —
   **Resolvido (§3.5, §2.4).** Um teste A/B empírico em duas bibliotecas
   representativas mostrou que o parâmetro testado
   (`--length_required 36` vs. `50`) faz diferença desprezível na
   sobrevivência; o Set B (50, mais trimagem de poli-G/poli-X e análise de
   sobre-representação) foi adotado para o lote completo por ser
   estritamente não pior e adicionar segurança relevante para a química
   NovaSeq X confirmada, a custo zero medido.
3. **O tamanho de inserto/fragmento da biblioteca não está confirmado.**
   Isso é necessário para análises em nível de isoforma (FASE 6) e não é
   reportado pelo QC de dados brutos da Macrogen; precisa ser solicitado
   ao fornecedor ou estimado pós-alinhamento
   (`picard CollectInsertSizeMetrics`).
4. **A direção da orientação de fita da biblioteca (forward vs. reverse)
   está inferida, não confirmada.** O nome do kit declarado pelo
   fornecedor indica um protocolo stranded, mas a orientação do read ainda
   precisa ser confirmada empiricamente pós-alinhamento
   (`salmon --libType A` ou `RSeQC infer_experiment.py`).
5. **Cinco dos 17 tubos submetidos à Macrogen não foram entregues nesta
   remessa** (Control ID-4; Benzamidine ID-6; SKTI ID-11, ID-13; GORE3
   ID-17). Cada grupo de tratamento ainda fecha em n=3 nesta entrega, então
   isso não bloqueia a análise, mas o motivo da lacuna (réplicas de
   contingência nunca sequenciadas, ou uma entrega futura pendente) não
   está confirmado.
6. **Um desvio de linha de comando do FastQC ocorreu e é divulgado para o
   registro:** a flag `-d qc/tmp` falhou ("Option d is ambiguous") durante
   a execução e a ferramenta caiu no comportamento padrão de arquivo
   temporário. As 26 saídas foram, mesmo assim, produzidas com sucesso, e
   nenhum arquivo perdido ou corrompido foi encontrado na inspeção
   (`codigo/fase1_blocoA/run_fastqc_multiqc.sh` traz essa nota inline).
7. **O poder estatístico agora está assimétrico entre grupos de
   tratamento E entre contrastes planejados, não só ao longo do conjunto
   de dados como um todo (§3.7, Tabelas 3–4).** Benzamidina e SKTI retêm
   cada uma apenas 2 de 3 réplicas com profundidade próxima de completa
   após a trimagem; Controle e GORE3 não têm esse problema. Quatro dos
   seis contrastes planejados da FASE 5 tocam um grupo de profundidade
   reduzida, e os dois de maior impacto (#2 GORE3 vs. Benzamidina; #3
   GORE3 vs. SKTI/H4) são exatamente os dois que carregam a maior
   assimetria. Isso agrava, em vez de duplicar, a limitação geral de
   poder com n=3 já declarada em `docs/04_viabilidade.md` §1.1. **Ainda
   não resolvido — plano de resolução declarado no §4** (reverificar com
   taxa de mapeamento e dispersão do DESeq2 quando as FASES 2 e 5
   rodarem, não inferido só pela contagem de reads).
8. **O corte de cor de >10% de adapter-dimer na Fig. 3 é uma escolha
   visual post-hoc**, feita depois de inspecionar a distribuição bimodal
   no painel (b), não um limiar declarado antes de ver o dado (diferente
   do limiar de ΔQ > 5,0 Phred na Fig. 1). É divulgado como tal e não deve
   ser lido como tendo o mesmo peso probatório.
9. ~~**A FASE 2 Bloco B está incompleta no momento da redação.**~~ —
   **Resolvido (§3.9).** As 13 amostras do STAR e as 13 do Subread
   (incluindo a rerrodada do ID-1) concluíram com sucesso. O problema de
   concorrência que causou as falhas de segmentação originais (dois jobs
   de alinhamento de 16 threads lançados ao mesmo tempo no mesmo servidor)
   era operacional, não uma propriedade dos dados de sequenciamento, e não
   se repetiu quando a rerrodada do ID-1 foi lançada depois que a via STAR
   já tinha terminado. As taxas de mapeamento do STAR por amostra
   (Tabela 6) estão exportadas em
   `resultados/fase2_blocoB_star_mapping_summary.csv`.
10. **O featureCounts padrão (sem `-M -O --fraction`) vai descartar/
    subcontar reads ambíguos especificamente na família multigênica de
    serino-proteases tipo tripsina (FASE 3, §2.6).** Zytnicki (2017, PMID
    28915787) reporta que habilitar o resgate de multi-mapping/
    multi-sobreposição "quase sempre produz resultados enviesados", então
    não é usado — mas a família que a hipótese secundária H1 deste
    projeto trata é exatamente a mais exposta a esse conservadorismo
    padrão (parálogos próximos, atribuição ambígua de reads). **Não
    resolvido aqui** — adiado para a FASE 9 (curadoria manual da família
    de serino-proteases) para esse conjunto específico de genes. Nenhum
    benchmark em inseto ou família multigênica foi encontrado numa busca
    dirigida de literatura; Kwon (2015, PMID 26112470, *Xenopus*, só
    abstract) é a evidência mais próxima disponível, não uma solução.
11. **A indexação decoy-aware do Salmon (FASE 3, §2.6) é validada só em
    humano e camundongo.** Srivastava et al. (2020, PMID 32894187)
    testaram 109 datasets reais humanos + simulações de camundongo —
    nenhum genoma de inseto ou não-modelo. O benefício esperado (redução
    de atribuição espúria de reads) é uma extrapolação razoável para
    *A. gemmatalis*, não um fato estabelecido para esta espécie — mesma
    estrutura de ressalva da transferência planta→inseto de Coxe et al.
    (2024) já declarada acima.

---

## Referências

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

---

## Reprodutibilidade — localização de código e dados

| Item | Caminho |
|---|---|
| Mapeamento de amostras / tabela replace-names | `codigo/fase1_blocoA/samplesheet.tsv`, `samplesheet_replace_names.tsv` |
| Download de FASTQ + verificação MD5 | `codigo/fase1_blocoA/download_and_verify.sh`, `md5sum.txt` |
| Execução FastQC + MultiQC | `codigo/fase1_blocoA/run_fastqc_multiqc.sh` |
| Análise de QC + geração de figura (Fig. 1) | `codigo/fase1_blocoA/analyze_blocoA.py` |
| Análise por tile resolvida por posição + geração de figura (Fig. 2) | `codigo/fase1_blocoA/per_tile_analysis.py` |
| Teste A/B de parâmetros do fastp | `codigo/fase1_blocoB/run_fastp_ab_test.sh`, `compare_ab_test.py` |
| Trimagem completa em lote (13 amostras, Set B) | `codigo/fase1_blocoB/run_fastp_full_trim.sh` |
| Resumo pós-trimagem + geração da Fig. 3 | `codigo/fase1_blocoB/analyze_blocoB.py` |
| Curvas antes/depois + geração da Fig. 4 | `codigo/fase1_blocoB/plot_before_after_trim.py`, `extract_fig4_data.py` |
| Resultados (CSV, legível por máquina) | `resultados/blocoA_results.csv`, `resultados/blocoA1_pertile_results.csv`, `resultados/blocoB_ab_test_comparison.csv`, `resultados/blocoB_trim_summary.csv`, `resultados/figure4_quality_curves.csv` |
| Versões exatas de ferramenta/ambiente | `resultados/blocoA_ENV_VERSIONS.txt` |
| Figura 1 (PNG 300 dpi) | `figuras/Figure1_blocoA_quality_dip.png` |
| Figura 2 (PNG 300 dpi) | `figuras/Figure2_blocoA1_pertile_heatmap.png` |
| Figura 3 (PNG 300 dpi) | `figuras/Figure3_blocoB_trimming.png` |
| Figura 4 (PNG 300 dpi) | `figuras/Figure4_blocoB_before_after.png` |
| FASTQ trimados (26 arquivos) | servidor: `~/rnaseq-Anticarsia-GORE3/trimmed/` (não versionado — dado grande, não vai ao git) |
| Relatórios HTML completos FastQC/MultiQC/fastp | servidor: `~/rnaseq-Anticarsia-GORE3/qc/{pre_trim,post_trim,ab_test}/` (não versionado) |
| Scripts do piloto de seleção de alinhador (STAR vs. HISAT2) | `codigo/fase2_blocoA/` (`run_star_hisat2_subsample.sh`, `build_star_index.sh`, `build_hisat2_index_annotated.sh`, `convert_gff_to_gtf.sh`, `analyze_fase2_blocoA.py`) |
| Resultados do piloto de seleção de alinhador (Tabela 5) | `resultados/fase2_blocoA_star_vs_hisat2.csv` |
| Resumo de mapeamento do STAR no lote completo (Tabela 6) | `resultados/fase2_blocoB_star_mapping_summary.csv` |
| Verificação entre fases, estatísticas completas STAR/Subread, geração da Fig. 5 (Tabela 7) | `codigo/fase2_blocoB/analyze_blocoB2_alignment.py` → `resultados/fase2_blocoB_star_full_stats.csv`, `resultados/fase2_blocoB_subread_stats.csv` |
| Figura 5 (PNG 300 dpi) | `figuras/Figure5_fase2_blocoB_mapping_rates.png` |
| Scripts de alinhamento do lote completo (STAR + Subread) | `codigo/fase2_blocoB/` (`run_alignment_full.sh`, `run_subread_align_full.sh`, `check_strandedness.sh`, `analyze_strandedness.py`) |
| BAMs e logs do STAR/Subread (13 bibliotecas, concluído) | servidor: `~/rnaseq-Anticarsia-GORE3/{bam/star,bam/subread,qc/fase2_blocoB_star,qc/fase2_blocoB_subread}/` (não versionado — dado grande) |
| Correção do GTF (gene_id ausente) + decisão de strand (FASE 3 Bloco A) | `codigo/fase3_blocoA/fix_gtf_missing_geneid.sh`, `decide_libtype.py` → `resultados/fase3_blocoA_strand_decision.csv` |
| Auditoria de ferramentas (FASE 3 Bloco B) | `codigo/fase3_blocoB/check_tools.sh` → `resultados/fase3_blocoB_env_check.txt` |
| Contagem de genes de produção (FASE 3 Bloco C) | `codigo/fase3_blocoC/run_featurecounts_genelevel.sh`, `analyze_featurecounts.py` → `resultados/fase3_blocoC_featurecounts_summary.csv`, `resultados/fase3_blocoC_gene_counts.txt` |
| Figura 6 (PNG 300 dpi) | `figuras/Figure6_fase3_blocoC_featurecounts_assigned.png` |
| Índice Salmon decoy-aware + quant (FASE 3 Bloco D) | `codigo/fase3_blocoD/build_salmon_decoy_index.sh`, `run_salmon_quant_full.sh`, `analyze_salmon_mapping.py` |
| Adaptação do tximport (FASE 3 Bloco E) | `codigo/fase3_blocoE/build_tx2gene.py`, `build_samplesheet.py`, `00_tximport_gore3.R` |
| Verificação cruzada entre quantificadores (FASE 3 Bloco F) | `codigo/fase3_blocoF/analyze_fase3_consistency.py` → `resultados/fase3_blocoF_crosscheck.csv` |
| Índice/quant do Salmon, saídas do tximport (grande) | servidor: `~/rnaseq-Anticarsia-GORE3/{salmon_index_decoy,salmon}/` (não versionado — dado grande) |
