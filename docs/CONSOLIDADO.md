# BASE TEÓRICA CONSOLIDADA — Pós-doc GORE3

*Documento único gerado a partir dos arquivos temáticos de `docs/`. Para edição, altere os arquivos individuais e regenere este consolidado — não edite aqui diretamente.*

*Gerado em 18/07/2026. Referências completas em `referencias.bib`.*


---


<a id="parte-1"></a>

## Base teórica — Pós-doc GORE3

Fundamentação para o projeto *"Resposta transcriptômica e interação estrutural do inibidor peptídico GORE3 em lagartas-praga de culturas agrícolas"* (UFV / INCT-IPP, supervisão Profa. Maria Goreti de Almeida Oliveira).

Material de apoio para a escrita da introdução e para o ajuste da metodologia antes do início das análises.

**Escopo definido:** *Anticarsia gemmatalis* por enquanto. RNA-Seq em sequenciamento na Macrogen.

---

### Arquivos

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

### Sumário executivo

**O projeto é viável**, com três ressalvas que exigem decisão antes de começar.

#### 1. O genoma de referência mudou o jogo

*A. gemmatalis* passou a ter genoma RefSeq — **`GCF_050436995.1`** (ilAntGemm2), com anotação NCBI. O projeto foi redigido em Set/2025 assumindo montagem *de novo* com Trinity, o que hoje é subótimo. Migrar para pipeline **genoma-guiado** melhora quantificação, viabiliza análise de splicing alternativo com métodos estabelecidos e resolve a atribuição de isoformas de tripsina — que é justamente a pergunta central do projeto.

Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md).

#### 2. Há muito ativo local reaproveitável

Pipelines Nextflow maduros, setups GROMACS validados, estruturas de tripsina já modeladas e protonadas em pH intestinal, e docking do GORE3 já produzido (Vina + HADDOCK). O projeto não contabiliza nada disso. O trabalho real é menor do que o documento sugere.

Ver [`04_viabilidade.md`](04_viabilidade.md).

#### 3. GORE3 = `LALAY` — e isso muda o desenho do docking

**Confirmado em 18/07/2026:** GORE3 é o pentapeptídeo **`LALAY`** (Leu-Ala-Leu-Ala-Tyr).

A consequência é técnica e importante: `LALAY` **não tem nenhum resíduo básico**. O subsítio S1 da tripsina é ancorado no **Asp189**, que liga cadeias laterais de Lys/Arg — razão pela qual os demais peptídeos publicados da série terminam em K ou R. O GORE3 não faz essa ponte salina.

Portanto o modo de ligação do GORE3 é **pergunta em aberto, não premissa**. A metodologia do `.docx`, que posiciona a caixa de docking sobre o sítio catalítico por pressuposição, precisa ser revista para testar S1 e S'2 explicitamente — e um *blind docking* prévio passa a ser recomendável.

Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) §1.1 e [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) §5.

---

### O achado que dá originalidade ao projeto

O resumo do próprio projeto (`GORE3-abstract.docx`) registra que o GORE3 produz **respostas opostas nas duas espécies**: superexpressão de proteases em *S. frugiperda*, mas **redução** da atividade proteolítica em *A. gemmatalis*.

Isso não é ruído. É a diferença entre um inseto que consegue montar resposta compensatória e um que não consegue — e é exatamente o que a transcriptômica pode explicar. Nenhum trabalho do grupo abordou isso diretamente.

Ver [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md).

---

### Como usar na escrita da introdução

Ordem sugerida de leitura para montar o texto:

1. `01` §1 e §2 → contexto agronômico e o problema
2. `01` §3 a §5 → inibidores de protease como alternativa e como funcionam
3. `01` §6 → por que os inibidores falham (adaptação) — esta é a tensão que justifica o trabalho
4. `02` → o que o grupo já fez e o que ainda não sabe
5. `05` → a lacuna e a hipótese

Toda afirmação nos arquivos vem com citação. As que não têm fonte confirmada estão marcadas com ⚠️ e listadas em `NOTAS_DE_AUDITORIA.md`.

---

*Última atualização: 18/07/2026*



---


<a id="parte-2"></a>

## Fundamentação teórica

Base conceitual para a introdução. Cada afirmação traz a fonte; o que não pôde ser verificado está marcado ⚠️ e listado em [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md).

---

### 1. *Anticarsia gemmatalis* e o problema agronômico

A lagarta-da-soja, *Anticarsia gemmatalis* Hübner, é um dos principais desfolhadores da soja no Brasil. A literatura recente do próprio grupo a descreve consistentemente como "uma das mais importantes pragas desfolhadoras da soja" (Paulo et al., 2026; de Andrade et al., 2026).

Um ponto taxonômico que aparece de forma inconsistente na literatura e merece atenção na escrita: a espécie é atribuída ora a **Noctuidae**, ora a **Erebidae**. Ambas as grafias aparecem em publicações recentes revisadas por pares — Paulo et al. (2026) e dos Santos et al. (2025) usam Noctuidae; Pilon et al. (2018) e Pezenti et al. (2023) usam Erebidae. A classificação em Erebidae reflete a revisão filogenética mais moderna de Noctuoidea. **Recomendação:** adotar Erebidae e mencionar Noctuidae como sinonímia de uso corrente, ou simplesmente manter consistência interna no texto.

#### Controle atual e suas limitações

O manejo se apoia hoje em duas frentes principais:

- **Plantas Bt**, expressando toxinas Cry de *Bacillus thuringiensis*. A eficácia depende da ligação da toxina a receptores específicos no epitélio do intestino médio — aminopeptidases N (APN), fosfatase alcalina, caderina. Em *A. gemmatalis*, dez sequências de APN foram identificadas no transcriptoma e sete delas confirmadas experimentalmente como ligantes de Cry1Ac por *ligand blotting* e espectrometria de massas (Lanzaro et al., 2024). Mutações nesses receptores estão entre os mecanismos de resistência — o que torna o mapeamento desses alvos parte da estratégia de contenção.
- **Inseticidas químicos**, com os custos ambientais e de saúde conhecidos, e sob pressão crescente de resistência.

É esse duplo gargalo — resistência a Bt e passivo ambiental dos químicos — que sustenta a busca por moléculas alternativas.

---

### 2. Digestão proteica no intestino médio de Lepidoptera

O intestino médio de lepidópteros é um ambiente **alcalino**, condição que define quais enzimas operam ali e que precisa ser respeitada em qualquer modelagem estrutural. Tripsinas purificadas a partir de bactérias do intestino de *A. gemmatalis* mostraram-se ativas na faixa de **pH 7,5–10**, com atividade máxima a 40 °C e massa molecular de aproximadamente 25 kDa (Pilon et al., 2017).

> **Consequência prática para o projeto:** protonar as estruturas em pH alcalino antes do docking/MD, e não em pH 7,0. Os arquivos locais já protonados a pH 8,2 (ver [`04_viabilidade.md`](04_viabilidade.md)) estão corretos nesse aspecto.

As **serino-proteases do tipo tripsina** respondem pela digestão primária. Duas características importam para o trabalho:

1. **Multiplicidade de isoformas.** Pilon et al. (2017) concluíram pela existência de isoformas distintas de tripsina no intestino de *A. gemmatalis*, notando que as enzimas de origem bacteriana não dependiam de íons cálcio — ao contrário das tripsinas solúveis e insolúveis já caracterizadas na própria lagarta.
2. **Contribuição da microbiota.** Parte da atividade proteolítica intestinal vem de bactérias simbiontes — *Bacillus cereus*, *Enterococcus mundtii*, *E. gallinarum*, *Staphylococcus xylosus* foram isoladas e tiveram suas tripsinas purificadas (Pilon et al., 2017). Isso significa que o transcriptoma do hospedeiro não captura toda a capacidade proteolítica do sistema — uma limitação a declarar explicitamente.

#### Arquitetura do sítio ativo

A tríade catalítica canônica das serino-proteases — **His57, Asp102, Ser195** (numeração do quimotripsinogênio) — e o bolsão de especificidade **S1**, cujo **Asp189** no fundo determina a preferência da tripsina por resíduos básicos (Lys/Arg), são os elementos estruturais centrais. Paulo et al. (2026) identificaram exatamente esse conjunto — His57, Asp102, Ser195, Asp189 e Gly197 — como os resíduos críticos na ligação de peptídeos inibidores às tripsinas de *A. gemmatalis*.

Esse é o alvo estrutural do GORE3.

---

### 3. Inibidores de protease como estratégia de defesa

Inibidores de protease (IPs) são proteínas amplamente distribuídas em plantas, onde atuam como agentes antinutricionais contra herbívoros. Nas leguminosas, os IPs se acumulam de forma constitutiva em sementes e podem ser induzidos em folhas após dano (revisão: Sultana et al., 2022).

O efeito sobre o inseto é indireto mas eficaz: ao bloquear as proteases digestivas, o IP reduz a liberação de aminoácidos essenciais, o que se traduz em **atraso no desenvolvimento, deformidades e queda de fertilidade** (Sultana et al., 2022).

Os dois IPs de soja mais estudados nesse contexto:

- **SKTI** (*Soybean Kunitz Trypsin Inhibitor*) — inibidor tipo Kunitz, alvo primário de tripsina
- **SBBI** (*Soybean Bowman-Birk Inhibitor*) — inibidor bifuncional tripsina/quimotripsina

#### O resultado que revela o problema

Mendonça et al. (2020) expuseram larvas de *A. gemmatalis* a SKTI e SBBI e encontraram um padrão que é central para justificar todo este projeto:

| Efeito | Resultado |
|---|---|
| Sobrevivência larval | **Não reduzida** (curvas de Kaplan-Meier indicaram estímulo) |
| Desenvolvimento | Atrasado |
| Peso pré-pupal | Reduzido |
| Atividade de tripsina — dia 12 | **Inibida** |
| Atividade de tripsina — dia 15 | **Aumentada** nas larvas expostas a SKTI |

Ou seja: o inibidor natural funciona por alguns dias e depois o inseto **reverte o quadro**. A inibição inicial dá lugar a um aumento de atividade proteolítica. É a assinatura clássica da resposta compensatória.

O contraste com um inibidor sintético é instrutivo. A **benzamidina**, inibidor químico de tripsina, pulverizada sobre plantas de soja, causou cerca de **50% de mortalidade larval** e afetou negativamente escolha larval, preferência de adultos e oviposição (Pilon et al., 2018) — efeito que os IPs proteicos naturais não alcançaram.

---

### 4. O modelo de Laskowski

O mecanismo canônico de inibição de serino-proteases por IPs proteicos é o **modelo padrão de Laskowski**: o inibidor se apresenta como um **pseudo-substrato**, encaixando seu *reactive center loop* (RCL) no sítio ativo da enzima. Forma-se um complexo de altíssima afinidade em que a hidrólise da ligação cindível é extraordinariamente lenta, de modo que a enzima fica sequestrada em vez de clivar o inibidor produtivamente.

Esse modelo é a base conceitual de todo o desenho racional de peptídeos do grupo: se é o **laço** que faz o trabalho de reconhecimento, então um peptídeo curto que reproduza esse laço deveria reter parte da capacidade inibitória — sem o custo de produzir uma proteína inteira.

Foi precisamente essa a lógica aplicada por Saikhedkar et al. (2018) ⚠️ e, no grupo, por de Almeida Barros et al. (2021) e Paulo et al. (2026).

---

### 5. Do inibidor proteico ao peptídeo mimético

Inibidores proteicos completos enfrentam obstáculos práticos: custo de produção, estabilidade, e — no caso de expressão transgênica — o tamanho do transgene e possíveis efeitos colaterais na planta.

Peptídeos curtos desenhados a partir do RCL oferecem uma alternativa: síntese barata, possibilidade de produção recombinante, e espaço para otimização racional guiada por docking.

O grupo demonstrou que a estratégia funciona. Paulo et al. (2026) desenharam quatro pentapeptídeos inspirados nos RCLs de **BPTI** e **SKTI** — `TGPCK`, `TGPCR`, `AVIMK`, `AVIMR` — e confirmaram por ensaios cinéticos que **todos** atuam como inibidores competitivos das tripsinas de *A. gemmatalis*, com `TGPCK` apresentando a maior eficácia.

O trabalho também trouxe um achado mecanístico fino: a afinidade correlacionou-se com o **tipo** de interação química formada. Ligações **pi-sigma** associaram-se a maior afinidade (AVIMK), enquanto contatos alquil/pi-alquil e C–H associaram-se a menor afinidade (AVIMR, TGPCK). Isso sugere que a otimização de peptídeos da série não deve mirar apenas "mais contatos", mas contatos de natureza específica.

O detalhamento da série GORE está em [`02_estado_da_arte_GORE.md`](02_estado_da_arte_GORE.md).

---

### 6. Adaptação e resistência — a tensão central

Este é o ponto que justifica o projeto, e vale desenvolvê-lo na introdução com cuidado.

Insetos herbívoros co-evoluíram com os IPs das plantas e dispõem de um repertório de contramedidas:

1. **Hiperprodução de proteases** — compensar a inibição pelo volume. É o que Mendonça et al. (2020) observaram no dia 15 com SKTI.
2. **Síntese de isoformas insensíveis** — expressar variantes de tripsina que o inibidor não reconhece. A existência de múltiplas isoformas em *A. gemmatalis* (Pilon et al., 2017) fornece o substrato genético para isso, e Coura et al. (2022) documentaram **reprogramação extensa de isoformas proteicas** no intestino médio da espécie alimentada com inibidores de protease, acompanhada de alterações histopatológicas. O perfil de proteases intestinais e seus padrões de ligação a inibidores foram caracterizados por Silva-Júnior et al. (2021).
3. **Degradação proteolítica do próprio inibidor** — clivar o IP em vez de ser inibido por ele. Relevante especialmente para IPs proteicos como SKTI.
4. **Vias de detoxificação e resposta a estresse oxidativo** — P450s, GSTs, superóxido dismutase, catalase, peroxidase. dos Santos et al. (2025) mostraram que o GORE-2 induziu resposta de detoxificação e estresse oxidativo mais forte que o SKTI.
5. **Contribuição da microbiota intestinal** — proteases de origem bacteriana que o inibidor pode não alcançar (Pilon et al., 2017).

A implicação é direta: **medir apenas atividade enzimática total não distingue esses mecanismos.** Um inseto que hiperproduz uma tripsina sensível e outro que expressa uma isoforma insensível podem apresentar a mesma leitura bioquímica agregada e estarem fazendo coisas completamente diferentes.

É aí que a transcriptômica entra — não como complemento descritivo, mas como o único método capaz de separar essas hipóteses. E é aí que o acoplamento com a análise estrutural fecha o argumento: identificadas as isoformas induzidas, é possível testar *in silico* se elas de fato escapam ao GORE3.

---

### 7. Contexto de defesa da planta

Vale registrar, para posicionamento, que a resistência da soja a *A. gemmatalis* não se resume a IPs. Um trabalho recente do mesmo ambiente institucional mostrou que genótipos resistentes acumulam **rutina** e seu derivado O-metilado **narcisina**, e que a O-metilação aumenta acentuadamente a toxicidade: a rutina metilada causou cerca de **95% de mortalidade em 5 dias**, contra ~17 dias para atingir letalidade comparável com a rutina não metilada (de Assis et al., 2026). O docking contra as 70 proteínas mais abundantes do intestino larval indicou ligação de ambos os flavonóis a proteases, P450s e GSTs.

Isso reforça um ponto conceitual útil: **proteases digestivas e maquinaria de detoxificação são alvos convergentes** de estratégias defensivas bastante distintas. O GORE3 ataca o primeiro eixo; a resposta do inseto mobiliza o segundo.

---

### Referências desta seção

Todas com DOI ou PMID verificado — ver [`referencias.bib`](referencias.bib).

- de Almeida Barros et al. (2021) — *Pest Manag Sci* 77(4) — PMID 33200876
- de Andrade et al. (2026) — *Int J Biol Macromol* — PMID 41956187
- de Assis et al. (2026) — *J Sci Food Agric* — PMID 41999131
- Coura et al. (2022) — *Ann Appl Biol* 180(3):383-397 — doi:10.1111/aab.12740
- Silva-Júnior et al. (2021) — *Arch Insect Biochem Physiol* 107(3) — doi:10.1002/arch.21792
- dos Santos et al. (2025) — *Eur J Entomol* 122:119-136 — doi:10.14411/eje.2025.015
- Lanzaro et al. (2024) — *Front Physiol* — PMID 39534858
- Mendonça et al. (2020) — *Arch Insect Biochem Physiol* — PMID 31625209
- Paulo et al. (2026) — *Arch Insect Biochem Physiol* — PMID 41510779
- Pezenti et al. (2023) — *Genome* — PMID 36971261
- Pilon, A.M. et al. (2018) — *An Acad Bras Cienc* — PMID 30365718
- Pilon, F.M. et al. (2017) — *Arch Insect Biochem Physiol* — PMID 28762531
- Sultana et al. (2022) — *Plant Cell Rep* 41(2) — PMID 34674016



---


<a id="parte-3"></a>

## Estado da arte — a série GORE

Reconstrução da linhagem de peptídeos inibidores desenvolvida pelo grupo (LBBM / UFV, coordenação Profa. Maria Goreti de Almeida Oliveira), a partir do que está **publicado e verificável**.

O nome "GORE" é uma homenagem à supervisora (Goreti).

---

### 1. Linha do tempo publicada

#### GORE1 e GORE2 — a prova de conceito (2021)

**de Almeida Barros et al., 2021** — *Pest Management Science* 77(4) — PMID 33200876

Primeiro trabalho da série. Dois peptídeos desenhados racionalmente para inibir as tripsinas de *A. gemmatalis*, avaliados por docking, cinética e bioensaio.

| | GORE1 | GORE2 |
|---|---|---|
| Kᵢ (L-BApNA) | **0,49 mM** | **0,10 mM** |
| Tipo de inibição | Competitiva reversível | Competitiva reversível |
| Efeito *in vivo* | Prejudica sobrevivência e desenvolvimento | Idem, mais potente |

O docking revelou padrões críticos de ligação de hidrogênio com resíduos do sítio ativo das tripsinas de *A. gemmatalis* e de outros lepidópteros. Energias de ligação negativas foram interpretadas como indicativas de inibição efetiva.

Conclusão dos autores: os peptídeos servem de **linha de base para o desenho de novos inibidores de tripsina por ferramentas peptidomiméticas** — que é literalmente o programa de pesquisa que o GORE3 continua.

> ⚠️ **A sequência de aminoácidos de GORE1 e GORE2 não consta do resumo público.** Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) §1.

---

#### GORE2 sob a ótica transcriptômica (2025)

**dos Santos et al., 2025** — *European Journal of Entomology* 122:119-136 — doi:10.14411/eje.2025.015

*(Primeiro autor: Eulálio G. D. dos Santos — este é o antecessor metodológico direto do pós-doc.)*

RNA-Seq do intestino médio de *A. gemmatalis* após **24 h** de exposição, comparando o tripeptídeo **GORE-2** ao **SKTI** natural.

Resultados centrais:

- Ambos induziram **reprogramação transcricional extensa** no intestino médio
- Padrões de resposta comparáveis, envolvendo genes de proteases digestivas e proteínas de defesa
- Genes ligados à **matriz peritrófica** entre os afetados
- **SKTI** disparou ativação mais robusta de sinalização de defesa
- **GORE-2** provocou resposta mais forte de **detoxificação e estresse oxidativo**
- O derivado sintético foi mais eficaz em inibir a proteólise e reduzir a sobrevivência

Dois pontos deste trabalho são metodologicamente importantes para o novo projeto:

1. **GORE-2 é descrito como tripeptídeo** derivado do SKTI. Isso fixa a escala da série inicial.
2. **O tempo de exposição foi 24 h.** O desenho do novo projeto precisa declarar e justificar seu próprio ponto de coleta — e vale considerar que Mendonça et al. (2020) mostraram que a resposta compensatória a SKTI só apareceu por volta do **dia 15**. Um único ponto em 24 h captura a resposta imediata, não a adaptação. Ver [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) §3.

---

#### GORE 1-2 T — o salto para produção recombinante (2026)

**de Andrade et al., 2026** — *International Journal of Biological Macromolecules* — PMID 41956187

Peptídeo **quimérico recombinante** construído a partir dos tripeptídeos de ligação à tripsina da série.

| Item | Dado |
|---|---|
| Vetor | pET-41(a)+ |
| Cepa de expressão | *E. coli* **BL21(DE3)pLysS** (melhor desempenho entre as testadas) |
| Forma | Fusão com GST, predominantemente na **fração insolúvel** |
| Massa confirmada (LC-MS) | **≈ 4,6 kDa** |
| Kᵢ aparente | **≈ 100 µM** |
| Tipo de inibição | Competitiva |
| Subsítios engajados | **S1–S3** |
| MD | **100 ns**, RMSD de backbone estável, raio de giro compacto, ligações de H persistentes |

Este trabalho é o **modelo metodológico** mais próximo do que o pós-doc precisa fazer na parte estrutural: docking localizando o peptídeo na fenda catalítica + MD de 100 ns + análise de estabilidade. Os autores o descrevem explicitamente como "*framework* reprodutível que integra modelagem molecular com expressão heteróloga".

A estrutura local `Milena-MD\data\GORE12T-ligand.pdb` (75 aa: sete cópias de tripeptídeos VLR/VLK alternados unidos por linkers `GGSGGSGGS`) corresponde a este construto. ⚠️ A correspondência é inferida por contexto, não confirmada documentalmente.

---

#### Peptídeos derivados de RCL — a geração pentapeptídica (2026)

**Paulo et al., 2026** — *Archives of Insect Biochemistry and Physiology* — PMID 41510779

Quatro **pentapeptídeos** inspirados nos *reactive center loops* de **BPTI** e **SKTI**:

| Peptídeo | Observação |
|---|---|
| `TGPCK` | **Maior eficácia** entre os quatro |
| `TGPCR` | Competitivo |
| `AVIMK` | Maior afinidade, associada a ligações **pi-sigma** |
| `AVIMR` | Menor afinidade (alquil/pi-alquil, C–H) |

Todos confirmados como **inibidores competitivos** das tripsinas de *A. gemmatalis* por ensaio de inibição enzimática.

Resíduos-chave da enzima na ligação: **His57, Asp102, Ser195, Asp189, Gly197**.

Ressalva dos próprios autores, que vale reproduzir na discussão do projeto: estudos futuros devem avaliar os efeitos **quando aplicados às plantas**, considerando interações metabólicas e possível fitotoxicidade. Esse é um gargalo real no caminho até o produto.

---

### 2. Onde o GORE3 se encaixa

Aqui é preciso separar o que está publicado do que está em documento interno.

#### Sequência

> **GORE3 = `LALAY`** — Leu-Ala-Leu-Ala-Tyr, pentapeptídeo.
> Confirmado pelo pesquisador em 18/07/2026.

Composição relevante para a análise estrutural: **nenhum resíduo básico**. Dois Leu (hidrofóbicos), dois Ala (pequenos), uma Tyr (aromática, com hidroxila).

Isso distingue o GORE3 dos demais peptídeos da série já publicados, que terminam em Lys ou Arg justamente para ocupar o subsítio S1 da tripsina — ancorado no Asp189. O GORE3 não pode formar essa ponte salina, o que torna seu modo de ligação uma pergunta em aberto e não uma premissa. Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) §1.1 e [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) §5.

#### O que consta do resumo interno (`GORE3-abstract.docx`)

> ⚠️ **Fonte não revisada por pares.** Os dados abaixo vêm do resumo do próprio projeto e de comunicação interna do grupo. Devem ser tratados como resultados preliminares até publicação.

- GORE3 é descrito como inibidor de serino-proteases derivado do modelo do **SKTI**
- Efeitos em *S. frugiperda* e *A. gemmatalis*: atraso no ciclo larval, redução do peso pupal, queda da eficiência alimentar, mortalidade relevante
- Inibição significativa de proteases tripsina-like
- Indução de resposta antioxidante: aumento de **SOD, CAT, POX, GST**
- Cinética *in vitro*: **inibição competitiva**, dependente de concentração, **IC₅₀ na faixa micromolar**
- Atraso de desenvolvimento relatado de até **50 dias** (documento `Abstract-projeto-eulalio.docx`)

#### O achado que mais importa

O mesmo documento registra um **contraste entre espécies**:

| Espécie | Resposta ao GORE3 |
|---|---|
| *S. frugiperda* | **Superexpressão de proteases** — resposta compensatória à inibição |
| *A. gemmatalis* | **Redução** da atividade proteolítica + intensificação das rotas de detoxificação |

E acrescenta que esses dados **diferem** dos observados com GORE1 e GORE2.

Se confirmado, isso é o resultado mais interessante de toda a série: o GORE3 conseguiria, em *A. gemmatalis*, escapar do mecanismo de compensação que derrotou o SKTI no experimento de Mendonça et al. (2020). É uma afirmação forte, que a transcriptômica pode sustentar ou refutar de forma direta.

Ver [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) §1.

---

### 3. Progressão da potência ao longo da série

Compilando os valores publicados — com a ressalva de que **Kᵢ e IC₅₀ não são diretamente comparáveis** e que as condições de ensaio variam:

| Molécula | Parâmetro | Valor | Fonte |
|---|---|---|---|
| GORE1 | Kᵢ | 0,49 mM | PMID 33200876 |
| GORE2 | Kᵢ | 0,10 mM | PMID 33200876 |
| GORE 1-2 T | Kᵢ aparente | ≈ 100 µM (0,10 mM) | PMID 41956187 |
| GORE3 | IC₅₀ | "faixa micromolar" ⚠️ | Documento interno |

A tendência é de ganho de potência, mas **o valor do GORE3 não está quantificado em fonte verificável** e "faixa micromolar" é vago demais para entrar num texto científico. Obter o número exato é pendência para a introdução.

---

### 4. Peptídeos da série com estrutura 3D disponível localmente

Extraídos diretamente de arquivos PDB (leitura dos carbonos-α), portanto **sequências reais dos modelos**, mas cujo mapeamento para os nomes GORE é inferido:

| Sequência | Arquivo | Rótulo atribuído |
|---|---|---|
| `LALAY` | `analise-alosterica\data\LALAY.pdb`; `Paper-Daniel-Pablo\RE-Docking-1BTY-trypsin-GORE3\GORE3-PEPFOLD4.pdb` | **GORE3** ✅ confirmado |
| `LALAK` | `Spodoptera-GORE4\...\cluster1_1.pdb`; `MD-gromacs\poses\acr157-gore4-c1\ligand.pdb` | GORE4 ⚠️ |
| `LALAR` | `analise-alosterica\data\LALAR.pdb` | Variante ⚠️ |
| 75-mer VLR/VLK | `Milena-MD\data\GORE12T-ligand.pdb` | GORE 1-2 T |

**Ponto em aberto (não bloqueante):** `LALAY` não aparece entre os peptídeos nomeados em Paulo et al. (2026) (`TGPCK`/`TGPCR`/`AVIMK`/`AVIMR`). Como a sequência do GORE3 está confirmada, a leitura mais provável é que ele pertença a uma linha de trabalho distinta daquela publicação — possivelmente ainda inédita.

Isso importa para a **escrita da introdução**: define se o GORE3 é apresentado como continuação direta de Paulo et al. (2026) ou como desenvolvimento paralelo. Confirmar com a supervisora. As sequências de GORE1, GORE2 e GORE5–13 seguem sem correspondência documentada.

---

### 5. Síntese — o que a série já estabeleceu

1. Peptídeos curtos derivados de RCL **funcionam** como inibidores competitivos de tripsinas de *A. gemmatalis* — resultado replicado em três publicações independentes do grupo
2. A potência melhorou ao longo das gerações, de Kᵢ sub-milimolar para micromolar
3. A produção **recombinante** é viável (GORE 1-2 T, ≈4,6 kDa)
4. O efeito *in vivo* é real: atraso de desenvolvimento, queda de peso pupal, mortalidade
5. A resposta do inseto envolve **detoxificação e estresse oxidativo**, não apenas proteases
6. O docking identifica consistentemente o engajamento do sítio catalítico e dos subsítios S1–S3

### 6. O que a série ainda não estabeleceu

1. **Se o inseto se adapta ao GORE3 ao longo do tempo** — todos os transcriptomas são de ponto único
2. **Quais isoformas específicas de tripsina são induzidas** e se elas escapam do inibidor
3. **Por que as duas espécies respondem de forma oposta**
4. **Se as interações vistas no docking persistem** em escala de tempo relevante para as isoformas do GORE3 (o MD de 100 ns existe para GORE 1-2 T, não para GORE3 ⚠️)
5. **Splicing alternativo** — mencionado como objetivo, nunca executado na série
6. **Comportamento em planta** — fitotoxicidade e interações metabólicas (ressalva explícita de Paulo et al., 2026)

Os itens 1 a 5 são endereçáveis por este pós-doc.

---

### Referências desta seção

- de Almeida Barros et al. (2021) — *Pest Manag Sci* — PMID 33200876
- de Andrade et al. (2026) — *Int J Biol Macromol* — PMID 41956187
- dos Santos et al. (2025) — *Eur J Entomol* 122:119-136 — doi:10.14411/eje.2025.015
- Mendonça et al. (2020) — *Arch Insect Biochem Physiol* — PMID 31625209
- Paulo et al. (2026) — *Arch Insect Biochem Physiol* — PMID 41510779 (PMC12784448)



---


<a id="parte-4"></a>

## Metodologia — atualização para o padrão atual

Revisão crítica da metodologia proposta em `Projeto-Eulalio-Pós-doc2.docx` (§2), com o que é padrão em 2026 e a justificativa de cada mudança.

> **Sobre versões:** este documento **não fixa números de versão**. Versões devem ser conferidas no momento da instalação (anaconda.org / repositório oficial) e registradas no ambiente. Pinos de versão citados de memória já causaram falha real de pipeline em outro projeto.

---

### Quadro-resumo

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

### 1. 🔴 Montagem *de novo* → pipeline genoma-guiado

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

#### Por que isso importa especificamente para este projeto

Não é uma troca cosmética. A pergunta central do trabalho é sobre **isoformas de tripsina** — quais são induzidas, quais escapam do inibidor. Montagem *de novo* é estruturalmente ruim para isso:

- Trinity **fragmenta e funde** transcritos de famílias gênicas com alta similaridade de sequência. Tripsinas de lepidópteros são exatamente esse caso: muitas cópias parálogas quase idênticas.
- Sem coordenadas genômicas, não há como distinguir **isoforma de splicing** de **parálogo** de **artefato de montagem**.
- A quantificação sobre um transcriptoma *de novo* redundante distribui reads de forma ambígua entre contigs quase idênticos, inflando a incerteza justamente nos genes de interesse.
- **Análise de splicing alternativo** — objetivo declarado do projeto — é inviável sem anotação genômica. Ferramentas como rMATS e DEXSeq (citadas no próprio `GORE3-abstract.docx`) **exigem** genoma anotado.

#### Fluxo recomendado

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

#### Manter Trinity como via secundária

Recomendo **não descartar** a montagem *de novo*, e sim rodá-la em paralelo, por três razões concretas:

1. Capturar transcritos ausentes da anotação (a anotação é automática, não curada)
2. Capturar transcritos de **origem bacteriana** — a microbiota contribui com atividade proteolítica relevante em *A. gemmatalis* (Pilon et al., 2017), e essas sequências não estarão no genoma do hospedeiro
3. Comparabilidade com dos Santos et al. (2025), que usou *de novo*

O grupo já tem montagem Trinity de *A. gemmatalis* pronta localmente — ver [`04_viabilidade.md`](04_viabilidade.md).

---

### 2. 🟡 Kallisto → Salmon (+ tximport obrigatório)

O projeto especifica Kallisto 0.44 (de 2017). Salmon é a escolha mais comum hoje, com correções de viés (GC, posicional, sequência) que Kallisto não aplica por padrão.

**Erro de omissão mais sério que a escolha da ferramenta:** o projeto vai direto de pseudoalinhamento para DESeq2. Falta o **`tximport`**, que agrega estimativas de nível de transcrito para nível de gene e — criticamente — passa os *offsets* de comprimento efetivo ao DESeq2. Pular essa etapa e alimentar o DESeq2 com contagens de TPM arredondadas é um erro estatístico real, não formalidade.

O pipeline local `RNA-Seq-not-model` já implementa Salmon + `tximport` (`scripts/00_tximport.R`).

---

### 3. 🟡 TRAPID / Blast2GO / KOBAS 2.0 → eggNOG-mapper v2 + clusterProfiler

- **KOBAS 2.0** — a versão citada está descontinuada; o sucessor é o KOBAS-i. Mas, para um projeto que já usará R, **clusterProfiler** é a escolha mais prática (enriquecimento GO e KEGG, correção de múltiplos testes embutida, visualização).
- **Blast2GO** — a versão gratuita é limitada; o fluxo moderno equivalente é eggNOG-mapper ou InterProScan.
- **eggNOG-mapper v2** — padrão atual para anotação funcional de não-modelos, com ortologia, GO, KEGG KO e domínios PFAM numa passada.

**Ponto de atenção sobre KEGG:** o projeto propõe usar *Helicoverpa armigera* e *Bombyx mori* como referência para enriquecimento. Com genoma próprio disponível, o correto é construir o mapeamento **gene→GO/KO da própria *A. gemmatalis*** via eggNOG-mapper e usar `clusterProfiler::enricher` com esse universo customizado. Usar outra espécie como proxy introduz viés de anotação e não é mais necessário.

O pipeline local já tem `02_gene2go_build.R` e `03_enrichment.R` para exatamente isso.

---

### 4. 🔴 Phyre2 → AlphaFold

O projeto tem uma **contradição interna**: o objetivo (§ resumo e §27) menciona "AlphaFold e/ou modelagem por homologia", mas a metodologia (§2.9) especifica apenas **Phyre2**.

Phyre2 é modelagem por homologia baseada em perfis-HMM, tecnologia anterior à ruptura do AlphaFold2 (Jumper et al., 2021 — PMID 34265844). Para uma tripsina, que tem abundância de templates de alta identidade, Phyre2 até produz modelo utilizável — mas não há razão para preferi-lo.

**Recomendado:**
- **AlphaFold2 / ColabFold** para as estruturas das isoformas de tripsina
- **AlphaFold3** (Abramson et al., 2024 — PMID 38718835) quando o objetivo for predizer diretamente o **complexo** proteína–peptídeo, o que se conecta ao item 5
- Manter a validação estereoquímica proposta (ProSA-web, Ramachandran) — continua correta e necessária
- Registrar as métricas de confiança do próprio AlphaFold (**pLDDT**, **PAE**), que o projeto não menciona e que são hoje esperadas em revisão por pares

O usuário já tem infraestrutura de AlphaFold3 no projeto `trypsin-agemmatalis-structural`.

---

### 5. 🔴 Docking de peptídeo: Vina/PyRx não é adequado sozinho

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

### 6. 🔴 CGenFF para o GORE3 — erro conceitual

O projeto (§2.10) diz:

> "O peptídeo GORE3 será parametrizado usando o CGenFF (CHARMM General Force Field), garantindo compatibilidade com o campo de força aplicado à tripsina."

**Isso está incorreto.** O CGenFF existe para **pequenas moléculas orgânicas do tipo fármaco** que não têm parâmetros nos campos de força biomoleculares. Um peptídeo composto de aminoácidos canônicos **já é coberto** pelo campo de força de proteína (CHARMM36m ou AMBER) — que foi parametrizado precisamente para isso.

Usar CGenFF num peptídeo canônico é, ao mesmo tempo:
- **desnecessário** — os parâmetros já existem e são melhores
- **prejudicial** — parâmetros CGenFF por analogia são menos acurados para backbone peptídico que os do FF de proteína
- **fonte de erro operacional** — descompasso de versão do CGenFF já causou problema real em outro projeto do usuário

**Correção:** tratar receptor e peptídeo com **o mesmo campo de força de proteína**, gerando a topologia do complexo numa única passada do `pdb2gmx`. CGenFF só entraria se houvesse ligante de pequena molécula na simulação — o que seria o caso para a **benzamidina**, se ela for simulada como controle.

---

### 7. 🟠 Campo de força: CHARMM36m × AMBER99SB-ILDN

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

### 8. 🟡 Desenho experimental: réplicas

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

### 9. 🟡 Etapas ausentes que devem entrar

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

### 10. 🟡 MM/PBSA — usar, mas declarar as limitações

O projeto menciona MM-PBSA para energia de ligação. É prática comum e aceitável, mas com ressalvas que devem estar no texto:

- Métodos *end-point* como MM/PBSA e MM/GBSA fornecem **energias relativas**, úteis para **ranquear** ligantes, não valores absolutos comparáveis a Kᵢ experimental
- A **entropia configuracional** normalmente é omitida ou aproximada de forma grosseira; a alternativa acessível é a **entropia de interação**, que o usuário já tem implementada (`Milena-MD/bin/interaction_entropy.py`)
- Resultados dependem fortemente da constante dielétrica interna escolhida — declarar o valor
- **Replicatas independentes** de MD (3 réplicas com sementes distintas) são hoje mais valorizadas que uma única trajetória longa, por permitirem barra de erro

**Recomendado:** 3 réplicas × 100 ns por complexo, em vez de 1 × 300 ns. O ganho em estimativa de incerteza compensa.

Ferramenta: **gmx_MMPBSA**. O usuário já tem ambiente funcional (`mmgbsa-env`) e conhece as armadilhas operacionais (correção de PBC antes da análise).

---

### 11. Fluxo consolidado recomendado

#### Transcriptômica

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

#### Estrutural

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

#### Integração — o diferencial

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

### Referências desta seção

- Jumper et al. (2021) — *Nature* — PMID 34265844 — AlphaFold2
- Abramson et al. (2024) — *Nature* — PMID 38718835 — AlphaFold3
- Pilon, F.M. et al. (2017) — PMID 28762531 — microbiota proteolítica
- dos Santos et al. (2025) — doi:10.14411/eje.2025.015
- de Andrade et al. (2026) — PMID 41956187
- Assembly `GCF_050436995.1` — NCBI Datasets



---


<a id="parte-5"></a>

## Análise de viabilidade

Avaliação honesta do que é executável, com que recursos e em que prazo.

**Veredito: o projeto é viável**, e o esforço real é menor do que o documento sugere, porque boa parte da infraestrutura computacional já existe e está validada. Os riscos concentram-se em **dados** (sequenciamento pendente) e em **uma pendência de definição** (sequência do GORE3), não em capacidade técnica.

> Todos os caminhos abaixo foram verificados como existentes em 18/07/2026.

---

### 1. Situação dos dados

#### O que existe

| Item | Onde | Situação |
|---|---|---|
| Genoma de referência | `GCF_050436995.1` (NCBI) | ✅ Público, anotado (RS_2025_08) |
| RNA-Seq anterior (controle / SKTI / GORE2) | BioProject **PRJNA1494060**, SRA SRP717437 | ✅ Depositado, 8 SRR |
| Montagem Trinity de *A. gemmatalis* | `C:\Users\eulal\.claude\caracterization-trypsin\data\raw\trinity_assembly.fasta` | ✅ Local |
| Sequências de tripsina de *A. gemmatalis* | `C:\Users\eulal\Desktop\LEBPP\Dsign-racional-peptid-inib\anticarsia_gemmatalis_trypsins.fasta` | ✅ Local |
| Sequências de tripsina de *S. frugiperda* | mesma pasta, `spodoptera_frugiperda_trypsins.fasta` | ✅ Local (para expansão futura) |
| Template cristalográfico | `1tld.cif` (mesma pasta) | ✅ Local |

#### O que falta

| Item | Impacto | Mitigação |
|---|---|---|
| **FASTQ do experimento GORE3** | 🔴 Bloqueia todo o bloco transcriptômico | Em sequenciamento na Macrogen. Documentação em `RNA-Seq-Macrogen\` e `Desktop\LEBPP\Pós-doc-eulalio\Macrogen-Docs\` |
| FASTQ bruto do Control R1/C1A (2020) | 🟡 Sem cópia local | Recuperável do SRA se necessário |
| Tabela de DEGs processada de *A. gemmatalis* | 🟡 Não existe localmente | Reprocessável a partir do SRA |
| Dados de *S. frugiperda* | ⚪ Fora do escopo atual | — |

**O caminho crítico é o sequenciamento.** Enquanto os FASTQ não chegam, todo o bloco estrutural pode avançar em paralelo — e boa parte dele já está feita.

---

### 2. Ativos computacionais reaproveitáveis

Este é o ponto onde o projeto subestima o que já tem.

#### 2.1 Pipeline RNA-Seq — `RNA-Seq-not-model`

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

#### 2.2 Fluxo transcriptoma → estrutura — `caracterization-trypsin`

`C:\Users\eulal\.claude\caracterization-trypsin\nextflow\` — pipeline de 11 fases que já implementa exatamente a integração que dá originalidade a este projeto: Trinity → CD-HIT → TransDecoder → HMMER (identificação de tripsinas) → MAFFT/IQ-TREE (filogenia) → AlphaFold → Vina → GROMACS.

Espelho em `C:\Users\eulal\trypsin-agemmatalis-structural\`.

#### 2.3 Setups GROMACS validados

`C:\Users\eulal\.claude\inhibitor-selection\params\` (verificado):
`minim.mdp`, `ions.mdp`, `nvt.mdp`, `npt.mdp`, `md.mdp`

⚠️ Estes `.mdp` são de linhagem **AMBER99SB-ILDN + TIP3P**. Se a decisão for CHARMM36m, precisam de revisão (esquema de cutoff e tratamento de vdW diferem entre as famílias de campo de força — não é troca de uma linha).

#### 2.4 Scripts de análise de MD — `Milena-MD`

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

#### 2.5 Estruturas de tripsina prontas

`C:\Users\eulal\.claude\analise-alosterica\data\` — modelos finais + subpasta `protonated\` com estruturas já tratadas em **pH 8,2** (verificado: `ACR157-final_ph8.2.pdb`, `QCL936-final_ph8.2.pdb`, `XP273-final_ph8.2.pdb` e correspondentes `.pqr`).

Isso está **correto** e é frequentemente esquecido: o intestino de lepidóptero é alcalino (Pilon et al., 2017), e protonar a pH 7,0 seria erro.

Adicionalmente: `C:\Users\eulal\Desktop\LEBPP\GORE4-ate-GORE13\Anticarsia-trypsin\` com 12 isoformas `DN*_i*-clean.pdb`.

#### 2.6 Docking do GORE3 já produzido

`C:\Users\eulal\Desktop\LEBPP\GORE4-ate-GORE13\GORE3\` (verificado) — resultados **HADDOCK** empacotados para cinco isoformas:

`ACR157-GORE3_Haddock.tgz`, `DN773-GORE3_Haddock.tgz`, `DN1441-GORE3_Haddock.tgz`, `DN1937-GORE3_Haddock.tgz`, `QCL936-GORE3_Haddock.tgz`

Mais `Residuos-cataliticos.docx` na mesma pasta.

E, em `Desktop\LEBPP\Paper-Daniel-Pablo\`: redocking de validação contra tripsina bovina (**1BTY**), docking DN773/DN1937 × GORE3 e controles com benzamidina.

> **Implicação:** o protocolo de docking recomendado em [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §5 — HADDOCK + redocking de controle — **já está em uso na prática**. Falta apenas escrevê-lo no projeto, que ainda descreve Vina/PyRx.

#### 2.7 Textos base

| Arquivo | Uso |
|---|---|
| `C:\Users\eulal\.claude\analise-alosterica\artigo.md` | Manuscrito vivo sobre o peptídeo no sítio S'2, em português — melhor ponto de partida textual |
| `C:\Users\eulal\.claude\caracterization-trypsin\docs\introduction.md` | Introdução sobre tripsinas de *A. gemmatalis* |
| `C:\Users\eulal\.claude\MD-gromacs\artigo_md.md` | Redação de metodologia de MD |
| `Desktop\LEBPP\Paper-Daniel-Pablo\Manuscript_Daniel Guimarães_Versão final.docx` | Manuscrito do docking (publicado como PMID 41510779) |
| `C:\Users\eulal\.claude\analise-alosterica\paper-goreti.pdf` | Base do sítio S'2 |

---

### 3. Hardware e tempo

**Servidor:** Debian, RTX 5070 Ti 16 GB, 32 cores (`eulalio@200.235.143.10`, requer VPN).

#### Bloco transcriptômico

Com genoma de referência, o custo computacional é modesto. Índice STAR de um genoma de lepidóptero, alinhamento de ~12–20 bibliotecas, quantificação e DESeq2 — trabalho de **horas a poucos dias**, não semanas. A montagem Trinity paralela é o passo mais caro (memória, não GPU) e roda uma vez.

**Gargalo real: não é computacional. É a chegada dos dados.**

#### Bloco estrutural

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

### 4. Riscos

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

### 5. Estratégia de execução recomendada

#### Enquanto o sequenciamento não chega

1. ✅ ~~Resolver a pendência da sequência do GORE3~~ — feito: `LALAY`
2. **Decidir o campo de força** — bloqueia todo o MD
3. **Consolidar o docking já feito** — os `.tgz` do HADDOCK contêm resultados ainda não analisados de forma unificada
4. **Baixar e indexar `GCF_050436995.1`**
5. **Rodar o pipeline genoma-guiado sobre PRJNA1494060** — reprocessar o experimento GORE2/SKTI contra o genoma novo. Isso valida o pipeline com dados reais, dá um resultado publicável por si (comparação *de novo* × genoma-guiado) e deixa tudo pronto para quando o GORE3 chegar
6. **Iniciar MD das isoformas já modeladas**

O item 5 é o de melhor retorno: transforma tempo de espera em validação de método.

#### Quando os dados chegarem

Pipeline já testado → resultado rápido → seleção de isoformas → MD dirigida → integração.

---

### 6. Custo

Não há custo computacional adicional (infraestrutura própria). O custo relevante é o **sequenciamento**, já contratado na Macrogen.

Os documentos de cotação estão em `C:\Users\eulal\.claude\RNA-Seq-Macrogen\` e `Desktop\LEBPP\Pós-doc-eulalio\Macrogen-Docs\`. ⚠️ Valores não reproduzidos aqui por não terem sido conferidos.

---

### Referências desta seção

- Pilon, F.M. et al. (2017) — PMID 28762531 — pH intestinal alcalino
- Assembly `GCF_050436995.1` — NCBI
- BioProject PRJNA1494060 / SRA SRP717437 — dados anteriores do grupo



---


<a id="parte-6"></a>

## Lacunas, hipóteses e contribuição original

O que ainda não se sabe, o que este projeto pode testar, e o que o diferencia do que o grupo já publicou.

Serve de base para as seções de **justificativa** e **objetivos** da introdução.

---

### 1. A lacuna central — por que as duas espécies respondem de forma oposta

#### O fato

O resumo interno do projeto registra que o GORE3 produz respostas divergentes:

| Espécie | Atividade proteolítica | Interpretação |
|---|---|---|
| *S. frugiperda* | **Superexpressão de proteases** | Resposta compensatória bem-sucedida |
| *A. gemmatalis* | **Redução** da atividade + detoxificação intensificada | Compensação falha ou é redirecionada |

⚠️ Dado de documento interno, não publicado. Precisa de confirmação.

#### Por que isso importa

O mecanismo de escape mais bem documentado em Lepidoptera é a **hiperprodução compensatória de proteases**. Mendonça et al. (2020) observaram exatamente isso em *A. gemmatalis* exposta ao SKTI: inibição no dia 12, **aumento** de atividade de tripsina no dia 15.

Se o GORE3 realmente impede essa compensação em *A. gemmatalis*, ele estaria contornando o principal mecanismo de resistência a inibidores de protease. Isso é uma alegação forte — e testável.

#### A pergunta

**A ausência de compensação em *A. gemmatalis* é incapacidade ou redirecionamento?**

Duas possibilidades com consequências opostas:

- **(a) Incapacidade** — o inseto não consegue montar a resposta. O GORE3 seria robusto contra adaptação. Ótima notícia para desenvolvimento de produto.
- **(b) Redirecionamento** — o inseto abandonou a via proteolítica e investiu em detoxificação (o aumento de SOD/CAT/POX/GST aponta nessa direção). Nesse caso a resistência apenas mudou de endereço, e surgiria por outro caminho sob pressão de seleção.

**Transcriptômica distingue as duas.** Bioquímica de atividade total, não.

---

### 2. Lacuna — isoformas, não genes

Este é o ponto mais fino e o mais negligenciado.

*A. gemmatalis* tem múltiplas isoformas de tripsina (Pilon et al., 2017). Análise de expressão diferencial no nível de **gene** agrega todas elas num único valor — e portanto **não consegue** detectar o mecanismo mais interessante: a substituição de uma isoforma sensível por uma insensível, com atividade total constante.

Um exemplo concreto do que passaria despercebido:

```
Isoforma A (sensível ao GORE3):    100 → 20   ↓
Isoforma B (insensível):            20 → 100  ↑
─────────────────────────────────────────────
Total no nível de gene:            120 → 120  (nenhuma mudança detectada)
```

A leitura no nível de gene, e o ensaio enzimático de atividade total, mostrariam "sem efeito". Mas o inseto teria escapado completamente.

#### Não é hipótese solta — já há evidência proteica

Coura et al. (2022) documentaram exatamente esse fenômeno em *A. gemmatalis* alimentada com inibidores de protease: **reprogramação extensa de isoformas proteicas**, acompanhada de alterações histopatológicas no intestino médio.

Ou seja, o grupo já demonstrou no nível **de proteína** que a troca de isoformas acontece. O que falta é a contrapartida no nível de **transcrito**, resolvida por isoforma e ligada à estrutura — que é o que este projeto pode entregar.

**Requisito metodológico:** só é possível resolver isso com **quantificação em nível de isoforma sobre genoma anotado** — o que exige a migração para pipeline genoma-guiado ([`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §1). Com montagem *de novo*, isoformas e parálogos são indistinguíveis.

Nenhum trabalho da série GORE fez essa análise.

---

### 3. Lacuna — o tempo

Todos os transcriptomas da série são de **ponto único**:

- dos Santos et al. (2025): **24 h** de exposição
- O projeto atual: ponto único não especificado

Mas a literatura do próprio grupo mostra que a resposta é **dependente do tempo**: em Mendonça et al. (2020), a inibição apareceu no dia 12 e se **inverteu** no dia 15.

Um único ponto em 24 h captura a resposta imediata ao estresse. **Não captura adaptação.** E adaptação é justamente o problema que motiva a busca por inibidores melhores.

**Recomendação:** se houver qualquer margem orçamentária, incluir um **segundo ponto temporal tardio**. O ganho científico de dois pontos (ex.: 24 h e 7–15 dias) supera o de mais réplicas num único ponto, porque permite distinguir *resposta* de *adaptação* — que é a pergunta que ninguém na série respondeu.

Se não houver margem, escolher o ponto **com justificativa explícita** e declarar a limitação.

---

### 4. Lacuna — o docking nunca foi validado por MD para o GORE3

Situação atual:

| Molécula | Docking | MD |
|---|---|---|
| GORE1 / GORE2 | ✅ PMID 33200876 | ❌ |
| GORE 1-2 T | ✅ | ✅ 100 ns (PMID 41956187) |
| Peptídeos RCL (TGPCK etc.) | ✅ PMID 41510779 | ❌ |
| **GORE3** | ✅ (local, HADDOCK + Vina) | ❌ ⚠️ |

O docking é uma fotografia estática. Ele identifica poses plausíveis, mas não diz se elas **persistem**. Para um peptídeo flexível de 5 resíduos num sítio ativo raso, essa distinção não é acadêmica — poses de docking de peptídeos curtos frequentemente se dissolvem nos primeiros nanossegundos de simulação.

**Sem MD, a "assinatura digital" prometida no resumo do projeto não tem sustentação.**

---

### 5. Lacuna — S1 ou S'2?

O grupo trabalha com duas hipóteses de sítio de ligação:

- **S1** — sítio de especificidade canônico, ancorado no Asp189; mecanismo competitivo clássico, consistente com toda a cinética publicada
- **S'2** — sítio do lado dos produtos (Tyr39/His40/Tyr151 na numeração da referência local), investigado na linha `analise-alosterica`

A cinética publicada indica **inibição competitiva** para GORE1, GORE2, GORE 1-2 T e os peptídeos RCL — o que é consistente com ocupação de S1 ou de região sobreposta ao sítio ativo.

Mas a metodologia do projeto **assume** S1 ao posicionar a caixa de docking manualmente sobre o sítio catalítico. Isso não testa a hipótese; pressupõe-a.

#### A composição do GORE3 torna essa pergunta urgente

Com a sequência confirmada — **`LALAY`** = Leu-Ala-Leu-Ala-Tyr — a questão deixa de ser especulativa.

`LALAY` **não contém nenhum resíduo básico**. E o subsítio S1 da tripsina é definido pelo **Asp189** no fundo do bolsão, que ancora cadeias laterais de Lys/Arg por interação eletrostática. É exatamente por isso que os peptídeos de Paulo et al. (2026) terminam em **K** ou **R** (`TGPCK`, `TGPCR`, `AVIMK`, `AVIMR`) — eles reproduzem o resíduo P1 de um substrato canônico de tripsina.

**O GORE3 não pode fazer isso.**

Se a inibição competitiva do GORE3 se confirmar, restam duas explicações:

- **(a) Ocupação da fenda por subsítios não-S1** — S2/S3, via contatos hidrofóbicos (dois Leu) e empilhamento aromático (Tyr). Competitivo sem P1 canônico.
- **(b) Ligação em sítio distinto**, com efeito competitivo indireto — o que traria o **S'2** para o centro da explicação.

Nos dois casos, o mecanismo do GORE3 seria **diferente** do dos demais peptídeos da série. Isso não é um problema: é potencialmente o achado mais interessante do projeto, e explicaria por que o GORE3 se comporta de forma distinta de GORE1/GORE2 nos ensaios do grupo.

**Recomendação revisada:**

1. ***Blind docking*** sobre a superfície inteira da enzima, **antes** do docking dirigido — para não impor o resultado
2. Docking dirigido comparativo **S1 × S'2**
3. MD a partir das poses de ambos os sítios; a estabilidade decide
4. Comparar com um peptídeo da série que **tenha** resíduo básico, como controle interno de mecanismo

---

### 6. Hipóteses testáveis

Formuladas para serem falsificáveis, cada uma com o teste correspondente.

#### H1 — Escape por isoforma
> *A. gemmatalis* exposta ao GORE3 induz isoformas específicas de tripsina cuja arquitetura de sítio ativo reduz a afinidade pelo peptídeo.

**Teste:** quantificação por isoforma → modelagem das isoformas induzidas → docking/MD comparativo entre induzidas e reprimidas.
**Falsificação:** se as isoformas induzidas ligarem o GORE3 tão bem quanto as reprimidas, H1 cai.
**Apoio prévio:** Coura et al. (2022) já demonstraram reprogramação de isoformas proteicas em *A. gemmatalis* sob inibidores de protease.

#### H2 — Redirecionamento para detoxificação
> A resposta de *A. gemmatalis* ao GORE3 privilegia vias de detoxificação e antioxidantes em detrimento da compensação proteolítica.

**Teste:** enriquecimento funcional (GO/KEGG) comparando GORE3 × SKTI × benzamidina; expressão de P450, GST, UGT, SOD, CAT, POX.
**Apoio prévio:** dos Santos et al. (2025) já mostraram resposta de detoxificação mais forte para GORE-2 que para SKTI.

#### H3 — Persistência do complexo
> O complexo tripsina–GORE3 permanece estável em escala de 100 ns, com ligações de hidrogênio persistentes aos resíduos catalíticos.

**Teste:** 3 × 100 ns de MD; RMSD, ocupância de ligações de H, distâncias à tríade His57/Asp102/Ser195 e ao Asp189.
**Falsificação:** dissociação ou perda de contato com o sítio ativo.

#### H4 — Superioridade mecanística sobre o SKTI
> O GORE3 evita a compensação proteolítica que o SKTI induz.

**Teste:** contraste direto GORE3 × SKTI na expressão da família de serino-proteases.
**Requisito:** idealmente com ponto temporal tardio (§3).

#### H5 — Splicing alternativo como mecanismo
> A exposição ao GORE3 altera padrões de splicing de genes de proteases digestivas.

**Teste:** rMATS/DEXSeq sobre alinhamento genômico.
**Nota:** é objetivo declarado do projeto e **nunca foi executado** em nenhum trabalho da série.

#### H6 — Modo de ligação não canônico
> O GORE3 (`LALAY`), por não possuir resíduo básico, inibe as tripsinas de *A. gemmatalis* por um modo de ligação distinto do P1-Asp189 canônico usado pelos demais peptídeos da série.

**Teste:** *blind docking* → docking dirigido S1 × S'2 → MD comparativa; análise de contatos por resíduo e decomposição de energia livre por resíduo.
**Falsificação:** se o GORE3 ocupar S1 de forma estável e com energia comparável à de um peptídeo com Lys/Arg em P1, H6 cai.
**Por que importa:** se confirmada, é a explicação mecanística para o GORE3 se comportar de modo diferente de GORE1/GORE2 — e abre uma rota de otimização independente da química de P1.

---

### 7. A contribuição original

O projeto precisa responder com clareza: *o que isso acrescenta ao que o grupo já publicou?*

| Já feito pelo grupo | O que este projeto acrescenta |
|---|---|
| Transcriptoma GORE2 × SKTI, *de novo*, 24 h | Transcriptoma **genoma-guiado**, resolvido por isoforma |
| Docking de peptídeos GORE | Docking **validado por MD** e energia livre |
| Cinética de inibição | Explicação **molecular** do escape |
| Atividade proteolítica total | Discriminação **por isoforma** |
| Blocos transcriptômico e estrutural separados | **Integração**: o transcriptoma escolhe o que modelar |

#### O argumento de originalidade em uma frase

> Este é o primeiro trabalho da série a usar o transcriptoma **como instrumento de seleção** para a análise estrutural, testando diretamente se as isoformas de tripsina que o inseto induz sob pressão do inibidor são aquelas que escapam dele.

Esse ciclo fechado — expressão → estrutura → afinidade → volta à expressão — é o que separa um estudo descritivo de um estudo mecanístico. E é viável precisamente porque o genoma de referência ficou disponível.

---

### 8. Riscos científicos a declarar

Honestidade sobre o que o desenho **não** resolve:

1. **Microbiota.** Parte da atividade proteolítica intestinal é bacteriana (Pilon et al., 2017). O transcriptoma do hospedeiro não a captura. Declarar como limitação.
2. **Correlação ≠ causalidade.** Expressão diferencial não prova papel funcional. RNAi ou expressão heteróloga seriam a validação — fora do escopo, mas mencionáveis como perspectiva.
3. **MD não é experimento.** Estabilidade *in silico* sustenta hipótese, não substitui cinética.
4. **Ponto único de tempo** (se mantido) limita conclusões sobre adaptação.
5. **Anotação automática.** RS_2025_08 é pipeline automático; famílias multigênicas como tripsinas podem ter erros de anotação. Curadoria manual das tripsinas é necessária.
6. **Do laboratório à planta.** Paulo et al. (2026) alertam explicitamente para a necessidade de avaliar interações metabólicas e fitotoxicidade em planta. O projeto não chega lá, e não deve prometer que chega.

---

### Referências desta seção

- Coura et al. (2022) — *Ann Appl Biol* 180(3):383-397 — doi:10.1111/aab.12740
- de Almeida Barros et al. (2021) — PMID 33200876
- de Andrade et al. (2026) — PMID 41956187
- dos Santos et al. (2025) — doi:10.14411/eje.2025.015
- Mendonça et al. (2020) — PMID 31625209
- Paulo et al. (2026) — PMID 41510779
- Pilon, F.M. et al. (2017) — PMID 28762531



---


<a id="parte-7"></a>

## Correções ao documento do projeto

Inconsistências e erros detectados na leitura integral de `Projeto-Eulalio-Pós-doc2.docx` (109 parágrafos).

Ordenado por severidade. Cada item traz o trecho original, o problema e a correção proposta.

---

### 🔴 Críticas — corrigir antes de executar ou submeter

#### C1. Tratamento errado no desenho experimental

**Onde:** §2.3 (Preparação das bibliotecas)

> "...divididas em triplicatas de controle, SKTI, benzamidina e **GORE2**."

**Problema:** o projeto é sobre **GORE3**. Este é resíduo do projeto anterior (dos Santos et al., 2025, que de fato usou GORE-2). Num documento de pós-doc submetido a avaliação, um erro no nome da molécula de estudo dentro da própria seção de desenho experimental é grave.

**Correção:** `controle, SKTI, benzamidina e GORE3`.

**Verificar também** se o restante da metodologia não carrega outros resíduos do projeto anterior.

---

#### C2. Contradição AlphaFold × Phyre2

**Onde:** §27 (objetivos) vs. §2.9 (metodologia)

- §27: "...obtenção de estruturas 3D das proteases digestivas e do peptídeo GORE3 usando estratégias como **AlphaFold** e/ou modelagem por homologia."
- §2.9: "...será modelada por homologia usando a plataforma **Phyre2**."

**Problema:** o objetivo promete uma coisa, a metodologia entrega outra. Um avaliador nota.

**Correção:** adotar AlphaFold2/ColabFold na metodologia e acrescentar o reporte de pLDDT e PAE. Manter a validação estereoquímica já prevista (ProSA-web, Ramachandran). Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §4.

---

#### C3. CGenFF aplicado a peptídeo — erro conceitual

**Onde:** §2.10 (Dinâmica Molecular)

> "O peptídeo GORE3 será parametrizado usando o CGenFF (CHARMM General Force Field), garantindo compatibilidade com o campo de força aplicado à tripsina."

**Problema:** CGenFF destina-se a **pequenas moléculas orgânicas** sem parâmetros nos campos de força biomoleculares. Um peptídeo de aminoácidos canônicos já é coberto pelo campo de força de proteína — que é mais acurado para backbone peptídico do que parâmetros CGenFF atribuídos por analogia.

A justificativa dada ("garantindo compatibilidade") é o oposto do que ocorre: usar o mesmo FF de proteína para receptor e peptídeo é que garante compatibilidade.

**Correção:**

> "O peptídeo GORE3, composto de aminoácidos canônicos, será tratado com o mesmo campo de força de proteína aplicado à tripsina, gerando-se a topologia do complexo em uma única etapa. O CGenFF será empregado apenas para a benzamidina, quando simulada como controle de pequena molécula."

---

#### C4. Montagem *de novo* ignora o genoma de referência disponível

**Onde:** §2.5 (Controle de qualidade, trimagem e montagem *De novo*)

**Problema:** o projeto foi redigido em Set/2025, quando *A. gemmatalis* não tinha genoma de referência. Isso mudou: `GCF_050436995.1` (ilAntGemm2), com anotação NCBI RS_2025_08.

Manter montagem *de novo* como estratégia principal compromete diretamente dois objetivos declarados — análise de **isoformas** e de **splicing alternativo** — que não são resolvíveis sem coordenadas genômicas.

**Correção:** reescrever a seção para pipeline genoma-guiado, mantendo a montagem *de novo* como via complementar (transcritos não anotados e de origem bacteriana). Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §1.

---

### 🟡 Médias — corrigir antes de submeter

#### C5. Réplicas técnicas desnecessárias

**Onde:** §2.3

> "...o desenho experimental terá três réplicas técnicas e três réplicas biológicas do intestino da lagarta."

**Problema:** réplicas técnicas não agregam poder estatístico em RNA-Seq Illumina e consomem orçamento de sequenciamento.

**Correção:** eliminar réplicas técnicas; usar 4–5 réplicas biológicas por tratamento. Definir explicitamente quantos intestinos compõem uma réplica biológica — informação exigida em publicação e ausente do documento.

---

#### C6. Falta o `tximport` entre quantificação e DESeq2

**Onde:** §2.7

**Problema:** o texto vai direto do pseudoalinhamento (Kallisto) para o DESeq2. Falta a etapa de agregação transcrito→gene, que também transmite os *offsets* de comprimento efetivo ao modelo. Omiti-la é erro estatístico, não formalidade.

**Correção:** inserir `tximport` explicitamente. O script já existe em `RNA-Seq-not-model/scripts/00_tximport.R`.

---

#### C7. Análise de splicing sem ferramenta especificada

**Onde:** §27 menciona "isoformas alternativas" como objetivo; a metodologia (§2.5–2.8) **não especifica nenhuma ferramenta** de splicing.

**Correção:** especificar rMATS ou DEXSeq — ambos dependentes do genoma anotado (C4). Se a análise não for feita, remover a promessa do objetivo.

---

#### C8. Ferramentas de anotação desatualizadas

**Onde:** §2.8

**Problema:** TRAPID, Blast2GO e **KOBAS 2.0** (descontinuado). Além disso, o projeto propõe usar as anotações de *H. armigera* e *B. mori* como referência para enriquecimento — desnecessário agora que a espécie tem genoma próprio.

**Correção:** eggNOG-mapper v2 para anotação; clusterProfiler para enriquecimento, com universo gênico construído da própria *A. gemmatalis*.

---

#### C9. Erro de versionamento do DESeq2

**Onde:** §2.7

> "DESeq2 versão 3.15"

**Problema:** 3.15 é versão do **Bioconductor**, não do DESeq2.

**Correção:** citar a versão real do pacote e, separadamente, a versão do Bioconductor e do R. Conferir no ambiente, não de memória.

---

#### C10. Docking de peptídeo com ferramenta de pequena molécula

**Onde:** §2.9

**Problema:** AutoDock Vina/PyRx é inadequado como método principal para ligante peptídico flexível. Além disso, a caixa de busca posicionada manualmente sobre o sítio ativo **pressupõe** o resultado.

**Correção:** protocolo em camadas com HADDOCK e/ou AlphaFold3, Vina como triagem, redocking de controle. Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §5.

**Observação:** o grupo **já usa HADDOCK** para o GORE3 (arquivos em `Desktop\LEBPP\GORE4-ate-GORE13\GORE3\`). A metodologia escrita está atrás da prática real.

---

### 🟢 Menores — redação e formatação

#### C11. Numeração de seções salta

§2.3 é seguida diretamente por §2.5. Não existe §2.4.

**Correção:** renumerar, ou verificar se uma seção foi perdida na edição (possivelmente a extração de RNA, que aparece detalhada em `Abstract-projeto-eulalio.docx` mas não no projeto).

---

#### C12. Tempos verbais misturados

A metodologia oscila entre futuro e pretérito, às vezes na mesma frase:

- §2.2: "A dieta artificial **consistia** em..." / "...os ingredientes **serão** misturados..."
- §2.2: "O ágar e a água **foram autoclavados**..."
- §2.5: "O script TrinityStats.pl **calculou** as estatísticas..."
- §2.3: "A construção de bibliotecas individuais de cDNA **utilizou** o kit..."

**Causa provável:** texto adaptado de metodologia de trabalho já concluído.

**Correção:** padronizar tudo em **futuro** — o projeto descreve trabalho a ser feito.

---

#### C13. Referências de notícia usadas para dados econômicos

**Onde:** lista de referências

- `agrourbano.com.br/release/763/perdas-com-pragas-ultrapassam-r-60-bilhoes-por-ano-no-brasil`
- `cnabrasil.org.br/publicacoes/pib-do-agronegocio-registra-crescimento-de-6-49-no-primeiro-trimestre-de-2025`

**Problema:** são fontes jornalísticas/institucionais sustentando afirmações quantitativas sobre perdas econômicas e PIB. Em texto científico, dados numéricos devem vir de fonte primária (artigo revisado por pares, relatório oficial de órgão como CONAB/EMBRAPA/IBGE, ou publicação da FAO).

**Correção:** substituir por fonte primária, ou manter e marcar explicitamente como fonte secundária, com data de acesso. Não apresentar como se fosse literatura científica.

---

#### C14. Referências sem elementos completos

Vários itens da lista carecem de volume, páginas ou DOI. Alguns exemplos:

- "FREIRES, Samya Thalyta dos Santos. Utilização de inseticidas naturais na agricultura: uma revisão. 2022." — sem indicação de tipo de obra, instituição ou veículo
- "BERLINER, 1911" — citado no texto (§19) sem entrada correspondente verificável na lista

**Correção:** completar todos os elementos e verificar cada referência. Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) §3.

---

#### C15. Grafia do nome da espécie e família

**Onde:** §2.10 (e ao longo do texto)

- `A. gemmatlis` (§ do `Abstract-projeto-eulalio.docx`) — falta o "a": **gemmatalis**
- Família oscila entre **Noctuidae** e **Erebidae** conforme a fonte citada

**Correção:** revisar a grafia e adotar uma família de forma consistente. Ver [`01_fundamentacao_teorica.md`](01_fundamentacao_teorica.md) §1.

---

#### C16. Protocolo de extração de RNA descrito para folha de soja

**Onde:** `Abstract-projeto-eulalio.docx` (documento correlato)

> "Extraction of RNA from soybean leaves using the Trizol method / Grind 100 mg of **soybean leaves** in liquid nitrogen..."

**Problema:** o protocolo colado descreve extração de **folha de soja**, não de intestino de lagarta. Texto reaproveitado sem adaptação.

**Correção:** substituir pelo protocolo real de extração de intestino médio.

---

### Resumo por prioridade

| Prioridade | Itens | Ação |
|---|---|---|
| 🔴 Antes de executar | C1, C2, C3, C4 | Comprometem resultado ou avaliação |
| 🟡 Antes de submeter | C5, C6, C7, C8, C9, C10 | Rigor metodológico |
| 🟢 Revisão de texto | C11–C16 | Redação e referências |



---


<a id="parte-8"></a>

## Notas de auditoria

Registro do que foi verificado, como, e — sobretudo — **o que não pôde ser confirmado**.

Este arquivo existe para que nada nesta base teórica seja tomado como fato sem rastro. Onde faltou evidência, está declarado como lacuna em vez de preenchido por inferência.

**Data da auditoria:** 18/07/2026

---

### 1. ✅ RESOLVIDO — sequência do GORE3

> **GORE3 = `LALAY`** (Leu-Ala-Leu-Ala-Tyr), pentapeptídeo.
> **Confirmado pelo pesquisador (Eulálio) em 18/07/2026.**

A confirmação bate com a evidência estrutural independente extraída dos arquivos PDB locais (abaixo), o que fecha a questão para efeito de modelagem.

**Fica em aberto, e não é bloqueante:** `LALAY` não consta dos peptídeos nomeados em Paulo et al. (2026) — `TGPCK`, `TGPCR`, `AVIMK`, `AVIMR`. Isso indica que o GORE3 pertence a uma linha de trabalho distinta daquela publicação, provavelmente ainda não publicada. Vale confirmar antes de escrever a introdução, porque muda como o GORE3 é posicionado em relação à literatura do grupo.

**Continua pendente:** a correspondência nome ↔ sequência do restante da série (GORE1, GORE2, GORE5–GORE13). Ver §1.1.

#### 1.1 Consequência estrutural — atenção antes do docking

`LALAY` **não possui nenhum resíduo básico** (sem Lys, Arg ou His).

Isso importa: o bolsão de especificidade **S1** da tripsina tem o **Asp189** no fundo, e é ele que ancora cadeias laterais de Lys/Arg por ponte salina. É essa a razão de os pentapeptídeos de Paulo et al. (2026) terminarem em K ou R — eles reproduzem o P1 canônico de um substrato de tripsina.

O GORE3 não pode formar essa interação. Se a cinética indica inibição competitiva (documento interno ⚠️), então uma de duas coisas:

- **(a)** ocupa a fenda catalítica por **outros subsítios** (S2/S3), via contatos hidrofóbicos — plausível, dados os dois resíduos de Leu e a Tyr aromática
- **(b)** liga-se a um **sítio distinto**, e o efeito competitivo é indireto

Isso dá sustentação concreta à investigação do sítio **S'2** conduzida na linha `analise-alosterica` — e reforça a recomendação de [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §5 de **testar S1 e S'2 explicitamente**, em vez de posicionar a caixa de docking sobre o sítio catalítico por pressuposição, como o `.docx` propõe.

Um docking cego (*blind docking*) sobre a superfície inteira da enzima, antes do docking dirigido, passa a ser recomendável neste caso específico.

#### O que havia sido encontrado nos arquivos (evidência independente)

Nenhum documento localizado declara textualmente a sequência de aminoácidos do GORE3. O que existe é evidência **estrutural indireta**: extração dos carbonos-α de arquivos PDB locais.

| Sequência extraída | Arquivo de origem | Rótulo inferido de |
|---|---|---|
| `LALAY` | `.claude\analise-alosterica\data\LALAY.pdb` | nome do arquivo |
| `LALAY` | `Desktop\LEBPP\Paper-Daniel-Pablo\RE-Docking-1BTY-trypsin-GORE3\GORE3-PEPFOLD4.pdb` | **caminho contém "GORE3"** |
| `LALAK` | `Desktop\Spodoptera-GORE4\ACR157-GORE4_NEW\cluster1_1.pdb` | caminho contém "GORE4" |
| `LALAR` | `.claude\analise-alosterica\data\LALAR.pdb` | nome do arquivo |

A extração da sequência a partir dos PDB é confiável — são os resíduos reais dos modelos. **O que não é confiável é o mapeamento nome → sequência**, que se apoia apenas em nomes de pasta.

#### Observação adicional

Há uma inconsistência de escala na série:

- GORE-2 é descrito como **tripeptídeo** (dos Santos et al., 2025)
- GORE 1-2 T é construído de **tripeptídeos VLR/VLK** (75 aa com linkers)
- `SUBMISSAO_NCBI.md` (linha 113) registra **"VLA (código interno) = GORE2"** — um tripeptídeo, consistente
- `LALAY`, `LALAK`, `LALAR` são **pentapeptídeos**
- Os peptídeos de Paulo et al. (2026) também são **pentapeptídeos**

Ou seja, a série migrou de tri- para pentapeptídeos em algum momento — o que é consistente com GORE3 = `LALAY` (5 resíduos), agora confirmado.

#### Ação ainda requerida (não bloqueante)

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

### 2. Dados de fonte interna, não publicada

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

### 3. Referências do projeto original ainda não verificadas

O projeto lista ~60 referências. Nesta auditoria foram verificadas **18** (as que constam de `referencias.bib`). As demais **não** foram conferidas.

#### Prioritárias para verificar (citadas em pontos centrais do argumento)

| Referência | Por que importa | Situação |
|---|---|---|
| ~~Coura et al. (2022), *Ann Appl Biol*~~ | Reprogramação de isoformas + histopatologia | ✅ **Verificada via Crossref** — 180(3):383-397, doi:10.1111/aab.12740. Já no `.bib` |
| ~~Silva-Júnior et al. (2021), *Arch Insect Biochem Physiol*~~ | Perfil de proteases e ligação a inibidores | ✅ **Verificada via Crossref** — 107(3), doi:10.1002/arch.21792. Já no `.bib` |
| Saikhedkar et al. (2018) | Origem conceitual dos tripeptídeos de RCL | ⬜ conferir |
| Meriño-Cabrera et al. (2018, 2019) | Cinética de inibição | ⬜ conferir |
| Laskowski & Kato (1980); Laskowski & Qasim (2000) | Base do modelo mecanístico | ⬜ conferir |

#### Problemas específicos detectados

- **"Berliner, 1911"** — citado no texto (§19) mas **sem entrada correspondente na lista de referências**
- **"Barros et al., 2022"** — ambíguo; há vários trabalhos de Barros, e a lista não permite desambiguar
- **"FREIRES (2022)"** — sem tipo de obra, instituição ou veículo
- **Duas referências são links de notícia** (`agrourbano.com.br`, `cnabrasil.org.br`) usados para sustentar dados econômicos — ver [`06_correcoes_projeto.md`](06_correcoes_projeto.md) C13
- **"Greene (1976)"** — protocolo de criação; conferir dados completos
- **"Cepas et al., 2016, 2017"** (eggNOG) — a grafia correta do sobrenome é provavelmente **Huerta-Cepas**

**Nenhuma dessas foi incluída em `referencias.bib`.** Só entram após verificação.

---

### 4. O que foi verificado e como

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

### 5. O que NÃO foi verificado

Declarado para que ninguém assuma cobertura que não existe:

1. **Métricas do genoma** — N50, tamanho, nível de montagem, BUSCO de `GCF_050436995.1`. Nenhum número foi reproduzido nesta base teórica justamente por isso. **Conferir na página do assembly antes de escrever a metodologia.**
2. **Campo de força usado no MD de GORE 1-2 T** — o resumo de de Andrade et al. (2026) menciona 100 ns de MD mas não especifica o campo de força. Essa informação é necessária para a decisão CHARMM36m × AMBER ([`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §7). **Requer leitura do texto completo.**
3. **Conteúdo dos arquivos HADDOCK** (`.tgz`) — confirmada apenas a existência, não os resultados
4. **Valores da cotação Macrogen** — não abertos, não reproduzidos
5. **~42 referências** do projeto original (ver §3)
6. **Dados de *S. frugiperda*** — fora do escopo definido; não auditados
7. **Se o experimento GORE3 já foi coletado** — só se sabe que o sequenciamento está contratado

---

### 6. Decisões editoriais tomadas nesta base

Para transparência sobre escolhas que afetam o texto:

1. **Não foi reproduzido nenhum número sem fonte verificada.** Onde o dado existia mas a fonte não pôde ser confirmada, marcou-se ⚠️.
2. **Família taxonômica:** registrada a divergência Noctuidae/Erebidae em vez de escolher silenciosamente uma delas.
3. **Kᵢ e IC₅₀ não foram comparados diretamente** na tabela de progressão da série — são parâmetros diferentes, com ressalva explícita.
4. **Não foi afirmado que "GORE3 é melhor que GORE1/GORE2"** como fato. Está apresentado como alegação de fonte interna a ser testada.
5. **Não foi inventado nenhum valor de versão de software.** O documento de metodologia orienta conferir versões na instalação.

---

### 7. Próximas ações de verificação

Em ordem de prioridade:

| # | Ação | Bloqueia |
|---|---|---|
| 1 | Confirmar sequência do GORE3 com a supervisora | Toda a modelagem estrutural |
| 2 | Obter IC₅₀/Kᵢ quantificado do GORE3 | Escrita da introdução |
| 3 | Ler texto completo de de Andrade et al. (2026) para o campo de força | Decisão de MD |
| 4 | Conferir métricas do assembly `GCF_050436995.1` | Escrita da metodologia |
| 5 | Verificar as ~44 referências restantes | Submissão |
| 6 | Confirmar status do sequenciamento na Macrogen | Cronograma |



---
