# Релизы KadrFlow

Версия берётся из `kadrflow/_version.py`. Перед тегом обновите номер версии,
`README.md` и `release/v<версия>/RELEASE_NOTES.md`.

Проверьте исходники:

```bash
python -m unittest discover -s tests -p 'test_*.py'
node --check web/app.js
```

Пуш тега `v<версия>` запускает сборку Windows в GitHub Actions. После её
проверки workflow создаёт GitHub Release и прикрепляет установщик EXE,
переносимый ZIP и контрольные суммы SHA256. Установщик создаёт ярлыки в
меню «Пуск» и на рабочем столе; если WebView2 отсутствует, он устанавливает
его через официальный загрузчик Microsoft (для этого нужен интернет). macOS-сборка
создаётся отдельно `./build_app.sh` или `./build_dmg.sh` и публикуется после
проверки на macOS. До публикации архива ссылки на сайте ведут на исходники.

Не добавляйте в git `data/`, модели, `.venv*/`, готовые клипы и ключи OAuth.
