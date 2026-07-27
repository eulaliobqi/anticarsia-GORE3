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

Interpretação: **50 artigos fichados**. Cinco foram lidos no texto completo
(seções de resultados e discussão), 45 pelo abstract.

**Todo artigo com conteúdo integral em disco está fichado** — os 47 com texto
completo e os 3 com PDF. Os 75 restantes só têm abstract salvo porque são de
acesso fechado; estão listados em `PDFS_PENDENTES.md` e seguem marcados
`⚠️ PENDENTE DE FICHAMENTO`.

Cobertura por tema: 9 no Tema 1, 21 no Tema 2, 7 no Tema 3, 13 no Tema 4.
Dos 56 artigos Tier 1, 21 estão fichados — os outros 35 dependem de download
manual via CAFe.

O texto interpretativo vive em `scripts/fichas_tier1.py`, separado do gerador
de propósito: `gerar_artefatos.py` emite metadados verificados e **nunca**
escreve interpretação de artigo. Cada ficha declara em `Lido de` o que foi
efetivamente lido **ao escrevê-la** — ter o texto completo salvo não significa
tê-lo lido, e essa distinção está explícita no arquivo gerado.

## O que a leitura mudou no projeto

Três achados foram promovidos para os documentos do projeto:

1. **IC₅₀ do GORE3 existe publicado** — 433,98 µM, Kᵢ = 4,00 mM competitivo
   (Paulo et al. 2026), o que destrava parcialmente o item 2 de
   `NOTAS_DE_AUDITORIA.md` §7. Ressalva: é *S. frugiperda*.
2. **Duas inconsistências internas nesse mesmo artigo** — o Kᵢ da benzamidina
   difere 100× entre abstract e resultados, e a mortalidade não é monotônica
   com a dose. Registrado em `NOTAS_DE_AUDITORIA.md` §8.1.
3. **A janela de MD planejada pode ser curta demais para testar H6** — Kahler
   et al. (2018) viram a troca de modo de ligação só depois de 2 µs, contra os
   3 × 100 ns previstos. Registrado em `NOTAS_DE_AUDITORIA.md` §9 e como
   ressalva em `docs/03_metodologia_padrao_ouro.md`.

E dois achados sobre a H6, em direções opostas:

- **Contra a premissa de ancoragem canônica:** em `paulo2026peptides`, o ganho
  de afinidade dos pentapeptídeos depende de **lisina em P1** (mais ligações
  pi-sigma) — e o LALAY não tem resíduo básico.
- **A favor de um modo alternativo plausível:** `jiang2018halogen` mostra que o
  bolsão S1 de serino-proteases tipo tripsina admite grupo P1 **não básico**
  (halogenado), por ligação de halogênio em vez de ponte salina com o Asp189.
  O mecanismo específico não se transfere ao LALAY, mas o princípio sim: S1
  não exige carga positiva.

Também apareceu um alerta para a hipótese H1: `lokya2020response` já
demonstrou, por zimografia e qRT-PCR, que um inibidor Bowman-Birk faz
**isoformas de protease desaparecerem** e modula sua expressão — é o desenho
análogo ao que este projeto quer fazer por RNA-Seq, e portanto o precedente
contra o qual a originalidade da H1 será julgada.

## Regras

Nada entra sem DOI ou PMID resolvido na sessão. Ficha marcada `Lido de:
abstract` não pode conter número ou detalhe de protocolo que só apareceria no
corpo do artigo. Onde falta o dado e ele importa, escreve-se
`⚠️ [PENDENTE: ... — requer fulltext]` em vez de preencher.
