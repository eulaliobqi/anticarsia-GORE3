#!/bin/bash
# FASE 6, Bloco F (continuacao) - sashimi plot do evento SE mais
# significativo (menor FDR, desempate por maior |IncLevelDifference|,
# mesmo limiar do Bloco D) em cada um dos 3 contrastes, via
# rmats2sashimiplot sobre os BAMs subjunc (mesmos do Bloco B/C).
#
# rmats2sashimiplot instalado via pip nesta sessao (nao existia antes) -
# atualizou numpy no env compartilhado rnaseq-tools (1.26.4 -> 2.4.6);
# confirmado que rmats.py continua funcionando normalmente depois disso
# (`rmats.py --version` ok), sem re-rodar nada do Bloco B.
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
conda activate rnaseq-tools
cd ~/rnaseq-Anticarsia-GORE3

OUTDIR=resultados_server/fase6_blocoF/sashimi
mkdir -p "$OUTDIR"

declare -A TREAT_BAMS=(
  [Benzamidine]="bam/subjunc/ID-5.bam,bam/subjunc/ID-7.bam,bam/subjunc/ID-8.bam"
  [SKTI]="bam/subjunc/ID-9.bam,bam/subjunc/ID-10.bam,bam/subjunc/ID-12.bam"
  [GORE3]="bam/subjunc/ID-14.bam,bam/subjunc/ID-15.bam,bam/subjunc/ID-16.bam"
)
CONTROL_BAMS="bam/subjunc/ID-1.bam,bam/subjunc/ID-2.bam,bam/subjunc/ID-3.bam"

for name in Benzamidine SKTI GORE3; do
  contrast="${name}_vs_Control"
  src="resultados_server/fase6_blocoB/${contrast}/SE.MATS.JC.txt"
  top1="$OUTDIR/${name}_top_SE_event.txt"

  # pega o cabecalho + a linha com o menor FDR entre as que passam no
  # limiar (FDR<0.05, |IncLevelDifference|>=0.1), desempatando por maior
  # |dPSI| - mesmo limiar ja usado no Bloco D, nao um novo criterio.
  python3 -c "
import csv
rows = []
with open('$src') as f:
    reader = csv.DictReader(f, delimiter='\t')
    header = reader.fieldnames
    for row in reader:
        try:
            fdr = float(row['FDR']); dpsi = abs(float(row['IncLevelDifference']))
        except (ValueError, KeyError):
            continue
        if fdr < 0.05 and dpsi >= 0.1:
            rows.append((fdr, -dpsi, row))
rows.sort(key=lambda x: (x[0], x[1]))
with open('$top1', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=header, delimiter='\t')
    w.writeheader()
    if rows:
        w.writerow(rows[0][2])
        print('top event geneSymbol=', rows[0][2].get('geneSymbol'), 'FDR=', rows[0][0], 'dPSI=', -rows[0][1])
"

  rmats2sashimiplot \
    --b1 "${TREAT_BAMS[$name]}" \
    --b2 "$CONTROL_BAMS" \
    -e "$top1" \
    --event-type SE \
    --l1 "$name" --l2 "Control" \
    --exon_s 1 --intron_s 5 \
    -o "$OUTDIR/${name}" \
    > "$OUTDIR/${name}_sashimi.log" 2>&1
  echo "sashimi $name exit=$?"
done

echo FASE6_BLOCOF_SASHIMI_DONE_MARKER
