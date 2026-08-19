#!/bin/bash

# Alternativ, und angeblich besser,
# falls ein Linux-System die Bash an einem ganz ungewöhnlichen Ort versteckt hat, das ist am besten für portable Skripten
# Ermittelt dynamisch den Ordner dieses Skripts (perfekt für GitHub & Cron)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Remote-Backup-Konfiguration
# Hinweis für GitHub: Ersetze die IP-Adresse durch deine eigene lokale IP
ACER_HOST="${ACER_LOCAL_IP}"
ACER_BACKUP_DIR="~/backups/hp_wsl2/Python-Projects/research_digester"

echo "=== Starte automatische arXiv-KI-Pipeline ==="
date

# 1. In das Projektverzeichnis wechseln
cd "$PROJECT_DIR" || exit 1

# 2. Das Python-Skript direkt über die uv-Umgebung ausführen
# (uv run steuert automatisch die richtige .venv an!)
uv run fetcher.py

# 3. Git-Sicherungs-Layer
echo "Sichere Ergebnisse im lokalen Git-Repository..."

# Überprüfen, ob sich im research_log.md etwas geändert hat
GIT_CHANGED=false
if git status --porcelain | grep -q "research_log.md"; then
    git add research_log.md
    git commit -m "Auto-Update: Neues GDL-Forschungsprotokoll hinzugefügt am $(date +'%Y-%m-%d')"
    echo "[SUCCESS] Git-Commit erfolgreich durchgeführt."
    git push origin main
    echo "[SUCCESS] GitHub aktualisiert."
    git push acer main
    echo "[SUCCESS] Acer-Mirror aktualisiert."
    GIT_CHANGED=true

else
    echo "[INFO] Keine neuen Änderungen im Forschungsprotokoll gefunden."
fi

# 4. Remote-Backup-Layer (nur wenn neue Änderungen committet wurden)
if [ "$GIT_CHANGED" = true ]; then
    echo "Synchronisiere Änderungen mit dem Acer-Backup-Server..."
    if rsync -avz --exclude='.venv/' --exclude='__pycache__/' --exclude='*.pyc' "$PROJECT_DIR/" melanie@"$ACER_HOST":"$ACER_BACKUP_DIR"/; then
        echo "[SUCCESS] Remote-Backup erfolgreich abgeschlossen."
    else
        echo "[WARNING] Remote-Backup fehlgeschlagen. Lokales Git-Repository ist sicher."
    fi
else
    echo "[INFO] Kein Remote-Backup erforderlich. Keine neuen Änderungen."
fi

echo "=== Pipeline beendet ==="
