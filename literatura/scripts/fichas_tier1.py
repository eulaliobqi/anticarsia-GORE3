# -*- coding: utf-8 -*-
"""
Fichamento escrito a mao dos artigos Tier 1, apos leitura da fonte.

Separado de gerar_artefatos.py de proposito: o gerador emite metadados
verificados e nunca escreve interpretacao de artigo. Este arquivo e o
unico lugar onde entra texto interpretativo, e cada entrada declara em
`lido` exatamente o que foi lido para escreve-la.

Valores de `lido`:
  "fulltext"  secoes de resultados/discussao lidas no texto completo
  "abstract"  apenas o abstract lido
Toda afirmacao quantitativa abaixo veio da secao declarada. Onde o dado
nao foi conferido, o texto diz isso em vez de preencher.
"""

FICHAS = {

    # ---------------- TEMA 1 ----------------

    "paulo2026peptidic": dict(
        lido="fulltext",
        estabelece=(
            "Único trabalho publicado dedicado ao GORE3, contra tripsinas de "
            "*S. frugiperda*. Docking em quatro isoformas (XP_050552352.1, "
            "ACR25157.1, QLC28936.1, XP_050550273.1): ΔG do GORE3 entre −9,1 e "
            "−7,9 kcal/mol (média −8,25 ± 0,57) contra −6,1 a −5,2 da "
            "benzamidina (média −5,45 ± 0,44), diferença média de "
            "−2,8 ± 0,18 kcal/mol. A pose é descrita como rede de ligações de "
            "hidrogênio com resíduos polares que revestem o bolsão **S1/S1′** "
            "somada a contatos hidrofóbicos (alquil, π–alquil, empilhamento "
            "amida–π/π–π). Cinética: inibição competitiva com "
            "**Ki = 4,0 mM** (GORE3) e 16,49 µM (benzamidina); "
            "**IC50 = 433,98 µM** (GORE3) e 8,58 µM (benzamidina) — a "
            "benzamidina inibiu 89% a 60 µM, o GORE3 precisou de 700 µM para "
            "inibição comparável. In vivo a 0,30% (m/v): atividade de proteases "
            "totais **aumentou** após 20 dias; KM(app) subiu de 0,28 mM "
            "(controle) para 0,86 mM; período larval passou de 25 ± 0,15 para "
            "35 ± 0,15 dias; malformação de pupas a 0,02436% e 0,04873%; "
            "digestibilidade aproximada (AD) alterada só a 0,30%, sem efeito "
            "em ECI/ECD; consumo foliar sem diferença significativa."
        ),
        onde_entra=(
            "Introdução — é o estado da arte do próprio GORE3 e **fornece o "
            "IC50/Ki quantificado** que `NOTAS_DE_AUDITORIA.md` §7 listava como "
            "bloqueio da escrita da introdução (com a ressalva da espécie). "
            "Metodologia §11 — é o docking a reproduzir e estender. "
            "`NOTAS_DE_AUDITORIA.md` §8 — modo de ligação."
        ),
        ressalva=(
            "**Duas inconsistências internas no artigo publicado.** (a) O "
            "abstract dá Ki da benzamidina = 1,64 mM, mas a seção de resultados "
            "dá 16,49 µM — cem vezes de diferença, sem nota de reconciliação; o "
            "valor do GORE3 (4,00 mM) é o mesmo nos dois lugares. (b) A "
            "mortalidade **não é monotônica com a dose**: ~47% a 0,00241% e a "
            "0,04873%, mas apenas 6,7% e 26% nas concentrações maiores 0,1216% "
            "e 0,2432%. A mesma frase ainda reporta 'a mortality percentage of "
            "0.000067%', que repete a concentração no lugar da mortalidade. "
            "Não citar os valores de mortalidade sem sinalizar isso. "
            "Além disso: é *S. frugiperda*, não *A. gemmatalis*; é docking sem "
            "MD de validação; e o Ki milimolar é fraco em termos absolutos."
        ),
    ),

    "paulo2026peptides": dict(
        lido="fulltext",
        estabelece=(
            "Pentapeptídeos derivados de RCL de BPTI e SKTI contra tripsinas de "
            "Lepidoptera. Ki em extrato bruto de intestino de *A. gemmatalis*: "
            "TGPCK 2,2 mM < TGPCR 8,8 mM < AVIMK 14,4 mM < AVIMR 26,2 mM, todos "
            "com melhor ajuste ao modelo competitivo (R² de 0,77 a 0,94). "
            "Dois achados estruturais que importam mais que os Ki: o **número "
            "total de interações não correlaciona com a afinidade** "
            "(r = −0,289; p > 0,05), enquanto o número de contatos com os "
            "resíduos conservados His57, Asp102, Ser195, Asp189 e Gly197 "
            "correlaciona fortemente (r = −0,558; p < 0,00045); e **peptídeos "
            "com lisina na posição P1 formaram significativamente mais ligações "
            "pi-sigma**, associadas a maior afinidade."
        ),
        onde_entra=(
            "Introdução — a série de pentapeptídeos que antecede o GORE3. "
            "**Hipótese H6** — é o dado publicado mais direto contra a premissa "
            "de que o LALAY se ancora como os demais peptídeos da série: o "
            "ganho de afinidade descrito depende de Lys em P1, e o LALAY não "
            "tem resíduo básico algum."
        ),
        ressalva=(
            "Docking mais cinética, sem estrutura experimental do complexo. "
            "Todos os Ki estão na faixa milimolar. A correlação com resíduos "
            "catalíticos é observacional sobre poses preditas, não medida."
        ),
    ),

    "schultz2026synthetic": dict(
        lido="fulltext",
        estabelece=(
            "GORE1 e GORE2 contra tripsinas de *S. frugiperda*, com e sem "
            "perturbação da microbiota por antibiótico. Ki competitivos: "
            "GORE1 1,41 mM, GORE2 0,49 mM, SKTI 4,75 nM, benzamidina 16,70 µM. "
            "KM(app) do controle 1,86 mM; a maioria dos tratamentos elevou o "
            "KM (menor afinidade pelo substrato), mas o **GORE2 reduziu** o KM "
            "em todas as três concentrações (0,96; 0,96; 1,06 mM) — direção "
            "oposta. Sem diferença significativa de sobrevivência entre "
            "tratamentos (log-rank χ² = 1,714; p = 0,1904), mortalidade máxima "
            "de 10%, sobrevivência acima de 95% nos demais; sem efeito na "
            "duração larval (p = 0,9675). Massa de 5º instar e de pupa "
            "reduzidas pelo GORE1 (p < 0,0001), com a maior redução em "
            "GORE1 + antibiótico. ECI e ECD reduzidos por GORE1 e GORE2."
        ),
        onde_entra=(
            "Introdução — mostra que **afinidade cinética in vitro não prediz "
            "efeito fisiológico in vivo**, ponto que o projeto precisa "
            "assumir explicitamente ao propor seleção de isoformas por "
            "afinidade. Discussão do papel da microbiota intestinal, que "
            "conversa com `pilon2017guttrypsin`."
        ),
        ressalva=(
            "É *S. frugiperda*. **Não misturar com os Ki de Barros et al. "
            "2021**: lá GORE1 = 0,49 mM e GORE2 = 0,10 mM, mas em "
            "*A. gemmatalis*. A coincidência numérica entre o GORE2 daqui "
            "(0,49 mM) e o GORE1 de lá (0,49 mM) é armadilha de transcrição."
        ),
    ),

    "li2020peptides": dict(
        lido="fulltext",
        estabelece=(
            "Quatro peptídeos derivados do *reactive center loop* da serpina-3 "
            "de *Manduca sexta*, de 5 a 8 resíduos, todos começando no resíduo "
            "P14. O **pentapeptídeo Ac-SVAFS-NH2 bloqueou completamente** a "
            "atividade inibitória da serpina-3 sobre a protease PAP3 (atividade "
            "de PAP3 restaurada a 100% ± 6%, contra 9% ± 9% com a serpina "
            "íntegra), e o efeito **decai com o aumento do comprimento**: o "
            "octapeptídeo Ac-SVAFSATQ-NH2 bloqueou cerca de 50% (59% ± 5%). O "
            "peptídeo converte a serpina de inibidor em substrato e estabiliza "
            "termicamente o complexo — a serpina livre sofre transição "
            "conformacional entre 50 e 70 °C, enquanto o complexo mantém o "
            "espectro de dicroísmo circular até 90 °C."
        ),
        onde_entra=(
            "Introdução, eixo 1A — precedente direto de **pentapeptídeo** "
            "derivado de RCL com função demonstrada em Lepidoptera, e o achado "
            "de que nessa série o mais curto foi o mais eficaz, que é o "
            "argumento de plausibilidade para um pentapeptídeo como o GORE3."
        ),
        ressalva=(
            "O alvo é serpina de hemolinfa (imunidade), **não tripsina "
            "digestiva**, e o mecanismo é inserção do peptídeo na folha-β A da "
            "serpina, não inibição competitiva do sítio ativo de uma protease. "
            "Serve como precedente de desenho, não como modelo mecanístico do "
            "GORE3."
        ),
    ),

    "dewangan2026plant": dict(
        lido="fulltext",
        estabelece=(
            "Lipidômica e metabolômica integradas em *H. armigera* exposta ao "
            "inibidor recombinante rCanPI-7 (quatro domínios, ativo contra "
            "tripsinas e quimotripsinas), em cinética de 0,5 a 48 h. "
            "Reprogramação metabólica extensa: vias de aminoácidos, glutationa "
            "e pirimidina, com deslocamentos em alanina, arginina, histidina e "
            "aminoácidos de cadeia ramificada. Supressão da glicólise e do "
            "ciclo do ácido tricarboxílico indica queda do metabolismo "
            "energético primário. O estresse oxidativo aparece como depleção de "
            "glutationa, peroxidação lipídica e acúmulo de ceramida — "
            "assinaturas de disfunção mitocondrial. Como compensação, a larva "
            "mobiliza triglicerídeos e aminoácidos como fonte alternativa de "
            "energia, reforça defesas antioxidantes e ativa vias apoptóticas e "
            "neuromoduladoras."
        ),
        onde_entra=(
            "**Hipótese H2** — é o suporte publicado mais direto para a ideia "
            "de que a resposta a inibidor de protease pode privilegiar "
            "detoxificação e defesa antioxidante em vez de compensação "
            "proteolítica, e conecta o fenótipo de crescimento retardado ao "
            "desvio de recursos."
        ),
        ressalva=(
            "É *H. armigera*, e o inibidor é uma proteína multi-domínio, não um "
            "pentapeptídeo. São lipidômica e metabolômica, não transcriptômica: "
            "a ponte com genes diferencialmente expressos de detoxificação é "
            "inferência, não medida no artigo. Li apenas a seção de conclusões."
        ),
    ),

    # ---------------- TEMA 2 ----------------

    "schurch2016many": dict(
        lido="fulltext",
        estabelece=(
            "Experimento com **48 réplicas biológicas** em cada uma de duas "
            "condições em *S. cerevisiae*, para responder objetivamente quantas "
            "réplicas uma análise de RNA-Seq precisa. Com 3 réplicas, nove de 11 "
            "ferramentas testadas encontraram só 20–40% dos genes "
            "diferencialmente expressos identificados com o conjunto completo "
            "de 42 réplicas limpas — sobe para >85% só no subconjunto de genes "
            "com variação acima de 4×. **Recomendações formais dos autores:** "
            "(1) pelo menos **6 réplicas biológicas** por condição em qualquer "
            "experimento; (2) pelo menos **12** quando é importante identificar "
            "a maioria dos genes DE, incluindo os de fold-change pequeno; (3) "
            "com menos de 12 réplicas, usar **edgeR (exact)** ou **DESeq2**; "
            "com mais de 12, o **DESeq** original supera marginalmente os "
            "demais."
        ),
        onde_entra=(
            "Metodologia §11, item de réplicas — **contradiz diretamente a "
            "recomendação atual do projeto** ('≥4 biológicas, zero técnicas'). "
            "O número correto segundo esta referência é ≥6, subindo a ≥12 se "
            "o objetivo incluir capturar DEGs de fold-change pequeno — que é "
            "precisamente o caso de isoformas de tripsina com troca sutil "
            "(hipótese H1). Ação: **revisar `03_metodologia_padrao_ouro.md` "
            "para citar 6–12 réplicas, não 4**, e conversar com a Macrogen "
            "sobre viabilidade/custo antes de fechar o desenho."
        ),
        ressalva=(
            "É levedura, organismo unicelular com baixa variância biológica "
            "inter-réplica comparado a um inseto criado em condições "
            "semi-controladas — a variância real em *A. gemmatalis* pode ser "
            "maior, o que tornaria a recomendação ainda mais conservadora, não "
            "menos. Não é garantia de que 6 réplicas bastem aqui; é o piso "
            "empírico mínimo publicado."
        ),
    ),

    "froussios2019well": dict(
        lido="fulltext",
        estabelece=(
            "Estende o resultado de Schurch et al. (2016) de levedura para "
            "*Arabidopsis thaliana*, eucarioto complexo. Confirma que as "
            "medidas de expressão gênica são mais consistentes com uma "
            "**distribuição binomial negativa** do que log-normal ou normal, e "
            "que o **tamanho e a complexidade do transcriptoma não alteram a "
            "taxa de falsos positivos** das nove ferramentas de DGE testadas."
        ),
        onde_entra=(
            "Metodologia §11 — generaliza a recomendação de Schurch para além "
            "de levedura, o que é relevante porque *A. gemmatalis* é "
            "certamente mais complexo que levedura. Reforça a escolha de "
            "DESeq2/edgeR (ambos baseados em binomial negativa) sobre "
            "alternativas paramétricas gaussianas."
        ),
        ressalva=(
            "Planta, não inseto — mas o ponto (robustez da NB independente da "
            "complexidade do transcriptoma) é justamente o que generaliza a "
            "recomendação para organismos não testados diretamente."
        ),
    ),

    "zhang2020combat": dict(
        lido="fulltext",
        estabelece=(
            "Apresenta o ComBat-seq, correção de efeito de lote baseada em "
            "**regressão binomial negativa**, que mantém a natureza inteira das "
            "contagens (compatível com DESeq2/edgeR, ao contrário de métodos "
            "gaussianos que geram valores negativos artificiais). Em simulação "
            "com efeito de lote realista (1,5× de diferença de média, 2× de "
            "dispersão), ComBat-seq atinge **TPR = 0,89**, superior a incluir "
            "lote como covariável (0,87), ComBat original em logCPM (0,85), "
            "RUV-seq (0,83) e SVA-seq (0,87). Em cenário mais extremo (3× "
            "média, 4× dispersão), a vantagem cresce para **≥6 pontos "
            "percentuais de TPR** sobre as demais. Mantém FPR sob controle na "
            "maioria dos cenários testados."
        ),
        onde_entra=(
            "Metodologia §11 — preenche a lacuna explícita 'falta correção de "
            "lote', e é a ferramenta correspondente ao script já existente "
            "`RNA-Seq-not-model/scripts/05_batch_correction.R`. Se o "
            "sequenciamento da Macrogen sair em mais de uma corrida, esta é a "
            "citação para justificar a correção."
        ),
        ressalva=(
            "Em um cenário específico (sem diferença de dispersão entre "
            "lotes), o próprio ComBat-seq fica **redundante e mais "
            "conservador** que simplesmente incluir lote como covariável no "
            "modelo — não aplicar cegamente sem antes verificar se o desenho "
            "realmente tem lotes heterogêneos."
        ),
    ),

    "sergio2024comprehensive": dict(
        lido="fulltext",
        estabelece=(
            "Simula dados de RNA-Seq com complexidade controlada para testar o "
            "que mais afeta a montagem *de novo* de transcriptoma. **O grau de "
            "splicing alternativo teve o maior impacto negativo** na "
            "reconstrução de transcritos — sem splicing alternativo, "
            "reconstrução de 62,8–96,3%; no grau máximo de splicing, cai para "
            "11,6–48,7%. O tamanho do fragmento também importa: em fragmentos "
            "de 400 pb, nenhum montador reconstruiu transcritos até o 10º "
            "percentil de tamanho; subindo para 500–600 pb, o limiar melhora "
            "para o 15º percentil. Comprimento de leitura e tamanho de "
            "fragmento afetam a reconstrução de transcritos longos e curtos de "
            "forma **diferente**."
        ),
        onde_entra=(
            "Metodologia §11 — justifica tecnicamente por que a via Trinity "
            "*de novo* secundária (para transcritos ausentes da anotação) é "
            "estrutural e previsivelmente mais fraca justamente nos genes com "
            "mais isoformas — que são exatamente as famílias de interesse "
            "(serino-proteases). É argumento a favor do genoma-guiado como via "
            "primária, com números, não só afirmação qualitativa."
        ),
        ressalva=(
            "Dado inteiramente simulado, a partir do genoma humano. Os números "
            "percentuais não se transferem para *A. gemmatalis*; a direção do "
            "efeito (splicing prejudica montagem *de novo*) é o que generaliza."
        ),
    ),

    "vaquerogarcia2016view": dict(
        lido="fulltext",
        estabelece=(
            "Artigo original do **MAJIQ**, que define e quantifica splicing "
            "alternativo em unidades de *local splicing variations* (LSVs), "
            "capazes de capturar tanto os tipos clássicos de splicing quanto "
            "variações mais complexas. Em mapa de 12 tecidos de camundongo, "
            "**LSVs complexas constituem mais de 30%** das variações "
            "dependentes de tecido e afetam famílias de proteínas específicas; "
            "a prevalência de LSVs complexas é conservada em humanos."
        ),
        onde_entra=(
            "Metodologia §11 — alternativa ao par rMATS/DEXSeq para a "
            "**hipótese H5** (splicing alternativo). É a citação canônica do "
            "MAJIQ, cuja vantagem declarada é capturar eventos complexos além "
            "dos tipos clássicos (skipped exon, intron retention etc.), "
            "relevante se a resposta ao GORE3 envolver splicing não-canônico."
        ),
        ressalva=(
            "Demonstrado em camundongo, não em inseto. O ganho de LSVs "
            "complexas depende de profundidade e desenho — não avaliado aqui "
            "se compensa a curva de aprendizado extra frente a rMATS/DEXSeq, "
            "que já têm scripts documentados no grupo."
        ),
    ),

    "ferrerbonsoms2022identifiability": dict(
        lido="abstract",
        estabelece=(
            "Formaliza quando o problema de deconvolução de isoformas é "
            "identificável a partir de reads pareadas, e propõe método "
            "objetivo para escolher o comprimento de fragmento. Achado central: "
            "o comprimento de fragmento ótimo é **dependente do gene**, e para "
            "o transcriptoma humano o comprimento médio ótimo fica em "
            "**400–600 nt para genes codificantes** (150–200 nt para lncRNAs). "
            "O comprimento de leitura ótimo é o maior que couber dentro do "
            "fragmento. Combinar duas bibliotecas de fragmentos muito "
            "diferentes melhora significativamente a identificabilidade "
            "gênica."
        ),
        onde_entra=(
            "**Ponto crítico para o desenho real do sequenciamento.** "
            "'Paired-end, 150 nt' é o **comprimento de leitura**, não o "
            "comprimento de fragmento (inserto) — são parâmetros distintos, e "
            "este artigo é o que formaliza por que a distinção importa para "
            "quantificação de isoforma. **Ação concreta: confirmar com a "
            "Macrogen o tamanho médio do fragmento/inserto da biblioteca**, "
            "não só o comprimento de leitura. Se o inserto for menor que "
            "~250–300 nt (frequente em preparações padrão), a identificação "
            "de isoformas fica prejudicada mesmo com boa profundidade."
        ),
        ressalva=(
            "Só o abstract foi lido; valores calculados para transcriptoma "
            "humano, não para *A. gemmatalis*. A direção do argumento "
            "(fragmento maior ajuda deconvolução de isoforma) generaliza; os "
            "números de 400–600 nt não devem ser citados como alvo direto para "
            "este projeto."
        ),
    ),

    "norton2018outlier": dict(
        lido="abstract",
        estabelece=(
            "Desenvolve modelo de probabilidade para ponderar cada réplica de "
            "RNA-Seq como representativa de sua condição experimental na "
            "análise de splicing alternativo, detectando **amostras "
            "outlier** consistentemente diferentes das demais da mesma "
            "condição. Em vez de descartar essas amostras, propõe "
            "**down-weighting** — generalização do algoritmo MAJIQ que ganha "
            "poder estatístico em vez de perder dado."
        ),
        onde_entra=(
            "Metodologia — controle de qualidade para a **hipótese H5**. Com "
            "poucas réplicas (o padrão do projeto, mesmo revisado para 6), "
            "uma única réplica ruim pode dominar o resultado de splicing "
            "diferencial; este é o método declarado para lidar com isso sem "
            "simplesmente descartar dado caro."
        ),
        ressalva="Só o abstract foi lido; específico ao ecossistema MAJIQ.",
    ),

    "yadav2021pinir": dict(
        lido="abstract",
        estabelece=(
            "Base de dados PINIR, com **415 sequências** de inibidores de "
            "protease tipo Pin-II (família do inibidor tipo II de batata) "
            "anotadas manualmente, mapeando **695 domínios, 75 ligantes, 63 "
            "reactive center loops e 10 padrões de ponte dissulfeto**. A "
            "característica estrutural declarada da família é ter múltiplos "
            "domínios repetidos de inibição, padrão conservado de dissulfeto e "
            "um **reactive center loop tripeptídico**. A análise revelou "
            "subcategorias novas e ocorrência de domínios, RCLs e padrões de "
            "dissulfeto correlacionada com espécie."
        ),
        onde_entra=(
            "Introdução, eixo 1A — é o recurso que sustenta a afirmação de que "
            "o RCL da família Pin-II é tripeptídico, que é a base conceitual da "
            "série de tripeptídeos de Saikhedkar e, por extensão, da lógica de "
            "peptídeos curtos derivados de RCL."
        ),
        ressalva=(
            "Base de dados e análise de sequência; não traz dado funcional de "
            "inibição. Verificar se o recurso segue online antes de citá-lo "
            "como ferramenta utilizável."
        ),
    ),

    "liu2020proteolysis": dict(
        lido="abstract",
        estabelece=(
            "Determina os sítios de clivagem das protoxinas Cry1Ac e Cry2Ab por "
            "proteases do suco intestinal de *H. armigera*. Cry1Ac gera "
            "fragmento de ~65 kDa por clivagem em **Arg28**, na porção "
            "anterior da hélice α-1 do domínio I; Cry2Ab gera fragmento de ~50 "
            "kDa por clivagem em **Arg139**, entre as hélices α-3 e α-4 do "
            "domínio I. Ambos os resíduos foram preditos como **sítios de "
            "clivagem de tripsina**. As toxicidades (CL₅₀) das protoxinas foram "
            "equivalentes às das toxinas ativadas na cepa suscetível SCD."
        ),
        onde_entra=(
            "Tema 1, eixo 1B — demonstra que a tripsina intestinal é o agente "
            "de **ativação** da toxina Bt, não só de digestão. Isso é o "
            "argumento mecanístico para a interação inibidor de tripsina × Bt "
            "explorada em `fonseca2023soybean`, e um alerta: inibir tripsina "
            "pode reduzir a ativação do Bt."
        ),
        ressalva=(
            "*H. armigera*, não *A. gemmatalis*. Só o abstract foi lido; os "
            "valores de CL₅₀ não foram extraídos."
        ),
    ),

    "lokya2020response": dict(
        lido="abstract",
        estabelece=(
            "Purifica e caracteriza um inibidor Bowman-Birk de amendoim "
            "(PnBBI) de variedade híbrida interespecífica. Caracterização "
            "biofísica: baixa massa molecular, vários isoinibidores, formas "
            "diméricas/tetraméricas de ordem superior, predomínio de folhas-β "
            "antiparalelas e alças aleatórias, sítios reativos contra tripsina "
            "e quimotripsina, estabilidade ampla a pH e temperatura extremos "
            "(dados de MALDI TOF-TOF em ProteomeXchange PXD016933). Por "
            "ressonância plasmônica de superfície, é bifuncional mas **"
            "específico para tripsina, com estequiometria 1:2** frente à "
            "quimotripsina. Em bioensaio reduziu a massa larval, com queda da "
            "atividade de proteases tipo tripsina do intestino; zimografia uni "
            "e bidimensional mostrou **desaparecimento de várias isoformas**, e "
            "qRT-PCR indicou que o inibidor modula também a expressão dessas "
            "proteases."
        ),
        onde_entra=(
            "**Hipótese H1** — é evidência publicada de que um inibidor de "
            "protease altera o *perfil de isoformas* e não só a atividade "
            "total, medido por zimografia mais qRT-PCR. É o desenho "
            "experimental análogo ao que este projeto propõe fazer por "
            "RNA-Seq."
        ),
        ressalva=(
            "A espécie-alvo do bioensaio está truncada no abstract salvo "
            "(aparece como texto vazio); pelo contexto e pelo título é "
            "*Helicoverpa armigera*, **mas isso não foi verificado** — conferir "
            "no texto completo antes de citar a espécie."
        ),
    ),

    "soneson2015differential": dict(
        lido="abstract",
        estabelece=(
            "Demonstra que estimativas de abundância em nível de gene têm "
            "vantagem sobre análise em nível de transcrito em desempenho e "
            "interpretabilidade, e — o ponto central para este projeto — que a "
            "**presença de uso diferencial de isoformas infla a taxa de falsas "
            "descobertas** em análise de expressão diferencial de genes feita "
            "sobre matriz de contagem simples. O problema é corrigido "
            "incorporando offsets derivados das estimativas em nível de "
            "transcrito."
        ),
        onde_entra=(
            "Metodologia §11 — é a justificativa formal do `tximport` entre "
            "Salmon e DESeq2, etapa que o `.docx` omite. E é o argumento "
            "metodológico da **hipótese H1**: se a troca de isoformas de "
            "tripsina existe, a análise só em nível de gene distorce o "
            "resultado."
        ),
        ressalva=(
            "O próprio artigo registra que o problema é relativamente pequeno "
            "em vários conjuntos de dados reais — não presumir que será grande "
            "aqui sem verificar."
        ),
    ),

    "chisanga2022impact": dict(
        lido="abstract",
        estabelece=(
            "Compara as anotações Ensembl e RefSeq sobre um conjunto de "
            "referência do consórcio SEQC e conclui que **a anotação RefSeq "
            "levou a melhor acurácia de quantificação**, avaliada por "
            "correlação com verdades de referência que incluem mais de 800 "
            "genes validados por PCR em tempo real."
        ),
        onde_entra=(
            "Metodologia — sustenta usar a anotação RefSeq `RS_2025_08` do "
            "`GCF_050436995.1`, e é a referência que faltava para declarar que "
            "a escolha de anotação afeta o resultado da quantificação."
        ),
        ressalva=(
            "Dados humanos, com anotação madura e curada nas duas bases. **Não "
            "testa o caso deste projeto**, que é anotação automática de um "
            "genoma de não-modelo depositado há pouco — o risco de erro em "
            "famílias multigênicas como as serino-proteases permanece, e a "
            "curadoria manual segue necessária."
        ),
    ),

    "sarantopoulou2021comparative": dict(
        lido="fulltext",
        estabelece=(
            "Benchmark de quantificação de isoformas com dado real e simulado, "
            "cobrindo Salmon, kallisto, RSEM, Cufflinks, HTSeq, featureCounts e "
            "NRP. **Achado central e o mais importante para este projeto:** ao "
            "remover a isoforma mais expressa de um gene (simulando o "
            "cenário em que uma isoforma domina e outra é rara — exatamente "
            "o que a hipótese H1 propõe existir entre isoformas de tripsina "
            "sensíveis e insensíveis), **a acurácia de todos os métodos cai "
            "drasticamente, exceto HTSeq e featureCounts** — que por sua vez "
            "não resolvem isoforma nenhuma, só contam por gene. Na análise de "
            "expressão diferencial em nível de isoforma com genes sem "
            "expressão real em nenhuma réplica (controle negativo interno), "
            "**a FDR real ficou muito acima da reportada para todos os "
            "métodos** — a 0,01 de FDR nominal, houve ≥1.000 isoformas "
            "chamadas como DE indevidamente. Sleuth teve a menor taxa de "
            "falso positivo entre os métodos aplicáveis. **DESeq2 não foi "
            "desenhado para DE em nível de transcrito** e tem desempenho "
            "inferior a EBSeq/Sleuth nessa tarefa especificamente — mas ainda "
            "assim superou-os em manter especificidade em alguns cortes."
        ),
        onde_entra=(
            "**Advertência direta para a hipótese H1.** O cenário mais "
            "problemático do benchmark — isoforma dominante que desaparece — "
            "é estruturalmente o cenário que H1 propõe testar. Duas "
            "consequências para a metodologia: (1) **quantificação por "
            "isoforma via Salmon/tximport alimentando DESeq2 mede expressão "
            "de gene com sensibilidade a troca de isoforma, não substitui "
            "uma ferramenta de DE em nível de transcrito de verdade**; (2) se "
            "for reportar DE em nível de isoforma (não só de gene), usar "
            "método desenhado para isso (EBSeq, Sleuth) e **declarar "
            "explicitamente que a FDR real pode exceder a nominal**, com "
            "controle negativo (genes de expressão nula) quando possível."
        ),
        ressalva=(
            "Dado majoritariamente simulado a partir de anotação humana "
            "(hipocampo × fígado), com validação em dado real das mesmas "
            "amostras. Os métodos testados são de 2014-2016; ferramentas mais "
            "recentes (Salmon com bootstrap, tximport) podem ter corrigido "
            "parte do problema — não testado aqui."
        ),
    ),

    "coxe2024benchmarking": dict(
        lido="fulltext",
        estabelece=(
            "Benchmark de HISAT2, STAR, Subread e BBMap com dado simulado de "
            "*Arabidopsis thaliana* e SNPs anotados do TAIR, em parâmetros "
            "padrão, sem referência, e permissivos, medindo acurácia em "
            "resolução de base e de **base de junção** (a que importa para "
            "detecção correta de splicing). Conclusão dos autores: **os "
            "alinhadores populares têm desempenho parecido em resolução de "
            "base**, mas na resolução de junção — que é o que decide se um "
            "evento de splicing é atribuído corretamente — **o Subread é o "
            "mais promissor**, recomendado quando alta acurácia de junção "
            "importa. STAR e HISAT2 permanecem adequados para uso geral."
        ),
        onde_entra=(
            "Metodologia §11 — é o argumento com número real para escolher "
            "**Subread como alinhador, e não STAR/HISAT2 por padrão**, "
            "especificamente para a **hipótese H5** (splicing alternativo). "
            "Para expressão gênica geral sem foco em junção, STAR/HISAT2 "
            "seguem adequados."
        ),
        ressalva=(
            "É *Arabidopsis*, planta diploide, os próprios autores dizem que é "
            "'talvez menos complexa' que outros genomas vegetais, e não "
            "testam inseto. O ranking não se transfere automaticamente para "
            "*A. gemmatalis*; a lição estrutural — que ferramentas diferentes "
            "podem empatar em base mas divergir muito em junção — sim."
        ),
    ),

    "pardopalacios2024systematic": dict(
        lido="abstract",
        estabelece=(
            "Consórcio LRGASP: mais de 427 milhões de leituras longas de cDNA e "
            "de RNA direto, em humano, camundongo e peixe-boi, avaliando "
            "detecção de isoformas, quantificação e detecção *de novo*. "
            "Resultados centrais: **bibliotecas com leituras mais longas e mais "
            "acuradas produzem transcritos mais acurados do que bibliotecas com "
            "maior profundidade**, enquanto maior profundidade melhora a "
            "acurácia de quantificação; em genomas bem anotados as ferramentas "
            "baseadas em referência têm o melhor desempenho; e recomenda-se "
            "dado ortogonal adicional e réplicas quando o alvo são transcritos "
            "raros ou novos, ou quando se usa abordagem sem referência."
        ),
        onde_entra=(
            "Metodologia, eixo de fronteira — é a referência para decidir se "
            "vale acrescentar long-read para resolver isoformas de tripsina, e "
            "a base do trade-off comprimento × profundidade."
        ),
        ressalva=(
            "Espécies com anotação madura. A recomendação do próprio artigo "
            "sobre abordagens sem referência e dado ortogonal é o que mais se "
            "aproxima do caso de *A. gemmatalis*, cuja anotação é automática e "
            "recente."
        ),
    ),

    "yan2026comprehensive": dict(
        lido="abstract",
        estabelece=(
            "Avalia os montadores *de novo* de leitura longa RATTLE, RNA-Bloom2 "
            "e isONform contra o Trinity (leitura curta), em dado simulado com "
            "transcritos sequin e dado real de humano e ervilha, em "
            "profundidades de 6 a 60 milhões de leituras, cobrindo ONT cDNA, "
            "ONT RNA direto e PacBio."
        ),
        onde_entra=(
            "Metodologia — informa se a via Trinity secundária, prevista para "
            "transcritos ausentes da anotação, deveria migrar para long-read."
        ),
        ressalva=(
            "⚠️ Li apenas objetivos e desenho no abstract. **Não extraí qual "
            "ferramenta teve melhor desempenho nem sob quais condições** — não "
            "citar como justificativa de escolha antes de ler os resultados. O "
            "texto completo está em `fulltext/yan2026comprehensive.txt`."
        ),
    ),

    "patro2017salmon": dict(
        lido="abstract",
        estabelece=(
            "Apresenta o Salmon, método leve de quantificação de abundância de "
            "transcritos, combinando algoritmo de inferência paralela em duas "
            "fases, modelos de viés e mapeamento ultrarrápido. É descrito como "
            "**o primeiro quantificador transcriptoma-amplo a corrigir viés de "
            "conteúdo GC do fragmento**, o que segundo os autores melhora "
            "substancialmente a acurácia das estimativas e a sensibilidade da "
            "análise de expressão diferencial subsequente."
        ),
        onde_entra=(
            "Metodologia §11 — citação canônica da troca de Kallisto 0.44 por "
            "Salmon. A correção de viés de GC é o argumento técnico da troca."
        ),
        ressalva=(
            "Artigo-fonte de 2017; a justificativa de escolha *hoje* deve vir "
            "de benchmark recente (`sarantopoulou2021comparative`), não deste."
        ),
    ),

    "love2014moderated": dict(
        lido="abstract",
        estabelece=(
            "Apresenta o DESeq2, que usa **estimação por encolhimento** "
            "(*shrinkage*) de dispersões e de log-fold-changes para melhorar "
            "estabilidade e interpretabilidade das estimativas. O problema "
            "declarado é o de contagens com número pequeno de réplicas, "
            "discretude, grande faixa dinâmica e presença de outliers — que é "
            "exatamente o regime deste projeto."
        ),
        onde_entra=(
            "Metodologia §11 — citação canônica do DESeq2. Também é a "
            "referência que corrige o erro C7 de `06_correcoes_projeto.md`, "
            "onde o `.docx` cita 'DESeq2 versão 3.15' (3.15 é versão do "
            "Bioconductor, não do pacote)."
        ),
        ressalva=(
            "O encolhimento melhora estabilidade mas pressupõe que a maioria "
            "dos genes não é diferencialmente expressa — premissa a declarar."
        ),
    ),

    "chen2018fastp": dict(
        lido="abstract",
        estabelece=(
            "Artigo original do fastp, pré-processador de FASTQ que integra "
            "controle de qualidade, filtragem, corte e correção numa passagem."
        ),
        onde_entra="Metodologia §11 — etapa de trimagem, citação canônica.",
        ressalva=(
            "Superado pelo fastp 1.0 (`chen2025fastp`) como descrição da "
            "ferramenta atual; citar os dois quando a versão importar."
        ),
    ),

    "chen2025fastp": dict(
        lido="abstract",
        estabelece=(
            "Primeira grande atualização do fastp. Apresenta as novidades da "
            "versão 1.0 e os princípios de implementação, e **compara com "
            "Trimmomatic e Cutadapt** em simplicidade, eficiência e "
            "versatilidade."
        ),
        onde_entra=(
            "Metodologia §11 — é a referência recente que justifica manter "
            "fastp em vez do Trimmomatic que o `.docx` propõe."
        ),
        ressalva=(
            "A comparação é feita pelos próprios autores da ferramenta, não é "
            "benchmark independente. Tratar como descrição, não como evidência "
            "de superioridade."
        ),
    ),

    "ewels2016multiqc": dict(
        lido="abstract",
        estabelece=(
            "MultiQC agrega resultados de múltiplas ferramentas e múltiplas "
            "amostras num relatório único."
        ),
        onde_entra="Metodologia §11 — etapa de QC agregado.",
        ressalva="Ferramenta de relatório; não substitui inspeção do QC por amostra.",
    ),

    "cantalapiedra2021eggnog": dict(
        lido="abstract",
        estabelece=(
            "Atualização maior do eggNOG-mapper, anotação funcional baseada em "
            "atribuições de ortologia pré-computadas, agora otimizada para "
            "conjuntos (meta)genômicos grandes. A v2 traz genomas e bases "
            "funcionais atualizados para o eggNOG v5 e acrescenta: predição "
            "gênica *de novo* a partir de contigs brutos, predição de ortologia "
            "par-a-par embutida, descoberta rápida de domínios proteicos e "
            "decoração automática de GFF."
        ),
        onde_entra=(
            "Metodologia §11 — substitui TRAPID/Blast2GO/KOBAS 2.0 (este último "
            "descontinuado). A predição a partir de contigs é útil para a via "
            "Trinity secundária, de transcritos ausentes da anotação."
        ),
        ressalva=(
            "Anotação por ortologia herda os limites da cobertura do eggNOG "
            "para Lepidoptera — não verificado quão bem *A. gemmatalis* está "
            "representada."
        ),
    ),

    "wu2021clusterprofiler": dict(
        lido="abstract",
        estabelece=(
            "clusterProfiler 4.0: interface universal de análise de "
            "enriquecimento funcional **para milhares de organismos**, com "
            "ontologias e vias internas mais dados de anotação fornecidos pelo "
            "usuário ou obtidos de bases online, e interfaces no estilo "
            "*dplyr*/*ggplot2*."
        ),
        onde_entra=(
            "Metodologia §11 — enriquecimento GO/KEGG. O suporte a anotação "
            "fornecida pelo usuário é o que viabiliza o uso em organismo sem "
            "pacote `org.*.db` dedicado, que é o caso de *A. gemmatalis*."
        ),
        ressalva=(
            "Para organismo não-modelo o mapeamento GO vem do eggNOG-mapper; a "
            "qualidade do enriquecimento fica limitada pela qualidade dessa "
            "anotação, não pelo pacote."
        ),
    ),

    "fu2012accelerated": dict(
        lido="abstract",
        estabelece="CD-HIT acelerado para agrupamento de dados de sequenciamento de nova geração.",
        onde_entra="Metodologia §11 — remoção de redundância na via Trinity secundária.",
        ressalva="Só metadados e título conferidos; abstract curto, sem números extraídos.",
    ),

    "jones2014interproscan": dict(
        lido="abstract",
        estabelece="InterProScan 5, classificação funcional de proteínas em escala genômica.",
        onde_entra="Metodologia §11 — anotação de domínios, complementar ao eggNOG-mapper.",
        ressalva="Só metadados e título conferidos.",
    ),

    "langfelder2008wgcna": dict(
        lido="abstract",
        estabelece="WGCNA, pacote R para análise de rede de correlação ponderada.",
        onde_entra=(
            "Metodologia §11 — módulos de coexpressão e identificação de hubs, "
            "etapa ausente do `.docx`."
        ),
        ressalva=(
            "Exige número de amostras adequado; com poucas réplicas os módulos "
            "ficam instáveis. Verificar o n antes de prometer WGCNA no projeto."
        ),
    ),

    "langer2025empowering": dict(
        lido="abstract",
        estabelece=(
            "Reporta desenvolvimentos recentes do framework nf-core com a DSL2 "
            "do Nextflow, apresentando uma biblioteca extensa de módulos e "
            "subworkflows que permite adoção progressiva de padrões comuns, e "
            "o enquadra no paradigma **FAIR** (localizável, acessível, "
            "interoperável, reutilizável). Mostra a adoção por comunidades de "
            "pesquisa, incluindo seis consórcios EuroFAANG."
        ),
        onde_entra=(
            "Metodologia — é a referência **recente** (2025) que justifica "
            "adotar padrão nf-core, e conversa com os pipelines Nextflow DSL2 "
            "já existentes localmente."
        ),
        ressalva=(
            "Artigo de comunidade/adoção, não benchmark de desempenho. Não "
            "sustenta afirmação de que nf-core produz resultado melhor, só de "
            "que padroniza e favorece reprodutibilidade."
        ),
    ),

    "fenn2023alternative": dict(
        lido="abstract",
        estabelece=(
            "DICAST, framework modular que integra **onze mapeadores "
            "splice-aware e oito ferramentas de detecção de eventos** de "
            "splicing, com benchmark em dado simulado e em RNA-seq de sangue "
            "total. Aponta que os benchmarks anteriores focaram em "
            "quantificação de isoformas e mapeamento, negligenciando detecção "
            "de eventos. Dois resultados: **STAR e HISAT2 mostraram o melhor "
            "equilíbrio entre desempenho e tempo de execução**, e o desempenho "
            "das ferramentas de detecção de eventos **varia muito, sem nenhuma "
            "superar todas as outras**."
        ),
        onde_entra=(
            "Metodologia §11 — sustenta a escolha de STAR ou HISAT2 para o "
            "alinhamento genoma-guiado, e é a ressalva honesta a declarar ao "
            "escolher rMATS ou DEXSeq para a **hipótese H5** (splicing "
            "alternativo): a escolha de ferramenta não é neutra e nenhuma "
            "domina."
        ),
        ressalva=(
            "Dado humano (sangue total) e simulado. A conclusão sobre "
            "variabilidade entre ferramentas transfere como cautela; o ranking "
            "específico não."
        ),
    ),

    "chen2020differences": dict(
        lido="abstract",
        estabelece=(
            "Compara transcriptomas de intestino médio de cepas resistente e "
            "suscetível de *Chilo suppressalis* frente à toxina Cry1C, com "
            "montagem *de novo* de **139.206 unigenes** a partir de 373 milhões "
            "de leituras Illumina HiSeq e Roche 454."
        ),
        onde_entra=(
            "Tema 2, eixo 2C — desenho análogo ao deste projeto "
            "(transcriptoma de intestino médio, resistente × suscetível), útil "
            "como referência de escala e de estrutura de comparação."
        ),
        ressalva=(
            "Espécie diferente, e o estressor é toxina Bt, não inibidor de "
            "protease. Montagem *de novo*, que é justamente a abordagem que "
            "este projeto abandona por ter genoma de referência. Só o abstract "
            "foi lido; não extraí quais genes saíram diferencialmente expressos."
        ),
    ),

    "athavudeen2026pervasive": dict(
        lido="abstract",
        estabelece=(
            "Investiga a prevalência global, a regulação e a função do "
            "**splicing alternativo não-triplete** (em que as isoformas não "
            "mantêm o mesmo quadro de leitura) *in vivo* em *C. elegans*, "
            "usando RNA-Seq de tipo selvagem e de mutantes deficientes em NMD. "
            "Registra que o splicing não-triplete é às vezes tratado como "
            "evidência de erro ou ruído, e classifica suas consequências "
            "moleculares em três classes, incluindo isoformas sensíveis a NMD."
        ),
        onde_entra=(
            "Tema 2, fronteira — relevante para a **hipótese H5**: se aparecer "
            "splicing alternativo em tripsinas, este trabalho é o argumento de "
            "que nem todo evento não-triplete é ruído, e o alerta de que NMD "
            "precisa ser considerado na interpretação."
        ),
        ressalva=(
            "*C. elegans*, não inseto. Só o abstract foi lido; não extraí as "
            "três classes nem a prevalência quantificada."
        ),
    ),

    "morabito2023hdwgcna": dict(
        lido="abstract",
        estabelece=(
            "hdWGCNA, framework para redes de coexpressão em dados "
            "transcriptômicos de alta dimensão (single-cell e espacial), com "
            "inferência de rede, identificação de módulos, enriquecimento, "
            "testes estatísticos e visualização. Notavelmente, é **capaz de "
            "fazer análise de rede em nível de isoforma** usando single-cell de "
            "leitura longa."
        ),
        onde_entra=(
            "Tema 2, fronteira — a análise de rede **em nível de isoforma** é "
            "conceitualmente o que a hipótese H1 pede, ainda que aqui aplicada "
            "a single-cell."
        ),
        ressalva=(
            "Foi feito para single-cell e espacial; este projeto é bulk RNA-Seq. "
            "Aplicabilidade direta **não verificada** — não citar como "
            "ferramenta escolhida, apenas como direção."
        ),
    ),

    # ---------------- TEMA 3 ----------------

    "abramson2024accurate": dict(
        lido="abstract",
        estabelece=(
            "AlphaFold 3, com arquitetura substancialmente atualizada baseada "
            "em difusão, capaz de predizer a estrutura conjunta de complexos "
            "incluindo proteínas, ácidos nucleicos, moléculas pequenas, íons e "
            "resíduos modificados. Reporta **acurácia muito maior em interações "
            "proteína-ligante do que ferramentas de docking do estado da arte**, "
            "acurácia muito maior em interações proteína-ácido nucleico do que "
            "preditores específicos, e acurácia substancialmente maior em "
            "anticorpo-antígeno do que o AlphaFold-Multimer v2.3."
        ),
        onde_entra=(
            "Metodologia §11 — é a citação da opção de co-folding "
            "proteína-peptídeo que substitui o AutoDock Vina para o ligante "
            "peptídico (correção C5), junto com `tsaban2022harnessing`."
        ),
        ressalva=(
            "A comparação favorável é contra ferramentas de docking para "
            "**proteína-ligante** (molécula pequena); o abstract **não reporta "
            "métrica específica para complexo proteína-peptídeo**, que é o caso "
            "do GORE3. Não citar como evidência de superioridade nessa tarefa "
            "sem ler os resultados. Considerar também a restrição de acesso ao "
            "servidor e as alternativas abertas (Boltz, Chai, Protenix), não "
            "cobertas por este levantamento."
        ),
    ),

    "varadi2024alphafold": dict(
        lido="abstract",
        estabelece=(
            "O AlphaFold DB passou de 300 mil estruturas em 2021 para **mais de "
            "214 milhões** de estruturas preditas, integradas a PDB, UniProt, "
            "Ensembl, InterPro e MobiDB, com releases cobrindo organismos "
            "modelo, proteomas de saúde global e integração com Swiss-Prot."
        ),
        onde_entra=(
            "Metodologia — é onde checar se as tripsinas de *A. gemmatalis* já "
            "têm modelo depositado antes de rodar predição própria."
        ),
        ressalva=(
            "Cobertura por proteoma; **não verificado** se *A. gemmatalis* está "
            "incluída — o genoma é recente (2025). Conferir antes de assumir."
        ),
    ),

    "omidi2024alphafold": dict(
        lido="abstract",
        estabelece=(
            "Avalia quão bem o AlphaFold-Multimer reproduz interações mediadas "
            "por **regiões intrinsecamente desordenadas (IDRs)**, reunindo "
            "conjuntos que cobrem o espectro de modos de ligação de IDR. "
            "Conclui que o AlphaFold-Multimer prediz diversos tipos de "
            "estrutura de IDR ligada **com alta taxa de sucesso**."
        ),
        onde_entra=(
            "Metodologia, bloco estrutural — um pentapeptídeo livre é, na "
            "prática, um segmento desordenado; este é o dado mais próximo "
            "disponível sobre o desempenho de co-folding nesse regime."
        ),
        ressalva=(
            "IDR em contexto de proteína, não peptídeo sintético curto isolado. "
            "Só o abstract foi lido; a frase sobre distinguir predições "
            "verdadeiras está truncada no abstract salvo e **não foi extraída**."
        ),
    ),

    "zalewski2025protein": dict(
        lido="abstract",
        estabelece=(
            "Avalia o modelo de linguagem **ESMFold** para docking "
            "proteína-peptídeo, explorando estratégias como ligantes "
            "poliglicina e modificações que aumentam a amostragem. Resultado "
            "honesto: o número de modelos de qualidade aceitável entre os "
            "melhores ranqueados é **comparável ao de métodos tradicionais e "
            "geralmente inferior ao do AlphaFold-Multimer ou AlphaFold 3**, "
            "embora supere em alguns casos. O valor apontado é a combinação de "
            "qualidade com eficiência computacional, como componente de uma "
            "**abordagem de consenso**."
        ),
        onde_entra=(
            "Metodologia — sustenta a estratégia de consenso entre métodos de "
            "docking em vez de confiar numa ferramenta só, e ancora "
            "expectativas realistas sobre modelos de linguagem nessa tarefa."
        ),
        ressalva=(
            "Contexto de desenho de peptídeos terapêuticos. Não testa peptídeo "
            "em sítio ativo de serino-protease especificamente."
        ),
    ),

    "jiang2018halogen": dict(
        lido="abstract",
        estabelece=(
            "Testa se compostos halogenados podem servir como **grupo P1 para "
            "ligar ao bolsão de especificidade S1** de serino-proteases tipo "
            "tripsina, evitando a baixa biodisponibilidade dos grupos amidina "
            "ou guanidina tipicamente usados. Usa 4-clorobenzilamina, "
            "4-bromobenzilamina e 4-iodobenzilamina como sondas do modo de "
            "ligação."
        ),
        onde_entra=(
            "**Hipótese H6** — é o precedente publicado de que o S1 de uma "
            "tripsina pode ser ocupado por um grupo P1 **não básico**, por "
            "ligação de halogênio em vez de ponte salina com o Asp189. Amplia "
            "o espaço de modos de ligação plausíveis para o LALAY, que também "
            "não tem resíduo básico."
        ),
        ressalva=(
            "Halogênio não é resíduo de aminoácido: o LALAY não tem grupo "
            "halogenado, então o mecanismo específico **não se transfere**. O "
            "que transfere é o princípio de que S1 admite ancoragem sem carga "
            "positiva. Só o abstract foi lido."
        ),
    ),

    "tsaban2022harnessing": dict(
        lido="abstract",
        estabelece=(
            "Mostra que o AlphaFold2, embora concebido para enovelamento de "
            "monômeros, **modela interações peptídeo-proteína de forma rápida e "
            "acurada**. A implementação descrita gera modelos de complexo sem "
            "exigir alinhamento múltiplo para o parceiro peptídico e acomoda "
            "mudanças conformacionais do receptor induzidas pela ligação. Os "
            "autores comparam o comportamento com o protocolo de docking de "
            "peptídeo PIPER-FlexPepDock e discutem o que a rede memorizou."
        ),
        onde_entra=(
            "Metodologia §11, bloco estrutural — é a justificativa publicada "
            "para usar co-folding em vez de AutoDock Vina no ligante peptídico, "
            "que é a correção C5 de `06_correcoes_projeto.md`."
        ),
        ressalva=(
            "O próprio artigo explora o que o AF2 memorizou do conjunto de "
            "treino; para um peptídeo sintético sem homólogo depositado, como o "
            "GORE3, a expectativa de acurácia deve ser menor. Não é um "
            "benchmark cego."
        ),
    ),

    "kahler2018unexpected": dict(
        lido="abstract",
        estabelece=(
            "Simulação de dinâmica molecular de **10 microssegundos** de um "
            "complexo entre a peptidase relacionada a calicreína 7 e um peptídeo. "
            "Após mais de **dois microssegundos** de amostragem irrestrita, "
            "observa-se transição espontânea do modo de ligação, com rotação de "
            "**180° em torno do resíduo P1**: o peptídeo passa a ocupar a região "
            "do **lado prime** em vez do lado não-prime cognato, em conformação "
            "estável. A orientação resultante é semelhante à de estruturas de "
            "calicreínas com inibidor ocupando o lado prime."
        ),
        onde_entra=(
            "**Hipótese H6** — é o precedente publicado de que um peptídeo pode "
            "migrar espontaneamente para o lado prime de uma serino-protease e "
            "permanecer estável ali. Sustenta tanto o *blind docking* quanto a "
            "decisão sobre duração de MD."
        ),
        ressalva=(
            "**Alerta metodológico direto:** a transição só apareceu depois de "
            "dois microssegundos. O projeto prevê 3 × 100 ns — vinte vezes "
            "menos que o tempo em que o evento ocorreu neste sistema. Se o modo "
            "de ligação do GORE3 for análogo, 100 ns não o detectariam. "
            "Ressalva de transferência: é calicreína humana, não tripsina "
            "digestiva de inseto."
        ),
    ),

    # ---------------- TEMA 4 ----------------

    "carpane2022feeding": dict(
        lido="abstract",
        estabelece=(
            "Quantifica o consumo de larvas pequenas (menos de 1 cm) e médias "
            "(1 a 1,5 cm) das principais pragas lepidópteras da soja em tecido "
            "vegetativo e reprodutivo, comparando soja Bt (variedade M7739IPRO, "
            "evento MON87701, que expressa Cry1Ac) e não-Bt (BMX Desafio RR). "
            "Tecido vegetativo avaliado em ensaio de folha destacada em câmara "
            "de crescimento; estruturas reprodutivas em casa de vegetação, com "
            "infestação no florescimento e no enchimento de grãos. O objetivo "
            "declarado é dar base ao **nível de dano econômico** que orienta "
            "aplicação de inseticida."
        ),
        onde_entra=(
            "Introdução — **fonte primária para o dano por lepidópteros na soja "
            "na América do Sul**, substituindo o link de notícia "
            "`agrourbano.com.br` apontado em `06_correcoes_projeto.md` C13."
        ),
        ressalva=(
            "⚠️ Só o abstract foi lido. **Não extraí os valores de consumo nem "
            "confirmei se *A. gemmatalis* está entre as espécies quantificadas** "
            "— conferir no texto completo (`fulltext/carpane2022feeding.txt`) "
            "antes de citar qualquer número."
        ),
    ),

    "ongaratto2021resistance": dict(
        lido="abstract",
        estabelece=(
            "Avalia **30 genótipos de soja** quanto à expressão de antixenose "
            "por testes de oviposição, atratividade e consumo alimentar, e "
            "seleciona 13 genótipos promissores para avaliação seguinte. O "
            "enquadramento é que a estratégia primária de manejo de "
            "*A. gemmatalis* é controle químico e soja Bt transgênica, e que a "
            "resistência da planta hospedeira é alternativa eficiente e menos "
            "agressiva, especialmente dentro de MIP."
        ),
        onde_entra=(
            "Introdução — resistência de planta hospedeira como tática "
            "complementar, e fonte primária para o dano econômico causado por "
            "*A. gemmatalis* na soja."
        ),
        ressalva=(
            "Só o abstract foi lido; não extraí quais genótipos nem os valores. "
            "Classifica *A. gemmatalis* como **Erebidae**."
        ),
    ),

    "castro2019toxicity": dict(
        lido="abstract",
        estabelece=(
            "Avalia a toxicidade de *B. thuringiensis* subsp. *kurstaki* cepa "
            "HD-1 e as alterações citopatológicas no intestino médio de "
            "*A. gemmatalis*, calculando concentrações letais (CL₂₅, CL₅₀, "
            "CL₇₅, CL₉₀ e CL₉₉) e examinando fragmentos de intestino após "
            "ingestão bacteriana."
        ),
        onde_entra=(
            "Introdução — táticas atuais de controle e o alvo intestinal comum "
            "entre Bt e inibidores de protease. Também é referência de "
            "histopatologia de intestino médio da espécie, que conversa com "
            "`coura2022isoforms`."
        ),
        ressalva=(
            "Só o abstract foi lido; **os valores de CL não foram extraídos**. "
            "Classifica *A. gemmatalis* como Noctuidae, divergindo de "
            "`murua2018defoliation` e `ongaratto2021resistance` (Erebidae) — "
            "mais um caso da divergência taxonômica já registrada nas notas."
        ),
    ),

    "fernandes2022phenotypic": dict(
        lido="abstract",
        estabelece=(
            "Avalia a morfometria de adultos de *A. gemmatalis* submetidos a "
            "**subdoses** do bioinseticida à base de Bt (Dipel®) ao longo de "
            "**três gerações**, medindo largura, comprimento e área das asas "
            "anteriores e posteriores e o peso de tegumento, tórax, abdome, "
            "asas e do adulto inteiro, em machos e fêmeas. Registra que "
            "populações resistentes e efeitos subletais já foram reportados, "
            "mas que não havia estudo de plasticidade fenotípica na fase adulta "
            "sob subdoses."
        ),
        onde_entra=(
            "Introdução — efeito subletal e plasticidade ao longo de gerações "
            "como limitação das táticas atuais, e como alerta metodológico: "
            "efeito de um agente pode aparecer em geração posterior."
        ),
        ressalva=(
            "Só o abstract foi lido; **os resultados morfométricos não foram "
            "extraídos**. Curiosidade de citação: o texto grafa o autor do "
            "táxon Bt como 'Berliner, 1915' — o `.docx` do projeto cita "
            "'Berliner 1911', que segue como referência não localizada "
            "(ver `05_AUDITORIA_REFS_DOCX.md`); **pode ser a origem da "
            "citação, mas isso é hipótese, não verificação**."
        ),
    ),

    "bel2019specific": dict(
        lido="abstract",
        estabelece=(
            "Investiga suscetibilidade e ligação à membrana de borda em escova "
            "de *A. gemmatalis* e *Chrysodeixis includens* à toxina Cry1Ea. "
            "Bioensaios em larvas de primeiro ínstar mostraram atividade "
            "potente contra as duas pragas. Ensaios de competição com Cry1Ea "
            "marcada com ¹²⁵I demonstraram sítios de ligação específicos nas "
            "vesículas de membrana das duas espécies, e a competição "
            "heteróloga indicou que **Cry1Ea não compartilha sítios de ligação "
            "com Cry1Ac nem com Cry1Fa**."
        ),
        onde_entra=(
            "Introdução — base para o argumento de manejo de resistência: "
            "toxinas com sítios de ligação distintos podem ser combinadas. "
            "Contextualiza o valor de um mecanismo adicional e independente, "
            "como a inibição de protease."
        ),
        ressalva="Só o abstract foi lido; sem os valores de CL ou de afinidade.",
    ),

    "brito2015pangenome": dict(
        lido="abstract",
        estabelece=(
            "Comparação de genoma completo entre **17 isolados selvagens** do "
            "AgMNPV, descrito como o bioinseticida viral de maior sucesso do "
            "mundo, extensamente usado nos anos 1980 e 1990 no controle de "
            "*A. gemmatalis* em soja. O pangenoma contém **pelo menos 167 genes "
            "hipotéticos, 151 deles compartilhados por todos os genomas**; o "
            "gene *bro-a*, possivelmente envolvido em especificidade de "
            "hospedeiro, está ausente em alguns genomas."
        ),
        onde_entra=(
            "Introdução — o AgMNPV é o precedente histórico de controle "
            "biológico bem-sucedido desta praga específica, e portanto a "
            "referência contra a qual qualquer alternativa é julgada."
        ),
        ressalva=(
            "Só o abstract foi lido. É genômica viral; não informa sobre a "
            "fisiologia digestiva do inseto. O declínio de uso do AgMNPV a "
            "partir dos anos 2000 **não é abordado no abstract** e não deve ser "
            "afirmado a partir daqui."
        ),
    ),

    "costa2026chemical": dict(
        lido="abstract",
        estabelece=(
            "Mecanismos de defesa química de genótipos de soja contra "
            "lepidópteros desfolhadores — *A. gemmatalis*, *C. includens*, "
            "*H. armigera* e espécies de *Spodoptera*. Registra que as "
            "estratégias convencionais baseadas em inseticida químico dão "
            "controle apenas parcial com impacto ambiental, e que a **soja Bt, "
            "embora eficaz contra algumas espécies, tem toxicidade limitada "
            "contra *Spodoptera***."
        ),
        onde_entra=(
            "Introdução — referência de 2026 para o enquadramento do problema e "
            "para a lacuna deixada pelo Bt, que é o espaço que um inibidor "
            "peptídico ocuparia."
        ),
        ressalva=(
            "Só o abstract foi lido, e a frase sobre *Spodoptera* está truncada "
            "no texto salvo. Não extraí quais compostos nem quais genótipos."
        ),
    ),

    "ramos2021identification": dict(
        lido="abstract",
        estabelece=(
            "Identifica em *A. gemmatalis* a sequência de um peptídeo "
            "semelhante a cecropina B (**AgCecropB**), clona-a sem o peptídeo "
            "sinal em vetor plasmidial bacteriano para expressão heteróloga e "
            "realiza testes antimicrobianos."
        ),
        onde_entra=(
            "Tema 4, eixo 4C — precedente de **expressão heteróloga de "
            "peptídeo derivado da própria *A. gemmatalis***, útil como "
            "referência de viabilidade técnica de produção recombinante, que "
            "conversa com `andrade2026recombinant` (GORE 1-2 T)."
        ),
        ressalva=(
            "É peptídeo antimicrobiano da imunidade do inseto, **não inibidor "
            "de protease digestiva** — o alvo e o mecanismo são outros. Só o "
            "abstract foi lido; sem resultados dos testes antimicrobianos."
        ),
    ),

    "murua2018defoliation": dict(
        lido="abstract",
        estabelece=(
            "Avalia soja expressando Cry1Ac contra pragas lepidópteras alvo e "
            "não-alvo, comparada a soja não-Bt com e sem tratamento de semente "
            "(inseticida diamida Fortenza). Lista *A. gemmatalis* entre as "
            "pragas primárias de Lepidoptera da soja e **a classifica como "
            "Erebidae**. Levanta explicitamente o risco de que o uso de plantas "
            "transgênicas, ao reduzir a aplicação de inseticida contra as "
            "pragas-alvo, permita que **outras espécies se tornem mais "
            "prevalentes** no agroecossistema."
        ),
        onde_entra=(
            "Introdução — táticas atuais de manejo e a limitação do Bt, que é o "
            "espaço que um inibidor peptídico com mecanismo distinto ocuparia. "
            "Também documenta o uso de **Erebidae**, reforçando a divergência "
            "taxonômica Noctuidae/Erebidae já registrada nas notas."
        ),
        ressalva=(
            "⚠️ Só o abstract foi lido; sem os valores de desfolha. Contexto "
            "argentino."
        ),
    ),

    "patarroyovargas2020inhibition": dict(
        lido="abstract",
        estabelece=(
            "Caracterização cinética das tripsinas intestinais de "
            "*A. gemmatalis*, purificadas em coluna de p-aminobenzamidina "
            "agarose. Para o substrato L-BApNA: **KM = 0,503 mM**, "
            "Vmax = 46,650 nM·s⁻¹. Ki dos inibidores, **todos com inibição "
            "competitiva linear**: benzamidina 11,2 µM, berenil 32,4 µM, "
            "**SKTI 0,25 nM** e SBBI 1,4 nM. O SKTI foi o mais potente, e os "
            "autores concluem apontando-o como ponto de partida para a "
            "fabricação de **peptídeos miméticos** — que é exatamente a linha "
            "que originou a série GORE."
        ),
        onde_entra=(
            "Introdução — é a linha de base cinética contra a qual todo Ki da "
            "série GORE deve ser comparado, e a justificativa publicada da "
            "estratégia de peptídeos miméticos. Metodologia — o KM de 0,503 mM "
            "é o parâmetro do ensaio a reproduzir."
        ),
        ressalva=(
            "O Ki da benzamidina aqui (11,2 µM) difere do de Schultz et al. "
            "2026 (16,70 µM) e do de Paulo et al. 2026 (16,49 µM), mas essas "
            "duas medidas são em *S. frugiperda* e esta é em *A. gemmatalis* — "
            "espécies diferentes, não é discrepância. Só o abstract foi lido; "
            "o PDF está em `pdfs/patarroyovargas2020inhibition.pdf`."
        ),
    ),

    "pilon2018protease": dict(
        lido="abstract",
        estabelece=(
            "Benzamidina **pulverizada sobre plantas de soja** aumentou a "
            "atividade de inibição de tripsina na folha e reduziu a atividade "
            "proteolítica total no extrato de intestino médio das larvas que "
            "se alimentaram dessas folhas. Diferentes concentrações causaram "
            "cerca de **50% de mortalidade larval**, e afetaram negativamente a "
            "escolha da larva, a preferência da mariposa e a oviposição. "
            "**Concentrações baixas aumentaram a mortalidade e prejudicaram "
            "escolha e oviposição tanto quanto as doses altas.** O enquadramento "
            "declarado é o de base para desenvolver peptídeos miméticos como "
            "inseticidas biorracionais."
        ),
        onde_entra=(
            "Introdução — prova de conceito de que inibição de protease "
            "funciona em campo por pulverização, não só em dieta artificial, e "
            "de que há efeito comportamental (deterrência) além do digestivo."
        ),
        ressalva=(
            "A observação de que dose baixa iguala dose alta é relevante para "
            "ler a curva não monotônica de Paulo et al. 2026 (§8.1 das notas) — "
            "mas aqui é benzamidina, outro composto. Classifica "
            "*A. gemmatalis* como **Erebidae**. Só o abstract foi lido."
        ),
    ),

    "lanzaro2024toxin": dict(
        lido="abstract",
        estabelece=(
            "Caracteriza as aminopeptidases N (APNs) do intestino médio de "
            "*A. gemmatalis* e identifica receptor para a toxina Cry1Ac. O "
            "enquadramento é que mutações em receptores de Cry (APN, fosfatase "
            "alcalina, caderina) estão entre os fatores associados ao "
            "desenvolvimento de resistência, e que identificar os receptores "
            "funcionais é pré-requisito para estratégias que contornem esse "
            "cenário."
        ),
        onde_entra=(
            "Introdução — documenta que a via Bt em *A. gemmatalis* tem "
            "mecanismo de resistência mapeável, o que sustenta o argumento de "
            "buscar um modo de ação distinto (inibição de protease digestiva). "
            "Também é fonte de referência sobre o proteoma do intestino médio "
            "da espécie."
        ),
        ressalva=(
            "Só o abstract foi lido. A entrada já existente em "
            "`docs/referencias.bib` registra '10 APNs no transcriptoma; 7 "
            "confirmadas como ligantes de Cry1Ac' — **esses números não foram "
            "reconferidos nesta leitura**."
        ),
    ),

    "assis2026insect": dict(
        lido="abstract",
        estabelece=(
            "O genótipo de soja resistente IAC 17 acumula não só rutina "
            "(quercetina 3-O-rutinosídeo, [M+H]⁺ = 611 Da) mas também seu "
            "derivado **O-metilado isoramnetina 3-O-rutinosídeo (narcisina, "
            "[M+H]⁺ = 625 Da)**. O composto de 625 Da foi purificado por "
            "HPLC de fase reversa e confirmado estruturalmente por "
            "cromatografia líquida. O trabalho combina identificação de "
            "metabólito, ensaio biológico e modelagem baseada em estrutura, e "
            "argumenta que o papel da **O-metilação de flavonóis** no reforço "
            "da defesa vegetal não havia sido demonstrado antes."
        ),
        onde_entra=(
            "Introdução — defesa química da soja contra *A. gemmatalis* como "
            "contexto para a defesa por inibidor de protease, e precedente "
            "recente de trabalho que integra metabólito, bioensaio e modelagem "
            "estrutural no mesmo sistema planta-praga."
        ),
        ressalva=(
            "Só o abstract foi lido. A entrada já em `docs/referencias.bib` "
            "cita '~95% de mortalidade em 5 dias' e 'docking contra 70 "
            "proteínas do intestino' — **não reconferidos nesta leitura**. "
            "O alvo é enzima digestiva e de detoxificação, não tripsina "
            "especificamente."
        ),
    ),

    "fonseca2023soybean": dict(
        lido="abstract",
        estabelece=(
            "Testa se um inibidor de tripsina de soja (SBTI) atrapalha o "
            "desenvolvimento de populações suscetível e resistente a Bt de "
            "*S. frugiperda* alimentadas em milho Bt (expressando Cry1F, "
            "Cry1A.105 e Cry2Ab2) e não-Bt. A justificativa declarada é que, no "
            "intestino de lepidópteros, serino-proteases participam tanto da "
            "digestão de proteína dietética quanto da **ativação ou degradação "
            "das proteínas inseticidas** — ou seja, inibir protease interfere "
            "no próprio mecanismo do Bt."
        ),
        onde_entra=(
            "Introdução — precedente de combinação inibidor de protease × Bt, e "
            "de efeito sobre população **já resistente**, que é um argumento "
            "forte para o valor prático de inibidores peptídicos."
        ),
        ressalva=(
            "⚠️ Só o abstract foi lido. O título afirma que o SBTI *reduz* a "
            "resistência ao milho transgênico, mas **não conferi a magnitude "
            "nem em qual população** — não citar efeito quantificado sem ler os "
            "resultados. É *S. frugiperda* em milho, não *A. gemmatalis* em soja."
        ),
    ),
}
