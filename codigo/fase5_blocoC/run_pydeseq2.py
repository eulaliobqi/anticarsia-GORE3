#!/usr/bin/env python3
"""FASE 5, Bloco C2 (Python) - segunda implementacao independente do modelo
estatistico, pedido explicito do usuario ("nao use somente R, explore
tambem o python"). Usa PyDESeq2 (Muzellec et al. 2023, PMID 37669147,
mantido por scverse) sobre as MESMAS contagens de gene do tximport (Bloco
B) que alimentam o DESeq2 em R (Bloco C1) - controla a variavel de
quantificacao upstream, isolando a comparacao no motor estatistico em si.

ASSIMETRIA DECLARADA, NAO ESCONDIDA: o PyDESeq2 nao tem equivalente ao
offset de comprimento de transcrito do tximport (verificado direto no
codigo-fonte, pydeseq2/ds.py: so existe log(size_factors), escalar por
amostra, nao uma matriz gene x amostra). Esta via roda sem essa correcao
de vies - a concordancia com o R (Bloco E) precisa ser lida com essa
ressalva em mente, nao como comparacao 100% equivalente.
"""
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

COUNTS_CSV = "resultados_server/fase5_blocoB/txi_counts_for_python.csv"
SAMPLESHEET = "resultados/fase3_blocoE_samplesheet.csv"
OUT_DIR = "resultados_server/fase5_blocoC"

CONTRASTS = [
    ("condition", "Benzamidine", "Control"),
    ("condition", "SKTI", "Control"),
    ("condition", "GORE3", "Control"),
]


def main():
    counts = pd.read_csv(COUNTS_CSV, index_col=0)  # amostras x genes

    metadata = pd.read_csv(SAMPLESHEET, index_col="sample")
    metadata = metadata[metadata["condition"] != "FatBody"]  # mesmo motivo do R: ID-18 fora do desenho
    metadata = metadata.loc[counts.index]  # mesma ordem de amostras

    # Controle como referencia - mesma convencao do lado R (Bloco C1),
    # para os coeficientes/contrastes serem diretamente comparaveis.
    metadata["condition"] = pd.Categorical(
        metadata["condition"], categories=["Control", "Benzamidine", "SKTI", "GORE3"]
    )

    # Filtro de baixa contagem: rowSums >= 10 - mesmo criterio do lado R
    # (soma por GENE across as amostras; aqui as amostras sao linhas,
    # entao soma por coluna).
    n_before = counts.shape[1]
    keep = counts.sum(axis=0) >= 10
    counts = counts.loc[:, keep]
    print(f"Filtro baixa contagem: {n_before} -> {counts.shape[1]} genes (soma >= 10)")

    # `ref_level=` foi testado num teste-piloto com dado sintetico (12
    # amostras, 4 grupos) e confirmado DEPRECIADO nesta versao (0.5.4) -
    # "no longer has any effect" - nao passar, so gera aviso. O nivel de
    # referencia (Controle) e' controlado pela ORDEM das categorias do
    # dtype categorico de `condition` (primeiro nivel = referencia,
    # confirmado no mesmo teste-piloto: LFC columns saem como
    # "condition[T.Benzamidine]" etc., nao "Control" - Control absorvido
    # no Intercept, exatamente o comportamento esperado).
    dds = DeseqDataSet(
        counts=counts,
        metadata=metadata,
        design="~condition",
        refit_cooks=True,
    )
    dds.deseq2()

    import os
    os.makedirs(OUT_DIR, exist_ok=True)

    for factor, tratamento, referencia in CONTRASTS:
        stat = DeseqStats(dds, contrast=[factor, tratamento, referencia], alpha=0.05)
        stat.summary()
        # Nomenclatura de coeficiente do PyDESeq2 (formulaic/patsy-style,
        # confirmada em teste-piloto com dado sintetico - NAO e'
        # "condition_X_vs_Control" como no R): "condition[T.<nivel>]".
        stat.lfc_shrink(coeff=f"{factor}[T.{tratamento}]")
        res = stat.results_df
        out_path = f"{OUT_DIR}/pydeseq2_{tratamento}_vs_{referencia}_all.csv"
        res.to_csv(out_path)
        print(f"Escrito: {out_path} ({res.shape[0]} genes)")

    print("PyDESeq2 concluido para os 3 contrastes.")


if __name__ == "__main__":
    main()
