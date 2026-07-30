#!/bin/bash
set -uo pipefail

DEST="$HOME/rnaseq-Anticarsia-GORE3/raw_fastq"
mkdir -p "$DEST"
cd "$DEST" || exit 1

LOG="$DEST/download.log"
echo "=== Início: $(date) ===" | tee -a "$LOG"

while IFS=$'\t' read -r fname url; do
    [ -z "$fname" ] && continue
    echo "--- Baixando $fname: $(date) ---" | tee -a "$LOG"
    for attempt in 1 2 3 4 5; do
        wget -c --tries=3 --timeout=120 -O "$fname" "$url" 2>>"$LOG" && break
        echo "   tentativa $attempt falhou para $fname, retry..." | tee -a "$LOG"
        sleep 10
    done
done < "$DEST/download_urls.txt"

echo "=== Downloads concluídos: $(date) ===" | tee -a "$LOG"
echo "=== Verificando md5sum ===" | tee -a "$LOG"
md5sum -c "$DEST/md5sum.txt" 2>&1 | tee "$DEST/md5sum_check.log"

if grep -q "FAILED" "$DEST/md5sum_check.log"; then
    echo "=== ATENÇÃO: pelo menos um arquivo falhou no md5sum ===" | tee -a "$LOG"
else
    echo "=== Todos os 26 arquivos OK no md5sum: $(date) ===" | tee -a "$LOG"
fi
echo "DONE_MARKER" | tee -a "$LOG"
