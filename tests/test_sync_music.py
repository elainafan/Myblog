"""Offline regression tests for downloads, playlist publication, and pruning."""
from argparse import Namespace
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sync_music as music


class SyncMusicTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.music = self.root / "static/music"
        self.bili = self.music / "bilibili"
        self.index = self.root / "data/music/generated.json"
        paths = patch.multiple(music, ROOT=self.root, STATIC_MUSIC=self.music,
                               BILIBILI_MUSIC=self.bili, LOCAL_META=self.index.with_name("local.json"),
                               GENERATED_PLAYLIST=self.index)
        paths.start()
        self.addCleanup(paths.stop)
        for bvid in ["current", "stale"]:
            folder = self.bili / bvid
            folder.mkdir(parents=True)
            (folder / "music.m4a").write_bytes(b"existing audio")
            music.write_json(folder / "info.json", {"name": bvid, "bvid": bvid, "page": 1})
        with redirect_stdout(StringIO()):
            music.write_playlist()
        self.favorites = [{"bvid": b, "title": b, "page": 1} for b in ("current", "new")]

    def snapshot(self):
        return {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob("*") if p.is_file()}

    def run_cli(self, *arguments, download=None, command="bilibili"):
        if download is None:
            def download(track, staging, executable):
                (staging / "music.m4a").write_bytes(b"new audio")

        output = StringIO()
        with patch.object(sys, "argv", ["sync_music.py", command, "--media-id", "1", *arguments]), \
             patch.object(music, "fetch_bilibili_favorite", return_value=self.favorites), \
             patch.object(music, "fetch_bilibili_pages", return_value=[{"cid": 42, "page": 1}]), \
             patch.object(music, "download_audio", side_effect=download), \
             redirect_stdout(output), redirect_stderr(output):
            status = music.main()
        return status, output.getvalue()

    def test_preview_lists_removals_and_writes_nothing(self):
        before = self.snapshot()
        for command in ("bilibili", "all"):
            status, output = self.run_cli("--dry-run", command=command)
            self.assertEqual(status, 0, output)
            self.assertIn("Remove: bilibili/stale", output)
            self.assertIn("Download: bilibili/new", output)
            self.assertEqual(self.snapshot(), before)

    def test_limit_preserves_unseen_tracks_even_if_limit_exceeds_list(self):
        for limit in ("1", "10"):
            status, output = self.run_cli("--limit", limit)
            self.assertEqual(status, 0, output)
            self.assertNotIn("Remove:", output)
            self.assertTrue((self.bili / "stale/music.m4a").exists())
            self.assertIn("stale", [t["bvid"] for t in json.loads(self.index.read_text())])

    def test_full_sync_retires_only_stale_tracks(self):
        status, output = self.run_cli()
        self.assertEqual(status, 0, output)
        self.assertFalse((self.bili / "stale").exists())
        self.assertEqual({t["bvid"] for t in json.loads(self.index.read_text())}, {"new", "current"})

    def test_failed_force_refresh_preserves_playlist_and_every_existing_file(self):
        before = self.snapshot()

        def fail_second(track, staging, executable):
            (staging / "music.m4a").write_bytes(b"partial new audio")
            if track.info["bvid"] == "new":
                raise OSError("connection interrupted")

        status, output = self.run_cli("--force", download=fail_second)
        self.assertNotEqual(status, 0)
        self.assertIn("connection interrupted", output)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / ".music-sync.lock").exists())

    def test_incomplete_favorites_cannot_authorize_cleanup(self):
        payload = {"code": 0, "data": {"has_more": False, "info": {"media_count": 5},
                                       "medias": [{"type": 2, "bvid": "current"}]}}
        with patch.object(music, "http_get_json", return_value=payload), self.assertRaises(RuntimeError):
            music.fetch_bilibili_favorite("1", None)

    def test_banned_upload_and_multipart_identity(self):
        included = "BV1Q2421M7pf"  # Only Everyday World (P2) is eligible.
        banned = "BV1du4m1u7rL"
        parts = [{"page": n, "cid": 100 + n} for n in (1, 2, 3)]
        with patch.object(music, "fetch_bilibili_pages", return_value=parts) as read_pages:
            plan = music.read_track_plan([{"bvid": banned}, {"bvid": included, "page": 3}], None)
        read_pages.assert_called_once_with(included, None)
        self.assertEqual([(t.cid, t.directory.name, t.info["sourceUrl"]) for t in plan],
                         [(102, "p02", f"https://www.bilibili.com/video/{included}?p=2")])

    def test_412_uses_public_audio_for_the_selected_cid(self):
        track = music.BilibiliTrack(self.bili / "part", 102, "",
                                    {"bvid": "example", "page": 2, "sourceUrl": "https://www.bilibili.com/video/example?p=2"})
        payload = {"code": 0, "data": {"dash": {"audio": [
            {"mimeType": "audio/mp4", "bandwidth": 100, "baseUrl": "https://media.example/quiet"},
            {"mimeType": "audio/mp4", "bandwidth": 200, "baseUrl": "https://media.example/best"},
        ]}}}

        def download(url, target):
            self.assertEqual(url, "https://media.example/best")
            target.write_bytes(b"\x00\x00\x00\x18ftypisom")

        with patch.object(music.subprocess, "run", return_value=Namespace(returncode=1, stderr="HTTP Error 412")), \
             patch.object(music, "http_get_json", return_value=payload) as read, \
             patch.object(music, "download_file", side_effect=download), redirect_stdout(StringIO()):
            music.download_audio(track, self.root, "yt-dlp")
        self.assertIn("cid=102", read.call_args.args[0])
        self.assertTrue((self.root / "music.m4a").is_file())


if __name__ == "__main__":
    unittest.main()
