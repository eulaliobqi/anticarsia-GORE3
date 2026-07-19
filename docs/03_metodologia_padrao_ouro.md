# Metodologia — atualização para o padrão atual

Revisão crítica da metodologia proposta em `Projeto-Eulalio-Pós-doc2.docx` (§2), com o que é padrão em 2026 e a justificativa de cada mudança.

> **Sobre versões:** este documento **não fixa números de versão**. Versões devem ser conferidas no momento da instalação (anaconda.org / repositório oficial) e registradas no ambiente. Pinos de versão citados de memória já causaram falha real de pipeline em outro projeto.

---

## Quadro-resumo

| # | Projeto propõe | Padrão atual recomendado | Severidade |
|---|---|---|---|
| 1 | Montagem *de novo* (Trinity) | **Pipeline genoma-guiado** contra `GCF_050436995.1` | 🔴 Crítica |
| 2 | Kallisto | **Salmon** + `tximport` | 🟡 Média |
| 3 | TRAPID / Blast2GO / KOBAS 2.0 | **eggNOG-mapper v2** + **clusterProfiler** | 🟡 Média |
| 4 | Phyre2 | **AlphaFold** (ou ColabFold) | 🔴 Crítica |
| 5 | AutoDock Vina / PyRx para peptídeo | **HADDOCK** e/ou co-folding; Vina só como triagem | 🔴 Crítica |
| 6 | GORE3 parametrizado por **CGenFF** | **Campo de força de proteína** | 🔴 Erro conceitual |
| 7 | CHARMM36m | Decisão consciente vs. AMBER99SB-ILDN (legado local) | 🟠 Decisão |
| 8 | 3 réplicas técnicas + 3 biológicas | **≥ 4 réplicas biológicas**, zero técnicas | 🟡 Média |
| 9 | (ausente) | **BUSCO**, análise de splicing, controle de lote | 🟡 Lacuna |
| 10 | MM-PBSA sem ressalva | MM/GBSA **com limitações declaradas** | 🟡 Média |

---

## 1. 🔴 Montagem *de novo* → pipeline genoma-guiado

**A mudança mais importante deste documento.**

O projeto propõe Trinity → CD-HIT → TransDecoder, o fluxo correto para organismo **sem** genoma de referência. Era a situação de *A. gemmatalis* quando o projeto foi redigido (Set/2025).

**Isso mudou.** A espécie tem agora genoma RefSeq:

| Item | Valor |
|---|---|
| Assembly RefSeq | **`GCF_050436995.1`** |
| Nome | **ilAntGemm2** (primary haplotype) |
| BioProject (genoma) | PRJNA1225766 |
| Anotação | NCBI Eukaryotic Genome Annotation Pipeline, release **RS_2025_08** |

*(Verificar métricas de contiguidade — N50, BUSCO, nível de montagem — na página do assembly antes de finalizar a metodologia escrita. Não reproduzir números não conferidos.)*

### Por que isso importa especificamente para este projeto

Não é uma troca cosmética. A pergunta central do trabalho é sobre **isoformas de tripsina** — quais são induzidas, quais escapam do inibidor. Montagem *de novo* é estruturalmente ruim para isso:

- Trinity **fragmenta e funde** transcritos de famílias gênicas com alta similaridade de sequência. Tripsinas de lepidópteros são exatamente esse caso: muitas cópias parálogas quase idênticas.
- Sem coordenadas genômicas, não há como distinguir **isoforma de splicing** de **parálogo** de **artefato de montagem**.
- A quantificação sobre um transcriptoma *de novo* redundante distribui reads de forma ambígua entre contigs quase idênticos, inflando a incerteza justamente nos genes de interesse.
- **Análise de splicing alternativo** — objetivo declarado do projeto — é inviável sem anotação genômica. Ferramentas como rMATS e DEXSeq (citadas no próprio `GORE3-abstract.docx`) **exigem** genoma anotado.

### Fluxo recomendado

```
FASTQ
  → QC (FastQC + MultiQC)
  → trimagem (fastp)
  → alinhamento splice-aware (STAR ou HISAT2) vs. GCF_050436995.1
  → quantificação (featureCounts sobre a anotação, ou Salmon em modo seletivo)
  → DESeq2
  → splicing alternativo (rMATS ou DEXSeq)
  → anotação/enriquecimento (eggNOG-mapper + clusterProfiler)
```

### Manter Trinity como via secundária

Recomendo **não descartar** a montagem *de novo*, e sim rodá-la em paralelo, por três razões concretas:

1. Capturar transcritos ausentes da anotação (a anotação é automática, não curada)
2. Capturar transcritos de **origem bacteriana** — a microbiota contribui com atividade proteolítica relevante em *A. gemmatalis* (Pilon et al., 2017), e essas sequências não estarão no genoma do hospedeiro
3. Comparabilidade com dos Santos et al. (2025), que usou *de novo*

O grupo já tem montagem Trinity de *A. gemmatalis* pronta localmente — ver [`04_viabilidade.md`](04_viabilidade.md).

---

## 2. 🟡 Kallisto → Salmon (+ tximport obrigatório)

O projeto especifica Kallisto 0.44 (de 2017). Salmon é a escolha mais comum hoje, com correções de viés (GC, posicional, sequência) que Kallisto não aplica por padrão.

**Erro de omissão mais sério que a escolha da ferramenta:** o projeto vai direto de pseudoalinhamento para DESeq2. Falta o **`tximport`**, que agrega estimativas de nível de transcrito para nível de gene e — criticamente — passa os *offsets* de comprimento efetivo ao DESeq2. Pular essa etapa e alimentar o DESeq2 com contagens de TPM arredondadas é um erro estatístico real, não formalidade.

O pipeline local `RNA-Seq-not-model` já implementa Salmon + `tximport` (`scripts/00_tximport.R`).

---

## 3. 🟡 TRAPID / Blast2GO / KOBAS 2.0 → eggNOG-mapper v2 + clusterProfiler

- **KOBAS 2.0** — a versão citada está descontinuada; o sucessor é o KOBAS-i. Mas, para um projeto que já usará R, **clusterProfiler** é a escolha mais prática (enriquecimento GO e KEGG, correção de múltiplos testes embutida, visualização).
- **Blast2GO** — a versão gratuita é limitada; o fluxo moderno equivalente é eggNOG-mapper ou InterProScan.
- **eggNOG-mapper v2** — padrão atual para anotação funcional de não-modelos, com ortologia, GO, KEGG KO e domínios PFAM numa passada.

**Ponto de atenção sobre KEGG:** o projeto propõe usar *Helicoverpa armigera* e *Bombyx mori* como referência para enriquecimento. Com genoma próprio disponível, o correto é construir o mapeamento **gene→GO/KO da própria *A. gemmatalis*** via eggNOG-mapper e usar `clusterProfiler::enricher` com esse universo customizado. Usar outra espécie como proxy introduz viés de anotação e não é mais necessário.

O pipeline local já tem `02_gene2go_build.R` e `03_enrichment.R` para exatamente isso.

---

## 4. 🔴 Phyre2 → AlphaFold

O projeto tem uma **contradição interna**: o objetivo (§ resumo e §27) menciona "AlphaFold e/ou modelagem por homologia", mas a metodologia (§2.9) especifica apenas **Phyre2**.

Phyre2 é modelagem por homologia baseada em perfis-HMM, tecnologia anterior à ruptura do AlphaFold2 (Jumper et al., 2021 — PMID 34265844). Para uma tripsina, que tem abundância de templates de alta identidade, Phyre2 até produz modelo utilizável — mas não há razão para preferi-lo.

**Recomendado:**
- **AlphaFold2 / ColabFold** para as estruturas das isoformas de tripsina
- **AlphaFold3** (Abramson et al., 2024 — PMID 38718835) quando o objetivo for predizer diretamente o **complexo** proteína–peptídeo, o que se conecta ao item 5
- Manter a validação estereoquímica proposta (ProSA-web, Ramachandran) — continua correta e necessária
- Registrar as métricas de confiança do próprio AlphaFold (**pLDDT**, **PAE**), que o projeto não menciona e que são hoje esperadas em revisão por pares

O usuário já tem infraestrutura de AlphaFold3 no projeto `trypsin-agemmatalis-structural`.

---

## 5. 🔴 Docking de peptídeo: Vina/PyRx não é adequado sozinho

AutoDock Vina foi desenhado para **pequenas moléculas** com poucos graus de liberdade rotacionais. Um pentapeptídeo tem backbone flexível e muitos rotâmeros de cadeia lateral — regime em que a função de score e a busca do Vina degradam de forma conhecida.

Além disso, a caixa de busca descrita no projeto é posicionada manualmente sobre "a parte da enzima conhecida por ser importante para sua função". Isso **presume a resposta** (ligação no sítio catalítico) em vez de testá-la — o que é especialmente problemático dado que o próprio grupo investiga um sítio alternativo (S'2) em outra linha de trabalho.

**Recomendado — protocolo em camadas:**

1. **Triagem** — Vina/PyRx pode ficar, mas declarado como triagem inicial, não como evidência final
2. **Docking dedicado a peptídeos** — **HADDOCK** (docking informado por dados, lida bem com flexibilidade) e/ou **AlphaFold3** em modo de co-folding
3. **Controle positivo obrigatório** — redocking de um complexo tripsina–inibidor de estrutura conhecida (ex.: benzamidina em tripsina) para validar o protocolo. O grupo já fez isso com 1BTY localmente
4. **Comparação S1 × S'2** — testar os dois sítios em vez de assumir S1
5. **Convergência de MD** — o docking gera hipótese; a MD testa

O grupo já tem resultados HADDOCK do GORE3 em quatro isoformas de tripsina (ver [`04_viabilidade.md`](04_viabilidade.md)) — o protocolo mais forte já está em uso na prática, apenas não foi escrito no projeto.

---

## 6. 🔴 CGenFF para o GORE3 — erro conceitual

O projeto (§2.10) diz:

> "O peptídeo GORE3 será parametrizado usando o CGenFF (CHARMM General Force Field), garantindo compatibilidade com o campo de força aplicado à tripsina."

**Isso está incorreto.** O CGenFF existe para **pequenas moléculas orgânicas do tipo fármaco** que não têm parâmetros nos campos de força biomoleculares. Um peptídeo composto de aminoácidos canônicos **já é coberto** pelo campo de força de proteína (CHARMM36m ou AMBER) — que foi parametrizado precisamente para isso.

Usar CGenFF num peptídeo canônico é, ao mesmo tempo:
- **desnecessário** — os parâmetros já existem e são melhores
- **prejudicial** — parâmetros CGenFF por analogia são menos acurados para backbone peptídico que os do FF de proteína
- **fonte de erro operacional** — descompasso de versão do CGenFF já causou problema real em outro projeto do usuário

**Correção:** tratar receptor e peptídeo com **o mesmo campo de força de proteína**, gerando a topologia do complexo numa única passada do `pdb2gmx`. CGenFF só entraria se houvesse ligante de pequena molécula na simulação — o que seria o caso para a **benzamidina**, se ela for simulada como controle.

---

## 7. 🟠 Campo de força: CHARMM36m × AMBER99SB-ILDN

O projeto especifica **CHARMM36m**. Todo o legado computacional local usa **AMBER99SB-ILDN + TIP3P** (`inhibitor-selection`, `Milena-MD`, `MD-gromacs`).

Ambos são campos de força respeitáveis e amplamente usados para proteínas. A escolha aqui é menos sobre qualidade absoluta e mais sobre **consequências práticas**:

| | CHARMM36m | AMBER99SB-ILDN |
|---|---|---|
| Peptídeos curtos / desordenados | Reconhecidamente melhor calibrado | Adequado, mas com tendência a superestimar hélice em alguns casos |
| Reuso do legado do grupo | Nenhum — setup do zero | Total — `.mdp`, scripts e análises prontos |
| Comparabilidade com GORE 1-2 T | A conferir no artigo | A conferir no artigo |
| Risco operacional | Maior (primeira vez na maioria dos projetos) | Menor |

**Recomendação:** dado que o GORE3 é um peptídeo curto e provavelmente flexível, o argumento técnico favorece **CHARMM36m**. Mas a decisão deve ser tomada com dois dados que ainda faltam:

1. **Qual campo de força foi usado no MD de 100 ns do GORE 1-2 T** (de Andrade et al., 2026) — usar o mesmo garante comparabilidade direta com a publicação anterior do grupo, o que tem peso na revisão
2. Se há tempo para validar um setup novo

Um projeto do grupo (Tatiana-MD) já roda CHARMM36 no servidor, então a infraestrutura existe.

**O que não pode acontecer:** escolher CHARMM36m no papel e rodar AMBER na prática, ou vice-versa. Declarar e cumprir.

---

## 8. 🟡 Desenho experimental: réplicas

O projeto (§2.3) propõe "**três réplicas técnicas e três réplicas biológicas**".

**Réplicas técnicas são desnecessárias em RNA-Seq Illumina moderno.** A variabilidade técnica da plataforma é baixa e bem modelada pela distribuição binomial negativa que o DESeq2 já assume. O poder estatístico vem de **réplicas biológicas** — e réplicas técnicas consomem orçamento de sequenciamento sem contribuir para ele.

**Recomendado:**
- Eliminar réplicas técnicas
- **Mínimo 3, preferencialmente 4–5 réplicas biológicas** por tratamento
- Realocar o orçamento economizado para mais réplicas biológicas ou para um segundo ponto temporal (ver [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) §3)
- Registrar explicitamente o que constitui uma réplica biológica (número de intestinos agrupados por réplica) — o projeto não define isso, e é informação exigida na publicação
- **Randomizar** a alocação de amostras às lanes/posições para não confundir lote com tratamento

> ⚠️ **Inconsistência a corrigir:** §2.3 lista os tratamentos como "controle, SKTI, benzamidina e **GORE2**". O projeto é sobre **GORE3**. Ver [`06_correcoes_projeto.md`](06_correcoes_projeto.md).

---

## 9. 🟡 Etapas ausentes que devem entrar

| Etapa | Por quê |
|---|---|
| **BUSCO** | Métrica padrão de completude para montagem/anotação. Revisores pedem. Usar linhagem Lepidoptera ou Insecta |
| **Análise de splicing alternativo** | É objetivo declarado do projeto, mas **nenhuma ferramenta é especificada na metodologia**. rMATS ou DEXSeq — ambos exigem o genoma (item 1) |
| **Análise dirigida da família de serino-proteases** | A pergunta central não é respondida por DEGs globais. Precisa de: identificação de todas as tripsinas anotadas → alinhamento → filogenia → expressão por isoforma |
| **Controle de lote / covariáveis** | Se as amostras forem sequenciadas em corridas diferentes, incluir no modelo do DESeq2 |
| **WGCNA** | Citado no `GORE3-abstract.docx`, ausente da metodologia do `.docx` do projeto. Script pronto em `RNA-Seq-not-model/scripts/04_wgcna.R` |
| **Validação por RT-qPCR** | Padrão esperado para confirmar um subconjunto de DEGs. Requer genes de referência validados — o grupo tem **AgRPL10** de outro projeto |
| **Deposição dos dados** | SRA/BioProject. O grupo já tem o fluxo estabelecido (PRJNA1494060) |

---

## 10. 🟡 MM/PBSA — usar, mas declarar as limitações

O projeto menciona MM-PBSA para energia de ligação. É prática comum e aceitável, mas com ressalvas que devem estar no texto:

- Métodos *end-point* como MM/PBSA e MM/GBSA fornecem **energias relativas**, úteis para **ranquear** ligantes, não valores absolutos comparáveis a Kᵢ experimental
- A **entropia configuracional** normalmente é omitida ou aproximada de forma grosseira; a alternativa acessível é a **entropia de interação**, que o usuário já tem implementada (`Milena-MD/bin/interaction_entropy.py`)
- Resultados dependem fortemente da constante dielétrica interna escolhida — declarar o valor
- **Replicatas independentes** de MD (3 réplicas com sementes distintas) são hoje mais valorizadas que uma única trajetória longa, por permitirem barra de erro

**Recomendado:** 3 réplicas × 100 ns por complexo, em vez de 1 × 300 ns. O ganho em estimativa de incerteza compensa.

Ferramenta: **gmx_MMPBSA**. O usuário já tem ambiente funcional (`mmgbsa-env`) e conhece as armadilhas operacionais (correção de PBC antes da análise).

---

## 11. Fluxo consolidado recomendado

### Transcriptômica

| Etapa | Ferramenta |
|---|---|
| QC | FastQC + MultiQC |
| Trimagem | fastp |
| Alinhamento | STAR ou HISAT2 → `GCF_050436995.1` |
| Quantificação | featureCounts ou Salmon + tximport |
| Completude | BUSCO |
| Expressão diferencial | DESeq2 (padj < 0,05; \|log2FC\| ≥ 1) |
| Splicing | rMATS ou DEXSeq |
| Anotação | eggNOG-mapper v2 (+ InterProScan) |
| Enriquecimento | clusterProfiler |
| Coexpressão | WGCNA |
| Montagem paralela | Trinity + CD-HIT + TransDecoder (transcritos não anotados e bacterianos) |

> **Nota sobre o corte de significância:** o projeto propõe padj < 0,01. É defensável e conservador. padj < 0,05 é o mais comum e aumenta o poder. Qualquer um serve — desde que declarado e mantido.

### Estrutural

| Etapa | Ferramenta |
|---|---|
| Estruturas das tripsinas | AlphaFold2/ColabFold (isoformas priorizadas pelo transcriptoma) |
| Validação | ProSA-web, Ramachandran, pLDDT/PAE |
| Protonação | pdb2pqr/PROPKA em **pH alcalino** (~8,2) |
| Estrutura do peptídeo | PEP-FOLD ou AlphaFold |
| Docking | HADDOCK e/ou AlphaFold3; Vina como triagem; redocking de controle |
| MD | GROMACS, 3 × 100 ns, FF único para proteína+peptídeo |
| Análises | RMSD, RMSF, Rg, SASA, ligações de H, contatos, distâncias da tríade catalítica |
| Energia livre | gmx_MMPBSA + entropia de interação |
| Fingerprint | ProLIF |

### Integração — o diferencial

```
DEGs de tripsina (transcriptoma)
        ↓ prioriza
isoformas a modelar
        ↓
AlphaFold → docking → MD
        ↓
GORE3 inibe as isoformas INDUZIDAS ou não?
```

Este loop é o que transforma dois conjuntos de resultados paralelos num argumento único. Ver [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md).

---

## Referências desta seção

- Jumper et al. (2021) — *Nature* — PMID 34265844 — AlphaFold2
- Abramson et al. (2024) — *Nature* — PMID 38718835 — AlphaFold3
- Pilon, F.M. et al. (2017) — PMID 28762531 — microbiota proteolítica
- dos Santos et al. (2025) — doi:10.14411/eje.2025.015
- de Andrade et al. (2026) — PMID 41956187
- Assembly `GCF_050436995.1` — NCBI Datasets
