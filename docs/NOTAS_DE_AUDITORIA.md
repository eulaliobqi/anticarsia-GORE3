# Notas de auditoria

Registro do que foi verificado, como, e — sobretudo — **o que não pôde ser confirmado**.

Este arquivo existe para que nada nesta base teórica seja tomado como fato sem rastro. Onde faltou evidência, está declarado como lacuna em vez de preenchido por inferência.

**Data da auditoria:** 18/07/2026

---

## 1. 🔴 A sequência do GORE3 NÃO está confirmada

**Esta é a pendência mais importante do projeto. Bloqueia toda a modelagem estrutural.**

### O que foi encontrado

Nenhum documento localizado declara textualmente a sequência de aminoácidos do GORE3. O que existe é evidência **estrutural indireta**: extração dos carbonos-α de arquivos PDB locais.

| Sequência extraída | Arquivo de origem | Rótulo inferido de |
|---|---|---|
| `LALAY` | `.claude\analise-alosterica\data\LALAY.pdb` | nome do arquivo |
| `LALAY` | `Desktop\LEBPP\Paper-Daniel-Pablo\RE-Docking-1BTY-trypsin-GORE3\GORE3-PEPFOLD4.pdb` | **caminho contém "GORE3"** |
| `LALAK` | `Desktop\Spodoptera-GORE4\ACR157-GORE4_NEW\cluster1_1.pdb` | caminho contém "GORE4" |
| `LALAR` | `.claude\analise-alosterica\data\LALAR.pdb` | nome do arquivo |

A extração da sequência a partir dos PDB é confiável — são os resíduos reais dos modelos. **O que não é confiável é o mapeamento nome → sequência**, que se apoia apenas em nomes de pasta.

### Por que isso é problemático

A publicação mais recente do grupo (Paulo et al., 2026 — PMID 41510779), cujo primeiro autor é **Daniel Guimarães Silva Paulo** — o mesmo "Daniel" da pasta local `Paper-Daniel-Pablo` — nomeia quatro pentapeptídeos:

`TGPCK` · `TGPCR` · `AVIMK` · `AVIMR`

**`LALAY` não está entre eles.**

Três explicações possíveis, e não há como escolher entre elas a partir dos arquivos:

1. GORE3 é uma molécula distinta das quatro publicadas
2. A nomenclatura interna mudou entre o trabalho e a publicação
3. Os arquivos `LALAY` pertencem a outra linha de trabalho (possivelmente a investigação do sítio S'2)

### Observação adicional

Há uma inconsistência de escala na série:

- GORE-2 é descrito como **tripeptídeo** (dos Santos et al., 2025)
- GORE 1-2 T é construído de **tripeptídeos VLR/VLK** (75 aa com linkers)
- `SUBMISSAO_NCBI.md` (linha 113) registra **"VLA (código interno) = GORE2"** — um tripeptídeo, consistente
- `LALAY`, `LALAK`, `LALAR` são **pentapeptídeos**
- Os peptídeos de Paulo et al. (2026) também são **pentapeptídeos**

Ou seja, a série migrou de tri- para pentapeptídeos em algum momento. Isso torna plausível que `LALAY` seja de fato GORE3 — mas plausível não é confirmado.

### ⚠️ Ação requerida

**Confirmar com a Profa. Maria Goreti ou com Daniel Paulo, antes de qualquer modelagem:**

1. Qual a sequência exata do GORE3?
2. Qual a correspondência nome ↔ sequência de toda a série (GORE1 a GORE13)?
3. `LALAY`/`LALAK` correspondem a quais moléculas?

**Fontes locais ainda não abertas que podem conter a resposta:**
- `Desktop\LEBPP\Pós-doc-eulalio\Lab-meeting-GORE3.pptx`
- `Desktop\LEBPP\Pós-doc-eulalio\GORE3-GORE4-GORE5....jpeg` (imagem — pode conter tabela da série)
- `Desktop\LEBPP\GORE4-ate-GORE13\` (pasta dedicada à série)
- `Desktop\LEBPP\Paper-Daniel-Pablo\DOCKING RESULTS.docx`

---

## 2. Dados de fonte interna, não publicada

Os dados abaixo vêm de `GORE3-abstract.docx` e `Abstract-projeto-eulalio.docx` — documentos do grupo, **não revisados por pares**. Estão usados na base teórica com marcação ⚠️ e devem ser tratados como preliminares.

| Afirmação | Situação |
|---|---|
| GORE3 tem IC₅₀ "na faixa micromolar" | ⚠️ Valor não quantificado. Vago demais para publicação — obter o número |
| Superexpressão de proteases em *S. frugiperda* sob GORE3 | ⚠️ Não publicado |
| Redução de atividade proteolítica em *A. gemmatalis* sob GORE3 | ⚠️ Não publicado — **é o achado central do projeto** |
| Aumento de SOD, CAT, POX, GST | ⚠️ Não publicado |
| Atraso de desenvolvimento "de até 50 dias" | ⚠️ Não publicado; sem indicação de condição experimental |
| Larvas de 3º ínstar entre 0,348 g e 0,367 g | ⚠️ Não publicado |
| Ciclo de vida de 34,90 dias (machos) / 35,60 (fêmeas) | ⚠️ Citado sem fonte no documento original |
| "Mercado que cresce mais de 15% ao ano" (§19 do projeto) | ⚠️ Baseado em referência não verificada |

**Recomendação:** ao escrever a introdução, dados não publicados devem ser apresentados como "resultados preliminares do grupo (dados não publicados)" — nunca como fato estabelecido com citação.

---

## 3. Referências do projeto original ainda não verificadas

O projeto lista ~60 referências. Nesta auditoria foram verificadas **18** (as que constam de `referencias.bib`). As demais **não** foram conferidas.

### Prioritárias para verificar (citadas em pontos centrais do argumento)

| Referência | Por que importa | Situação |
|---|---|---|
| ~~Coura et al. (2022), *Ann Appl Biol*~~ | Reprogramação de isoformas + histopatologia | ✅ **Verificada via Crossref** — 180(3):383-397, doi:10.1111/aab.12740. Já no `.bib` |
| ~~Silva-Júnior et al. (2021), *Arch Insect Biochem Physiol*~~ | Perfil de proteases e ligação a inibidores | ✅ **Verificada via Crossref** — 107(3), doi:10.1002/arch.21792. Já no `.bib` |
| Saikhedkar et al. (2018) | Origem conceitual dos tripeptídeos de RCL | ⬜ conferir |
| Meriño-Cabrera et al. (2018, 2019) | Cinética de inibição | ⬜ conferir |
| Laskowski & Kato (1980); Laskowski & Qasim (2000) | Base do modelo mecanístico | ⬜ conferir |

### Problemas específicos detectados

- **"Berliner, 1911"** — citado no texto (§19) mas **sem entrada correspondente na lista de referências**
- **"Barros et al., 2022"** — ambíguo; há vários trabalhos de Barros, e a lista não permite desambiguar
- **"FREIRES (2022)"** — sem tipo de obra, instituição ou veículo
- **Duas referências são links de notícia** (`agrourbano.com.br`, `cnabrasil.org.br`) usados para sustentar dados econômicos — ver [`06_correcoes_projeto.md`](06_correcoes_projeto.md) C13
- **"Greene (1976)"** — protocolo de criação; conferir dados completos
- **"Cepas et al., 2016, 2017"** (eggNOG) — a grafia correta do sobrenome é provavelmente **Huerta-Cepas**

**Nenhuma dessas foi incluída em `referencias.bib`.** Só entram após verificação.

---

## 4. O que foi verificado e como

| Item | Método | Resultado |
|---|---|---|
| 16 referências do `.bib` | NCBI E-utilities (`esummary.fcgi`), consulta direta por PMID | ✅ DOI, volume, páginas e ano confirmados na fonte |
| Coura et al. (2022), Silva-Júnior et al. (2021) | API Crossref, consulta por DOI | ✅ Título, autoria, volume e páginas confirmados |
| dos Santos et al. (2025) | `WebFetch` da página do artigo em eje.cz | ✅ DOI `10.14411/eje.2025.015`, vol. 122, pp. 119-136, autoria e resumo confirmados |
| Genoma `GCF_050436995.1` | Busca web → páginas NCBI Datasets e relatório de anotação | ✅ Assembly e anotação RS_2025_08 existem |
| Caminhos de arquivos locais | Teste de existência no sistema de arquivos | ✅ Todos os 8 caminhos principais de `04_viabilidade.md` confirmados |
| Conteúdo do projeto | Extração via `python-docx`, 109 parágrafos lidos integralmente | ✅ |
| Sequências de peptídeos | Extração de carbonos-α de arquivos PDB | ⚠️ Sequências reais, mapeamento de nomes **não** confirmado |

---

## 5. O que NÃO foi verificado

Declarado para que ninguém assuma cobertura que não existe:

1. **Métricas do genoma** — N50, tamanho, nível de montagem, BUSCO de `GCF_050436995.1`. Nenhum número foi reproduzido nesta base teórica justamente por isso. **Conferir na página do assembly antes de escrever a metodologia.**
2. **Campo de força usado no MD de GORE 1-2 T** — o resumo de de Andrade et al. (2026) menciona 100 ns de MD mas não especifica o campo de força. Essa informação é necessária para a decisão CHARMM36m × AMBER ([`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §7). **Requer leitura do texto completo.**
3. **Conteúdo dos arquivos HADDOCK** (`.tgz`) — confirmada apenas a existência, não os resultados
4. **Valores da cotação Macrogen** — não abertos, não reproduzidos
5. **~42 referências** do projeto original (ver §3)
6. **Dados de *S. frugiperda*** — fora do escopo definido; não auditados
7. **Se o experimento GORE3 já foi coletado** — só se sabe que o sequenciamento está contratado

---

## 6. Decisões editoriais tomadas nesta base

Para transparência sobre escolhas que afetam o texto:

1. **Não foi reproduzido nenhum número sem fonte verificada.** Onde o dado existia mas a fonte não pôde ser confirmada, marcou-se ⚠️.
2. **Família taxonômica:** registrada a divergência Noctuidae/Erebidae em vez de escolher silenciosamente uma delas.
3. **Kᵢ e IC₅₀ não foram comparados diretamente** na tabela de progressão da série — são parâmetros diferentes, com ressalva explícita.
4. **Não foi afirmado que "GORE3 é melhor que GORE1/GORE2"** como fato. Está apresentado como alegação de fonte interna a ser testada.
5. **Não foi inventado nenhum valor de versão de software.** O documento de metodologia orienta conferir versões na instalação.

---

## 7. Próximas ações de verificação

Em ordem de prioridade:

| # | Ação | Bloqueia |
|---|---|---|
| 1 | Confirmar sequência do GORE3 com a supervisora | Toda a modelagem estrutural |
| 2 | Obter IC₅₀/Kᵢ quantificado do GORE3 | Escrita da introdução |
| 3 | Ler texto completo de de Andrade et al. (2026) para o campo de força | Decisão de MD |
| 4 | Conferir métricas do assembly `GCF_050436995.1` | Escrita da metodologia |
| 5 | Verificar as ~44 referências restantes | Submissão |
| 6 | Confirmar status do sequenciamento na Macrogen | Cronograma |
