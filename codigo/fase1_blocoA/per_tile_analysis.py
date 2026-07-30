"""
Bloco A.1 - fechamento da lacuna do per-tile (posicao-resolvido).
Testa se o defeito de qualidade em cycles 44-90 (R1) de Benzamidine_R2,
Benzamidine_R3 e SKTI_R2 e' fisicamente localizado num subconjunto de
tiles (assinatura tecnica: alta variancia entre tiles DENTRO da janela,
poucos tiles muito piores que os outros) ou se afeta todos os tiles de
forma aproximadamente uniforme (assinatura NAO-tecnica: provavel efeito
de composicao/quimica da biblioteca especifica naquele trecho do read,
nao um defeito fisico do flowcell).

Gera:
  - blocoA1_pertile_results.csv (estatisticas por amostra)
  - Figure2_blocoA1_pertile_heatmap.png (heatmap tile x posicao, 2 amostras representativas)
"""
import zipfile, re, os, csv, statistics

QC_DIR = os.path.expanduser("~/rnaseq-Anticarsia-GORE3/qc/pre_trim")
SAMPLES = ["ID-1","ID-2","ID-3","ID-5","ID-7","ID-8","ID-9","ID-10","ID-12","ID-14","ID-15","ID-16","ID-18"]
LABELS = {
    "ID-1":"Control_R1","ID-2":"Control_R2","ID-3":"Control_R3",
    "ID-5":"Benzamidine_R1","ID-7":"Benzamidine_R2","ID-8":"Benzamidine_R3",
    "ID-9":"SKTI_R1","ID-10":"SKTI_R2","ID-12":"SKTI_R3",
    "ID-14":"GORE3_R1","ID-15":"GORE3_R2","ID-16":"GORE3_R3",
    "ID-18":"FatBody",
}
WINDOW = (44, 90)

def read_fastqc_data(sample, read=1):
    zpath = os.path.join(QC_DIR, f"{sample}_{read}_fastqc.zip")
    with zipfile.ZipFile(zpath) as z:
        inner = f"{sample}_{read}_fastqc/fastqc_data.txt"
        return z.read(inner).decode("utf-8", errors="replace")

def parse_per_tile(text):
    i = text.find(">>Per tile sequence quality")
    j = text.find(">>END_MODULE", i)
    block = text[i:j]
    tiles = {}  # tile -> list of (lo, hi, dev)
    for line in block.splitlines():
        if line.startswith(">>") or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        tile, base, dev = parts[0], parts[1], float(parts[2])
        if "-" in base:
            lo, hi = map(int, base.split("-"))
        else:
            lo = hi = int(base)
        tiles.setdefault(tile, []).append((lo, hi, dev))
    return tiles

def windowed_mean(rows, lo_bound, hi_bound):
    tw, twq = 0.0, 0.0
    for lo, hi, dev in rows:
        ov_lo, ov_hi = max(lo, lo_bound), min(hi, hi_bound)
        if ov_lo > ov_hi:
            continue
        w = ov_hi - ov_lo + 1
        tw += w
        twq += w * dev
    return (twq / tw) if tw else None

results = []
heatmap_data = {}  # sample -> {tile: {pos_label: dev}}  (kept for the 2 representative samples)

for s in SAMPLES:
    text = read_fastqc_data(s, 1)
    tiles = parse_per_tile(text)
    max_pos = max(hi for rows in tiles.values() for _, hi, _ in rows)

    per_tile_window = []
    per_tile_flank = []
    for tile, rows in tiles.items():
        w = windowed_mean(rows, WINDOW[0], WINDOW[1])
        f_lo = windowed_mean(rows, 1, WINDOW[0] - 1)
        f_hi = windowed_mean(rows, WINDOW[1] + 1, max_pos)
        wl, wh = WINDOW[0] - 1, max_pos - WINDOW[1]
        f = (f_lo * wl + f_hi * wh) / (wl + wh) if (f_lo is not None and f_hi is not None) else None
        if w is not None:
            per_tile_window.append(w)
        if f is not None:
            per_tile_flank.append(f)

    mean_w, std_w = statistics.mean(per_tile_window), statistics.pstdev(per_tile_window)
    mean_f, std_f = statistics.mean(per_tile_flank), statistics.pstdev(per_tile_flank)
    ratio = (std_w / std_f) if std_f > 0 else None
    n_tiles = len(per_tile_window)

    results.append(dict(
        id=s, label=LABELS[s], n_tiles=n_tiles,
        mean_dev_window=round(mean_w, 3), std_dev_window=round(std_w, 3),
        mean_dev_flank=round(mean_f, 3), std_dev_flank=round(std_f, 3),
        std_ratio_window_over_flank=round(ratio, 3) if ratio else None,
    ))

    if s in ("ID-1", "ID-8"):
        # keep full tile x position grid for heatmap (representative clean vs worst)
        grid = {}
        for tile, rows in tiles.items():
            grid[tile] = {}
            for lo, hi, dev in rows:
                grid[tile][(lo, hi)] = dev
        heatmap_data[s] = grid

csv_path = os.path.join(QC_DIR, "blocoA1_pertile_results.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader()
    w.writerows(results)
print(f"CSV: {csv_path}")
for r in results:
    print(r)

# ---- Figure 2: heatmap tile x position, ID-1 (clean) vs ID-8 (worst) ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300, sharey=False)

for ax, sample in zip(axes, ["ID-1", "ID-8"]):
    grid = heatmap_data[sample]
    tiles_sorted = sorted(grid.keys())
    positions_sorted = sorted(set(pos for t in grid.values() for pos in t.keys()))
    mat = np.full((len(tiles_sorted), len(positions_sorted)), np.nan)
    for ti, tile in enumerate(tiles_sorted):
        for pi, pos in enumerate(positions_sorted):
            mat[ti, pi] = grid[tile].get(pos, np.nan)

    im = ax.imshow(mat, aspect="auto", cmap="RdBu", vmin=-3, vmax=3,
                    extent=[0, len(positions_sorted), 0, len(tiles_sorted)])
    # mark the 44-90 window
    win_lo_idx = next(i for i, (lo, hi) in enumerate(positions_sorted) if hi >= WINDOW[0])
    win_hi_idx = next((i for i, (lo, hi) in enumerate(positions_sorted) if lo > WINDOW[1]), len(positions_sorted))
    ax.axvspan(win_lo_idx, win_hi_idx, color="black", alpha=0.0, linewidth=1.5,
               edgecolor="black", linestyle="--")
    ax.axvline(win_lo_idx, color="black", linestyle="--", linewidth=1)
    ax.axvline(win_hi_idx, color="black", linestyle="--", linewidth=1)
    ax.set_title(f"{LABELS[sample]} ({sample})", fontsize=10)
    ax.set_xlabel("Read-1 cycle (binned)")
    ax.set_yticks([])

axes[0].set_ylabel("Tile (flow-cell physical position)")
cbar = fig.colorbar(im, ax=axes, shrink=0.8, label="Per-tile quality deviation (Phred)")
fig.suptitle("Per-tile quality deviation across read-1 cycles: clean vs. worst-affected library",
             fontsize=11, y=1.02)
fig_path = os.path.join(QC_DIR, "Figure2_blocoA1_pertile_heatmap.png")
plt.savefig(fig_path, bbox_inches="tight")
print(f"Figura: {fig_path}")
