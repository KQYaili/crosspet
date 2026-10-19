"""Check character data without opening CrossPet.

    python3 tests/character_assets_test.py
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "characters"


def pose_file(folder: Path, pose: str) -> bool:
    return (folder / f"{pose}.webp").is_file() or any(folder.glob(f"{pose}-*.webp"))


class CharacterAssetsTest(unittest.TestCase):
    def test_every_character_has_idle_and_valid_webp(self):
        folders = [path for path in ROOT.iterdir() if path.is_dir()]
        self.assertGreaterEqual(len(folders), 8)
        for folder in folders:
            with self.subTest(character=folder.name):
                self.assertTrue((folder / "character.json").is_file())
                data = json.loads((folder / "character.json").read_text(encoding="utf-8"))
                if not data.get("egg"):
                    self.assertTrue(pose_file(folder, "idle"), folder.name)
                for image in folder.glob("*.webp"):
                    data = image.read_bytes()
                    self.assertGreater(len(data), 32, image.name)
                    self.assertTrue(data.startswith(b"RIFF") and data[8:12] == b"WEBP", image.name)

    def test_configured_poses_have_images(self):
        for folder in ROOT.iterdir():
            if not folder.is_dir():
                continue
            data = json.loads((folder / "character.json").read_text(encoding="utf-8"))
            wanted = list(data.get("idleActions") or [])
            for key in ("pokePose", "correctedPose"):
                if data.get(key):
                    wanted.append(data[key])
            long_think = data.get("longThink") or {}
            if long_think.get("pose"):
                wanted.append(long_think["pose"])
            for pose in wanted:
                with self.subTest(character=folder.name, pose=pose):
                    self.assertTrue(pose_file(folder, pose), f"{folder.name} missing {pose}")

    def test_claude_new_poses_and_grok_work_poses(self):
        claude = ROOT / "claude"
        for pose in ("ip_detective", "suspend_lesson", "suspicious_pout"):
            self.assertTrue(pose_file(claude, pose))
        data = json.loads((claude / "character.json").read_text(encoding="utf-8"))
        self.assertEqual(data["pokePose"], "suspicious_pout")
        self.assertIn("ip_detective", data["idleActions"])
        self.assertIn("suspend_lesson", data["idleActions"])
        grok = ROOT / "grok"
        for pose in ("idle", "thinking", "listening", "reading", "writing", "running",
                     "happy", "oops", "surprised", "compact", "edge_left", "edge_right",
                     "edge_left_peek", "edge_right_peek"):
            self.assertTrue(pose_file(grok, pose), pose)


if __name__ == "__main__":
    unittest.main()
