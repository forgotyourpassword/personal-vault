#!/usr/bin/env bash
# Watches the Obsidian daily journal folder and fires the KPI dashboard
# whenever a journal file (YYYY-MM-DD.md) is closed after writing.
#
# Debounce: waits 30 s of quiet after the last write before firing,
# so rapid saves during writing don't spam Telegram.

JOURNAL_DIR="${OBSIDIAN_VAULT_PATH:-/home/mike/vault}/Journal/Daily"
SCRIPT="/home/mike/.hermes/scripts/journal_kpi.py"
PYTHON="/home/mike/.hermes/venv/bin/python"
ENV_FILE="/home/mike/.hermes/.env"
LOG="/home/mike/.hermes/logs/journal_watcher.log"
DEBOUNCE=30   # seconds to wait after last save before firing

mkdir -p "$(dirname "$LOG")"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

log "Journal watcher started. Watching: $JOURNAL_DIR"

# Load env vars (Telegram credentials)
# shellcheck disable=SC1090
set -a; source "$ENV_FILE"; set +a

TIMER_PID=""

fire_dashboard() {
    log "Journal save detected — running KPI dashboard..."
    OBSIDIAN_VAULT_PATH="${OBSIDIAN_VAULT_PATH:-/home/mike/vault}" \
        "$PYTHON" "$SCRIPT" >> "$LOG" 2>&1 \
        && log "KPI dashboard sent OK." \
        || log "KPI dashboard FAILED. Check log above."
}

# inotifywait loop — watch for CLOSE_WRITE on date-named files only
inotifywait -m -e close_write --format "%f" "$JOURNAL_DIR" 2>>"$LOG" | \
while read -r filename; do
    # Only react to files matching YYYY-MM-DD.md
    if [[ "$filename" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$ ]]; then
        log "Write detected: $filename — debouncing ${DEBOUNCE}s..."

        # Cancel any pending timer
        if [[ -n "$TIMER_PID" ]]; then
            kill "$TIMER_PID" 2>/dev/null
        fi

        # Start a new debounce timer in background
        (sleep "$DEBOUNCE"; fire_dashboard) &
        TIMER_PID=$!
    fi
done
