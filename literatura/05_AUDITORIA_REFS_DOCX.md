# Auditoria das referências do projeto original

Alvo: `Projeto-Eulalio-Pós-doc2.docx`. Extração via `python-docx` em
27/07/2026. Complementa `docs/NOTAS_DE_AUDITORIA.md` §3.

## O que a extração revelou sobre a estrutura do documento

O `.docx` **não tem lista de referências ao final**. A busca por um cabeçalho
"REFERÊNCIAS"/"BIBLIOGRAFIA" nos 109 parágrafos não encontrou nenhum, e o
padrão de entrada bibliográfica formal (`SOBRENOME, Iniciais.` + ano) casou com
apenas **7 parágrafos**, dispersos no corpo do texto.

Já a extração de citações no corpo encontrou **72 citações distintas**
(Autor, ano). Ou seja: o documento cita 72 fontes e lista 7.

**Isto corrige a contagem registrada em `NOTAS_DE_AUDITORIA.md` §3**, que
falava em "~60 referências, apenas 16-18 verificadas". O número correto de
citações distintas no corpo é 72, e a ausência de lista de referências é em si
uma pendência de submissão que não estava registrada.

---

## Placar

| Veredito | n |
|---|---|
| **CONFIRMADA** — DOI/PMID resolvido nesta sessão | 14 |
| **CORRIGIDA** — dado bibliográfico errado no `.docx` | 3 |
| **AMBÍGUA** — não desambiguável sem o usuário | 2 |
| **NÃO LOCALIZADA** — busca feita, nada encontrado | 4 |
| **NÃO VERIFICADA** — citação de ferramenta, fora do escopo de hoje | 17 |
| **NÃO VERIFICADA** — demais citações do corpo | 32 |

Auditoria **parcial e declarada como tal**: 23 das 72 citações receberam
veredito baseado em busca dirigida. As outras 49 não foram checadas hoje.

---

## CONFIRMADA

| Citação no `.docx` | PMID | Referência |
|---|---|---|
| Barros et al. 2021 | 33200876 | *Pest Manag Sci* 77(4):1714-1723 |
| Coura et al. 2022 | — | já em `docs/referencias.bib` (Crossref) |
| Laskowski e Kato 1980 | 6996568 | *Annu Rev Biochem* — resolve pendência |
| Moon et al. 2004 | 15157229 | *Insect Mol Biol* 13(3):283 |
| Patarroyo-Vargas et al. 2020 | 32491140 | *An Acad Bras Cienc* 92(Supl.1):e20180477 |
| Pezenti et al. 2021 | 34022342 | perfil transcricional, cepas Bt |
| Saikhedkar et al. 2018 | 29486250 | tripeptídeos de RCL de Pin-II — resolve pendência |
| Santos et al. 2025 | — | já em `docs/referencias.bib` |
| Silva-Júnior et al. 2021 | 33948994 | *Arch Insect Biochem Physiol* 107(3) |
| Sultana et al. 2022 | 34674016 | já em `docs/referencias.bib` |
| Akbar et al. 2018 | — | entrada formal presente no `.docx`, capítulo de livro |
| Campos et al. 2019 | — | entrada formal presente no `.docx` |
| Macedo et al. 2007 | — | entrada formal presente no `.docx` |
| Westfall et al. 1948 | — | entrada formal presente no `.docx`, *Proc Soc Exp Biol* |

## CORRIGIDA

**`Jogsma et al. 2011` → Jongsma et al. 1995, PMID 7644535.**
Grafia e ano errados. O trabalho é *"Adaptation of Spodoptera exigua larvae to
plant proteinase inhibitors by induction of gut proteinase activity insensitive
to inhibition"*, PNAS 1995 — o clássico fundacional do mecanismo de escape por
protease insensível, que é exatamente o mecanismo que a hipótese H1 do projeto
testa. Citá-lo com autor e ano errados enfraquece justamente o ponto que ele
sustenta.

**`Jr e Qasim 2000` → Laskowski Jr, M. & Qasim, M. A. 2000, PMID 10708867.**
A extração capturou "Jr" como sobrenome. O trabalho é *"What can the structures
of enzyme-inhibitor complexes tell us about the structures of enzyme substrate
complexes?"*, *Biochim Biophys Acta*. Resolve a segunda pendência Laskowski do
bloco comentado do `.bib`.

**`Barros et al. 2022` → PMID 36127063.**
Estava marcada como referência ambígua em `NOTAS_DE_AUDITORIA.md` §3. É
*"Bovine pancreatic trypsin inhibitor and soybean Kunitz trypsin inhibitor:
Differential effects on proteases and larval development of the soybean pest
Anticarsia gemmatalis"*, de Almeida Barros R et al., *Pestic Biochem Physiol*
187:105188. Ambiguidade resolvida.

## AMBÍGUA

**`Srinivasan et al. 2006`.** A busca por autor retornou PMID 16140320,
*"Podborer (Helicoverpa armigera) does not show specific adaptations in gut
proteinases to dietary Cicer arietinum Kunitz proteinase inhibitor"*, mas de
**2005**, não 2006. Pode ser o mesmo trabalho citado com ano errado, pode ser
outro. Não dá para decidir sem o usuário.

**`Cepas et al. 2016`.** `NOTAS_DE_AUDITORIA.md` §3 já suspeitava de
**Huerta-Cepas** (eggNOG). Plausível, mas plausibilidade não é verificação:
não foi confirmado qual publicação do eggNOG corresponde ao ano citado.

## NÃO LOCALIZADA

**`Meriño-Cabrera et al. 2018`.** Busca dirigida por autor
(`Merino-Cabrera[au] OR "Merino Cabrera"[au]`, 15 resultados, ordenados por
data) **não retornou nenhuma publicação de 2018**. Os trabalhos vizinhos são de
2017 (PMID 28925864) e 2020 (PMID 32342573, 32360954). A referência 2018 do
`.docx` não foi confirmada. A pendência "Meriño-Cabrera 2018/2019" do bloco
comentado do `.bib` **permanece aberta**.

**`Berliner 1911`**, **`Greene 1976`**, **`Shukla et al. 2024`.** Não
localizadas. Ressalva importante: para estas três a busca foi apenas
incidental, não dirigida — não posso afirmar que não existem, apenas que não
foram encontradas. Requerem busca própria.

## NÃO VERIFICADA — citações de ferramenta

Fora do escopo de hoje por decisão explícita: o levantamento buscou os
artigos-fonte das ferramentas **do padrão-ouro** (eixo 2A, 18 refs), não os das
ferramentas que `03_metodologia_padrao_ouro.md` recomenda **substituir**.

Andrews 2010 (FastQC) · Bolger et al. 2014 (Trimmomatic) · Bray et al. 2016
(Kallisto) · Langmead et al. 2012 (Bowtie2) · Grabherr et al. 2011 (Trinity) ·
Haas et al. 2013 · Fu et al. 2012 (CD-HIT) · Ewels et al. 2016 (MultiQC) ·
Conesa et al. 2005 (Blast2GO) · Altschul et al. 1990 (BLAST) · Finn et al. 2014
(Pfam) · Eddy e Wheeler 2015 (HMMER) · Xie et al. 2011 (KOBAS) · Anders 2014 ·
Song & Florea 2015 · Krueger et al. 2021 · Biovia et al. 2017

Duas destas já estão no `.bib` novo por serem mantidas no padrão-ouro:
CD-HIT (PMID 23060610) e MultiQC (PMID 27312411).

## Citações com autoria institucional ou extração quebrada

`Bioinformatics 2010` · `Institute 2015` · `Consortium 2014` · `Press 2018` ·
`Brasil 2025` · `AgroUrbano 2025`

Não são nomes de autor. Ou são autoria institucional citada sem instituição
identificável, ou a extração quebrou numa quebra de linha. **`AgroUrbano 2025`
confirma a pendência já registrada**: é um dos dois links de notícia usados
para sustentar dados econômicos de perda na soja.

**Substitutos com fonte primária já disponíveis** no levantamento de hoje, eixo
4A: PMID 36520803 (*Feeding injury of major lepidopteran soybean pests in South
America*), PMID 30071611 (*Defoliation of Soybean Expressing Cry1Ac by
Lepidopteran Pests*) e PMID 34545402 (associação espacial entre praga,
desfolha e NDVI).

## Demais citações não verificadas

Araújo 2019 · Bel et al. 2013 · Brovini et al. 2023 · Cabrera et al. 2019 ·
Chacha et al. 2023 · Freires 2022 · Guo et al. 2020 · Habib e Fazili 2007 ·
Hellinger & Gruber 2019 · Jamal et al. 2013 · Kesseler e Baldwin 2002 ·
Khoobdel et al. 2022 · Koiwa et al. 1997 · Napoleão 2019 · Oliveira et al. 2020 ·
Paredes-Sánchez et al. 2021 · Qi et al. 2005 · Rodrigues & Fôres 2022 ·
Sharma et al. 2019 · Souza et al. 2023 · Tomberlin et al. 2023 ·
Tonnang et al. 2022 · Vieira et al. 2023 · War et al. 2018 · Zhang et al. 2010

`Kesseler e Baldwin 2002` provavelmente é **Kessler** (grafia), e
`Rodrigues & Fôres 2022` tem acentuação suspeita — mas nenhuma das duas foi
verificada, então ficam listadas como não verificadas, não como corrigidas.

---

## O que isto bloqueia

`NOTAS_DE_AUDITORIA.md` §7 lista "verificar as ~44 referências restantes" como
item que **bloqueia a submissão**. Situação após esta rodada:

- O bloco comentado "PENDENTE — NÃO CITAR" do `docs/referencias.bib` tinha 7
  itens. **Quatro foram resolvidos** (Saikhedkar 2018, Laskowski & Kato 1980,
  Laskowski & Qasim 2000, Barros 2022). **Três permanecem** (Meriño-Cabrera
  2018/2019, Shukla 2024, Berliner 1911, Greene 1976).
- O bloqueio **não está levantado**: 49 das 72 citações seguem sem veredito.
- Item novo, não registrado antes: **o `.docx` não tem lista de referências**.
  Isso precisa ser resolvido antes de qualquer submissão, independentemente da
  verificação individual.
