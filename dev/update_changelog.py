"""Update `CHANGELOG.md` based on commits since the latest release tag.

Commit type conventions: https://mbercx.github.io/python-copier/dev-standards/#specifying-the-type-of-change
"""

# ruff: noqa: S603, S607

import re
import subprocess
from pathlib import Path

from qe_tools.__about__ import __version__

ROOT = Path(__file__).resolve().parent.parent
GIT_REMOTE = "origin"

CHANGELOG_SECTIONS: dict[str, str] = {
    "💥": "Breaking changes",
    "📦": "Dependency updates",
    "❌": "Deprecations",
    "✨": "New features",
    "👌": "Improvements",
    "🐛": "Bug fixes",
    "📚": "Documentation",
}

DEVELOPER_SECTIONS: dict[str, str] = {
    "🔄": "Refactor",
    "🧪": "Tests",
    "⏪": "Reverts",
    "🔧": "DevOps",
    "🧹": "Cleanup",
}

ALL_SECTIONS = CHANGELOG_SECTIONS | DEVELOPER_SECTIONS

EXCLUDED_EMOJIS: set[str] = {"🚀", "🐭", "❓"}


def get_github_url() -> str | None:
    """Derive `https://github.com/org/repo` from the git remote origin, or `None`."""
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", GIT_REMOTE],
            capture_output=True,
            check=True,
            encoding="utf-8",
            cwd=ROOT,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None

    match = re.match(r"(?:https://github\.com/|git@github\.com:)(.+?)(?:\.git)?$", url)
    return f"https://github.com/{match.group(1)}" if match else None


def get_latest_tag() -> str | None:
    """Return the latest `vX.Y.Z` tag, or `None` if no tags exist."""
    result = subprocess.run(
        ["git", "tag", "--sort=v:refname"],
        capture_output=True,
        check=True,
        encoding="utf-8",
        cwd=ROOT,
    )
    tags = [
        t for t in result.stdout.splitlines() if re.fullmatch(r"v\d+\.\d+\.\d+\S*", t)
    ]
    return tags[-1] if tags else None


def get_commits(since_tag: str | None) -> str:
    """Return the `git log` output since the given tag, or all commits if `None`."""
    cmd = ["git", "log", "--pretty=format:%h|%H|%s"]
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")
    return subprocess.run(
        cmd,
        capture_output=True,
        check=True,
        encoding="utf-8",
        cwd=ROOT,
    ).stdout


def classify_commit(message: str) -> tuple[str | None, str]:
    """Return `(emoji, stripped_message)` or `(None, message)` if not a changelog type."""
    for emoji in ALL_SECTIONS:
        if message.startswith(emoji):
            return emoji, message[len(emoji) :].lstrip()
    return None, message


def update_changelog() -> None:
    """Update `CHANGELOG.md` for a first draft of the release."""
    version = __version__

    changelog_path = ROOT / "CHANGELOG.md"
    current = (
        changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else ""
    )

    if f"## v{version}" in current:
        print(f"🔄 Version v{version} already in CHANGELOG.md. Skipping.")
        return

    github_url = get_github_url()
    if github_url is None:
        print(
            f"⚠️  Could not derive GitHub URL from remote '{GIT_REMOTE}'. Commit links will use plain hashes."
        )

    latest_tag = get_latest_tag()
    commits_raw = get_commits(latest_tag)

    if not commits_raw.strip():
        print("🤷 No commits found since last tag. Skipping.")
        return

    pr_pattern = re.compile(r"\s*\(#\d+\)$")

    sections: dict[str, list[str]] = {emoji: [] for emoji in ALL_SECTIONS}
    uncategorized: list[str] = []

    for line in commits_raw.splitlines():
        if not line:
            continue
        hash_short, hash_long, message = line.split("|", maxsplit=2)

        # Strip PR number from the message
        message = pr_pattern.sub("", message)

        # Classify by leading emoji
        emoji, stripped_msg = classify_commit(message)

        if emoji is None and any(message.startswith(e) for e in EXCLUDED_EMOJIS):
            continue

        if github_url:
            entry = (
                f"* {stripped_msg} [[{hash_short}]({github_url}/commit/{hash_long})]"
            )
        else:
            entry = f"* {stripped_msg} [{hash_short}]"

        if emoji is None:
            uncategorized.append(entry)
            print(f"⚠️  Uncategorized commit: {hash_short} {message}")
        else:
            sections[emoji].append(entry)

    # Build changelog: uncategorized first to improve visibility
    section_text = ""
    if uncategorized:
        section_text += "\n### ❓ Uncategorized\n\n"
        section_text += "\n".join(uncategorized) + "\n"

    # Main changelog sections -> User oriented
    for emoji, section_name in CHANGELOG_SECTIONS.items():
        if sections[emoji]:
            section_text += f"\n### {emoji} {section_name}\n\n"
            section_text += "\n".join(sections[emoji]) + "\n"

    # Developer section with plain-text subsections
    dev_text = ""
    for emoji, section_name in DEVELOPER_SECTIONS.items():
        if sections[emoji]:
            dev_text += f"\n{emoji} {section_name}\n\n"
            dev_text += "\n".join(sections[emoji]) + "\n"

    if dev_text:
        section_text += f"\n#### Developer\n{dev_text}"

    header = "# Changelog\n\n"
    body = current.removeprefix("# Changelog").lstrip("\n")
    new_entry = f"## v{version}\n{section_text}"
    changelog_path.write_text(header + new_entry + "\n" + body, encoding="utf-8")
    print(f"✨ Updated CHANGELOG.md for v{version}.")


if __name__ == "__main__":
    update_changelog()
