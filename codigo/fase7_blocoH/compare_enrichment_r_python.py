#!/usr/bin/env python3
"""FASE 7, Bloco H - verificacao cruzada R (clusterProfiler) x Python
(gseapy) para o enriquecimento GO, mesmo espirito do Bloco E da FASE 5
(comparacao entre motores e' achado empirico do dataset, nao um
benchmark pronto da literatura - os dois pacotes usam implementacoes
distintas do teste hipergeometrico/ajuste de FDR, nao ha garantia
a priori de que os conjuntos de termos significativos batam)."""
import pandas as pd

G_DIR = "resultados_server/fase7_blocoG"
OUT_CSV = "resultados_server/fase7_blocoH/cross_engine_go_comparison.csv"

CONTRASTS = ["Benzamidine_vs_Control", "SKTI_vs_Control", "GORE3_vs_Control"]


def jaccard(a, b):
    u = a | b
    return len(a & b) / len(u) if u else float("nan")


def main():
    import os
    os.makedirs("resultados_server/fase7_blocoH", exist_ok=True)

    rows = []
    for rotulo in CONTRASTS:
        r_df = pd.read_csv(f"{G_DIR}/clusterprofiler_GO_{rotulo}.csv")
        py_df = pd.read_csv(f"{G_DIR}/gseapy_GO_{rotulo}.csv")

        r_terms = set(r_df["ID"]) if "ID" in r_df.columns and len(r_df) else set()
        py_terms = set(py_df["go_id"]) if "go_id" in py_df.columns and len(py_df) else set()

        inter = r_terms & py_terms
        jac = jaccard(r_terms, py_terms)

        print(f"\n=== {rotulo} ===")
        print(f"GO significativos: R(clusterProfiler)={len(r_terms)}, Python(gseapy)={len(py_terms)}")
        print(f"Intersecao: {len(inter)} | Jaccard: {jac:.4f}")

        rows.append({
            "contraste": rotulo,
            "n_sig_R_clusterProfiler": len(r_terms),
            "n_sig_Python_gseapy": len(py_terms),
            "n_intersecao": len(inter),
            "jaccard": round(jac, 4),
            "pct_R_confirmado_em_Python": round(100 * len(inter) / len(r_terms), 1) if r_terms else float("nan"),
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_CSV, index=False)
    print(f"\nEscrito: {OUT_CSV}")
    print("\nBloco H (verificacao cruzada R x Python, enriquecimento GO) concluido.")


if __name__ == "__main__":
    main()
