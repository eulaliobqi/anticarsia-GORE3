---
Documento vivo — artigo 2 do pós-doutorado GORE3 (Eulálio, UFV/INCT-IPP).
Escopo: o teste mecanístico da família de serino-proteases (hipótese H1)
e, eventualmente, os contrastes cabeça-a-cabeça (GORE3×Benzamidina,
GORE3×SKTI) adiados do artigo 1 (`artigo.md`). Separado em diretório
próprio (`paper-2/`) em 01/08/2026 por decisão explícita do usuário — ver
memória do projeto. Dados do artigo 1 (expressão diferencial FASE 5,
splicing FASE 6, anotação funcional FASE 7) são reaproveitados lendo
`resultados/` na raiz do repo, não duplicados aqui.
Última atualização: 01/08/2026 (FASE 9, Blocos A-E concluídos; Bloco F —
ponte estrutural — adiado, escopo ainda não decidido).
---

# Artigo 2 — Análise dirigida da família de serino-proteases (FASE 9, hipótese H1)

## Resumo

*[Não escrito — o Bloco F da FASE 9 (ponte estrutural) ainda está com
escopo indefinido, e o trabalho de FASE 9.5/10 (cabeça-a-cabeça) não
começou. Pela convenção já estabelecida neste projeto, não se fabrica
Resumo/Introdução antes dos resultados reais existirem.]*

## 1. Contexto e motivação

O artigo 1 (`artigo.md`, FASES 1-7) caracterizou expressão diferencial e
splicing alternativo para GORE3, SKTI e Benzamidina vs. Controle, cada
um independentemente. Encerrou com um achado real, não planejado: o
evento de splicing mais significativo do próprio contraste GORE3 (FASE
6, §3.19, Fig. 19) cai num gene com domínio Pfam PF00089 (clã
tripsina/quimotripsina). Este artigo segue esse fio até a conclusão
originalmente proposta pelo projeto — o teste mecanístico (H1): o GORE3
induz uma **troca da isoforma dominante de tripsina**, distinguível de
uma simples mudança de nível de expressão, em genes que são tripsinas
digestivas de verdade (não qualquer gene com domínio do clã
quimotripsina)?

## 2. Métodos

### 2.1 Curadoria primária: do domínio Pfam à tripsina digestiva (Bloco B)

O Pfam PF00089 (anotação da FASE 7, Mistry et al. 2021) cobre o clã
quimotripsina inteiro — 316 genes no genoma todo — não especificamente
tripsinas digestivas; proteases de domínio CLIP, ativadores de
profenoloxidase e outros membros não-digestivos da família carregam o
mesmo domínio. Uma primeira camada de curadoria foi aplicada: a proteína
representativa de cada um dos 316 genes foi escaneada contra as duas
assinaturas de sequência PROSITE que juntas distinguem serino-proteases
da família tripsina (Sigrist et al. 2026, PMID 41263099) —
**PS00134** (sítio ativo histidina,
`[LIVM]-[ST]-A-[STAG]-H-C`) e **PS00135** (sítio ativo serina,
`[DNSTAGC]-[GSTAPIMVQH]-x(2)-G-[DE]-S-G-[GS]-[SAPHV]-[LIVMFYWH]-
[LIVMFYSTANQH]`), ambas verificadas contra a entrada atual do
PROSITE/InterPro, não de memória. **168/316 genes carregam os dois
padrões.** Código: `codigo/fase9_blocoB/prosite_scan.py`.

### 2.2 Confirmação estrutural da tríade catalítica por MSA (Bloco C)

**Uma correção metodológica real, feita antes de aceitar qualquer
resultado.** Uma primeira tentativa alinhou as proteínas representativas
INTEIRAS dos 168 candidatos mais duas sequências de referência
(tripsinogênio bovino, PDB 1TGN cadeia A, obtido do RCSB; e
`XP_075977317.1`, a tripsina de *A. gemmatalis* já confirmada no
diagnóstico da origem do LALAY deste projeto) com MAFFT (`--auto`).
**Zero dos 168 candidatos** manteve o His/Ser catalítico na coluna do
alinhamento correspondente a nenhuma das duas referências — alinhamento
global de sequência inteira é inadequado aqui porque proteínas com
PF00089 variam substancialmente em arquitetura de domínio (ex. um
domínio CLIP N-terminal precede o domínio tripsina em vários candidatos,
confirmado diretamente na tabela de domínio do `hmmscan` da FASE 7).
**Corrigido:** o alinhamento foi restrito ao envelope do domínio Pfam
PF00089 (± 5 aa de margem) por sequência, extraído das coordenadas do
domtblout do `hmmscan` da FASE 7 — prática padrão para MSA entre
proteínas com arquitetura de domínio variável, não um ajuste ad-hoc.
Código: `codigo/fase9_blocoC/build_domain_input.py`,
`codigo/fase9_blocoC/run_mafft.sh`.

O alinhamento corrigido (MAFFT `--auto`, restrito ao domínio) foi usado
para localizar, em cada uma das duas referências, a coluna exata do
alinhamento do His catalítico (match PS00134) e do Ser (match PS00135);
as duas referências concordaram na mesma coluna em ambos os casos,
confirmando a validade da checagem cruzada. Cada um dos 168 candidatos
foi então checado quanto a His/Ser nessas mesmas colunas equivalentes às
referências (não apenas "o motivo em algum lugar da sequência", que o
Bloco B já havia estabelecido). **166/168 candidatos passam.** Um
segundo bug, não relacionado (erro de índice no próprio script de
verificação desta sessão, não sinal biológico), foi encontrado e
corrigido antes de aceitar esse número — ver comentários no código de
`codigo/fase9_blocoC/verify_triad_columns.py` para o relato completo.

**Uma limitação declarada, não escondida:** o terceiro membro da tríade
catalítica (Asp102) não tem uma assinatura de sequência PROSITE única e
igualmente específica; sua confirmação rigorosa exige validação
geométrica 3D (distâncias Ser-Oγ⋯His-Nε2 e His-Nδ1⋯Asp-Oδ1, ângulo
Ser-His-Asp) sobre uma estrutura predita ou experimental — adiada para
o Bloco F (ponte estrutural), não realizada aqui.

### 2.3 Filogenia da família curada (Bloco D)

Os 166 genes curados (+ as duas referências) foram realinhados em nível
de domínio, aparados com **trimAl** (`-automated1`), e uma árvore de
máxima verossimilhança foi construída com **IQ-TREE 3** (Wong et al.
2026, PMID 42085559 — confirmado via busca bibliográfica própria desta
sessão como o release principal atual, não a v2 herdada de scripts de
projetos anteriores) usando **ModelFinder** para seleção automática de
modelo, 1000 réplicas de bootstrap ultrarrápido e 1000 réplicas SH-aLRT.
Enraizada na referência de tripsinogênio bovino (1TGN_A) como outgroup —
uma única sequência distantemente relacionada (mamífero vs. inseto),
declarada explicitamente como uma escolha simples de enraizamento, não
uma amostragem rigorosa de outgroup. Código: `codigo/fase9_blocoD/`
(comandos trimAl + IQ-TREE3, rodados no servidor, ver tabela de
Reprodutibilidade).

### 2.4 Cruzamento com expressão e splicing (Bloco E) — o teste de H1

Para os 166 genes curados, a pertinência aos conjuntos de genes
diferencialmente expressos (FASE 5, DESeq2/R) e com splicing
significativo (FASE 6, rMATS-turbo ∪ MAJIQ) foi checada por contraste
(Benzamidina/SKTI/GORE3 vs. Controle), reaproveitando diretamente as
tabelas de resultado já calculadas e já versionadas do artigo 1
(`resultados/fase5_blocoD/`, `resultados/fase6_blocoD/`) — nenhuma
reanálise de expressão ou splicing foi feita. Cada gene curado foi
classificado por contraste como: **nível+identidade** (DE E splicing
significativo — o sinal mais forte para H1), **só nível** (DE, sem
splicing), **só identidade** (splicing, sem DE), ou **sem mudança
significativa**. Código: `codigo/fase9_blocoE/cross_reference_h1.py`.

## 3. Resultados

### 3.1 Funil de curadoria

| Etapa | Genes restantes | Método |
|---|---:|---|
| Hits Pfam PF00089 (FASE 7, clã quimotripsina inteiro) | 316 | `hmmscan` |
| + PROSITE PS00134 & PS00135 (Bloco B) | 168 | motivo de sequência |
| + His/Ser na coluna equivalente à referência (Bloco C) | **166** | MSA restrita ao domínio |

### 3.2 Filogenia

168 táxons (166 genes curados + 2 referências), modelo de melhor ajuste
por BIC: **Q.PFAM+R7** (matriz empírica treinada em alinhamentos Pfam
com modelo FreeRate de 7 categorias — selecionado pelo ModelFinder, não
assumido), comprimento total da árvore 52,633, log-verossimilhança
−24396,35. Arquivos da árvore:
`resultados/fase9_blocoD/tree/curated_family.{treefile,contree}`.
Topologia ainda não foi inspecionada manualmente para resolver
parálogos verdadeiros de possível erro de anotação (docs/07 §10, item
3) — pendente.

### 3.3 O cruzamento de H1

**Tabela 1 | Genes de tripsina curados (n=166) por status DE/splicing, por contraste vs. Controle.**

| Contraste | Nível + identidade (DE ∩ splicing) | Só nível (DE) | Só identidade (splicing) | Sem mudança significativa | Qualquer mudança |
|---|---:|---:|---:|---:|---:|
| Benzamidina | 0 | 5 | 3 | 158 | 8/166 |
| SKTI | 1 | 37 | 1 | 127 | 39/166 |
| GORE3 | 1 | 41 | 3 | 121 | 45/166 |

**O candidato mais forte para H1 encontrado nesta sessão: `gene-LOC142975421`
é o único gene de tripsina curado, em qualquer contraste, mostrando
mudança significativa tanto de nível de expressão QUANTO de splicing —
especificamente no contraste GORE3.** `gene-LOC142980480` (já destacado
no artigo 1, Fig. 19 — o evento do sashimi plot) confirma um padrão
**só-identidade** em GORE3: uma mudança clara em nível de isoforma não
acompanhada de uma chamada de DE em nível de gene, ilustrando exatamente
a distinção "nível vs. identidade" que motivou a FASE 6/9. Dois genes se
repetem como flagados por splicing tanto em SKTI quanto em GORE3
(`gene-LOC142977339`, `gene-LOC142983873`), estendendo a convergência
funcional SKTI≈GORE3 já reportada no artigo 1 (§3.18) até genes de
tripsina curados específicos. A pegada de Benzamidina segue sendo a
menor e menos específica dos três tratamentos, coerente com toda
análise anterior deste projeto.

**Interpretação, limitada ao que é mostrado aqui:** esta é evidência em
nível de gene e de evento de splicing consistente com H1 para um
conjunto pequeno e específico de genes de tripsina curados no GORE3 —
ainda não é prova estrutural ou funcional de uma troca de isoforma com
afinidade de ligação do GORE3 alterada. Essa confirmação é o propósito
explícito do Bloco F (ponte estrutural), adiado.

## 4. Limitações (declaradas explicitamente)

1. **Asp102 (terceiro resíduo da tríade catalítica) não foi verificado
   nesta rodada** — não existe um padrão PROSITE único e confiável para
   ele; verificação própria exige validação geométrica 3D sobre
   estrutura predita/experimental, adiada para o bloco estrutural (ainda
   sem escopo decidido).
2. **O outgroup filogenético é uma única sequência de mamífero**
   (tripsinogênio bovino), não um painel curado de outgroup — adequado
   para um primeiro enraizamento, não para inferência rigorosa de tempo
   de divergência ou evento de duplicação.
3. **A topologia da árvore ainda não foi revisada manualmente** para
   separar parálogos verdadeiros de possível fragmentação de anotação
   gênica (IDs `LOC` adjacentes que possam representar um único gene
   mal-dividido) — a filogenia existe; sua interpretação para esse
   propósito específico, ainda não.
4. **As quatro estruturas "prontas" antes assumidas reutilizáveis**
   (`analise-alosterica/data/protonated/`) **foram checadas nesta sessão
   e não são confirmadas como sequências de *A. gemmatalis***. — vêm de
   um projeto de triagem anterior e não relacionado (espécie não
   confirmada). Qualquer trabalho estrutural futuro precisa verificar
   identidade/accession antes de reutilizar, não assumir.
5. **O Bloco F (predição estrutural AlphaFold3/Boltz-2 + docking) não
   foi rodado** — computacionalmente pesado (GPU, horas por isoforma) e
   seu escopo (quantos dos genes flagados por H1 modelar) foi
   deliberadamente deixado para decidir depois de ver os resultados do
   Bloco E, conforme o plano aprovado. Não iniciado nesta sessão a
   pedido do usuário (pausa para conferência manual).
6. **A curadoria via PROSITE/MSA (Blocos B-C) é um filtro em nível de
   sequência, não um ensaio funcional** — os 166 genes curados são
   candidatos fortes a atividade de tripsina digestiva com base na
   conservação do motivo catalítico, não confirmados experimentalmente
   como cataliticamente ativos.

## Referências

Sigrist, C. J. A., Cuche, B. A., de Castro, E., Coudert, E., Redaschi,
N. & Bridge, A. The PROSITE database for protein families, domains, and
sites. *Nucleic Acids Res.* **54**, D451–D458 (2026). PMID 41263099.

Wong, T. K. F. et al. IQ-TREE 3: phylogenomic inference software using
complex evolutionary models. *Mol. Biol. Evol.* (2026). PMID 42085559.

Mistry, J. et al. Pfam: The protein families database in 2021. *Nucleic
Acids Res.* **49**, D412–D419 (2021). PMID 33125078. *(reaproveitada do
artigo 1, FASE 7 — as chamadas de domínio Pfam PF00089 são o ponto de
partida do Bloco B aqui.)*

---

## Reprodutibilidade — localização de código e dados

| Item | Caminho |
|---|---|
| Bibliografia (bib + fichas) | `paper-2/docs/referencias.bib`, `paper-2/docs/literatura.md` |
| Triagem por motivo PROSITE (Bloco B) | `paper-2/codigo/fase9_blocoB/prosite_scan.py` → `paper-2/resultados/fase9_blocoB/prosite_scan.csv` |
| Entrada MSA restrita ao domínio + execução (Bloco C) | `paper-2/codigo/fase9_blocoC/build_domain_input.py`, `run_mafft.sh` (servidor: `resultados_server/fase9_blocoC_domain_input.faa`, `_domain_aligned.fasta`) |
| Verificação de coluna da tríade catalítica (Bloco C) | `paper-2/codigo/fase9_blocoC/verify_triad_columns.py` → `paper-2/resultados/fase9_blocoC/triad_curated.csv` |
| trimAl + IQ-TREE3 (Bloco D, rodado no servidor, screen `fase9_iqtree`) | `trimal -in resultados_server/fase9_blocoD_curated_aligned.fasta -out resultados_server/fase9_blocoD_curated_trimmed.fasta -automated1` depois `iqtree3 -s ... -m MFP -bb 1000 -alrt 1000 -o 1TGN_A_bovine_trypsinogen_reference` → `paper-2/resultados/fase9_blocoD/tree/curated_family.{treefile,contree,iqtree}` |
| Cruzamento de H1 (Bloco E) | `paper-2/codigo/fase9_blocoE/cross_reference_h1.py` → `paper-2/resultados/fase9_blocoE/{h1_gene_level_detail.csv,h1_summary.csv}` |

**Dados grandes não versionados (só servidor):** `resultados_server/fase9_blocoC_domain_input.faa`/`_domain_aligned.fasta` (alinhamento completo dos 168+2), `resultados_server/fase9_blocoD_curated_trimmed.fasta` (alinhamento aparado), arquivos intermediários do IQ-TREE (`.ckp.gz`, `.model.gz`, `.mldist`, `.bionj`, `.splits.nex`, `.log`) — só `.treefile`/`.contree`/`.iqtree` (relatório) foram copiados para o repo, pequenos e suficientes para reproduzir a interpretação.
