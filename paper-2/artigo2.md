---
Living document — paper 2 of the GORE3 post-doctoral project
(Eulálio, UFV/INCT-IPP). Scope: the mechanistic serine-protease-family
test (hypothesis H1) and, eventually, the head-to-head contrasts
(GORE3×Benzamidine, GORE3×SKTI) deferred from paper 1 (`artigo.md`).
Separated into its own directory (`paper-2/`) on 01/08/2026 per the
user's explicit decision — see project memory. Data from paper 1
(Phase 5 differential expression, Phase 6 splicing, Phase 7 functional
annotation) are reused by reading `resultados/` at the repo root, not
duplicated here.
Last updated: 01/08/2026 (Phase 9, Blocks A–E complete; Block F —
structural bridge — deferred, scope not yet decided).
---

# Paper 2 — Directed serine-protease-family analysis (Phase 9, hypothesis H1)

## Abstract

*[Not written — Phase 9 Block F (structural bridge) is still undecided
in scope, and Phase 9.5/10 head-to-head work has not started. Per this
project's own convention, no Abstract/Introduction is fabricated ahead
of the actual results.]*

## 1. Background and motivation

Paper 1 (`artigo.md`, Phases 1–7) characterized differential expression
and alternative splicing for GORE3, SKTI, and Benzamidine vs. Control,
each independently. It closed with a real, undesigned finding: the
single most significant splicing event in the GORE3 contrast (Phase 6,
§3.19, Fig. 19) falls in a gene carrying a Pfam PF00089 (trypsin/
chymotrypsin-clan) domain. This paper follows that thread to its
intended conclusion — the project's originally stated mechanistic
test (H1): does GORE3 induce a **switch in the dominant trypsin
isoform**, distinguishable from a simple change in overall expression
level, in genes that are *bona fide* digestive trypsins (not just any
gene carrying a chymotrypsin-clan domain)?

## 2. Methods

### 2.1 Primary curation: from Pfam domain to digestive trypsin (Block B)

Pfam PF00089 (Phase 7 annotation, Mistry et al. 2021) covers the entire
chymotrypsin clan — 316 genes genome-wide — not specifically digestive
trypsins; CLIP-domain proteases, prophenoloxidase activators, and other
non-digestive family members carry the same domain. A first curation
layer was applied: the representative protein of each of the 316 genes
was scanned for the two PROSITE sequence signatures that jointly
distinguish trypsin-family serine proteases (Sigrist et al. 2026,
PMID 41263099) — **PS00134** (histidine active site,
`[LIVM]-[ST]-A-[STAG]-H-C`) and **PS00135** (serine active site,
`[DNSTAGC]-[GSTAPIMVQH]-x(2)-G-[DE]-S-G-[GS]-[SAPHV]-[LIVMFYWH]-
[LIVMFYSTANQH]`), both verified against the current PROSITE/InterPro
entry, not recalled from memory. **168/316 genes carry both patterns.**
Code: `codigo/fase9_blocoB/prosite_scan.py`.

### 2.2 Structural confirmation of the catalytic triad by MSA (Block C)

**A real methodological correction, made before accepting any result.**
A first attempt aligned full-length representative proteins of the 168
candidates plus two reference sequences (bovine trypsinogen, PDB 1TGN
chain A, fetched from RCSB; and `XP_075977317.1`, the *A. gemmatalis*
trypsin already confirmed in this project's earlier LALAY-origin
diagnostic) with MAFFT (`--auto`). **Zero of the 168 candidates**
retained the catalytic His/Ser at the alignment column matching either
reference — full-length global alignment is inappropriate here because
PF00089-carrying proteins vary substantially in domain architecture
(e.g. an N-terminal CLIP domain precedes the trypsin domain in several
candidates, confirmed directly in the Phase 7 `hmmscan` domain table).
**Corrected:** alignment was restricted to the Pfam PF00089 domain
envelope (± 5 aa margin) per sequence, extracted from the Phase 7
`hmmscan` domtblout coordinates — standard practice for MSA across
proteins with variable domain architecture, not an ad-hoc fix. Code:
`codigo/fase9_blocoC/build_domain_input.py`,
`codigo/fase9_blocoC/run_mafft.sh`.

The corrected alignment (MAFFT `--auto`, domain-restricted) was used to
locate, in each of the two references, the exact alignment column of
the catalytic His (PS00134 match) and Ser (PS00135 match); both
references agreed on the same two columns, confirming the cross-check's
validity. Each of the 168 candidates was then checked for His/Ser at
those same reference-equivalent columns (not merely "the motif
somewhere in the sequence," which Block B already established).
**166/168 candidates pass.** A second, unrelated bug (an indexing error
in this session's own verification script, not a biological signal) was
found and corrected before this number was accepted — see code comments
in `codigo/fase9_blocoC/verify_triad_columns.py` for the full account.

**A limitation declared, not hidden:** the third catalytic-triad member
(Asp102) has no equally specific single PROSITE sequence signature; its
rigorous confirmation requires 3D geometric validation (Ser-Oγ⋯His-Nε2
and His-Nδ1⋯Asp-Oδ1 distances, Ser-His-Asp angle) on a predicted or
experimental structure — deferred to Block F (structural bridge), not
performed here.

### 2.3 Phylogeny of the curated family (Block D)

The 166 curated genes (+ the two references) were re-aligned at the
domain level, trimmed with **trimAl** (`-automated1`), and a maximum-
likelihood tree was built with **IQ-TREE 3** (Wong et al. 2026,
PMID 42085559 — confirmed via this session's own literature search to
be the current major release, not the older v2 inherited from earlier
project scripts) using **ModelFinder** for automatic model selection,
1000 ultrafast bootstrap replicates, and 1000 SH-aLRT replicates.
Rooted on the bovine trypsinogen reference (1TGN_A) as outgroup — a
single, distantly related (mammalian vs. insect) sequence, declared
explicitly as a simple rooting choice, not a rigorous outgroup sampling.
Code: `codigo/fase9_blocoD/` (trimAl + IQ-TREE3 commands, server-run,
see Reproducibility table).

### 2.4 Cross-reference with expression and splicing (Block E) — the H1 test

For the 166 curated genes, membership in the Phase 5 (DESeq2/R)
differentially-expressed gene sets and the Phase 6 (rMATS-turbo ∪ MAJIQ)
significantly-spliced gene sets was checked per contrast
(Benzamidine/SKTI/GORE3 vs. Control), directly reusing the already-
computed, already-versioned result tables from paper 1
(`resultados/fase5_blocoD/`, `resultados/fase6_blocoD/`) — no
re-analysis of expression or splicing data was performed. Each curated
gene was classified per contrast as: **level+identity** (both DE and
significantly spliced — the strongest H1 signal), **level only** (DE,
not spliced), **identity only** (spliced, not DE), or **no significant
change**. Code: `codigo/fase9_blocoE/cross_reference_h1.py`.

## 3. Results

### 3.1 Curation funnel

| Step | Genes remaining | Method |
|---|---:|---|
| Pfam PF00089 hits (Phase 7, whole chymotrypsin clan) | 316 | `hmmscan` |
| + PROSITE PS00134 & PS00135 (Block B) | 168 | sequence motif |
| + His/Ser at reference-equivalent MSA column (Block C) | **166** | domain-restricted MSA |

### 3.2 Phylogeny

168 taxa (166 curated genes + 2 references), best-fit model by BIC:
**Q.PFAM+R7** (a Pfam-alignment-trained empirical matrix with a 7-category
FreeRate model — selected by ModelFinder, not assumed), total tree
length 52.633, log-likelihood −24396.35. Tree files:
`resultados/fase9_blocoD/tree/curated_family.{treefile,contree}`.
Topology has not yet been manually inspected for paralog-vs.-annotation-
error resolution (docs/07 §10, item 3) — pending.

### 3.3 The H1 cross-reference

**Table 1 | Curated trypsin genes (n=166) by DE/splicing status, per contrast vs. Control.**

| Contrast | Level + identity (DE ∩ splicing) | Level only (DE) | Identity only (splicing) | No significant change | Any change |
|---|---:|---:|---:|---:|---:|
| Benzamidine | 0 | 5 | 3 | 158 | 8/166 |
| SKTI | 1 | 37 | 1 | 127 | 39/166 |
| GORE3 | 1 | 41 | 3 | 121 | 45/166 |

**The strongest candidate for H1 found this session: `gene-LOC142975421`
is the only curated trypsin gene, in any contrast, showing both a
significant expression-level change AND a significant splicing change —
specifically in the GORE3 contrast.** `gene-LOC142980480` (already
highlighted in paper 1, Fig. 19 — the sashimi-plotted event) confirms an
**identity-only** pattern in GORE3: a clear isoform-level shift not
accompanied by a gene-level DE call, illustrating exactly the
"level vs. identity" distinction that motivated Phase 6/9. Two genes
recur as splicing-flagged across both SKTI and GORE3
(`gene-LOC142977339`, `gene-LOC142983873`), extending the SKTI≈GORE3
functional convergence already reported in paper 1 (§3.18) down to
specific curated trypsin genes. Benzamidine's footprint remains the
smallest and least specific of the three treatments, consistent with
every prior analysis in this project.

**Interpretation, bounded by what is shown here:** this is gene-level
and splicing-event-level evidence consistent with H1 for a small,
specific set of curated trypsin genes in GORE3 — it is not yet
structural or functional proof of an isoform switch with altered GORE3
binding. That confirmation is the explicit purpose of the deferred
Block F (structural bridge).

## 4. Limitations (declared explicitly)

1. **Asp102 (third catalytic-triad residue) was not verified in this
   round** — no reliable single PROSITE pattern exists for it; proper
   verification requires 3D geometric validation on a predicted/
   experimental structure, deferred to the (undecided-scope) structural
   block.
2. **The phylogenetic outgroup is a single mammalian sequence** (bovine
   trypsinogen), not a curated outgroup panel — adequate for a first
   rooting, not for rigorous divergence-time or duplication-event
   inference.
3. **Tree topology has not been manually reviewed** to separate true
   paralogs from possible gene-annotation fragmentation (adjacent `LOC`
   IDs that might represent one mis-split gene) — the phylogeny exists;
   its interpretation for that specific purpose does not yet.
4. **The four "ready" structures previously assumed reusable
   (`analise-alosterica/data/protonated/`) were checked this session and
   found NOT to be confirmed *A. gemmatalis* sequences** — they originate
   from an earlier, unrelated screening project (species unconfirmed).
   Any future structural work must verify identity/accession before
   reuse, not assume it.
5. **Block F (AlphaFold3/Boltz-2 structure prediction + docking) has not
   been run** — computationally heavy (GPU, hours per isoform) and its
   scope (how many of the H1-flagged genes to model) was intentionally
   left for a decision after seeing the Block E results, per the
   approved plan. Not started this session at the user's request
   (pausing for manual verification).
6. **PROSITE/MSA-based curation (Blocks B–C) is a sequence-level
   filter, not a functional assay** — the 166 curated genes are strong
   candidates for digestive trypsin activity based on catalytic-motif
   conservation, not experimentally confirmed as catalytically active.

## References

Sigrist, C. J. A., Cuche, B. A., de Castro, E., Coudert, E., Redaschi,
N. & Bridge, A. The PROSITE database for protein families, domains, and
sites. *Nucleic Acids Res.* **54**, D451–D458 (2026). PMID 41263099.

Wong, T. K. F. et al. IQ-TREE 3: phylogenomic inference software using
complex evolutionary models. *Mol. Biol. Evol.* (2026). PMID 42085559.

Mistry, J. et al. Pfam: The protein families database in 2021. *Nucleic
Acids Res.* **49**, D412–D419 (2021). PMID 33125078. *(reused from
paper 1, Phase 7 — Pfam PF00089 domain calls are the starting point of
Block B here.)*

---

## Reproducibility — code and data locations

| Item | Path |
|---|---|
| Bibliography (bib + notes) | `paper-2/docs/referencias.bib`, `paper-2/docs/literatura.md` |
| PROSITE motif scan (Block B) | `paper-2/codigo/fase9_blocoB/prosite_scan.py` → `paper-2/resultados/fase9_blocoB/prosite_scan.csv` |
| Domain-restricted MSA input + run (Block C) | `paper-2/codigo/fase9_blocoC/build_domain_input.py`, `run_mafft.sh` (server: `resultados_server/fase9_blocoC_domain_input.faa`, `_domain_aligned.fasta`) |
| Catalytic-triad column verification (Block C) | `paper-2/codigo/fase9_blocoC/verify_triad_columns.py` → `paper-2/resultados/fase9_blocoC/triad_curated.csv` |
| trimAl + IQ-TREE3 (Block D, server-run, screen `fase9_iqtree`) | `trimal -in resultados_server/fase9_blocoD_curated_aligned.fasta -out resultados_server/fase9_blocoD_curated_trimmed.fasta -automated1` then `iqtree3 -s ... -m MFP -bb 1000 -alrt 1000 -o 1TGN_A_bovine_trypsinogen_reference` → `paper-2/resultados/fase9_blocoD/tree/curated_family.{treefile,contree,iqtree}` |
| H1 cross-reference (Block E) | `paper-2/codigo/fase9_blocoE/cross_reference_h1.py` → `paper-2/resultados/fase9_blocoE/{h1_gene_level_detail.csv,h1_summary.csv}` |

**Dados grandes não versionados (só servidor):** `resultados_server/fase9_blocoC_domain_input.faa`/`_domain_aligned.fasta` (alinhamento completo dos 168+2), `resultados_server/fase9_blocoD_curated_trimmed.fasta` (alinhamento trimado), arquivos intermediários do IQ-TREE (`.ckp.gz`, `.model.gz`, `.mldist`, `.bionj`, `.splits.nex`, `.log`) — só `.treefile`/`.contree`/`.iqtree` (relatório) foram copiados para o repo, pequenos e suficientes para reproduzir a interpretação.
