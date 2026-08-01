"""FASE 9, Bloco B - triagem primaria por padrao PROSITE (PS00134/PS00135)
nos 316 genes com dominio Pfam PF00089 (FASE 7), sobre as proteinas
representativas (1/gene, isoforma mais longa, ja calculadas na FASE 7).

Objetivo: os 316 hits de Pfam PF00089 cobrem o cla quimotripsina inteiro
(FASE 7), nao so tripsinas digestivas - este bloco eh o primeiro funil
real de curadoria, antes de qualquer filogenia ou cruzamento com
expressao/splicing fazer sentido biologicamente.

Padroes verificados via busca nesta sessao contra a entrada real do
InterPro/PROSITE (nao de memoria, PMID 41263099 - sigrist2026prosite):
- PS00134 (TRYPSIN_HIS, sitio ativo His): [LIVM]-[ST]-A-[STAG]-H-C
- PS00135 (TRYPSIN_SER, sitio ativo Ser): [DNSTAGC]-[GSTAPIMVQH]-x(2)-G-[DE]-S-G-[GS]-[SAPHV]-[LIVMFYWH]-[LIVMFYSTANQH]

Convertidos para regex Python (sintaxe PROSITE x(n) = qualquer aminoacido,
n vezes -> ".{n}" em regex).

Entrada: lista de 316 gene_id (extraida de
resultados/fase6_blocoE/pfam_hits_per_gene_ref_fase7.csv, filtro PF00089
- ja versionado no repo, artigo 1) + a proteina representativa de cada
gene (FASE 7, ja calculada, nao reanotada aqui).
"""
import re
import csv

PS00134 = re.compile(r"[LIVM][ST]A[STAG]HC")
PS00135 = re.compile(r"[DNSTAGC][GSTAPIMVQH].{2}G[DE]SG[GS][SAPHV][LIVMFYWH][LIVMFYSTANQH]")

with open("/home/eulalio/rnaseq-Anticarsia-GORE3/pf00089_genes.txt") as f:
    target_genes = set(line.strip() for line in f if line.strip())

gene_to_protein = {}
with open("/home/eulalio/rnaseq-Anticarsia-GORE3/resultados_server/fase7_blocoB/gene_to_representative_protein.tsv") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        if row["gene_id"] in target_genes:
            gene_to_protein[row["gene_id"]] = row["protein_id"]

protein_to_gene = {v: k for k, v in gene_to_protein.items()}

sequences = {}
current_id = None
current_seq = []
with open("/home/eulalio/rnaseq-Anticarsia-GORE3/genome_annotation/proteome/protein_representative.faa") as f:
    for line in f:
        line = line.rstrip("\n")
        if line.startswith(">"):
            if current_id is not None and current_id in protein_to_gene:
                sequences[protein_to_gene[current_id]] = "".join(current_seq)
            current_id = line[1:].split()[0]
            current_seq = []
        else:
            current_seq.append(line)
    if current_id is not None and current_id in protein_to_gene:
        sequences[protein_to_gene[current_id]] = "".join(current_seq)

print(f"genes alvo: {len(target_genes)}, proteinas mapeadas: {len(gene_to_protein)}, sequencias extraidas: {len(sequences)}")

rows = []
for gene in sorted(target_genes):
    seq = sequences.get(gene, "")
    his_match = PS00134.search(seq)
    ser_match = PS00135.search(seq)
    rows.append({
        "gene_id": gene,
        "protein_id": gene_to_protein.get(gene, ""),
        "protein_length": len(seq),
        "PS00134_TRYPSIN_HIS": "PASS" if his_match else "FAIL",
        "PS00134_match": his_match.group(0) if his_match else "",
        "PS00134_pos": his_match.start() + 1 if his_match else "",
        "PS00135_TRYPSIN_SER": "PASS" if ser_match else "FAIL",
        "PS00135_match": ser_match.group(0) if ser_match else "",
        "PS00135_pos": ser_match.start() + 1 if ser_match else "",
        "both_patterns": "PASS" if (his_match and ser_match) else "FAIL",
    })

out_path = "/home/eulalio/rnaseq-Anticarsia-GORE3/resultados_server/fase9_blocoB_prosite_scan.csv"
with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

n_both = sum(1 for r in rows if r["both_patterns"] == "PASS")
n_his = sum(1 for r in rows if r["PS00134_TRYPSIN_HIS"] == "PASS")
n_ser = sum(1 for r in rows if r["PS00135_TRYPSIN_SER"] == "PASS")
n_missing_seq = sum(1 for r in rows if r["protein_length"] == 0)
print(f"PS00134 (His) PASS: {n_his}/{len(rows)}")
print(f"PS00135 (Ser) PASS: {n_ser}/{len(rows)}")
print(f"AMBOS PASS: {n_both}/{len(rows)}")
print(f"sem sequencia mapeada: {n_missing_seq}")
print(f"salvo em {out_path}")
