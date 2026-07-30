import json, os

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/ab_test")
SAMPLES = ["ID-1", "ID-8"]
SETS = ["setA", "setB"]

rows = []
for s in SAMPLES:
    for st in SETS:
        with open(os.path.join(QC_DIR, f"{s}_{st}.json")) as f:
            d = json.load(f)
        bf = d["summary"]["before_filtering"]
        af = d["summary"]["after_filtering"]
        fr = d["filtering_result"]
        total_before = bf["total_reads"]
        total_after = af["total_reads"]
        survival = 100 * total_after / total_before
        adapter = d.get("adapter_cutting", {})
        rows.append(dict(
            sample=s, param_set=st,
            reads_before=total_before, reads_after=total_after,
            pct_survival=round(survival, 2),
            q20_before=round(bf["q20_rate"]*100, 2), q20_after=round(af["q20_rate"]*100, 2),
            q30_before=round(bf["q30_rate"]*100, 2), q30_after=round(af["q30_rate"]*100, 2),
            mean_len_before=bf["read1_mean_length"], mean_len_after=af["read1_mean_length"],
            gc_before=round(bf["gc_content"]*100, 2), gc_after=round(af["gc_content"]*100, 2),
            low_quality=fr.get("low_quality_reads", 0),
            too_short=fr.get("too_short_reads", 0),
            too_many_N=fr.get("too_many_N_reads", 0),
            adapter_trimmed_reads=adapter.get("adapter_trimmed_reads", "N/A"),
            duplication_rate=round(d.get("duplication", {}).get("rate", 0)*100, 2),
        ))

hdr = ["sample","param_set","reads_before","reads_after","pct_survival",
       "q20_before","q20_after","q30_before","q30_after",
       "mean_len_before","mean_len_after","gc_before","gc_after",
       "low_quality","too_short","too_many_N","adapter_trimmed_reads","duplication_rate"]
print("\t".join(hdr))
for r in rows:
    print("\t".join(str(r[h]) for h in hdr))

# Save CSV too
import csv
csv_path = os.path.join(QC_DIR, "ab_test_comparison.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    w.writerows(rows)
print(f"\nCSV: {csv_path}")
