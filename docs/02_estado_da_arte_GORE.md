# Estado da arte — a série GORE

Reconstrução da linhagem de peptídeos inibidores desenvolvida pelo grupo (LBBM / UFV, coordenação Profa. Maria Goreti de Almeida Oliveira), a partir do que está **publicado e verificável**.

O nome "GORE" é uma homenagem à supervisora (Goreti).

---

## 1. Linha do tempo publicada

### GORE1 e GORE2 — a prova de conceito (2021)

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

### GORE2 sob a ótica transcriptômica (2025)

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

### GORE 1-2 T — o salto para produção recombinante (2026)

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

### Peptídeos derivados de RCL — a geração pentapeptídica (2026)

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

## 2. Onde o GORE3 se encaixa

Aqui é preciso separar o que está publicado do que está em documento interno.

### Sequência

> **GORE3 = `LALAY`** — Leu-Ala-Leu-Ala-Tyr, pentapeptídeo.
> Confirmado pelo pesquisador em 18/07/2026.

Composição relevante para a análise estrutural: **nenhum resíduo básico**. Dois Leu (hidrofóbicos), dois Ala (pequenos), uma Tyr (aromática, com hidroxila).

Isso distingue o GORE3 dos demais peptídeos da série já publicados, que terminam em Lys ou Arg justamente para ocupar o subsítio S1 da tripsina — ancorado no Asp189. O GORE3 não pode formar essa ponte salina, o que torna seu modo de ligação uma pergunta em aberto e não uma premissa. Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) §1.1 e [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) §5.

### O que consta do resumo interno (`GORE3-abstract.docx`)

> ⚠️ **Fonte não revisada por pares.** Os dados abaixo vêm do resumo do próprio projeto e de comunicação interna do grupo. Devem ser tratados como resultados preliminares até publicação.

- GORE3 é descrito como inibidor de serino-proteases derivado do modelo do **SKTI**
- Efeitos em *S. frugiperda* e *A. gemmatalis*: atraso no ciclo larval, redução do peso pupal, queda da eficiência alimentar, mortalidade relevante
- Inibição significativa de proteases tripsina-like
- Indução de resposta antioxidante: aumento de **SOD, CAT, POX, GST**
- Cinética *in vitro*: **inibição competitiva**, dependente de concentração, **IC₅₀ na faixa micromolar**
- Atraso de desenvolvimento relatado de até **50 dias** (documento `Abstract-projeto-eulalio.docx`)

### O achado que mais importa

O mesmo documento registra um **contraste entre espécies**:

| Espécie | Resposta ao GORE3 |
|---|---|
| *S. frugiperda* | **Superexpressão de proteases** — resposta compensatória à inibição |
| *A. gemmatalis* | **Redução** da atividade proteolítica + intensificação das rotas de detoxificação |

E acrescenta que esses dados **diferem** dos observados com GORE1 e GORE2.

Se confirmado, isso é o resultado mais interessante de toda a série: o GORE3 conseguiria, em *A. gemmatalis*, escapar do mecanismo de compensação que derrotou o SKTI no experimento de Mendonça et al. (2020). É uma afirmação forte, que a transcriptômica pode sustentar ou refutar de forma direta.

Ver [`05_lacunas_e_hipoteses.md`](05_lacunas_e_hipoteses.md) §1.

---

## 3. Progressão da potência ao longo da série

Compilando os valores publicados — com a ressalva de que **Kᵢ e IC₅₀ não são diretamente comparáveis** e que as condições de ensaio variam:

| Molécula | Parâmetro | Valor | Fonte |
|---|---|---|---|
| GORE1 | Kᵢ | 0,49 mM | PMID 33200876 |
| GORE2 | Kᵢ | 0,10 mM | PMID 33200876 |
| GORE 1-2 T | Kᵢ aparente | ≈ 100 µM (0,10 mM) | PMID 41956187 |
| GORE3 | IC₅₀ | "faixa micromolar" ⚠️ | Documento interno |

A tendência é de ganho de potência, mas **o valor do GORE3 não está quantificado em fonte verificável** e "faixa micromolar" é vago demais para entrar num texto científico. Obter o número exato é pendência para a introdução.

---

## 4. Peptídeos da série com estrutura 3D disponível localmente

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

## 5. Síntese — o que a série já estabeleceu

1. Peptídeos curtos derivados de RCL **funcionam** como inibidores competitivos de tripsinas de *A. gemmatalis* — resultado replicado em três publicações independentes do grupo
2. A potência melhorou ao longo das gerações, de Kᵢ sub-milimolar para micromolar
3. A produção **recombinante** é viável (GORE 1-2 T, ≈4,6 kDa)
4. O efeito *in vivo* é real: atraso de desenvolvimento, queda de peso pupal, mortalidade
5. A resposta do inseto envolve **detoxificação e estresse oxidativo**, não apenas proteases
6. O docking identifica consistentemente o engajamento do sítio catalítico e dos subsítios S1–S3

## 6. O que a série ainda não estabeleceu

1. **Se o inseto se adapta ao GORE3 ao longo do tempo** — todos os transcriptomas são de ponto único
2. **Quais isoformas específicas de tripsina são induzidas** e se elas escapam do inibidor
3. **Por que as duas espécies respondem de forma oposta**
4. **Se as interações vistas no docking persistem** em escala de tempo relevante para as isoformas do GORE3 (o MD de 100 ns existe para GORE 1-2 T, não para GORE3 ⚠️)
5. **Splicing alternativo** — mencionado como objetivo, nunca executado na série
6. **Comportamento em planta** — fitotoxicidade e interações metabólicas (ressalva explícita de Paulo et al., 2026)

Os itens 1 a 5 são endereçáveis por este pós-doc.

---

## Referências desta seção

- de Almeida Barros et al. (2021) — *Pest Manag Sci* — PMID 33200876
- de Andrade et al. (2026) — *Int J Biol Macromol* — PMID 41956187
- dos Santos et al. (2025) — *Eur J Entomol* 122:119-136 — doi:10.14411/eje.2025.015
- Mendonça et al. (2020) — *Arch Insect Biochem Physiol* — PMID 31625209
- Paulo et al. (2026) — *Arch Insect Biochem Physiol* — PMID 41510779 (PMC12784448)
