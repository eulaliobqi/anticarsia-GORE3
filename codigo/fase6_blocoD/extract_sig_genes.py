"""FASE 6, Bloco D - extracao dos genes com splicing significativo por
contraste, nos dois motores (rMATS-turbo e MAJIQ), e calculo da
convergencia (Jaccard) entre eles.

Limiares declarados ANTES de contar, mesmo padrao das fases anteriores:
- rMATS-turbo: FDR < 0.05 e |IncLevelDifference| >= 0.1 (limiar padrao
  comumente usado, nao ajustado a este dataset).
- MAJIQ: probability_changing >= 0.9 (convencao propria do MAJIQ para
  "P(|dPSI|>0.2) alta").

Roda no servidor (le diretamente os *.MATS.JC.txt de
resultados_server/fase6_blocoB/ e o *.deltapsi.tsv de
resultados_server/fase6_blocoC/deltapsi/, que sao grandes/nao
versionados) e escreve os resumos pequenos em
resultados_server/fase6_blocoD/ - de la, foram copiados para
resultados/fase6_blocoD/ (versionado, pequeno o suficiente).
"""
import csv
import os

RMATS_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/resultados_server/fase6_blocoB")
MAJIQ_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/resultados_server/fase6_blocoC/deltapsi")
OUT_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/resultados_server/fase6_blocoD")
os.makedirs(OUT_DIR, exist_ok=True)

FDR_THRESH = 0.05
DPSI_THRESH = 0.1
PC_THRESH = 0.9

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]

for contrast in CONTRASTS:
    # rMATS: unir os 5 tipos de evento, coletar GeneID + o proprio tipo/coordenadas
    rmats_rows = []
    for ev in ["SE", "A5SS", "A3SS", "MXE", "RI"]:
        path = os.path.join(RMATS_DIR, contrast, f"{ev}.MATS.JC.txt")
        with open(path) as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                try:
                    fdr = float(row["FDR"])
                    dpsi = float(row["IncLevelDifference"])
                except (ValueError, KeyError):
                    continue
                if fdr < FDR_THRESH and abs(dpsi) >= DPSI_THRESH:
                    rmats_rows.append({
                        "gene_id": row["GeneID"].strip('"'),
                        "gene_symbol": row.get("geneSymbol", "").strip('"'),
                        "event_type": ev,
                        "FDR": fdr,
                        "IncLevelDifference": dpsi,
                    })
    with open(os.path.join(OUT_DIR, f"rmats_sig_{contrast}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["gene_id", "gene_symbol", "event_type", "FDR", "IncLevelDifference"])
        w.writeheader()
        w.writerows(rmats_rows)

    # MAJIQ deltapsi TSV: primeira linha e um comentario JSON de metadados
    # (prefixo "#"), a linha seguinte e' o cabecalho real das colunas.
    path = os.path.join(MAJIQ_DIR, f"{contrast}.deltapsi.tsv")
    majiq_rows = []
    with open(path) as f:
        header_line = None
        for line in f:
            if line.startswith("#"):
                continue
            header_line = line
            break
        reader = csv.DictReader(f, delimiter="\t", fieldnames=header_line.strip("\n").split("\t"))
        for row in reader:
            try:
                pc = float(row["probability_changing"])
                dpsi = float(row["dpsi_mean"])
            except (ValueError, KeyError):
                continue
            if pc >= PC_THRESH:
                majiq_rows.append({
                    "gene_id": row["gene_id"],
                    "gene_symbol": row["gene_name"],
                    "event_type": row["event_type"],
                    "probability_changing": pc,
                    "dpsi_mean": dpsi,
                })
    with open(os.path.join(OUT_DIR, f"majiq_sig_{contrast}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["gene_id", "gene_symbol", "event_type", "probability_changing", "dpsi_mean"])
        w.writeheader()
        w.writerows(majiq_rows)

    rmats_genes = set(r["gene_id"] for r in rmats_rows)
    majiq_genes = set(r["gene_id"] for r in majiq_rows)
    inter = rmats_genes & majiq_genes
    union = rmats_genes | majiq_genes
    jacc = len(inter) / len(union) if union else 0.0
    print(f"{contrast}: rMATS_genes={len(rmats_genes)} MAJIQ_genes={len(majiq_genes)} "
          f"intersecao={len(inter)} uniao={len(union)} jaccard={jacc:.3f}")

print("FASE6_BLOCOD_EXTRACT_DONE_MARKER")
