# Base bibliográfica — pós-doc GORE3

Levantamento de **27/07/2026**. 125 artigos, todos com DOI ou PMID resolvido
na sessão. Serve à escrita da introdução e à defesa de cada escolha
metodológica em [`../docs/03_metodologia_padrao_ouro.md`](../docs/03_metodologia_padrao_ouro.md).

## Números

| | |
|---|---|
| Referências verificadas | **125** |
| Com texto completo | 47 |
| Com PDF | 3 |
| Com abstract salvo | 123 |
| Fechados (download manual) | 75 |
| `docs/referencias.bib` | 17 → **131 entradas** |

Recência por papel da referência: justificativa metodológica com mediana
**2024** (20 de 30 são 2023+); artigos-fonte de ferramenta em 2017, isentos
por serem citação canônica; contexto biológico com mediana 2021.

## Estrutura

```
literatura/
├── 00_PROTOCOLO_BUSCA.md            strings, funil, rotas testadas
├── 01_peptideos_inibidores_tripsina.md   41 refs (1A-1D)
├── 02_rnaseq.md                          31 refs (2A-2D)
├── 03_biologia_estrutural.md             30 refs (3A-3E)
├── 04_manejo_anticarsia.md               23 refs (4A-4D)
├── 05_AUDITORIA_REFS_DOCX.md        veredito das 72 citações do .docx
├── PDFS_PENDENTES.md                75 fechados, link p/ CAFe/UFV
├── INDEX.json                       índice legível por máquina
├── metadata.json                    metadados crus do Europe PMC
├── referencias_novas.bib            gerado; já mesclado no docs/referencias.bib
├── abstracts/                       123 abstracts (versionado)
├── fulltext/                        47 textos completos (git-ignored)
├── pdfs/                            3 PDFs (git-ignored)
└── scripts/
    ├── fetch_literatura.py          busca metadados + recupera conteúdo
    └── gerar_artefatos.py           .bib, INDEX.json, fichas, pendentes
```

`fulltext/` e `pdfs/` não são versionados: são obra do editor. Reprodutíveis a
qualquer momento rodando o script.

## Como usar

**Para escrever a introdução:** abrir o `.md` do tema. Cada ficha traz autores,
periódico, DOI/PMID clicável e o campo **Lido de**, que declara o que foi
efetivamente lido daquele artigo.

**Para achar referência por assunto:** `INDEX.json` tem tema, eixo, tier e
nível de acesso por artigo.

**Para citar:** usar `docs/referencias.bib`, que é a fonte única de verdade.

## Estado do fichamento

Metadados: **completos e verificados** para os 125.

Interpretação (`O que estabelece` / `Onde entra`): **pendente** — as fichas
estão marcadas `⚠️ PENDENTE DE FICHAMENTO`. Isso é deliberado. O gerador não
escreve interpretação de artigo; esse texto é escrito à mão depois de ler a
fonte, e o campo `Lido de` registra o que foi lido. Preencher a partir do
conhecimento prévio do modelo violaria a regra de não-fabricação.

Prioridade para a próxima sessão: os artigos **Tier 1 que já têm texto
completo em disco** — são os que dá para fichar sem depender de download
manual.

## Regras

Nada entra sem DOI ou PMID resolvido na sessão. Ficha marcada `Lido de:
abstract` não pode conter número ou detalhe de protocolo que só apareceria no
corpo do artigo. Onde falta o dado e ele importa, escreve-se
`⚠️ [PENDENTE: ... — requer fulltext]` em vez de preencher.
