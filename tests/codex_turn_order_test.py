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

    def test_subagent_events_follow_the_root_turn(self):
        # Codex 的子代理：主会话的 session_id、子线程自己的 turn_id 和 agent_id；它的第一条消息也触发 UserPromptSubmit
        child = dict(tid="C1", agent_id="child-1", agent_type="worker")
        self.send("UserPromptSubmit")
        self.send("PreToolUse", tool_name="spawn_agent")
        self.send("SubagentStart", **child)
        self.assertEqual(self.send("UserPromptSubmit", **child)["event"], "SubagentStart")
        self.assertEqual(self.send("PreToolUse", tool_name="exec_command", **child)["pose"], "running")
        self.send("SubagentStop", **child)
        self.send("PostToolUse", tool_name="wait_agent")
        self.assertEqual(self.send("Stop")["pose"], "happy")

    def test_subagent_after_root_stop_stays_finished(self):
        child = dict(tid="C1", agent_id="child-1", agent_type="worker")
        self.send("UserPromptSubmit")
        self.send("Stop")
        for late in ("SubagentStart", "UserPromptSubmit", "PreToolUse", "PostToolUse", "SubagentStop"):
            with self.subTest(late=late):
                current = self.send(late, tool_name="exec_command", **child)
                self.assertEqual((current["event"], current["pose"]), ("Stop", "happy"))
        self.assertEqual(self.send("UserPromptSubmit", tid="T2")["pose"], "listening")

    def test_manual_compact_is_its_own_turn(self):
        # 手动 /compact 单独算一轮：新的 turn_id，没有 UserPromptSubmit，也没有 Stop
        self.send("UserPromptSubmit")
        self.send("Stop")
        self.assertEqual(self.send("PreCompact", tid="K1", trigger="manual")["pose"], "compact")
        current = self.send("PostCompact", tid="K1", trigger="manual")
        self.assertEqual((current["event"], current["pose"]), ("Stop", "happy"))
        self.assertEqual(self.send("SubagentStop", tid="T1")["event"], "Stop")

    def test_codex_keeps_its_tool_count_to_itself(self):
        # Codex 换成 Claude 的模型时由 Claude 来演：它的计数记在自己那边，不把 Claude Code 正数着的清零
        claude = self.data / "characters" / "claude"
        claude.mkdir(parents=True)
        (claude / "character.json").write_text("{}", encoding="utf-8")
        (claude / "idle.webp").write_bytes(b"RIFF")

        def claude_code(name, **extra):
            return invoke(self.state, self.data, {"hook_event_name": name, "session_id": "cc", **extra}, "claude")
        claude_code("UserPromptSubmit")
        for _ in range(7):
            claude_code("PreToolUse", tool_name="Read")
        self.send("UserPromptSubmit", sid="codex", tid="X1", model="claude-sonnet-5")
        host = json.loads((self.state / "gpt-host.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(host["character"], "claude")
        claude_code("PreToolUse", tool_name="Edit")
        self.assertEqual(claude_code("Stop")["pose"], "proud")

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
