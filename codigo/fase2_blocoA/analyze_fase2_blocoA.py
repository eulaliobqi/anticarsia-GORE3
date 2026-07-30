"""
FASE 2, Bloco A - compara STAR vs. HISAT2 (ambos com indice ANOTADO,
RS_2026_04) na subamostra de 2M pares, e compara os dois contra o piloto
HISAT2 SEM anotacao do Bloco C (FASE 1) para medir o ganho da anotacao.

Por que comparamos assim:
- STAR e HISAT2 sao os dois candidatos aceitos pelo "padrao ouro" do
  projeto (docs/03_metodologia_padrao_ouro.md) para a via de expressao
  genica - nenhum documento escolhe um sobre o outro, entao decidimos com
  dado real em vez de preferencia.
- O piloto do Bloco C (fase1_blocoC/analyze_blocoC.py ->
  resultados/blocoC_param_sweep.csv, coluna "hisat2_overall_alignment_pct",
  linhas com set == "setB") usou HISAT2 sem anotacao - reaproveitar esse
  numero aqui, em vez de rodar de novo, mostra o quanto a anotacao real
  melhora o mapeamento sem gastar tempo de maquina extra.
"""
import csv
import os
import re

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/fase2_blocoA_test")
BLOCOC_CSV = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/resultados/blocoC_param_sweep.csv")
OUT_CSV = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/resultados/fase2_blocoA_star_vs_hisat2.csv")

SAMPLES = ["ID-1", "ID-7", "ID-8", "ID-9", "ID-10"]
LABELS = {
    "ID-1": "Control_R1 (limpa)", "ID-7": "Benzamidine_R2",
    "ID-8": "Benzamidine_R3", "ID-9": "SKTI_R1", "ID-10": "SKTI_R2",
}
APPROVAL_THRESHOLD = 80.0  # unico criterio numerico do projeto (docs/07_analise_rnaseq.md)


def parse_star_log_final_out(path):
    """
    Le o Log.final.out que o STAR gera para cada amostra e extrai a taxa de
    mapeamento "geral", definida aqui (pratica comum em RNA-Seq) como a
    soma de:
      - "Uniquely mapped reads %"            -> read mapeia num unico lugar
      - "% of reads mapped to multiple loci" -> read mapeia em >1 lugar
    Excluimos de proposito "too many loci" e as categorias de "unmapped"
    (mismatches demais / curto demais / outro motivo), porque essas nao
    contam como "mapeado" em nenhum sentido util para o criterio de
    aprovacao do projeto (>80%, docs/07_analise_rnaseq.md).
    """
    with open(path) as f:
        text = f.read()
    uniquely = re.search(r"Uniquely mapped reads %\s*\|\s*([\d.]+)%", text)
    multi = re.search(r"% of reads mapped to multiple loci\s*\|\s*([\d.]+)%", text)
    if not uniquely or not multi:
        return None
    return round(float(uniquely.group(1)) + float(multi.group(1)), 2)


def parse_hisat2_summary(path):
    """Mesma logica de parsing usada em fase1_blocoC/analyze_blocoC.py -
    procura a linha 'XX.XX% overall alignment rate' que o HISAT2 escreve
    no arquivo passado via --summary-file."""
    if not os.path.exists(path):
        return None
    with open(path) as f:
        text = f.read()
    m = re.search(r"([\d.]+)%\s*overall alignment rate", text)
    return float(m.group(1)) if m else None


def load_blocoC_pilot_rates():
    """Recupera, do CSV ja gerado na FASE 1/Bloco C, a taxa de mapeamento
    do indice HISAT2 SEM anotacao (Set B = configuracao de trimagem de
    producao, a unica relevante aqui - o Bloco C testou varios *sets de
    trimagem*, nao varios indices; para esta comparacao usamos so a linha
    setB porque e' o dado de trimagem que realmente vai para producao)."""
    pilot = {}
    with open(BLOCOC_CSV, newline="") as f:
        for row in csv.DictReader(f):
            if row["set"] == "setB":
                pilot[row["id"]] = float(row["hisat2_overall_alignment_pct"])
    return pilot


rows = []
pilot_rates = load_blocoC_pilot_rates()

for s in SAMPLES:
    star_rate = parse_star_log_final_out(
        os.path.join(QC_DIR, f"{s}_STAR_Log.final.out"))
    hisat2_rate = parse_hisat2_summary(
        os.path.join(QC_DIR, f"{s}_HISAT2_annotated.hisat2_summary.txt"))
    pilot_rate = pilot_rates.get(s)

    rows.append(dict(
        id=s, label=LABELS[s],
        star_mapping_pct=star_rate,
        hisat2_annotated_mapping_pct=hisat2_rate,
        hisat2_pilot_no_annotation_pct=pilot_rate,
        # ganho de anotacao = quanto o indice anotado melhorou sobre o
        # piloto sem anotacao, usando o MESMO alinhador (HISAT2) dos dois
        # lados - isolando o efeito da anotacao do efeito de trocar de
        # ferramenta.
        annotation_gain_pp=(round(hisat2_rate - pilot_rate, 2)
                             if hisat2_rate is not None and pilot_rate is not None else None),
        star_vs_hisat2_diff_pp=(round(star_rate - hisat2_rate, 2)
                                 if star_rate is not None and hisat2_rate is not None else None),
        star_meets_80pct=(star_rate is not None and star_rate > APPROVAL_THRESHOLD),
        hisat2_meets_80pct=(hisat2_rate is not None and hisat2_rate > APPROVAL_THRESHOLD),
    ))

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
with open(OUT_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

hdr = list(rows[0].keys())
print("\t".join(hdr))
for r in rows:
    print("\t".join(str(r[h]) for h in hdr))
print(f"\nCSV: {OUT_CSV}")

# ---- Decisao pre-declarada (mesmo criterio combinado com o usuario) ----
# Se a diferenca MEDIA (STAR - HISAT2) nas 5 amostras for >= 2 pontos
# percentuais, o Bloco B roda so o vencedor nas 13 bibliotecas completas
# (economiza tempo de maquina). Se for < 2pp (dentro do que consideramos
# ruido de amostragem/indice, mesmo limiar de "ganho real" usado no
# Bloco C), o Bloco B roda os DOIS completos, ja que o padrao ouro aceita
# qualquer um e a redundancia vira validacao cruzada sem custo alto.
diffs = [r["star_vs_hisat2_diff_pp"] for r in rows if r["star_vs_hisat2_diff_pp"] is not None]
mean_diff = round(sum(diffs) / len(diffs), 2) if diffs else None
print(f"\n=== Decisao Bloco A -> Bloco B ===")
print(f"Diferenca media STAR - HISAT2 (pp): {mean_diff}")
if mean_diff is None:
    print("Nao foi possivel calcular (dados faltando) - revisar logs antes de decidir.")
elif abs(mean_diff) >= 2.0:
    winner = "STAR" if mean_diff > 0 else "HISAT2"
    print(f"=> Diferenca >= 2pp: rodar SO {winner} nas 13 bibliotecas completas no Bloco B.")
else:
    print("=> Diferenca < 2pp (ruido): rodar STAR E HISAT2 completos no Bloco B (redundancia/validacao cruzada).")
