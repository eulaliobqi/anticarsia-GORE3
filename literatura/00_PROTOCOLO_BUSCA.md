# Protocolo de busca — levantamento bibliográfico do pós-doc GORE3

Data de execução: **27/07/2026**. Base: **PubMed** (via MCP `pubmed-mcp`, que
encapsula as E-utilities do NCBI). Metadados bibliográficos completos (DOI,
volume, páginas, status de acesso aberto) obtidos do **Europe PMC**
(`resultType=core`).

Resultado: **125 referências verificadas**, todas com DOI ou PMID resolvido
nesta sessão.

---

## Regras aplicadas

**Identificador obrigatório.** Nenhuma referência entra sem DOI ou PMID
confirmado aqui. Referência sem identificador vai para
[05_AUDITORIA_REFS_DOCX.md](05_AUDITORIA_REFS_DOCX.md) como pendência
declarada — não é mantida em silêncio nem removida em silêncio.

**Precedência de ferramenta.** `pubmed-mcp` acima de `WebSearch` para
atribuição de PMID e periódico. Regra herdada de `project_lncc_peptideos_ia`:
o WebSearch já atribuiu periódico errado pelo menos uma vez neste projeto.

**Recência.** O corte depende do papel da referência:

| Papel | Exigência | Resultado obtido |
|---|---|---|
| Justificativa metodológica (eixos 2B, 2D, 3A–3D) | 2023+ | mediana **2024**; 20 de 30 são 2023+ |
| Artigo-fonte de ferramenta (eixo 2A) | qualquer ano — citação canônica | mediana 2017, isento por regra |
| Contexto biológico (temas 1 e 4) | 2020+ com exceção justificada | mediana 2021; 40 de 59 são 2020+ |
| Clássico fundacional | sem corte, marcado como tal | Laskowski & Kato 1980, Jongsma 1995 |

**Proveniência.** Cada ficha declara em `Lido de:` o que foi efetivamente
lido. Ficha marcada `abstract` não pode conter número ou detalhe de protocolo
que só apareceria no corpo do artigo.

---

## Lição de execução: a busca em linguagem natural falha

As quatro primeiras buscas usaram frases descritivas
(`"Lepidoptera midgut trypsin isoforms serine protease diversity"`) e
**retornaram zero resultados**. O MCP repassa a string literalmente ao PubMed,
que a interpreta como conjunção de todos os termos. Todas as buscas seguintes
usaram sintaxe booleana com tags de campo (`[tiab]`, `[ti]`, `[au]`), e foi
isso que produziu os resultados.

Duas consequências práticas registradas para reuso:

1. **Busca por autor foi o que mais rendeu.** `Merino-Cabrera[au]` revelou de
   uma vez a linhagem inteira da série de peptídeos do grupo — incluindo o
   artigo de origem de 2017 (PMID 28925864), os tripeptídeos (35315942) e os
   dipeptídeos com arginina (35715046) — que nenhuma busca temática tinha
   trazido. O mesmo padrão resolveu Saikhedkar 2018 e Laskowski.
2. **Nomes de ferramenta precisam de busca própria.** Buscar RNA-Seq por tópico
   não traz o artigo do STAR nem do Salmon. E `Salmon[ti]` sozinho traz peixe:
   foi preciso `Salmon[ti] AND (transcript[tiab] OR "RNA-seq"[tiab])`.

---

## Eixos de busca e rendimento

### Tema 1 — Peptídeos inibidores de tripsina (41 refs)

| Eixo | Assunto | n |
|---|---|---|
| 1A | Peptídeos curtos desenhados; derivados de *reactive center loop* | 14 |
| 1B | Tripsinas digestivas de Lepidoptera: isoformas, especificidade S1 | 6 |
| 1C | Adaptação do inseto e resposta compensatória a inibidores | 13 |
| 1D | Cinética de inibição e o modelo canônico de Laskowski | 8 |

Strings principais:
```
(peptide[Title] AND (trypsin inhibitor[Title/Abstract] OR protease inhibitor[Title/Abstract]))
    AND (insect OR Lepidoptera OR larvae)            [2018-2026]
"reactive center loop"[tiab] AND (peptide[tiab] OR inhibitor[tiab])
"protease inhibitor"[tiab] AND insect[tiab] AND (adaptation[tiab] OR compensatory[tiab] OR insensitive[tiab])
midgut[tiab] AND trypsin[tiab] AND (Lepidoptera[tiab] OR caterpillar[tiab] OR larvae[tiab])
Merino-Cabrera[au] OR "Merino Cabrera"[au]
Saikhedkar[au]
Laskowski M[au] AND Qasim MA[au]
Jongsma MA[au] AND (protease inhibitor[tiab] OR proteinase inhibitor[tiab])
Moon J[au] AND cowpea bruchid[tiab]
```

### Tema 2 — RNA-Seq (31 refs)

| Eixo | Assunto | n |
|---|---|---|
| 2A | Artigos-fonte das ferramentas prescritas em `03_metodologia §11` | 18 |
| 2B | Benchmarks e boas práticas (2023+) | 5 |
| 2C | Transcriptômica de intestino de inseto sob estresse | 4 |
| 2D | Fronteira 2024–2026 | 4 |

```
Salmon[ti] OR "selective alignment"[tiab] OR tximport[ti] OR DESeq2[ti] OR featureCounts[ti]
HISAT[ti] OR fastp[ti] OR MultiQC[ti] OR BUSCO[ti] OR "STAR: ultrafast"[ti]
eggNOG[ti] OR clusterProfiler[ti] OR WGCNA[ti] OR InterProScan[ti] OR "nf-core"[ti]
RNA-seq[ti] AND (benchmark[tiab] OR comparison[tiab]) AND (aligner[tiab] OR quantification[tiab])   [2022-2026]
("differential transcript usage"[tiab] OR "isoform-level"[tiab] OR "alternative splicing"[ti]) AND RNA-seq[tiab]   [2021-2026]
insect[tiab] AND midgut[tiab] AND transcriptome[tiab] AND (detoxification[tiab] OR cytochrome P450[tiab] OR glutathione S-transferase[tiab])   [2020-2026]
```

### Tema 3 — Biologia estrutural (30 refs)

| Eixo | Assunto | n |
|---|---|---|
| 3A | Predição de estrutura (AlphaFold e sucessores) | 4 |
| 3B | Docking proteína–peptídeo | 7 |
| 3C | Campos de força e dinâmica molecular | 4 |
| 3D | Energia livre de ligação e limitações | 6 |
| 3E | Arquitetura de subsítios de serino-proteases | 9 |

```
AlphaFold[ti]   [2023-2026]
("protein-peptide"[tiab] AND docking[tiab]) OR ("peptide docking"[tiab]) OR (HADDOCK[tiab])   [2020-2026]
(MM-PBSA[tiab] OR MM/GBSA[tiab] OR MMPBSA[tiab] OR MMGBSA[tiab]) AND (accuracy[tiab] OR limitation[tiab] OR pitfall[tiab] OR benchmark[tiab] OR entropy[tiab])   [2020-2026]
("force field"[tiab] AND (CHARMM36m[tiab] OR AMBER[tiab]) AND (peptide[tiab] OR "intrinsically disordered"[tiab]))   [2019-2026]
(trypsin[tiab] OR "serine protease"[tiab]) AND (S1 pocket[tiab] OR "substrate specificity"[tiab] OR subsite[tiab]) AND (Asp189[tiab] OR "specificity pocket"[tiab] OR "catalytic triad"[tiab])   [2015-2026]
"prime side"[tiab] OR "S' subsite"[tiab] OR "non-canonical binding"[tiab] AND protease[tiab] AND inhibitor[tiab]   [2015-2026]
```

O eixo 3E foi criado depois de a primeira rodada tê-lo deixado vazio — a
verificação de cobertura pegou isso. É o eixo que sustenta a hipótese H6
(modo de ligação não canônico do GORE3).

### Tema 4 — Manejo de *Anticarsia* com peptídeos (23 refs)

| Eixo | Assunto | n |
|---|---|---|
| 4A | A praga e o dano — fonte primária | 4 |
| 4B | Táticas atuais de controle | 11 |
| 4C | Bioinseticidas peptídicos, entrega e seletividade | 7 |
| 4D | Recursos genômicos | 1 |

```
Anticarsia gemmatalis[tiab]   [2018-2026]
Anticarsia gemmatalis[tiab] AND (soybean[tiab] OR soja[tiab]) AND (damage[tiab] OR defoliation[tiab] OR yield[tiab] OR loss[tiab])   [2015-2026]
```

O eixo 4D ficou com **1 referência apenas** — lacuna declarada, não silenciosa.
Os recursos genômicos de *A. gemmatalis* estão majoritariamente em registros
de banco de dados (RefSeq `GCF_050436995.1`, BioProject) e não em artigos
indexados; as duas entradas `@misc` correspondentes já estão em
`docs/referencias.bib`.

---

## Recuperação de conteúdo

Cascata por artigo, primeira que funcionar vence:

1. **Europe PMC `fullTextXML`** — texto completo de artigos OA.
2. **Unpaywall** `best_oa_location.url_for_pdf` — PDF de depósito aberto.
3. Fechado → só o abstract é salvo; o artigo vai para
   [PDFS_PENDENTES.md](PDFS_PENDENTES.md).

**Duas rotas foram testadas e descartadas na etapa de validação**, antes do
lote (a validação prévia é o que evitou repetir o resultado de 2 PDFs em 24 do
script `design-inibidores/baixar_artigos.py`):

- `europepmc/webservices/rest/{PMCID}/fullTextPDF` → **404** mesmo para artigo
  comprovadamente OA.
- **NCBI PMC OA Web Service** (`oa.fcgi`) → responde 200, mas devolve link
  `format="tgz"` para `ftp.ncbi.nlm.nih.gov`, e o equivalente HTTPS do caminho
  retorna **404**. Não é rota utilizável hoje.

A troca de "baixar PDF" por "baixar texto completo" foi deliberada: texto é
pesquisável e permite conferir cada afirmação contra a fonte, que é o
requisito da regra de não-fabricação. PDF continua sendo baixado quando o
Unpaywall entrega um.

**Resultado:** 47 com texto completo, 3 com PDF, 123 de 125 com abstract
salvo. **40% com conteúdo integral** — dentro da faixa de 40–60% prevista, e
explicada pela composição: métodos de bioinformática são majoritariamente OA,
entomologia aplicada (*Pest Manag Sci*, *Arch Insect Biochem Physiol*,
*Pestic Biochem Physiol*) é majoritariamente fechada.

Dois artigos ficaram sem abstract no Europe PMC; um deles (PMID 41907587,
*Binding Free Energies without Alchemy*) não tem registro no Europe PMC e
consta apenas do PubMed — está registrado como tal no `INDEX.json`.

---

## Reprodutibilidade

```bash
cd literatura
python scripts/fetch_literatura.py    # metadados + texto/PDF + abstracts
python scripts/gerar_artefatos.py     # .bib, INDEX.json, fichas, pendentes
```

A lista curada de PMIDs, com atribuição de tema/eixo/tier, está no dicionário
`CURADOS` de `scripts/fetch_literatura.py` — é a fonte de verdade da seleção.
`scripts/gerar_artefatos.py` **não escreve interpretação de artigo**: emite
metadados verificados e marca o campo interpretativo como pendente. O texto de
"O que estabelece" é escrito à mão depois de ler a fonte.
