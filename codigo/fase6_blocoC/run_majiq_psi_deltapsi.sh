#!/bin/bash
# FASE 6, Bloco C (continuacao) - cobertura PSI combinada (12 experimentos,
# um arquivo so com todos os prefixos) + deltapsi para os 3 contrastes vs.
# Controle, selecionando os grupos dentro do mesmo arquivo de cobertura via
# --select-grp1-prefixes/--select-grp2-prefixes.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate majiq-env
cd ~/rnaseq-Anticarsia-GORE3

LICENSE=~/majiq_license_academic_official.lic
BUILD=resultados_server/fase6_blocoC/build
SG="$BUILD/splicegraph.zarr"
PSICOV=resultados_server/fase6_blocoC/psi_coverage.zarr

SAMPLES="ID-1 ID-2 ID-3 ID-5 ID-7 ID-8 ID-9 ID-10 ID-12 ID-14 ID-15 ID-16"
SJFILES=""
for s in $SAMPLES; do
  SJFILES="$SJFILES $BUILD/${s}.sj"
done

echo "=== majiq psi-coverage (combinando os 12 experimentos) - $(date) ==="
majiq psi-coverage \
  "$SG" \
  "$PSICOV" \
  $SJFILES \
  --prefixes $SAMPLES \
  --nthreads 16 \
  --license "$LICENSE" \
  --overwrite \
  > resultados_server/fase6_blocoC/majiq_psicoverage.log 2>&1
echo "psi-coverage exit=$?"

mkdir -p resultados/fase6_blocoC resultados_server/fase6_blocoC/deltapsi

run_deltapsi() {
  local name="$1"; shift
  local grp1="$1"; shift   # tratamento
  local grp2="$1"; shift   # Controle

  echo "=== majiq deltapsi - ${name}_vs_Control - $(date) ==="
  majiq deltapsi \
    -psi1 "$PSICOV" --select-grp1-prefixes $grp1 \
    -psi2 "$PSICOV" --select-grp2-prefixes $grp2 \
    -n "$name" Control \
    --splicegraph "$SG" \
    --nthreads 16 \
    --license "$LICENSE" \
    --overwrite \
    --output-tsv resultados_server/fase6_blocoC/deltapsi/${name}_vs_Control.deltapsi.tsv \
    --output-voila resultados_server/fase6_blocoC/deltapsi/${name}_vs_Control.voila.zarr \
    > resultados_server/fase6_blocoC/deltapsi/${name}_vs_Control.log 2>&1
  echo "deltapsi ${name} exit=$?"
}

run_deltapsi "Benzamidine" "ID-5 ID-7 ID-8"    "ID-1 ID-2 ID-3"
run_deltapsi "SKTI"        "ID-9 ID-10 ID-12"  "ID-1 ID-2 ID-3"
run_deltapsi "GORE3"       "ID-14 ID-15 ID-16" "ID-1 ID-2 ID-3"

echo FASE6_BLOCOC_MAJIQ_DELTAPSI_DONE_MARKER
