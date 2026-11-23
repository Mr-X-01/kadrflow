# Релизы KadrFlow

Версия берётся из `kadrflow/_version.py`. Перед тегом обновите номер версии,
`README.md` и `release/v<версия>/RELEASE_NOTES.md`.

Проверьте исходники:

```bash
python -m unittest discover -s tests -p 'test_*.py'
node --check web/app.js
```

Пуш тега `v<версия>` запускает в GitHub Actions сборки Windows x64 и macOS
Apple Silicon/Intel. После проверок workflow прикрепляет к GitHub Release
установщик Windows EXE, переносимый ZIP, macOS DMG и ZIP для обеих архитектур,
а также контрольные суммы SHA256. Установщик Windows создаёт ярлыки в меню
«Пуск» и на рабочем столе; если WebView2 отсутствует, он устанавливает его
через официальный загрузчик Microsoft (для этого нужен интернет).

Для уже существующего релиза запустите workflow `Build` вручную с
`mac_only=true` и нужным `release_tag`. Он добавит macOS-файлы и обновит
описание релиза. Локально macOS-сборки создаются `./build_app.sh` и
`./build_dmg.sh` на Mac соответствующей архитектуры.

Не добавляйте в git `data/`, модели, `.venv*/`, готовые клипы и ключи OAuth.
