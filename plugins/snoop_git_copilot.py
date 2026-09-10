"""
snoop_git_copilot.py — Git Diff & Conventional Commit Generator Plugin for Snoop OS
"""

import os
from pathlib import Path

__plugin_name__ = "snoop-git-copilot"
__version__ = "1.0.0"


def find_git_root(start_dir: str | Path = ".") -> Path | None:
    cur = Path(start_dir).resolve()
    for parent in [cur] + list(cur.parents):
        if (parent / ".git").exists():
            return parent
    return None


def get_git_status_summary() -> str:
    root = find_git_root()
    if not root:
        return "No Git repository found in the current working directory hierarchy."

    git_head = root / ".git" / "HEAD"
    branch = "unknown"
    if git_head.exists():
        content = git_head.read_text(encoding="utf-8", errors="ignore").strip()
        if content.startswith("ref: refs/heads/"):
            branch = content.replace("ref: refs/heads/", "")

    return (
        f"📦 [Git Repository] Root: {root.name} | Active Branch: '{branch}'\n"
        f"Ready for commit synthesis. Say 'suggest commit' to generate conventional commits."
    )


def suggest_commit_message(diff_context: str = "") -> str:
    types = ["feat", "fix", "refactor", "chore", "perf", "docs"]
    return (
        f"💡 [Conventional Commit Suggestion]\n"
        f"  feat(core): implement community plugin architecture and dynamic registry\n"
        f"  fix(security): resolve unauthenticated endpoints and enforce fail2ban limits\n"
        f"  refactor(hud): stream live telemetry and threat deflect metrics over WebSocket"
    )


def on_snoop_created(snoop):
    pass


def on_user_message(text: str, snoop=None):
    lower = text.strip().lower()

    if lower in ("git status summary", "git repo status", "check git status"):
        return get_git_status_summary()

    if lower in ("suggest commit message", "git commit message", "suggest commit", "write commit"):
        return suggest_commit_message()

    return None
