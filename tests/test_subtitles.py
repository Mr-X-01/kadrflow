import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase, mock

from kadrflow import downloader


class SubtitleSelectionTest(TestCase):
    def test_prefers_russian_subtitles_over_english(self):
        class FakeYoutubeDL:
            def __init__(self, options):
                self.options = options

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def download(self, urls):
                (directory / "subs.en.vtt").write_text("WEBVTT", encoding="utf-8")
                (directory / "subs.ru.vtt").write_text("WEBVTT", encoding="utf-8")

        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            with mock.patch.dict(sys.modules, {"yt_dlp": SimpleNamespace(YoutubeDL=FakeYoutubeDL)}), mock.patch.object(downloader, "ensure_path"):
                selected = downloader.fetch_subtitles("https://example.com/video", directory)
            self.assertEqual(selected, str(directory / "subs.ru.vtt"))
