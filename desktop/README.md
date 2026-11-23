# Настольная версия (macOS)

`desktop/main.py` — точка входа .app: поднимает локальный сервер на 127.0.0.1 и открывает
окно WKWebView через pywebview. Данные хранятся в `~/Library/Application Support/KadrFlow`.

Сборка:

```bash
./build_app.sh     # dist/KadrFlow.app
./build_dmg.sh     # dist/KadrFlow-<версия>-macOS-<arm64|x86_64>.dmg и ZIP
```

Запуск без окна (для проверки):

```bash
KADRFLOW_HEADLESS=1 KADRFLOW_DATA=/tmp/kadrflow dist/KadrFlow.app/Contents/MacOS/KadrFlow
```

Лог: `~/Library/Application Support/KadrFlow/app.log`.
