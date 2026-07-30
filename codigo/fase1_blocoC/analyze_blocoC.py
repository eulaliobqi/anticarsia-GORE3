import json, os, csv, re

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/blocoC_test")
SAMPLES = ["ID-1", "ID-7", "ID-8", "ID-9", "ID-10"]
SETS = ["setB", "setC1", "setC2", "setC3"]
LABELS = {
    "ID-1": "Control_R1 (limpa)", "ID-7": "Benzamidine_R2",
    "ID-8": "Benzamidine_R3", "ID-9": "SKTI_R1", "ID-10": "SKTI_R2",
}
SET_DESC = {
    "setB": "baseline producao (qq20, overlap default)",
    "setC1": "qq15 (afrouxar qualidade)",
    "setC2": "qq20, overlap permissivo (20/8/30)",
    "setC3": "qq20, overlap restritivo (40/3/10) - contraprova",
}


def parse_hisat2_rate(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        text = f.read()
    m = re.search(r"([\d.]+)%\s*overall alignment rate", text)
    return float(m.group(1)) if m else None


rows = []
for s in SAMPLES:
    for set_ in SETS:
        json_path = os.path.join(QC_DIR, f"{s}_{set_}.json")
        with open(json_path) as f:
            d = json.load(f)
        bf, af = d["summary"]["before_filtering"], d["summary"]["after_filtering"]
        fr = d["filtering_result"]
        total_before = bf["total_reads"]
        total_after = af["total_reads"]
        dimer = fr.get("adapter_dimer_reads", 0)
        rows.append(dict(
            id=s, label=LABELS[s], set=set_, set_desc=SET_DESC[set_],
            reads_before=total_before, reads_after=total_after,
            pct_survival=round(100 * total_after / total_before, 2),
            pct_adapter_dimer=round(100 * dimer / total_before, 2),
            pct_low_quality=round(100 * fr.get("low_quality_reads", 0) / total_before, 2),
            pct_too_short=round(100 * fr.get("too_short_reads", 0) / total_before, 2),
            q30_before=round(bf["q30_rate"] * 100, 2),
            q30_after=round(af["q30_rate"] * 100, 2),
            mean_len_after=af["read1_mean_length"],
            hisat2_overall_alignment_pct=parse_hisat2_rate(
                os.path.join(QC_DIR, f"{s}_{set_}.hisat2_summary.txt")),
        ))

csv_path = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/resultados/blocoC_param_sweep.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

hdr = list(rows[0].keys())
print("\t".join(hdr))
for r in rows:
    print("\t".join(str(r[h]) for h in hdr))
print(f"\nCSV: {csv_path}")

# ---- Criterio de decisao (docs/07_analise_rnaseq.md / plano aprovado) ----
# Um Set C substitui o Set B na producao apenas se, nas 4 amostras
# problematicas (ID-7/8/9/10), simultaneamente:
#  1) pct_survival sobe >= 5 pp vs. Set B
#  2) q30_after nao cai abaixo de ~95%
#  3) hisat2_overall_alignment_pct nao cai vs. Set B
#  4) em ID-1 (controle limpo) o set nao piora nada
print("\n=== Avaliacao do criterio de decisao ===")
by_key = {(r["id"], r["set"]): r for r in rows}
problem_samples = ["ID-7", "ID-8", "ID-9", "ID-10"]

for set_ in ["setC1", "setC2", "setC3"]:
    print(f"\n--- {set_} ({SET_DESC[set_]}) vs. setB ---")
    passes = True
    for s in problem_samples:
        b = by_key[(s, "setB")]
        c = by_key[(s, set_)]
        d_surv = c["pct_survival"] - b["pct_survival"]
        q30_ok = c["q30_after"] >= 95.0
        map_b = b["hisat2_overall_alignment_pct"]
        map_c = c["hisat2_overall_alignment_pct"]
        map_ok = (map_b is None or map_c is None) or (map_c >= map_b)
        gain_ok = d_surv >= 5.0
        print(f"  {s}: d_survival={d_surv:+.2f}pp (>=5? {gain_ok}), "
              f"q30_after={c['q30_after']} (>=95? {q30_ok}), "
              f"mapping setB={map_b} setC={map_c} (nao piora? {map_ok})")
        passes = passes and gain_ok and q30_ok and map_ok
    ctrl_b = by_key[("ID-1", "setB")]
    ctrl_c = by_key[("ID-1", set_)]
    ctrl_ok = (ctrl_c["q30_after"] >= ctrl_b["q30_after"] - 0.3) and \
              ((ctrl_c["hisat2_overall_alignment_pct"] is None) or
               (ctrl_b["hisat2_overall_alignment_pct"] is None) or
               (ctrl_c["hisat2_overall_alignment_pct"] >= ctrl_b["hisat2_overall_alignment_pct"] - 0.5))
    print(f"  ID-1 controle nao piora? {ctrl_ok}")
    passes = passes and ctrl_ok
    print(f"  => {set_} {'VENCE Set B' if passes else 'nao atende ao criterio, Set B permanece'}")
