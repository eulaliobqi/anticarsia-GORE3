# Base teórica — Pós-doc GORE3

Fundamentação para o projeto *"Resposta transcriptômica e interação estrutural do inibidor peptídico GORE3 em lagartas-praga de culturas agrícolas"* (UFV / INCT-IPP, supervisão Profa. Maria Goreti de Almeida Oliveira).

Material de apoio para a escrita da introdução e para o ajuste da metodologia antes do início das análises.

**Escopo definido:** *Anticarsia gemmatalis* por enquanto. RNA-Seq em sequenciamento na Macrogen.

---

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| [`01_fundamentacao_teorica.md`](01_fundamentacao_teorica.md) | Praga, digestão proteica em Lepidoptera, inibidores de protease, modelo de Laskowski, mecanismos de adaptação |
| [`02_estado_da_arte_GORE.md`](02_estado_da_arte_GORE.md) | Linhagem GORE1 → GORE 1-2 T e o que o grupo já publicou; onde o GORE3 se encaixa |
| [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) | Metodologia revisada: o que o projeto propõe × padrão atual, com justificativa |
| [`04_viabilidade.md`](04_viabilidade.md) | Dados, ativos locais reaproveitáveis, hardware, prazos, riscos |
| [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) | Lacunas do conhecimento, hipóteses testáveis, contribuição original |
| [`06_correcoes_projeto.md`](06_correcoes_projeto.md) | Inconsistências detectadas no `.docx`, com correção proposta |
| [`referencias.bib`](referencias.bib) | BibTeX — somente referências com DOI/PMID verificado |
| [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) | O que foi verificado, como, e o que **não** pôde ser confirmado |

---

## Sumário executivo

**O projeto é viável**, com três ressalvas que exigem decisão antes de começar.

### 1. O genoma de referência mudou o jogo

*A. gemmatalis* passou a ter genoma RefSeq — **`GCF_050436995.1`** (ilAntGemm2), com anotação NCBI. O projeto foi redigido em Set/2025 assumindo montagem *de novo* com Trinity, o que hoje é subótimo. Migrar para pipeline **genoma-guiado** melhora quantificação, viabiliza análise de splicing alternativo com métodos estabelecidos e resolve a atribuição de isoformas de tripsina — que é justamente a pergunta central do projeto.

Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md).

### 2. Há muito ativo local reaproveitável

Pipelines Nextflow maduros, setups GROMACS validados, estruturas de tripsina já modeladas e protonadas em pH intestinal, e docking do GORE3 já produzido (Vina + HADDOCK). O projeto não contabiliza nada disso. O trabalho real é menor do que o documento sugere.

Ver [`04_viabilidade.md`](04_viabilidade.md).

### 3. A sequência do GORE3 não está confirmada documentalmente

Este é o ponto mais sensível. Não foi localizado nenhum documento que declare textualmente a sequência de aminoácidos do GORE3. Há evidência estrutural (`LALAY`, extraída de arquivos PDB locais), mas ela **não bate** com os peptídeos nomeados na publicação mais recente do grupo. Precisa ser resolvido com a supervisora antes de qualquer modelagem.

Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md), seção 1.

---

## O achado que dá originalidade ao projeto

O resumo do próprio projeto (`GORE3-abstract.docx`) registra que o GORE3 produz **respostas opostas nas duas espécies**: superexpressão de proteases em *S. frugiperda*, mas **redução** da atividade proteolítica em *A. gemmatalis*.

Isso não é ruído. É a diferença entre um inseto que consegue montar resposta compensatória e um que não consegue — e é exatamente o que a transcriptômica pode explicar. Nenhum trabalho do grupo abordou isso diretamente.

Ver [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md).

---

## Como usar na escrita da introdução

Ordem sugerida de leitura para montar o texto:

1. `01` §1 e §2 → contexto agronômico e o problema
2. `01` §3 a §5 → inibidores de protease como alternativa e como funcionam
3. `01` §6 → por que os inibidores falham (adaptação) — esta é a tensão que justifica o trabalho
4. `02` → o que o grupo já fez e o que ainda não sabe
5. `05` → a lacuna e a hipótese

Toda afirmação nos arquivos vem com citação. As que não têm fonte confirmada estão marcadas com ⚠️ e listadas em `NOTAS_DE_AUDITORIA.md`.

---

*Última atualização: 18/07/2026*
