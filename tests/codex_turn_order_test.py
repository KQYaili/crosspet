"""Isolated Codex hook checks. Does not open CrossPet or touch a user profile.

    python3 tests/codex_turn_order_test.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "integrations" / "crosspet-hook.py"
REPO = HOOK.parent.parent


def invoke(state: Path, data: Path, payload: dict, character="gpt"):
    env = dict(os.environ)
    env["CROSSPET_STATE_DIR"] = str(state)
    env["CROSSPET_DATA_DIR"] = str(data)
    env["CODEX_HOME"] = str(data / "not-a-real-codex-home")
    result = subprocess.run([sys.executable, str(HOOK), character], input=json.dumps(payload),
                            text=True, capture_output=True, env=env, timeout=8)
    if result.returncode != 0 or result.stderr:
        raise AssertionError((result.returncode, result.stderr, payload["hook_event_name"]))
    path = state / f"{character}-state.json"
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else None


class CodexTurnOrderTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.data = Path(self.temp.name) / "data"
        self.data.mkdir()
        (self.data / "ai-autostart-off").write_text("test", encoding="utf-8")
        self.state = Path(self.temp.name) / "state"
        self.state.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def send(self, name, pose_unused=None, tid="T1", sid="parent", **extra):
        payload = {"hook_event_name": name, "session_id": sid, "cwd": str(REPO), "model": "gpt-test", **extra}
        if tid is not None:
            payload["turn_id"] = tid
        return invoke(self.state, self.data, payload)

    def test_late_events_do_not_reopen_a_finished_turn(self):
        self.send("UserPromptSubmit")
        self.send("PreToolUse", tool_name="read_file")
        self.assertEqual(self.send("Stop")["pose"], "happy")
        for late in ("SubagentStop", "PostToolUse", "PreToolUse", "SubagentStart"):
            with self.subTest(late=late):
                current = self.send(late, tool_name="exec_command")
                self.assertEqual(current["event"], "Stop")
                self.assertEqual(current["pose"], "happy")

    def test_old_turn_cannot_overwrite_a_new_turn(self):
        self.send("UserPromptSubmit")
        self.send("Stop")
        self.send("UserPromptSubmit", tid="T2")
        self.send("PreToolUse", tid="T2", tool_name="apply_patch")
        stale = self.send("PostToolUse", tid="T1", tool_name="exec_command")
        self.assertEqual(stale["event"], "PreToolUse")
        self.assertEqual(self.send("Stop", tid="T2")["pose"], "happy")

    def test_interrupt_stays_finished(self):
        self.send("UserPromptSubmit")
        self.assertEqual(self.send("Interrupt")["pose"], "surprised")
        current = self.send("SubagentStop")
        self.assertEqual(current["event"], "Stop")
        self.assertEqual(current["pose"], "surprised")

    def test_sessions_stay_independent(self):
        self.send("UserPromptSubmit")
        self.send("Stop")
        self.send("UserPromptSubmit", sid="other", tid="T-other")
        self.send("PreToolUse", sid="other", tid="T-other", tool_name="exec_command")
        self.send("SubagentStop")
        self.send("Stop", sid="other", tid="T-other")
        sessions = json.loads((self.state / "gpt-sessions.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(set(sessions), {"parent", "other"})
        self.assertTrue(all(item["event"] == "Stop" for item in sessions.values()))

    def test_eight_tools_finish_proud(self):
        self.send("UserPromptSubmit")
        for _ in range(8):
            self.send("PreToolUse", tool_name="read_file")
        self.assertEqual(self.send("Stop")["pose"], "proud")

    def test_codex_home_events_are_ignored(self):
        # invoke() points CODEX_HOME at data/not-a-real-codex-home
        home = self.data / "not-a-real-codex-home" / "memories"
        home.mkdir(parents=True)
        current = invoke(self.state, self.data, {
            "hook_event_name": "PreToolUse", "session_id": "mem", "turn_id": "M",
            "cwd": str(home), "tool_name": "read_file", "model": "gpt-test"})
        self.assertIsNone(current)


if __name__ == "__main__":
    unittest.main()
