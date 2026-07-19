# Análise de viabilidade

Avaliação honesta do que é executável, com que recursos e em que prazo.

**Veredito: o projeto é viável**, e o esforço real é menor do que o documento sugere, porque boa parte da infraestrutura computacional já existe e está validada. Os riscos concentram-se em **dados** (sequenciamento pendente) e em **uma pendência de definição** (sequência do GORE3), não em capacidade técnica.

> Todos os caminhos abaixo foram verificados como existentes em 18/07/2026.

---

## 1. Situação dos dados

### O que existe

| Item | Onde | Situação |
|---|---|---|
| Genoma de referência | `GCF_050436995.1` (NCBI) | ✅ Público, anotado (RS_2025_08) |
| RNA-Seq anterior (controle / SKTI / GORE2) | BioProject **PRJNA1494060**, SRA SRP717437 | ✅ Depositado, 8 SRR |
| Montagem Trinity de *A. gemmatalis* | `C:\Users\eulal\.claude\caracterization-trypsin\data\raw\trinity_assembly.fasta` | ✅ Local |
| Sequências de tripsina de *A. gemmatalis* | `C:\Users\eulal\Desktop\LEBPP\Dsign-racional-peptid-inib\anticarsia_gemmatalis_trypsins.fasta` | ✅ Local |
| Sequências de tripsina de *S. frugiperda* | mesma pasta, `spodoptera_frugiperda_trypsins.fasta` | ✅ Local (para expansão futura) |
| Template cristalográfico | `1tld.cif` (mesma pasta) | ✅ Local |

### O que falta

| Item | Impacto | Mitigação |
|---|---|---|
| **FASTQ do experimento GORE3** | 🔴 Bloqueia todo o bloco transcriptômico | Em sequenciamento na Macrogen. Documentação em `RNA-Seq-Macrogen\` e `Desktop\LEBPP\Pós-doc-eulalio\Macrogen-Docs\` |
| FASTQ bruto do Control R1/C1A (2020) | 🟡 Sem cópia local | Recuperável do SRA se necessário |
| Tabela de DEGs processada de *A. gemmatalis* | 🟡 Não existe localmente | Reprocessável a partir do SRA |
| Dados de *S. frugiperda* | ⚪ Fora do escopo atual | — |

**O caminho crítico é o sequenciamento.** Enquanto os FASTQ não chegam, todo o bloco estrutural pode avançar em paralelo — e boa parte dele já está feita.

---

## 2. Ativos computacionais reaproveitáveis

Este é o ponto onde o projeto subestima o que já tem.

### 2.1 Pipeline RNA-Seq — `RNA-Seq-not-model`

`C:\Users\eulal\.claude\RNA-Seq-not-model\` — Nextflow DSL2, o mais maduro do acervo.

Módulos: `qc`, `trimming`, `assembly`, `orf_prediction`, `annotation`, `quantification`, `differential_expr`, `enrichment`, `report`.

Scripts R prontos em `scripts/` (verificados):

| Script | Função |
|---|---|
| `00_tximport.R` | Agregação transcrito→gene (a etapa que o projeto omite) |
| `01_deseq2.R` | Expressão diferencial |
| `02_gene2go_build.R` | Mapeamento gene→GO customizado |
| `03_enrichment.R` | Enriquecimento com universo próprio |
| `04_wgcna.R` | Coexpressão |
| `05_batch_correction.R` | Correção de lote |
| `install_packages.R` | Setup do ambiente |

**Adaptação necessária:** o pipeline é *de novo*. Para o modo genoma-guiado recomendado ([`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §1) é preciso acrescentar um caminho STAR/HISAT2 + featureCounts. Os módulos a jusante (DESeq2, enriquecimento, WGCNA) funcionam sem alteração.

**Esforço estimado:** moderado. Um módulo novo de alinhamento e ajuste do samplesheet.

### 2.2 Fluxo transcriptoma → estrutura — `caracterization-trypsin`

`C:\Users\eulal\.claude\caracterization-trypsin\nextflow\` — pipeline de 11 fases que já implementa exatamente a integração que dá originalidade a este projeto: Trinity → CD-HIT → TransDecoder → HMMER (identificação de tripsinas) → MAFFT/IQ-TREE (filogenia) → AlphaFold → Vina → GROMACS.

Espelho em `C:\Users\eulal\trypsin-agemmatalis-structural\`.

### 2.3 Setups GROMACS validados

`C:\Users\eulal\.claude\inhibitor-selection\params\` (verificado):
`minim.mdp`, `ions.mdp`, `nvt.mdp`, `npt.mdp`, `md.mdp`

⚠️ Estes `.mdp` são de linhagem **AMBER99SB-ILDN + TIP3P**. Se a decisão for CHARMM36m, precisam de revisão (esquema de cutoff e tratamento de vdW diferem entre as famílias de campo de força — não é troca de uma linha).

### 2.4 Scripts de análise de MD — `Milena-MD`

`C:\Users\eulal\.claude\Milena-MD\bin\` (verificado). Este é o acervo mais valioso do ponto de vista de tempo economizado:

| Script | Uso |
|---|---|
| `mmgbsa_interpret.py` | Interpretação de energia livre |
| `interaction_entropy.py` | Entropia de interação (resolve a limitação do MM/PBSA) |
| `contact_map.py` | Mapas de contato |
| `pharmacophore_profile.py` | Perfil farmacofórico |
| `prepare_complex.py` | Preparo de complexo |
| `pdb2pqr_process.py` | Protonação |
| `plot_results.py` | Gráficos |

Estes scripts foram validados na série trypsin × GORE 1-2 T, já encerrada. São diretamente aplicáveis ao GORE3.

### 2.5 Estruturas de tripsina prontas

`C:\Users\eulal\.claude\analise-alosterica\data\` — modelos finais + subpasta `protonated\` com estruturas já tratadas em **pH 8,2** (verificado: `ACR157-final_ph8.2.pdb`, `QCL936-final_ph8.2.pdb`, `XP273-final_ph8.2.pdb` e correspondentes `.pqr`).

Isso está **correto** e é frequentemente esquecido: o intestino de lepidóptero é alcalino (Pilon et al., 2017), e protonar a pH 7,0 seria erro.

Adicionalmente: `C:\Users\eulal\Desktop\LEBPP\GORE4-ate-GORE13\Anticarsia-trypsin\` com 12 isoformas `DN*_i*-clean.pdb`.

### 2.6 Docking do GORE3 já produzido

`C:\Users\eulal\Desktop\LEBPP\GORE4-ate-GORE13\GORE3\` (verificado) — resultados **HADDOCK** empacotados para cinco isoformas:

`ACR157-GORE3_Haddock.tgz`, `DN773-GORE3_Haddock.tgz`, `DN1441-GORE3_Haddock.tgz`, `DN1937-GORE3_Haddock.tgz`, `QCL936-GORE3_Haddock.tgz`

Mais `Residuos-cataliticos.docx` na mesma pasta.

E, em `Desktop\LEBPP\Paper-Daniel-Pablo\`: redocking de validação contra tripsina bovina (**1BTY**), docking DN773/DN1937 × GORE3 e controles com benzamidina.

> **Implicação:** o protocolo de docking recomendado em [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §5 — HADDOCK + redocking de controle — **já está em uso na prática**. Falta apenas escrevê-lo no projeto, que ainda descreve Vina/PyRx.

### 2.7 Textos base

| Arquivo | Uso |
|---|---|
| `C:\Users\eulal\.claude\analise-alosterica\artigo.md` | Manuscrito vivo sobre o peptídeo no sítio S'2, em português — melhor ponto de partida textual |
| `C:\Users\eulal\.claude\caracterization-trypsin\docs\introduction.md` | Introdução sobre tripsinas de *A. gemmatalis* |
| `C:\Users\eulal\.claude\MD-gromacs\artigo_md.md` | Redação de metodologia de MD |
| `Desktop\LEBPP\Paper-Daniel-Pablo\Manuscript_Daniel Guimarães_Versão final.docx` | Manuscrito do docking (publicado como PMID 41510779) |
| `C:\Users\eulal\.claude\analise-alosterica\paper-goreti.pdf` | Base do sítio S'2 |

---

## 3. Hardware e tempo

**Servidor:** Debian, RTX 5070 Ti 16 GB, 32 cores (`eulalio@200.235.143.10`, requer VPN).

### Bloco transcriptômico

Com genoma de referência, o custo computacional é modesto. Índice STAR de um genoma de lepidóptero, alinhamento de ~12–20 bibliotecas, quantificação e DESeq2 — trabalho de **horas a poucos dias**, não semanas. A montagem Trinity paralela é o passo mais caro (memória, não GPU) e roda uma vez.

**Gargalo real: não é computacional. É a chegada dos dados.**

### Bloco estrutural

| Tarefa | Estimativa |
|---|---|
| AlphaFold por isoforma de tripsina (~230 aa) | Rápido em GPU; MSA costuma dominar o tempo |
| MD, 100 ns, complexo tripsina+peptídeo solvatado | Ordem de **1–3 dias por réplica** em GPU única |
| 3 réplicas × 4 isoformas | ~**12–36 dias** de GPU, sequencial |
| gmx_MMPBSA | Horas por trajetória |

**Este é o gargalo computacional real.** Recomendações:

1. **Priorizar isoformas.** Não simular todas as tripsinas anotadas — usar o transcriptoma para escolher 3–5 (as mais expressas + as mais induzidas pelo GORE3). Esta é justamente a lógica de integração do projeto.
2. **Começar já**, com as isoformas já modeladas, sem esperar o RNA-Seq. Refinar a seleção depois.
3. As 3 réplicas de uma mesma condição são independentes — podem ser enfileiradas e rodadas sem supervisão.

> **Regras operacionais do servidor** (não negociáveis, já documentadas): `screen -S <nome>` antes de qualquer Nextflow; `gmx_mpi` com `mpirun -np 1`; `mamba` em vez de `conda`; correção de PBC (`gmx trjconv -pbc mol -center`) antes do gmx_MMPBSA.

---

## 4. Riscos

| # | Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | ~~Sequência do GORE3 indefinida~~ | — | ✅ **Resolvido** | GORE3 = `LALAY`, confirmado 18/07/2026. Risco substituído pelo #1b |
| 1b | **Sítio de ligação do GORE3 incerto** — sem resíduo básico, não ancora no Asp189/S1 | Alta | 🟠 Médio-alto | Testar S1 **e** S'2; *blind docking* prévio. Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) §1.1 |
| 2 | Atraso no sequenciamento | Média | 🔴 Alto | Avançar bloco estrutural em paralelo; reprocessar PRJNA1494060 como piloto do pipeline |
| 3 | Anotação automática incompleta para tripsinas | Média | 🟡 Médio | Montagem Trinity paralela + busca HMMER dirigida |
| 4 | Réplicas insuficientes para splicing | Média | 🟡 Médio | rMATS/DEXSeq exigem mais poder que DE simples. Definir n antes de sequenciar — depois é tarde |
| 5 | Decisão de campo de força adiada | Média | 🟡 Médio | Decidir **antes** de iniciar MD. Retrabalho aqui custa semanas de GPU |
| 6 | Contribuição da microbiota confunde interpretação | Média | 🟡 Médio | Declarar como limitação; usar montagem *de novo* para identificar transcritos não-hospedeiro |
| 7 | VPN/servidor indisponível | Baixa | 🟢 Baixo | Timeout de SSH normalmente indica VPN, não servidor fora |

---

## 5. Estratégia de execução recomendada

### Enquanto o sequenciamento não chega

1. ✅ ~~Resolver a pendência da sequência do GORE3~~ — feito: `LALAY`
2. **Decidir o campo de força** — bloqueia todo o MD
3. **Consolidar o docking já feito** — os `.tgz` do HADDOCK contêm resultados ainda não analisados de forma unificada
4. **Baixar e indexar `GCF_050436995.1`**
5. **Rodar o pipeline genoma-guiado sobre PRJNA1494060** — reprocessar o experimento GORE2/SKTI contra o genoma novo. Isso valida o pipeline com dados reais, dá um resultado publicável por si (comparação *de novo* × genoma-guiado) e deixa tudo pronto para quando o GORE3 chegar
6. **Iniciar MD das isoformas já modeladas**

O item 5 é o de melhor retorno: transforma tempo de espera em validação de método.

### Quando os dados chegarem

Pipeline já testado → resultado rápido → seleção de isoformas → MD dirigida → integração.

---

## 6. Custo

Não há custo computacional adicional (infraestrutura própria). O custo relevante é o **sequenciamento**, já contratado na Macrogen.

Os documentos de cotação estão em `C:\Users\eulal\.claude\RNA-Seq-Macrogen\` e `Desktop\LEBPP\Pós-doc-eulalio\Macrogen-Docs\`. ⚠️ Valores não reproduzidos aqui por não terem sido conferidos.

---

## Referências desta seção

- Pilon, F.M. et al. (2017) — PMID 28762531 — pH intestinal alcalino
- Assembly `GCF_050436995.1` — NCBI
- BioProject PRJNA1494060 / SRA SRP717437 — dados anteriores do grupo
