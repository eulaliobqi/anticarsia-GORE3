#!/bin/bash
# FASE 3, Bloco B - audita se as ferramentas necessarias para a quantificacao
# (gffread, featureCounts, salmon) ja estao instaladas no servidor, antes de
# assumir que sim (o modulo reaproveitavel RNA-Seq-not-model/modules/
# quantification.nf usa Salmon, mas isso nao garante que este servidor tenha
# Salmon instalado em nenhum dos envs ja usados no projeto).
#
# Se salmon nao existir em nenhum dos dois envs: instalar em "rnaseq-tools"
# (mesmo env que ja hospeda STAR/Subread-align - agrupamento por
# "ferramentas de alinhamento/mapeamento", nao por fase do projeto):
#   mamba install -n rnaseq-tools -c bioconda -c conda-forge "salmon>=1.10"
set -uo pipefail
source ~/miniforge3/etc/profile.d/conda.sh

echo "--- env ngs: gffread ---"
conda activate ngs
gffread --version 2>&1 || echo "gffread NAO encontrado em ngs"

echo "--- env ngs: featureCounts ---"
featureCounts -v 2>&1 || echo "featureCounts NAO encontrado em ngs"

echo "--- env ngs: salmon? ---"
salmon --version 2>&1 || echo "salmon NAO encontrado em ngs"

conda activate rnaseq-tools
echo "--- env rnaseq-tools: salmon? ---"
salmon --version 2>&1 || echo "salmon NAO encontrado em rnaseq-tools"

echo FASE3_BLOCOB_TOOLCHECK_DONE_MARKER
