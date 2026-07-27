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
        lido="abstract",
        estabelece=(
            "Benchmark de quantificação de isoformas de comprimento completo "
            "com dado simulado que reproduz propriedades do dado real "
            "(polimorfismo, sinal de íntron, cobertura não uniforme), cobrindo "
            "métodos baseados em genoma, em transcriptoma e em pseudoalinhamento, "
            "com uma abordagem simples como controle. Salmon, kallisto, RSEM e "
            "Cufflinks têm a maior acurácia em dado idealizado, mas **em dado "
            "realista não superam dramaticamente a abordagem simples**. Os "
            "parâmetros estruturais de maior impacto na acurácia são "
            "comprimento e complexidade de compressão da sequência, **não o "
            "número de isoformas**."
        ),
        onde_entra=(
            "Metodologia — calibra a expectativa sobre quantificação por "
            "isoforma, que é a base operacional da H1, e é a ressalva honesta a "
            "declarar junto com a escolha do Salmon."
        ),
        ressalva=(
            "Dado simulado. O efeito de anotação incompleta é investigado no "
            "artigo, mas não extraí a conclusão específica sobre esse ponto — "
            "que é justamente o mais relevante aqui. Requer leitura do texto "
            "completo antes de citar como justificativa nesse aspecto."
        ),
    ),

    "coxe2024benchmarking": dict(
        lido="abstract",
        estabelece=(
            "Benchmark de cinco alinhadores de RNA-Seq muito usados, com dado "
            "simulado de *Arabidopsis thaliana* e SNPs anotados do TAIR, "
            "medindo acurácia em resolução de base e de base de junção. A "
            "motivação declarada é que as ferramentas são tipicamente "
            "pré-ajustadas com dados humanos ou procarióticos e **podem não ser "
            "adequadas a outros organismos**."
        ),
        onde_entra=(
            "Metodologia — é o argumento publicado de que benchmark feito em "
            "humano não transfere automaticamente para outro clado, que "
            "sustenta declarar a escolha de alinhador como decisão e não como "
            "padrão herdado."
        ),
        ressalva=(
            "É planta, não inseto. O argumento sobre transferência entre clados "
            "vale; o ranking numérico específico não se transfere para "
            "*A. gemmatalis*. Não extraí qual alinhador venceu."
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

    # ---------------- TEMA 3 ----------------

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
