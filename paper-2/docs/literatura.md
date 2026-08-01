# Literatura — paper-2 (FASE 9+)

Fichamento leve, mesmo espírito do `literatura/02_rnaseq.md` do artigo 1,
mas sem replicar a estrutura inteira (Tier/fulltext) para um artigo que
ainda está no início. Migrar para o sistema completo se o paper-2
crescer.

### `sigrist2026prosite` — PMID 41263099

**O que estabelece:** Release atual (jan/2026) do PROSITE — padrões
PS00134 (His do sítio ativo) e PS00135 (Ser do sítio ativo) para a
família das serino-proteases tipo tripsina, complementados por ProRule.
Nota real do abstract: estruturas AlphaFold já são usadas rotineiramente
para definir limites de domínio na construção dos perfis, e o
ScanProsite agora visualiza matches sobre estruturas AlphaFold — reforça
a decisão da FASE 9 de combinar motivo de sequência (Bloco B) com
validação estrutural (Bloco F, se executado).

**Onde entra:** Bloco B — filtro primário de motivo nos 316 candidatos
Pfam PF00089 (FASE 7).

### `wong2026iqtree3` — PMID 42085559

**O que estabelece:** IQ-TREE versão 3 (maio/2026), terceiro release
principal — estende a v2 com modelos de mistura, fatores de concordância
gene/sítio, integração com estimativa de tempo de divergência
filogenômica, simulador de sequência. Confirmado via busca nesta sessão
como a versão mais atual disponível (não a v2, que era o que projetos
anteriores do grupo usavam).

**Onde entra:** Bloco D — filogenia da família de tripsinas curada.
