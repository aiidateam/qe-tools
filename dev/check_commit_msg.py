"""Validate that the commit subject starts with a recognized type emoji.

Convention: https://mbercx.github.io/python-copier/dev-standards/#specifying-the-type-of-change

Usage (called by pre-commit as a `commit-msg` hook):

    python dev/check_commit_msg.py .git/COMMIT_EDITMSG
"""

import sys
from pathlib import Path

# Keep in sync with `dev/update_changelog.py` and `docs/dev-standards.md`.
# Listed in priority order (matches the dev-standards table).
VALID_EMOJIS: tuple[str, ...] = (
    # Changelog sections
    "💥",
    "📦",
    "❌",
    "✨",
    "👌",
    "🐛",
    "📚",
    # Developer sections
    "🔄",
    "🧪",
    "⏪",
    "🔧",
    "🧹",
    # Excluded from changelog, but still valid types
    "🚀",
    "🐭",
    "❓",
)


def main() -> int:
    commit_msg_file = Path(sys.argv[1])
    message = commit_msg_file.read_text(encoding="utf-8")

    first_line = message.split("\n", maxsplit=1)[0]
    if not first_line.startswith(VALID_EMOJIS):
        print(
            f"❌ Commit subject must start with a type emoji.\n"
            f"\n"
            f"   Got:      {first_line!r}\n"
            f"\n"
            f"   Allowed:  {' '.join(VALID_EMOJIS)}\n"
            f"\n"
            f"   See: https://mbercx.github.io/python-copier/dev-standards/#specifying-the-type-of-change",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
