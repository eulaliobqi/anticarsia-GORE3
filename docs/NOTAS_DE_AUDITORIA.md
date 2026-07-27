# Notas de auditoria

Registro do que foi verificado, como, e — sobretudo — **o que não pôde ser confirmado**.

Este arquivo existe para que nada nesta base teórica seja tomado como fato sem rastro. Onde faltou evidência, está declarado como lacuna em vez de preenchido por inferência.

**Data da auditoria:** 18/07/2026

---

## 1. ✅ RESOLVIDO — sequência do GORE3

> **GORE3 = `LALAY`** (Leu-Ala-Leu-Ala-Tyr), pentapeptídeo.
> **Confirmado pelo pesquisador (Eulálio) em 18/07/2026.**

A confirmação bate com a evidência estrutural independente extraída dos arquivos PDB locais (abaixo), o que fecha a questão para efeito de modelagem.

**Fica em aberto, e não é bloqueante:** `LALAY` não consta dos peptídeos nomeados em Paulo et al. (2026) — `TGPCK`, `TGPCR`, `AVIMK`, `AVIMR`. Isso indica que o GORE3 pertence a uma linha de trabalho distinta daquela publicação, provavelmente ainda não publicada. Vale confirmar antes de escrever a introdução, porque muda como o GORE3 é posicionado em relação à literatura do grupo.

**Continua pendente:** a correspondência nome ↔ sequência do restante da série (GORE1, GORE2, GORE5–GORE13). Ver §1.1.

### 1.1 Consequência estrutural — atenção antes do docking

`LALAY` **não possui nenhum resíduo básico** (sem Lys, Arg ou His).

Isso importa: o bolsão de especificidade **S1** da tripsina tem o **Asp189** no fundo, e é ele que ancora cadeias laterais de Lys/Arg por ponte salina. É essa a razão de os pentapeptídeos de Paulo et al. (2026) terminarem em K ou R — eles reproduzem o P1 canônico de um substrato de tripsina.

O GORE3 não pode formar essa interação. Se a cinética indica inibição competitiva (documento interno ⚠️), então uma de duas coisas:

- **(a)** ocupa a fenda catalítica por **outros subsítios** (S2/S3), via contatos hidrofóbicos — plausível, dados os dois resíduos de Leu e a Tyr aromática
- **(b)** liga-se a um **sítio distinto**, e o efeito competitivo é indireto

Isso dá sustentação concreta à investigação do sítio **S'2** conduzida na linha `analise-alosterica` — e reforça a recomendação de [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §5 de **testar S1 e S'2 explicitamente**, em vez de posicionar a caixa de docking sobre o sítio catalítico por pressuposição, como o `.docx` propõe.

Um docking cego (*blind docking*) sobre a superfície inteira da enzima, antes do docking dirigido, passa a ser recomendável neste caso específico.

### O que havia sido encontrado nos arquivos (evidência independente)

Nenhum documento localizado declara textualmente a sequência de aminoácidos do GORE3. O que existe é evidência **estrutural indireta**: extração dos carbonos-α de arquivos PDB locais.

| Sequência extraída | Arquivo de origem | Rótulo inferido de |
|---|---|---|
| `LALAY` | `.claude\analise-alosterica\data\LALAY.pdb` | nome do arquivo |
| `LALAY` | `Desktop\LEBPP\Paper-Daniel-Pablo\RE-Docking-1BTY-trypsin-GORE3\GORE3-PEPFOLD4.pdb` | **caminho contém "GORE3"** |
| `LALAK` | `Desktop\Spodoptera-GORE4\ACR157-GORE4_NEW\cluster1_1.pdb` | caminho contém "GORE4" |
| `LALAR` | `.claude\analise-alosterica\data\LALAR.pdb` | nome do arquivo |

A extração da sequência a partir dos PDB é confiável — são os resíduos reais dos modelos. **O que não é confiável é o mapeamento nome → sequência**, que se apoia apenas em nomes de pasta.

### Observação adicional

Há uma inconsistência de escala na série:

- GORE-2 é descrito como **tripeptídeo** (dos Santos et al., 2025)
- GORE 1-2 T é construído de **tripeptídeos VLR/VLK** (75 aa com linkers)
- `SUBMISSAO_NCBI.md` (linha 113) registra **"VLA (código interno) = GORE2"** — um tripeptídeo, consistente
- `LALAY`, `LALAK`, `LALAR` são **pentapeptídeos**
- Os peptídeos de Paulo et al. (2026) também são **pentapeptídeos**

Ou seja, a série migrou de tri- para pentapeptídeos em algum momento — o que é consistente com GORE3 = `LALAY` (5 resíduos), agora confirmado.

### Ação ainda requerida (não bloqueante)

1. ✅ ~~Sequência do GORE3~~ — confirmada: `LALAY`
2. ⬜ Correspondência nome ↔ sequência do restante da série (GORE1, GORE2, GORE5–GORE13)
3. ⬜ `LALAK` corresponde a GORE4? (evidência local aponta nessa direção)
4. ⬜ O GORE3 já foi publicado em algum trabalho, ou é inédito?

**Fontes locais ainda não abertas que podem conter as respostas:**
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

> **Atualizado em 27/07/2026** pelo levantamento bibliográfico. Auditoria
> completa em [`../literatura/05_AUDITORIA_REFS_DOCX.md`](../literatura/05_AUDITORIA_REFS_DOCX.md).

**Correção da contagem registrada aqui antes.** A extração via `python-docx`
mostrou que o `.docx` **não tem lista de referências ao final** — nenhum
cabeçalho "REFERÊNCIAS"/"BIBLIOGRAFIA" nos 109 parágrafos, e apenas **7**
entradas bibliográficas formais dispersas no corpo. Já as citações no corpo
somam **72 distintas**. Portanto o número correto é 72 citadas × 7 listadas, e
não "~60 referências". A ausência de lista de referências é, por si, uma
pendência de submissão que não estava registrada.

`referencias.bib` passou de 17 para **131 entradas verificadas** (DOI ou PMID
resolvido). Das 72 citações do `.docx`, **23 receberam veredito**; 49 seguem
sem verificação.

### Prioritárias — situação após 27/07/2026

| Referência | Por que importa | Situação |
|---|---|---|
| ~~Coura et al. (2022), *Ann Appl Biol*~~ | Reprogramação de isoformas + histopatologia | ✅ Verificada via Crossref — 180(3):383-397, doi:10.1111/aab.12740 |
| ~~Silva-Júnior et al. (2021), *Arch Insect Biochem Physiol*~~ | Perfil de proteases e ligação a inibidores | ✅ Verificada; **PMID 33948994** acrescentado ao `.bib` |
| ~~Saikhedkar et al. (2018)~~ | Origem conceitual dos tripeptídeos de RCL | ✅ **PMID 29486250** — tripeptídeos de RCL de inibidores Pin-II vs. *H. armigera* |
| ~~Laskowski & Kato (1980)~~ | Base do modelo mecanístico | ✅ **PMID 6996568**, *Annu Rev Biochem* |
| ~~Laskowski & Qasim (2000)~~ | Base do modelo mecanístico | ✅ **PMID 10708867** — citado no `.docx` como "Jr e Qasim 2000" |
| ~~Barros et al. (2022)~~ | Era a referência ambígua | ✅ **PMID 36127063** — BPTI × SKTI em *A. gemmatalis* |
| **Meriño-Cabrera et al. (2018, 2019)** | Cinética de inibição | ❌ **Não localizada.** Busca dirigida por autor (`Merino-Cabrera[au]`, 15 resultados) não retornou publicação de 2018. Vizinhos: 2017 (PMID 28925864) e 2020 (PMID 32342573, 32360954) |

### Achado que altera o argumento

O `.docx` cita **"Jogsma et al. 2011"**. É **Jongsma et al. 1995**, PNAS,
PMID 7644535 — *"Adaptation of Spodoptera exigua larvae to plant proteinase
inhibitors by induction of gut proteinase activity insensitive to
inhibition"*. Grafia e ano errados no clássico fundacional do mecanismo de
escape por protease insensível, que é exatamente o mecanismo que a hipótese
**H1** testa. Já incorporado ao `.bib` como `jongsma1995adaptation`.

### Problemas específicos — situação

- **"Berliner, 1911"**, **"Greene (1976)"**, **"Shukla et al. (2024)"** — não
  localizadas. Ressalva: a busca foi incidental, não dirigida; não é possível
  afirmar que não existem.
- **"FREIRES (2022)"** — sem tipo de obra, instituição ou veículo. Não verificada.
- **"Cepas et al., 2016, 2017"** — a suspeita de **Huerta-Cepas** permanece
  plausível, mas plausibilidade não é verificação. Segue não confirmada.
- **"Srinivasan et al. 2006"** — a busca retornou PMID 16140320, mas de
  **2005**. Ambíguo; não decidível sem o usuário.
- **Duas referências são links de notícia** (`agrourbano.com.br`,
  `cnabrasil.org.br`) — ver [`06_correcoes_projeto.md`](06_correcoes_projeto.md) C13.
  **Substitutos com fonte primária já disponíveis**: PMID 36520803 (dano por
  lepidópteros na soja na América do Sul), PMID 30071611 (desfolha em soja
  Cry1Ac) e PMID 34545402 (praga × desfolha × NDVI).

**Nada entra em `referencias.bib` sem verificação.** As não confirmadas
permanecem no bloco comentado do arquivo, com o motivo.

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
5. **49 das 72 citações** do projeto original seguem sem veredito (ver §3 e
   [`../literatura/05_AUDITORIA_REFS_DOCX.md`](../literatura/05_AUDITORIA_REFS_DOCX.md)).
   Inclui as 17 citações de ferramentas que o padrão-ouro recomenda substituir
   (FastQC, Trimmomatic, Kallisto, Bowtie2, Blast2GO, KOBAS…), deixadas fora
   por decisão explícita de escopo.
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
| ~~2~~ | ~~Obter IC₅₀/Kᵢ quantificado do GORE3~~ | ✅ **Publicado**: IC₅₀ = 433,98 µM e Kᵢ = 4,00 mM (competitivo), Paulo et al. 2026 — mas em *S. frugiperda*. Para *A. gemmatalis* segue pendente |
| 3 | Ler texto completo de de Andrade et al. (2026) para o campo de força | Decisão de MD |
| 4 | Conferir métricas do assembly `GCF_050436995.1` | Escrita da metodologia |
| 5 | Verificar as 49 citações restantes do `.docx` | Submissão |
| 5b | **Montar a lista de referências do `.docx`** — ela não existe | Submissão |
| 6 | Confirmar status do sequenciamento na Macrogen | Cronograma |
| 7 | Fichar os artigos Tier 1 marcados `⚠️ PENDENTE DE FICHAMENTO` em `literatura/0[1-4]_*.md` | Escrita da introdução |

**Item novo, aberto em 27/07/2026 (ver §8).** O texto completo de Paulo et al.
(2026), PMID 41572648, descreve o modo de ligação do GORE3 como
**S1/S1′**, não S′2. Isso muda o enunciado da hipótese H6 e precisa ser
reconciliado com [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) antes
de escrever a metodologia de docking.

---

## 8. Modo de ligação do GORE3: o que a publicação diz

Registrado em 27/07/2026, ao recuperar o texto completo de **PMID 41572648**
(Paulo et al., *Pest Manag Sci* 82(5):4632-4647, doi:10.1002/ps.70579), que é
acesso aberto (PMC13071266).

O abstract afirma, textualmente, que o docking prevê para o GORE 3 em tripsinas
de *S. frugiperda* uma pose conservada entre isoformas com **"occupancy of
S1/S1′ and adjacent subsites and richer aromatic/hydrophobic contacts than the
S1-focused reference benzamidine"**, e reporta inibição competitiva com
**K = 4,00 mM** (GORE3) contra **1,64 mM** (benzamidina), mortalidade larval de
até **46,66%**.

Conferido no corpo do artigo (não só no abstract): *"a well-defined network of
hydrogen bonds with polar residues lining the S1/S1′ pocket is accompanied by
numerous hydrophobic contacts — alkyl, π–alkyl, and amide–π/π–π stacking —
distributed along the groove walls"*.

**As isoformas modeladas são nomeadas:** `XP_050552352.1`, `ACR25157.1`,
`QLC28936.1` e `XP_050550273.1`. Três delas correspondem aos arquivos já
protonados em pH 8,2 disponíveis localmente
(`analise-alosterica/data/protonated/ACR157-*`, `QCL936-*`, `XP273-*`) —
ou seja, o ativo local é reaproveitável para reproduzir e estender este
docking, com a ressalva de que são tripsinas de *S. frugiperda*.

**Por que isso importa aqui.** A base teórica registra o modo de ligação como
pergunta em aberto entre **S1** e **S′2**, e a hipótese H6 propõe modo não
canônico. A publicação não sustenta S′2: sustenta S1/S1′. São coisas
diferentes — S1′ é o primeiro subsítio do lado *prime*, adjacente à ligação
cindível; S′2 é outro. Três ressalvas antes de reescrever qualquer coisa:

1. O trabalho é em ***S. frugiperda***, não *A. gemmatalis* — que é o escopo
   definido deste projeto.
2. É **docking**, não estrutura experimental, e sem MD de validação.
3. Não elimina a pergunta de fundo: `LALAY` continua sem resíduo básico para
   a ponte salina com Asp189, e o próprio artigo descreve os contatos como
   aromáticos/hidrofóbicos.

Ou seja: a hipótese H6 **não** foi refutada, mas o enunciado "S1 × S′2" está
desatualizado em relação à literatura publicada e precisa ser reescrito como
"S1/S1′ × sítio alternativo", com o teste de *blind docking* mantido.

### 8.1 Duas inconsistências internas no artigo — não citar sem sinalizar

Detectadas ao ler o texto completo em 27/07/2026.

**(a) O Kᵢ da benzamidina não fecha.** O abstract dá **1,64 mM**; a seção de
resultados dá **16,49 µM**. São cem vezes de diferença, sem nota de
reconciliação no artigo. O valor do GORE3 (4,00 mM) é o mesmo nos dois lugares.
Note que 16,70 µM é também o valor que Schultz et al. (2026, PMID 41849700)
reportam para benzamidina na mesma espécie — o que sugere que o número do
abstract é que está errado, mas isso é inferência, não verificação.

**(b) A mortalidade não é monotônica com a dose.** Cerca de 47% a 0,00241% e a
0,04873% (m/v), mas apenas **6,7% e 26%** nas concentrações maiores 0,1216% e
0,2432%. A mesma frase ainda reporta *"resulting in a mortality percentage of
0.000067%"*, repetindo a concentração no lugar da mortalidade.

**Consequência prática:** o valor "mortalidade de até 46,66%" já registrado na
base teórica a partir do abstract continua correto como citação, mas **não pode
ser apresentado como resposta dose-dependente**. E o Kᵢ da benzamidina não deve
ser citado a partir deste artigo sem escolher uma das duas versões e declarar a
escolha.

---

## 9. Impacto na duração planejada da dinâmica molecular

Aberto em 27/07/2026 a partir de Kahler et al. (2018), PMID 29210603,
*J Biomol Struct Dyn* 36(15):4072-4084.

Simulação de MD de **10 µs** de um complexo peptidase-relacionada-a-calicreína
7 com peptídeo. Depois de **mais de 2 µs** de amostragem irrestrita, o peptídeo
sofre transição espontânea de modo de ligação, com rotação de 180° em torno do
resíduo P1, passando a ocupar a região do **lado prime** de forma estável.

**Por que isso é um problema para este projeto.** A metodologia prevê
**3 × 100 ns** ([`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md)
§11). Isso é vinte vezes menos do que o tempo em que o evento apareceu naquele
sistema. Se o GORE3 tiver comportamento análogo — e a hipótese H6 é exatamente
a de que o modo de ligação não é o canônico —, **uma janela de 100 ns não
detectaria a transição**, e o resultado seria interpretado como "complexo
estável no modo docado" por falta de amostragem, não por estabilidade real.

Ressalva de transferência: é calicreína humana, não tripsina digestiva de
inseto, e um único sistema.

**Não é recomendação de rodar 10 µs.** É motivo para (i) declarar
explicitamente a limitação de amostragem ao interpretar a MD, e (ii) avaliar se
alguma estratégia de amostragem melhorada cabe no orçamento de GPU antes de
tratar 3 × 100 ns como suficiente para testar H6.
