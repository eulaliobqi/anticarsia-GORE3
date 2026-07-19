# Fundamentação teórica

Base conceitual para a introdução. Cada afirmação traz a fonte; o que não pôde ser verificado está marcado ⚠️ e listado em [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md).

---

## 1. *Anticarsia gemmatalis* e o problema agronômico

A lagarta-da-soja, *Anticarsia gemmatalis* Hübner, é um dos principais desfolhadores da soja no Brasil. A literatura recente do próprio grupo a descreve consistentemente como "uma das mais importantes pragas desfolhadoras da soja" (Paulo et al., 2026; de Andrade et al., 2026).

Um ponto taxonômico que aparece de forma inconsistente na literatura e merece atenção na escrita: a espécie é atribuída ora a **Noctuidae**, ora a **Erebidae**. Ambas as grafias aparecem em publicações recentes revisadas por pares — Paulo et al. (2026) e dos Santos et al. (2025) usam Noctuidae; Pilon et al. (2018) e Pezenti et al. (2023) usam Erebidae. A classificação em Erebidae reflete a revisão filogenética mais moderna de Noctuoidea. **Recomendação:** adotar Erebidae e mencionar Noctuidae como sinonímia de uso corrente, ou simplesmente manter consistência interna no texto.

### Controle atual e suas limitações

O manejo se apoia hoje em duas frentes principais:

- **Plantas Bt**, expressando toxinas Cry de *Bacillus thuringiensis*. A eficácia depende da ligação da toxina a receptores específicos no epitélio do intestino médio — aminopeptidases N (APN), fosfatase alcalina, caderina. Em *A. gemmatalis*, dez sequências de APN foram identificadas no transcriptoma e sete delas confirmadas experimentalmente como ligantes de Cry1Ac por *ligand blotting* e espectrometria de massas (Lanzaro et al., 2024). Mutações nesses receptores estão entre os mecanismos de resistência — o que torna o mapeamento desses alvos parte da estratégia de contenção.
- **Inseticidas químicos**, com os custos ambientais e de saúde conhecidos, e sob pressão crescente de resistência.

É esse duplo gargalo — resistência a Bt e passivo ambiental dos químicos — que sustenta a busca por moléculas alternativas.

---

## 2. Digestão proteica no intestino médio de Lepidoptera

O intestino médio de lepidópteros é um ambiente **alcalino**, condição que define quais enzimas operam ali e que precisa ser respeitada em qualquer modelagem estrutural. Tripsinas purificadas a partir de bactérias do intestino de *A. gemmatalis* mostraram-se ativas na faixa de **pH 7,5–10**, com atividade máxima a 40 °C e massa molecular de aproximadamente 25 kDa (Pilon et al., 2017).

> **Consequência prática para o projeto:** protonar as estruturas em pH alcalino antes do docking/MD, e não em pH 7,0. Os arquivos locais já protonados a pH 8,2 (ver [`04_viabilidade.md`](04_viabilidade.md)) estão corretos nesse aspecto.

As **serino-proteases do tipo tripsina** respondem pela digestão primária. Duas características importam para o trabalho:

1. **Multiplicidade de isoformas.** Pilon et al. (2017) concluíram pela existência de isoformas distintas de tripsina no intestino de *A. gemmatalis*, notando que as enzimas de origem bacteriana não dependiam de íons cálcio — ao contrário das tripsinas solúveis e insolúveis já caracterizadas na própria lagarta.
2. **Contribuição da microbiota.** Parte da atividade proteolítica intestinal vem de bactérias simbiontes — *Bacillus cereus*, *Enterococcus mundtii*, *E. gallinarum*, *Staphylococcus xylosus* foram isoladas e tiveram suas tripsinas purificadas (Pilon et al., 2017). Isso significa que o transcriptoma do hospedeiro não captura toda a capacidade proteolítica do sistema — uma limitação a declarar explicitamente.

### Arquitetura do sítio ativo

A tríade catalítica canônica das serino-proteases — **His57, Asp102, Ser195** (numeração do quimotripsinogênio) — e o bolsão de especificidade **S1**, cujo **Asp189** no fundo determina a preferência da tripsina por resíduos básicos (Lys/Arg), são os elementos estruturais centrais. Paulo et al. (2026) identificaram exatamente esse conjunto — His57, Asp102, Ser195, Asp189 e Gly197 — como os resíduos críticos na ligação de peptídeos inibidores às tripsinas de *A. gemmatalis*.

Esse é o alvo estrutural do GORE3.

---

## 3. Inibidores de protease como estratégia de defesa

Inibidores de protease (IPs) são proteínas amplamente distribuídas em plantas, onde atuam como agentes antinutricionais contra herbívoros. Nas leguminosas, os IPs se acumulam de forma constitutiva em sementes e podem ser induzidos em folhas após dano (revisão: Sultana et al., 2022).

O efeito sobre o inseto é indireto mas eficaz: ao bloquear as proteases digestivas, o IP reduz a liberação de aminoácidos essenciais, o que se traduz em **atraso no desenvolvimento, deformidades e queda de fertilidade** (Sultana et al., 2022).

Os dois IPs de soja mais estudados nesse contexto:

- **SKTI** (*Soybean Kunitz Trypsin Inhibitor*) — inibidor tipo Kunitz, alvo primário de tripsina
- **SBBI** (*Soybean Bowman-Birk Inhibitor*) — inibidor bifuncional tripsina/quimotripsina

### O resultado que revela o problema

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

## 4. O modelo de Laskowski

O mecanismo canônico de inibição de serino-proteases por IPs proteicos é o **modelo padrão de Laskowski**: o inibidor se apresenta como um **pseudo-substrato**, encaixando seu *reactive center loop* (RCL) no sítio ativo da enzima. Forma-se um complexo de altíssima afinidade em que a hidrólise da ligação cindível é extraordinariamente lenta, de modo que a enzima fica sequestrada em vez de clivar o inibidor produtivamente.

Esse modelo é a base conceitual de todo o desenho racional de peptídeos do grupo: se é o **laço** que faz o trabalho de reconhecimento, então um peptídeo curto que reproduza esse laço deveria reter parte da capacidade inibitória — sem o custo de produzir uma proteína inteira.

Foi precisamente essa a lógica aplicada por Saikhedkar et al. (2018) ⚠️ e, no grupo, por de Almeida Barros et al. (2021) e Paulo et al. (2026).

---

## 5. Do inibidor proteico ao peptídeo mimético

Inibidores proteicos completos enfrentam obstáculos práticos: custo de produção, estabilidade, e — no caso de expressão transgênica — o tamanho do transgene e possíveis efeitos colaterais na planta.

Peptídeos curtos desenhados a partir do RCL oferecem uma alternativa: síntese barata, possibilidade de produção recombinante, e espaço para otimização racional guiada por docking.

O grupo demonstrou que a estratégia funciona. Paulo et al. (2026) desenharam quatro pentapeptídeos inspirados nos RCLs de **BPTI** e **SKTI** — `TGPCK`, `TGPCR`, `AVIMK`, `AVIMR` — e confirmaram por ensaios cinéticos que **todos** atuam como inibidores competitivos das tripsinas de *A. gemmatalis*, com `TGPCK` apresentando a maior eficácia.

O trabalho também trouxe um achado mecanístico fino: a afinidade correlacionou-se com o **tipo** de interação química formada. Ligações **pi-sigma** associaram-se a maior afinidade (AVIMK), enquanto contatos alquil/pi-alquil e C–H associaram-se a menor afinidade (AVIMR, TGPCK). Isso sugere que a otimização de peptídeos da série não deve mirar apenas "mais contatos", mas contatos de natureza específica.

O detalhamento da série GORE está em [`02_estado_da_arte_GORE.md`](02_estado_da_arte_GORE.md).

---

## 6. Adaptação e resistência — a tensão central

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

## 7. Contexto de defesa da planta

Vale registrar, para posicionamento, que a resistência da soja a *A. gemmatalis* não se resume a IPs. Um trabalho recente do mesmo ambiente institucional mostrou que genótipos resistentes acumulam **rutina** e seu derivado O-metilado **narcisina**, e que a O-metilação aumenta acentuadamente a toxicidade: a rutina metilada causou cerca de **95% de mortalidade em 5 dias**, contra ~17 dias para atingir letalidade comparável com a rutina não metilada (de Assis et al., 2026). O docking contra as 70 proteínas mais abundantes do intestino larval indicou ligação de ambos os flavonóis a proteases, P450s e GSTs.

Isso reforça um ponto conceitual útil: **proteases digestivas e maquinaria de detoxificação são alvos convergentes** de estratégias defensivas bastante distintas. O GORE3 ataca o primeiro eixo; a resposta do inseto mobiliza o segundo.

---

## Referências desta seção

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
