#!/usr/bin/env python3
"""Check Shared Goals repository map invariants.

This intentionally avoids snapshotting README prose. It validates the canonical
JSON contract and, when sibling repositories are checked out locally, checks that
README files contain the shared heading and link back to the canonical PRD repo.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "references" / "repository-map.json"
REQUIRED_REPOS = {
    "shared-goals/prd",
    "shared-goals/instance",
    "shared-goals/skill",
    "shared-goals/text-forge",
    "bongiozzo/whattodo",
}
REQUIRED_KEYS = {"name", "role", "url", "local_path"}
PRD_URL = "https://github.com/shared-goals/prd"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_map() -> dict[str, Any]:
    try:
        data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing repository map: {MAP_PATH}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {MAP_PATH}: {exc}")
    if not isinstance(data, dict):
        fail("repository map root must be an object")
    return data


def check_map_shape(data: dict[str, Any]) -> list[dict[str, Any]]:
    heading = data.get("required_heading")
    if heading != "## Shared Goals Repository Map":
        fail("required_heading must be '## Shared Goals Repository Map'")

    canonical_repo = data.get("canonical_repo")
    if canonical_repo != "shared-goals/prd":
        fail("canonical_repo must be shared-goals/prd")

    repos = data.get("repos")
    if not isinstance(repos, list) or not repos:
        fail("repos must be a non-empty list")

    names: list[str] = []
    roles: list[str] = []
    for index, repo in enumerate(repos, start=1):
        if not isinstance(repo, dict):
            fail(f"repo #{index} must be an object")
        missing = REQUIRED_KEYS - set(repo)
        if missing:
            fail(f"repo #{index} missing keys: {', '.join(sorted(missing))}")
        name = repo["name"]
        role = repo["role"]
        url = repo["url"]
        local_path = repo["local_path"]
        if not all(isinstance(value, str) and value.strip() for value in (name, role, url, local_path)):
            fail(f"repo #{index} values must be non-empty strings")
        if not url.startswith("https://github.com/"):
            fail(f"repo {name} url must be a GitHub URL")
        names.append(name)
        roles.append(role)

    if len(names) != len(set(names)):
        fail("repo names must be unique")
    if len(roles) != len(set(roles)):
        fail("repo roles must be unique")

    missing_repos = REQUIRED_REPOS - set(names)
    if missing_repos:
        fail(f"repository map missing required repos: {', '.join(sorted(missing_repos))}")

    if names[0] != "shared-goals/prd":
        fail("shared-goals/prd must be the first repository in reading order")

    return repos


def check_local_readmes(repos: list[dict[str, Any]], heading: str) -> tuple[int, int]:
    checked = 0
    skipped = 0
    for repo in repos:
        repo_path = (ROOT / repo["local_path"]).resolve()
        readme = repo_path / "README.md"
        if not readme.exists():
            skipped += 1
            print(f"skip: {repo['name']} README not found at {readme}")
            continue

        text = readme.read_text(encoding="utf-8")
        if heading not in text:
            fail(f"{repo['name']} README missing heading: {heading}")
        if repo["url"] not in text:
            fail(f"{repo['name']} README missing its own repository URL: {repo['url']}")
        if repo["name"] != "shared-goals/prd" and PRD_URL not in text:
            fail(f"{repo['name']} README must link to canonical PRD repo: {PRD_URL}")
        checked += 1
    return checked, skipped


def main() -> int:
    data = load_map()
    repos = check_map_shape(data)
    checked, skipped = check_local_readmes(repos, data["required_heading"])
    print(f"repository map ok: {len(repos)} repos, {checked} local README(s) checked, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
