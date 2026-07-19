# Lacunas, hipóteses e contribuição original

O que ainda não se sabe, o que este projeto pode testar, e o que o diferencia do que o grupo já publicou.

Serve de base para as seções de **justificativa** e **objetivos** da introdução.

---

## 1. A lacuna central — por que as duas espécies respondem de forma oposta

### O fato

O resumo interno do projeto registra que o GORE3 produz respostas divergentes:

| Espécie | Atividade proteolítica | Interpretação |
|---|---|---|
| *S. frugiperda* | **Superexpressão de proteases** | Resposta compensatória bem-sucedida |
| *A. gemmatalis* | **Redução** da atividade + detoxificação intensificada | Compensação falha ou é redirecionada |

⚠️ Dado de documento interno, não publicado. Precisa de confirmação.

### Por que isso importa

O mecanismo de escape mais bem documentado em Lepidoptera é a **hiperprodução compensatória de proteases**. Mendonça et al. (2020) observaram exatamente isso em *A. gemmatalis* exposta ao SKTI: inibição no dia 12, **aumento** de atividade de tripsina no dia 15.

Se o GORE3 realmente impede essa compensação em *A. gemmatalis*, ele estaria contornando o principal mecanismo de resistência a inibidores de protease. Isso é uma alegação forte — e testável.

### A pergunta

**A ausência de compensação em *A. gemmatalis* é incapacidade ou redirecionamento?**

Duas possibilidades com consequências opostas:

- **(a) Incapacidade** — o inseto não consegue montar a resposta. O GORE3 seria robusto contra adaptação. Ótima notícia para desenvolvimento de produto.
- **(b) Redirecionamento** — o inseto abandonou a via proteolítica e investiu em detoxificação (o aumento de SOD/CAT/POX/GST aponta nessa direção). Nesse caso a resistência apenas mudou de endereço, e surgiria por outro caminho sob pressão de seleção.

**Transcriptômica distingue as duas.** Bioquímica de atividade total, não.

---

## 2. Lacuna — isoformas, não genes

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

### Não é hipótese solta — já há evidência proteica

Coura et al. (2022) documentaram exatamente esse fenômeno em *A. gemmatalis* alimentada com inibidores de protease: **reprogramação extensa de isoformas proteicas**, acompanhada de alterações histopatológicas no intestino médio.

Ou seja, o grupo já demonstrou no nível **de proteína** que a troca de isoformas acontece. O que falta é a contrapartida no nível de **transcrito**, resolvida por isoforma e ligada à estrutura — que é o que este projeto pode entregar.

**Requisito metodológico:** só é possível resolver isso com **quantificação em nível de isoforma sobre genoma anotado** — o que exige a migração para pipeline genoma-guiado ([`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §1). Com montagem *de novo*, isoformas e parálogos são indistinguíveis.

Nenhum trabalho da série GORE fez essa análise.

---

## 3. Lacuna — o tempo

Todos os transcriptomas da série são de **ponto único**:

- dos Santos et al. (2025): **24 h** de exposição
- O projeto atual: ponto único não especificado

Mas a literatura do próprio grupo mostra que a resposta é **dependente do tempo**: em Mendonça et al. (2020), a inibição apareceu no dia 12 e se **inverteu** no dia 15.

Um único ponto em 24 h captura a resposta imediata ao estresse. **Não captura adaptação.** E adaptação é justamente o problema que motiva a busca por inibidores melhores.

**Recomendação:** se houver qualquer margem orçamentária, incluir um **segundo ponto temporal tardio**. O ganho científico de dois pontos (ex.: 24 h e 7–15 dias) supera o de mais réplicas num único ponto, porque permite distinguir *resposta* de *adaptação* — que é a pergunta que ninguém na série respondeu.

Se não houver margem, escolher o ponto **com justificativa explícita** e declarar a limitação.

---

## 4. Lacuna — o docking nunca foi validado por MD para o GORE3

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

## 5. Lacuna — S1 ou S'2?

O grupo trabalha com duas hipóteses de sítio de ligação:

- **S1** — sítio de especificidade canônico, ancorado no Asp189; mecanismo competitivo clássico, consistente com toda a cinética publicada
- **S'2** — sítio do lado dos produtos (Tyr39/His40/Tyr151 na numeração da referência local), investigado na linha `analise-alosterica`

A cinética publicada indica **inibição competitiva** para GORE1, GORE2, GORE 1-2 T e os peptídeos RCL — o que é consistente com ocupação de S1 ou de região sobreposta ao sítio ativo.

Mas a metodologia do projeto **assume** S1 ao posicionar a caixa de docking manualmente sobre o sítio catalítico. Isso não testa a hipótese; pressupõe-a.

**Recomendação:** testar ambos explicitamente. Um resultado negativo para S'2 é informativo e fecha a questão; um positivo seria um achado mecanístico relevante.

---

## 6. Hipóteses testáveis

Formuladas para serem falsificáveis, cada uma com o teste correspondente.

### H1 — Escape por isoforma
> *A. gemmatalis* exposta ao GORE3 induz isoformas específicas de tripsina cuja arquitetura de sítio ativo reduz a afinidade pelo peptídeo.

**Teste:** quantificação por isoforma → modelagem das isoformas induzidas → docking/MD comparativo entre induzidas e reprimidas.
**Falsificação:** se as isoformas induzidas ligarem o GORE3 tão bem quanto as reprimidas, H1 cai.
**Apoio prévio:** Coura et al. (2022) já demonstraram reprogramação de isoformas proteicas em *A. gemmatalis* sob inibidores de protease.

### H2 — Redirecionamento para detoxificação
> A resposta de *A. gemmatalis* ao GORE3 privilegia vias de detoxificação e antioxidantes em detrimento da compensação proteolítica.

**Teste:** enriquecimento funcional (GO/KEGG) comparando GORE3 × SKTI × benzamidina; expressão de P450, GST, UGT, SOD, CAT, POX.
**Apoio prévio:** dos Santos et al. (2025) já mostraram resposta de detoxificação mais forte para GORE-2 que para SKTI.

### H3 — Persistência do complexo
> O complexo tripsina–GORE3 permanece estável em escala de 100 ns, com ligações de hidrogênio persistentes aos resíduos catalíticos.

**Teste:** 3 × 100 ns de MD; RMSD, ocupância de ligações de H, distâncias à tríade His57/Asp102/Ser195 e ao Asp189.
**Falsificação:** dissociação ou perda de contato com o sítio ativo.

### H4 — Superioridade mecanística sobre o SKTI
> O GORE3 evita a compensação proteolítica que o SKTI induz.

**Teste:** contraste direto GORE3 × SKTI na expressão da família de serino-proteases.
**Requisito:** idealmente com ponto temporal tardio (§3).

### H5 — Splicing alternativo como mecanismo
> A exposição ao GORE3 altera padrões de splicing de genes de proteases digestivas.

**Teste:** rMATS/DEXSeq sobre alinhamento genômico.
**Nota:** é objetivo declarado do projeto e **nunca foi executado** em nenhum trabalho da série.

---

## 7. A contribuição original

O projeto precisa responder com clareza: *o que isso acrescenta ao que o grupo já publicou?*

| Já feito pelo grupo | O que este projeto acrescenta |
|---|---|
| Transcriptoma GORE2 × SKTI, *de novo*, 24 h | Transcriptoma **genoma-guiado**, resolvido por isoforma |
| Docking de peptídeos GORE | Docking **validado por MD** e energia livre |
| Cinética de inibição | Explicação **molecular** do escape |
| Atividade proteolítica total | Discriminação **por isoforma** |
| Blocos transcriptômico e estrutural separados | **Integração**: o transcriptoma escolhe o que modelar |

### O argumento de originalidade em uma frase

> Este é o primeiro trabalho da série a usar o transcriptoma **como instrumento de seleção** para a análise estrutural, testando diretamente se as isoformas de tripsina que o inseto induz sob pressão do inibidor são aquelas que escapam dele.

Esse ciclo fechado — expressão → estrutura → afinidade → volta à expressão — é o que separa um estudo descritivo de um estudo mecanístico. E é viável precisamente porque o genoma de referência ficou disponível.

---

## 8. Riscos científicos a declarar

Honestidade sobre o que o desenho **não** resolve:

1. **Microbiota.** Parte da atividade proteolítica intestinal é bacteriana (Pilon et al., 2017). O transcriptoma do hospedeiro não a captura. Declarar como limitação.
2. **Correlação ≠ causalidade.** Expressão diferencial não prova papel funcional. RNAi ou expressão heteróloga seriam a validação — fora do escopo, mas mencionáveis como perspectiva.
3. **MD não é experimento.** Estabilidade *in silico* sustenta hipótese, não substitui cinética.
4. **Ponto único de tempo** (se mantido) limita conclusões sobre adaptação.
5. **Anotação automática.** RS_2025_08 é pipeline automático; famílias multigênicas como tripsinas podem ter erros de anotação. Curadoria manual das tripsinas é necessária.
6. **Do laboratório à planta.** Paulo et al. (2026) alertam explicitamente para a necessidade de avaliar interações metabólicas e fitotoxicidade em planta. O projeto não chega lá, e não deve prometer que chega.

---

## Referências desta seção

- Coura et al. (2022) — *Ann Appl Biol* 180(3):383-397 — doi:10.1111/aab.12740
- de Almeida Barros et al. (2021) — PMID 33200876
- de Andrade et al. (2026) — PMID 41956187
- dos Santos et al. (2025) — doi:10.14411/eje.2025.015
- Mendonça et al. (2020) — PMID 31625209
- Paulo et al. (2026) — PMID 41510779
- Pilon, F.M. et al. (2017) — PMID 28762531
