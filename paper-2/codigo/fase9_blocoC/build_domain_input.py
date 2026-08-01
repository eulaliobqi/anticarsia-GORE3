"""FASE 9, Bloco C, passo 1 - monta o FASTA de entrada para a MSA da
triade catalitica: so a REGIAO DO DOMINIO Pfam PF00089 (env coord do
hmmscan da FASE 7) de cada um dos 168 candidatos que passaram o Bloco B
(motivo PROSITE), + 2 sequencias de referencia conhecidas.

Achado real, corrigido antes de rodar a versao final: a 1a tentativa
alinhou as proteinas INTEIRAS (full-length) e nenhum dos 168 candidatos
bateu a coluna catalitica das referencias no MSA resultante - PF00089
cobre um cla inteiro com arquiteturas de dominio muito diferentes (ex.
CLIP-domain antes do dominio tripsina em varios candidatos, confirmado
olhando o domtblout real de gene-BAEE/XP_075983212.1), o que faz
alinhamento global de sequencia inteira desalinhar a regiao catalitica.
Corrigido restringindo a MSA so' a regiao do dominio (+5aa de margem) -
pratica padrao para MSA entre proteinas com arquitetura de dominio
variavel, nao um ajuste ad-hoc.

Referencias (sequencias reais, buscadas nesta sessao, nao de memoria):
- 1TGN_A: tripsinogenio bovino, RCSB PDB (fasta real da entry 1TGN)
- XP_075977317.1: tripsina de A. gemmatalis ja confirmada em sessao
  anterior (diagnostico da origem do GORE3/LALAY), sequencia real via
  NCBI efetch
"""
import csv

# 1. coordenadas env_from/env_to do dominio PF00089, por protein_id, do
#    domtblout real da FASE 7 (nao reanotado aqui)
domain_coords = {}
with open("/home/eulalio/rnaseq-Anticarsia-GORE3/resultados_server/fase7_blocoB/pfam_domtblout.tsv") as f:
    for line in f:
        if line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 22:
            continue
        query_name = parts[3]   # protein_id
        if not parts[1].startswith("PF00089"):
            continue
        env_from, env_to = int(parts[19]), int(parts[20])
        score = float(parts[13])
        if query_name not in domain_coords or score > domain_coords[query_name][2]:
            domain_coords[query_name] = (env_from, env_to, score)

print(f"proteinas com coordenada de dominio PF00089 extraida: {len(domain_coords)}")

candidates = []
with open("/home/eulalio/rnaseq-Anticarsia-GORE3/resultados_server/fase9_blocoB_prosite_scan.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["both_patterns"] == "PASS":
            candidates.append((row["gene_id"], row["protein_id"]))
print(f"candidatos PASS (Bloco B): {len(candidates)}")

sequences = {}
current_id = None
current_seq = []
wanted_proteins = {p for _, p in candidates}
with open("/home/eulalio/rnaseq-Anticarsia-GORE3/genome_annotation/proteome/protein_representative.faa") as f:
    for line in f:
        line = line.rstrip("\n")
        if line.startswith(">"):
            if current_id is not None and current_id in wanted_proteins:
                sequences[current_id] = "".join(current_seq)
            current_id = line[1:].split()[0]
            current_seq = []
        else:
            current_seq.append(line)
    if current_id is not None and current_id in wanted_proteins:
        sequences[current_id] = "".join(current_seq)

REF_1TGN = "VDDDDKIVGGYTCGANTVPYQVSLNSGYHFCGGSLINSQWVVSAAHCYKSGIQVRLGEDNINVVEGNEQFISASKSIVHPSYNSNTLNNDIMLIKLKSAASLNSRVASISLPTSCASAGTQCLISGWGNTKSSGTSYPDVLKCLKAPILSDSSCKSAYPGQITSNMFCAGYLEGGKDSCQGDSGGPVVCSGKLQGIVSWGSGCAQKNKPGVYTKVCNYVSWIKQTIASN"
REF_XP075977317 = "MKSLLIVFALAALALAYEPIENNYHENVGIPEAARIMQAEQAMDFDGSRIVGGSAANAGAYPFLGGLVISLTSGHTSICGSSLLTNTRSVTAAHCWRSRDHQARQFVVVHGSNRLMSGGVRTTTTNVVMHGSYNINTLANDIAIINHNRVAYTNVIRNIGLASGSNQFAGSWANAAGFGATENGSSGNKRHVRLQVITNAVCRQTYGNTIIASTLCTSGAGRVGTCGGDSGGPLAIGNTLIGVTSFGYRPGCALGRPAGFARVTSFESWIRGRL"

PAD = 5
n_written = 0
n_no_coord = 0
out = "/home/eulalio/rnaseq-Anticarsia-GORE3/resultados_server/fase9_blocoC_domain_input.faa"
with open(out, "w") as f:
    f.write(">1TGN_A_bovine_trypsinogen_reference\n" + REF_1TGN + "\n")
    f.write(">XP_075977317.1_Agemmatalis_trypsin_reference\n" + REF_XP075977317 + "\n")
    for gene, protein in candidates:
        seq = sequences.get(protein, "")
        coord = domain_coords.get(protein)
        if not seq or not coord:
            n_no_coord += 1
            continue
        start, end = max(1, coord[0] - PAD), min(len(seq), coord[1] + PAD)
        domain_seq = seq[start - 1:end]
        f.write(f">{gene}\n{domain_seq}\n")
        n_written += 1

print(f"escritas {n_written} sequencias de dominio (+{PAD}aa de margem); {n_no_coord} sem coordenada PF00089")
print(f"salvo {out}")
