#!/usr/bin/env bash
# Сборка дистрибутива для архитектуры текущего Mac: DMG и ZIP.
set -euo pipefail
cd "$(dirname "$0")"

VERSION="$(python3 tools/version.py)"
ARCH="$(uname -m)"
case "$ARCH" in arm64|x86_64) ;; *) echo "Неподдерживаемая архитектура: $ARCH" >&2; exit 1;; esac
NAME="KadrFlow-${VERSION}-macOS-${ARCH}"

APP="dist/KadrFlow.app"
[ -d "$APP" ] || { echo "Сначала соберите приложение: ./build_app.sh"; exit 1; }

# ZIP — универсальный вариант, сохраняет подпись и права
ditto -c -k --sequesterRsrc --keepParent "$APP" "dist/${NAME}.zip"
du -sh "dist/${NAME}.zip"

# DMG для установки через Finder.
STAGE="build/dmg"
rm -rf "$STAGE"
mkdir -p "$STAGE"
ditto "$APP" "$STAGE/KadrFlow.app"
# Инструкция для тестера: Gatekeeper, что проверить, куда смотреть в логе
cp docs/MACOS-TEST.md "$STAGE/ЧИТАЙ-МЕНЯ.txt"
ln -s /Applications "$STAGE/Applications"

hdiutil create -volname "KadrFlow" -srcfolder "$STAGE" -ov -format UDZO \
    "dist/${NAME}.dmg" >/dev/null
echo "DMG: dist/${NAME}.dmg"
rm -rf "$STAGE"
