"""FASE 9, Bloco C, passo 3 - segunda camada de curadoria: confirma que
o His (PS00134) e o Ser (PS00135) de cada candidato caem na MESMA coluna
do MSA que o His/Ser catalitico das 2 referencias conhecidas (tripsina
bovina 1TGN_A e tripsina de A. gemmatalis XP_075977317.1) - nao so "tem
o motivo em algum lugar da sequencia" (Bloco B), mas "tem o motivo na
posicao estruturalmente equivalente a uma tripsina catalitica
confirmada".

Nota metodologica declarada, nao escondida: o terceiro membro da triade
(Asp102) nao tem um padrao PROSITE de sequencia unico e confiavel como
His/Ser - a verificacao geometrica real dele (angulos/distancias
Ser-His-Asp: Oγ-Ser⋯Nε2-His 2,0-2,7A, Nδ1-His⋯Oδ1-Asp 1,6-2,0A, angulo
115-140°) fica para o Bloco F/FASE 9.5, sobre estrutura 3D predita, nao
por MSA de sequencia aqui.

Achado real corrigido durante a execucao (nao escondido): a 1a versao
deste script tinha um bug de indice (calculava a posicao do Ser
catalitico como o 5o caractere do match PS00135, deveria ser o 7o -
G-[DE]-S e' indice 4-5-6 no padrao, nao 2-3-4) - dava 0/168 aprovados por
erro de codigo, nao por sinal biologico. Corrigido e conferido contra o
contexto de sequencia real das 2 referencias antes de aceitar o
resultado.
"""
import re
from Bio import AlignIO

PS00134 = re.compile(r"[LIVM][ST]A[STAG]HC")
PS00135 = re.compile(r"[DNSTAGC][GSTAPIMVQH].{2}G[DE]SG[GS][SAPHV][LIVMFYWH][LIVMFYSTANQH]")

aln = AlignIO.read("/home/eulalio/rnaseq-Anticarsia-GORE3/resultados_server/fase9_blocoC_domain_aligned.fasta", "fasta")
by_id = {rec.id: str(rec.seq) for rec in aln}


def ungapped_to_col(aligned_seq, ungapped_pos):
    """posicao 1-based na sequencia sem gap -> indice de coluna (0-based) no alinhamento"""
    count = 0
    for col, ch in enumerate(aligned_seq):
        if ch != "-":
            count += 1
            if count == ungapped_pos:
                return col
    return None


def find_motif_col(rec_id, pattern):
    aligned = by_id[rec_id]
    ungapped = aligned.replace("-", "")
    m = pattern.search(ungapped)
    if not m:
        return None, None
    return m, ungapped


def key_residue_ungapped_pos(match, which):
    start = match.start()
    if which == "His":
        # PS00134 = [LIVM]-[ST]-A-[STAG]-H-C -> His e' o indice 4 (penultimo) do match
        return start + len(match.group(0)) - 2 + 1  # 1-based
    if which == "Ser":
        # PS00135 = [DNSTAGC]-[GSTAPIMVQH]-x-x-G-[DE]-S-... -> Ser catalitico e' indice 6
        return start + 6 + 1  # 1-based


refs = {}
for ref_id in ["1TGN_A_bovine_trypsinogen_reference", "XP_075977317.1_Agemmatalis_trypsin_reference"]:
    m, ungapped = find_motif_col(ref_id, PS00134)
    pos = key_residue_ungapped_pos(m, "His")
    col = ungapped_to_col(by_id[ref_id], pos)
    refs.setdefault(ref_id, {})["His_col"] = col
    print(f"{ref_id}: His ungapped={pos}, col MSA={col}, contexto={ungapped[max(0,pos-6):pos+5]}")

    m, ungapped = find_motif_col(ref_id, PS00135)
    pos = key_residue_ungapped_pos(m, "Ser")
    col = ungapped_to_col(by_id[ref_id], pos)
    refs.setdefault(ref_id, {})["Ser_col"] = col
    print(f"{ref_id}: Ser ungapped={pos}, col MSA={col}, contexto={ungapped[max(0,pos-6):pos+5]}")

his_cols = {refs[r]["His_col"] for r in refs}
ser_cols = {refs[r]["Ser_col"] for r in refs}
print(f"\nColunas His das 2 referencias coincidem? {his_cols}")
print(f"Colunas Ser das 2 referencias coincidem? {ser_cols}")

assert len(his_cols) == 1 and len(ser_cols) == 1, (
    "referencias NAO coincidem na mesma coluna - checagem cruzada de posicao invalida, nao prosseguir"
)

his_col = his_cols.pop()
ser_col = ser_cols.pop()
print(f"\nUsando His_col={his_col}, Ser_col={ser_col} (0-based) para os 168 candidatos")

import csv
rows = []
for rec in aln:
    if rec.id in refs:
        continue
    seq = str(rec.seq)
    his_res = seq[his_col] if his_col < len(seq) else "-"
    ser_res = seq[ser_col] if ser_col < len(seq) else "-"
    his_ok = his_res == "H"
    ser_ok = ser_res == "S"
    rows.append({
        "gene_id": rec.id,
        "residue_at_His_col": his_res,
        "His_at_reference_column": "PASS" if his_ok else "FAIL",
        "residue_at_Ser_col": ser_res,
        "Ser_at_reference_column": "PASS" if ser_ok else "FAIL",
        "curated_pass": "PASS" if (his_ok and ser_ok) else "FAIL",
    })

out = "/home/eulalio/rnaseq-Anticarsia-GORE3/resultados_server/fase9_blocoC_triad_curated.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

n_pass = sum(1 for r in rows if r["curated_pass"] == "PASS")
print(f"\nCandidatos com His+Ser na coluna estruturalmente equivalente as referencias: {n_pass}/{len(rows)}")
print(f"salvo em {out}")
