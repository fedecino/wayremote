#!/usr/bin/env bash
# ==============================================================================
# Build script per WayRemote-x86_64.AppImage
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPDIR="$SCRIPT_DIR/WayRemote.AppDir"
OUTPUT_APPIMAGE="$SCRIPT_DIR/WayRemote-x86_64.AppImage"
LOCAL_APPIMAGETOOL="$SCRIPT_DIR/appimagetool-x86_64.AppImage"

echo "==> [WayRemote] Avvio compilazione AppImage..."

# 1. Verifica consistenza directory AppDir
if [ ! -d "$APPDIR" ]; then
    echo "ERRORE: Directory $APPDIR non trovata!" >&2
    exit 1
fi

# 2. Pulizia e Permessi corretti
echo "==> [WayRemote] Impostazione permessi eseguibili su AppRun..."
rm -rf "$APPDIR"/__pycache__ "$APPDIR"/*.pyc
chmod +x "$APPDIR/AppRun"
chmod +x "$APPDIR/connections.py"
chmod 644 "$APPDIR/wayremote.desktop"
if [ -f "$APPDIR/wayremote.png" ]; then
    chmod 644 "$APPDIR/wayremote.png"
fi

# 3. Verifica / Download di appimagetool
APPIMAGETOOL_CMD=""
if command -v appimagetool &>/dev/null; then
    APPIMAGETOOL_CMD="appimagetool"
    echo "==> [WayRemote] Trovato appimagetool di sistema: $(which appimagetool)"
elif [ -f "$LOCAL_APPIMAGETOOL" ] && [ -x "$LOCAL_APPIMAGETOOL" ]; then
    APPIMAGETOOL_CMD="$LOCAL_APPIMAGETOOL"
    echo "==> [WayRemote] Uso appimagetool locale: $LOCAL_APPIMAGETOOL"
else
    echo "==> [WayRemote] appimagetool non trovato. Download da GitHub releases..."
    DOWNLOAD_URL="https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    
    if command -v curl &>/dev/null; then
        curl -L -o "$LOCAL_APPIMAGETOOL" "$DOWNLOAD_URL"
    elif command -v wget &>/dev/null; then
        wget -O "$LOCAL_APPIMAGETOOL" "$DOWNLOAD_URL"
    else
        echo "ERRORE: curl o wget necessari per scaricare appimagetool." >&2
        exit 1
    fi
    chmod +x "$LOCAL_APPIMAGETOOL"
    APPIMAGETOOL_CMD="$LOCAL_APPIMAGETOOL"
fi

# 4. Generazione dell'AppImage
echo "==> [WayRemote] Generazione dell'archivio AppImage in corso..."
export ARCH=x86_64
export APPIMAGE_EXTRACT_AND_RUN=1

rm -f "$OUTPUT_APPIMAGE"

# Se l'appimagetool locale non può usare FUSE, usiamo l'opzione --appimage-extract-and-run
if [ "$APPIMAGETOOL_CMD" = "$LOCAL_APPIMAGETOOL" ]; then
    "$APPIMAGETOOL_CMD" --appimage-extract-and-run --no-appstream "$APPDIR" "$OUTPUT_APPIMAGE"
else
    "$APPIMAGETOOL_CMD" --no-appstream "$APPDIR" "$OUTPUT_APPIMAGE"
fi

chmod +x "$OUTPUT_APPIMAGE"

echo "================================================================="
echo " SUCCESSO: AppImage creata con successo!"
echo " Percorso: $OUTPUT_APPIMAGE"
echo " Dimensioni: $(du -h "$OUTPUT_APPIMAGE" | cut -f1)"
echo "================================================================="
