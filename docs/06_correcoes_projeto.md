# Correções ao documento do projeto

Inconsistências e erros detectados na leitura integral de `Projeto-Eulalio-Pós-doc2.docx` (109 parágrafos).

Ordenado por severidade. Cada item traz o trecho original, o problema e a correção proposta.

---

## 🔴 Críticas — corrigir antes de executar ou submeter

### C1. Tratamento errado no desenho experimental

**Onde:** §2.3 (Preparação das bibliotecas)

> "...divididas em triplicatas de controle, SKTI, benzamidina e **GORE2**."

**Problema:** o projeto é sobre **GORE3**. Este é resíduo do projeto anterior (dos Santos et al., 2025, que de fato usou GORE-2). Num documento de pós-doc submetido a avaliação, um erro no nome da molécula de estudo dentro da própria seção de desenho experimental é grave.

**Correção:** `controle, SKTI, benzamidina e GORE3`.

**Verificar também** se o restante da metodologia não carrega outros resíduos do projeto anterior.

---

### C2. Contradição AlphaFold × Phyre2

**Onde:** §27 (objetivos) vs. §2.9 (metodologia)

- §27: "...obtenção de estruturas 3D das proteases digestivas e do peptídeo GORE3 usando estratégias como **AlphaFold** e/ou modelagem por homologia."
- §2.9: "...será modelada por homologia usando a plataforma **Phyre2**."

**Problema:** o objetivo promete uma coisa, a metodologia entrega outra. Um avaliador nota.

**Correção:** adotar AlphaFold2/ColabFold na metodologia e acrescentar o reporte de pLDDT e PAE. Manter a validação estereoquímica já prevista (ProSA-web, Ramachandran). Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §4.

---

### C3. CGenFF aplicado a peptídeo — erro conceitual

**Onde:** §2.10 (Dinâmica Molecular)

> "O peptídeo GORE3 será parametrizado usando o CGenFF (CHARMM General Force Field), garantindo compatibilidade com o campo de força aplicado à tripsina."

**Problema:** CGenFF destina-se a **pequenas moléculas orgânicas** sem parâmetros nos campos de força biomoleculares. Um peptídeo de aminoácidos canônicos já é coberto pelo campo de força de proteína — que é mais acurado para backbone peptídico do que parâmetros CGenFF atribuídos por analogia.

A justificativa dada ("garantindo compatibilidade") é o oposto do que ocorre: usar o mesmo FF de proteína para receptor e peptídeo é que garante compatibilidade.

**Correção:**

> "O peptídeo GORE3, composto de aminoácidos canônicos, será tratado com o mesmo campo de força de proteína aplicado à tripsina, gerando-se a topologia do complexo em uma única etapa. O CGenFF será empregado apenas para a benzamidina, quando simulada como controle de pequena molécula."

---

### C4. Montagem *de novo* ignora o genoma de referência disponível

**Onde:** §2.5 (Controle de qualidade, trimagem e montagem *De novo*)

**Problema:** o projeto foi redigido em Set/2025, quando *A. gemmatalis* não tinha genoma de referência. Isso mudou: `GCF_050436995.1` (ilAntGemm2), com anotação NCBI RS_2025_08.

Manter montagem *de novo* como estratégia principal compromete diretamente dois objetivos declarados — análise de **isoformas** e de **splicing alternativo** — que não são resolvíveis sem coordenadas genômicas.

**Correção:** reescrever a seção para pipeline genoma-guiado, mantendo a montagem *de novo* como via complementar (transcritos não anotados e de origem bacteriana). Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §1.

---

## 🟡 Médias — corrigir antes de submeter

### C5. Réplicas técnicas desnecessárias

**Onde:** §2.3

> "...o desenho experimental terá três réplicas técnicas e três réplicas biológicas do intestino da lagarta."

**Problema:** réplicas técnicas não agregam poder estatístico em RNA-Seq Illumina e consomem orçamento de sequenciamento.

**Correção:** eliminar réplicas técnicas; usar 4–5 réplicas biológicas por tratamento. Definir explicitamente quantos intestinos compõem uma réplica biológica — informação exigida em publicação e ausente do documento.

---

### C6. Falta o `tximport` entre quantificação e DESeq2

**Onde:** §2.7

**Problema:** o texto vai direto do pseudoalinhamento (Kallisto) para o DESeq2. Falta a etapa de agregação transcrito→gene, que também transmite os *offsets* de comprimento efetivo ao modelo. Omiti-la é erro estatístico, não formalidade.

**Correção:** inserir `tximport` explicitamente. O script já existe em `RNA-Seq-not-model/scripts/00_tximport.R`.

---

### C7. Análise de splicing sem ferramenta especificada

**Onde:** §27 menciona "isoformas alternativas" como objetivo; a metodologia (§2.5–2.8) **não especifica nenhuma ferramenta** de splicing.

**Correção:** especificar rMATS ou DEXSeq — ambos dependentes do genoma anotado (C4). Se a análise não for feita, remover a promessa do objetivo.

---

### C8. Ferramentas de anotação desatualizadas

**Onde:** §2.8

**Problema:** TRAPID, Blast2GO e **KOBAS 2.0** (descontinuado). Além disso, o projeto propõe usar as anotações de *H. armigera* e *B. mori* como referência para enriquecimento — desnecessário agora que a espécie tem genoma próprio.

**Correção:** eggNOG-mapper v2 para anotação; clusterProfiler para enriquecimento, com universo gênico construído da própria *A. gemmatalis*.

---

### C9. Erro de versionamento do DESeq2

**Onde:** §2.7

> "DESeq2 versão 3.15"

**Problema:** 3.15 é versão do **Bioconductor**, não do DESeq2.

**Correção:** citar a versão real do pacote e, separadamente, a versão do Bioconductor e do R. Conferir no ambiente, não de memória.

---

### C10. Docking de peptídeo com ferramenta de pequena molécula

**Onde:** §2.9

**Problema:** AutoDock Vina/PyRx é inadequado como método principal para ligante peptídico flexível. Além disso, a caixa de busca posicionada manualmente sobre o sítio ativo **pressupõe** o resultado.

**Correção:** protocolo em camadas com HADDOCK e/ou AlphaFold3, Vina como triagem, redocking de controle. Ver [`03_metodologia_padrao_ouro.md`](03_metodologia_padrao_ouro.md) §5.

**Observação:** o grupo **já usa HADDOCK** para o GORE3 (arquivos em `Desktop\LEBPP\GORE4-ate-GORE13\GORE3\`). A metodologia escrita está atrás da prática real.

---

## 🟢 Menores — redação e formatação

### C11. Numeração de seções salta

§2.3 é seguida diretamente por §2.5. Não existe §2.4.

**Correção:** renumerar, ou verificar se uma seção foi perdida na edição (possivelmente a extração de RNA, que aparece detalhada em `Abstract-projeto-eulalio.docx` mas não no projeto).

---

### C12. Tempos verbais misturados

A metodologia oscila entre futuro e pretérito, às vezes na mesma frase:

- §2.2: "A dieta artificial **consistia** em..." / "...os ingredientes **serão** misturados..."
- §2.2: "O ágar e a água **foram autoclavados**..."
- §2.5: "O script TrinityStats.pl **calculou** as estatísticas..."
- §2.3: "A construção de bibliotecas individuais de cDNA **utilizou** o kit..."

**Causa provável:** texto adaptado de metodologia de trabalho já concluído.

**Correção:** padronizar tudo em **futuro** — o projeto descreve trabalho a ser feito.

---

### C13. Referências de notícia usadas para dados econômicos

**Onde:** lista de referências

- `agrourbano.com.br/release/763/perdas-com-pragas-ultrapassam-r-60-bilhoes-por-ano-no-brasil`
- `cnabrasil.org.br/publicacoes/pib-do-agronegocio-registra-crescimento-de-6-49-no-primeiro-trimestre-de-2025`

**Problema:** são fontes jornalísticas/institucionais sustentando afirmações quantitativas sobre perdas econômicas e PIB. Em texto científico, dados numéricos devem vir de fonte primária (artigo revisado por pares, relatório oficial de órgão como CONAB/EMBRAPA/IBGE, ou publicação da FAO).

**Correção:** substituir por fonte primária, ou manter e marcar explicitamente como fonte secundária, com data de acesso. Não apresentar como se fosse literatura científica.

---

### C14. Referências sem elementos completos

Vários itens da lista carecem de volume, páginas ou DOI. Alguns exemplos:

- "FREIRES, Samya Thalyta dos Santos. Utilização de inseticidas naturais na agricultura: uma revisão. 2022." — sem indicação de tipo de obra, instituição ou veículo
- "BERLINER, 1911" — citado no texto (§19) sem entrada correspondente verificável na lista

**Correção:** completar todos os elementos e verificar cada referência. Ver [`NOTAS_DE_AUDITORIA.md`](NOTAS_DE_AUDITORIA.md) §3.

---

### C15. Grafia do nome da espécie e família

**Onde:** §2.10 (e ao longo do texto)

- `A. gemmatlis` (§ do `Abstract-projeto-eulalio.docx`) — falta o "a": **gemmatalis**
- Família oscila entre **Noctuidae** e **Erebidae** conforme a fonte citada

**Correção:** revisar a grafia e adotar uma família de forma consistente. Ver [`01_fundamentacao_teorica.md`](01_fundamentacao_teorica.md) §1.

---

### C16. Protocolo de extração de RNA descrito para folha de soja

**Onde:** `Abstract-projeto-eulalio.docx` (documento correlato)

> "Extraction of RNA from soybean leaves using the Trizol method / Grind 100 mg of **soybean leaves** in liquid nitrogen..."

**Problema:** o protocolo colado descreve extração de **folha de soja**, não de intestino de lagarta. Texto reaproveitado sem adaptação.

**Correção:** substituir pelo protocolo real de extração de intestino médio.

---

## Resumo por prioridade

| Prioridade | Itens | Ação |
|---|---|---|
| 🔴 Antes de executar | C1, C2, C3, C4 | Comprometem resultado ou avaliação |
| 🟡 Antes de submeter | C5, C6, C7, C8, C9, C10 | Rigor metodológico |
| 🟢 Revisão de texto | C11–C16 | Redação e referências |
