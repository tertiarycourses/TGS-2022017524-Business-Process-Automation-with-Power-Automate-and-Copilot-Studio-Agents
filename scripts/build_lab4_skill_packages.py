#!/usr/bin/env python3
"""Build Copilot Studio skill packages for Labs 5 to 9.

Each skill lives in a  skills/<skill-name>/  folder somewhere under one of the
agent labs (the lab root itself, or a going-further/ kit, or a numbered agent
folder inside Lab 9), containing SKILL.md (uploadable) and TEACHING-NOTES.md
(trainer-only).

This script validates every SKILL.md and writes one .zip per skill into that
skills/_packages/ folder, with SKILL.md at the TOP LEVEL of the archive
(no wrapping parent folder) as Microsoft's packaging guidance requires.

TEACHING-NOTES.md is deliberately excluded from the archive — everything inside
a package is read by the model and would become part of the agent's behaviour.

Usage:  python3 scripts/build_lab4_skill_packages.py [--check]
        --check validates only and writes nothing.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

LABS = [
    "labs/Lab 5 - Your First Agent",
    "labs/Lab 6 - Procurement Agent with Tools",
    "labs/Lab 7 - Sales Agent with Knowledge",
    "labs/Lab 8 - IT Support Agent with Skills",
    "labs/Lab 9 - Multi-Agent Content Team",
]
PACKAGE_DIR_NAME = "_packages"
EXCLUDE_FROM_PACKAGE = {"TEACHING-NOTES.md"}

# Copilot Studio reads `name` and `description` from the YAML front matter.
# Keep the name a slug so it round-trips through the portal unchanged.
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_DESCRIPTION = 1024


class SkillError(Exception):
    pass


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_front_matter(text: str) -> dict[str, str]:
    """Return the YAML front-matter mapping from a SKILL.md body.

    Only the flat `key: value` subset is supported, which is all the format uses.
    """
    if not text.startswith("---\n"):
        raise SkillError("does not begin with a '---' YAML front-matter fence")
    end = text.find("\n---", 3)
    if end == -1:
        raise SkillError("YAML front matter is not closed by a '---' line")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise SkillError(f"front-matter line is not 'key: value': {line!r}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    body = text[end + 4 :]
    if not body.strip():
        raise SkillError("has front matter but no instructions after it")
    return fields


def validate(skill_md: Path, expected_name: str) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    fields = parse_front_matter(text)

    for required in ("name", "description"):
        if required not in fields:
            raise SkillError(f"front matter is missing '{required}'")
        if not fields[required]:
            raise SkillError(f"front matter '{required}' is empty")

    name = fields["name"]
    if not NAME_RE.match(name):
        raise SkillError(f"name {name!r} is not a lowercase-hyphen slug")
    if name != expected_name:
        raise SkillError(f"name {name!r} does not match its folder {expected_name!r}")
    if len(fields["description"]) > MAX_DESCRIPTION:
        raise SkillError(
            f"description is {len(fields['description'])} chars, over {MAX_DESCRIPTION}"
        )
    return fields


def package_files(skill_dir: Path) -> list[Path]:
    """Files that go into the archive: SKILL.md plus any supporting resources."""
    return sorted(
        p
        for p in skill_dir.rglob("*")
        if p.is_file()
        and p.name not in EXCLUDE_FROM_PACKAGE
        and not p.name.startswith(".")
    )


def build(skill_dir: Path, out_dir: Path, check_only: bool) -> tuple[str, int]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise SkillError("has no SKILL.md")

    fields = validate(skill_md, skill_dir.name)
    files = package_files(skill_dir)

    if check_only:
        return fields["name"], len(files)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_zip = out_dir / f"{skill_dir.name}.zip"
    # Deterministic archive: fixed timestamp so rebuilds don't churn git.
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(str(path.relative_to(skill_dir)), (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    return fields["name"], len(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate only, write nothing")
    args = parser.parse_args()

    failures: list[str] = []
    built = 0

    labs_root = repo_root() / "labs"
    skills_dirs: list[Path] = []
    for lab in LABS:
        lab_dir = repo_root() / lab
        if not lab_dir.is_dir():
            print(f"ERROR: cannot find {lab_dir}", file=sys.stderr)
            return 2
        # every skills/ folder under the lab: the lab root, going-further/ kits,
        # and the numbered agent folders inside Lab 6.
        skills_dirs.extend(
            sorted(p for p in lab_dir.rglob("skills") if p.is_dir() and PACKAGE_DIR_NAME not in p.parts)
        )

    for skills_dir in skills_dirs:
        agent_dir = skills_dir.parent

        skill_dirs = sorted(
            d for d in skills_dir.iterdir() if d.is_dir() and d.name != PACKAGE_DIR_NAME
        )
        if not skill_dirs:
            continue

        print(f"\n{agent_dir.relative_to(labs_root)}")
        out_dir = skills_dir / PACKAGE_DIR_NAME
        for skill_dir in skill_dirs:
            try:
                name, count = build(skill_dir, out_dir, args.check)
            except SkillError as exc:
                failures.append(f"{agent_dir.name}/{skill_dir.name}: {exc}")
                print(f"  FAIL  {skill_dir.name} — {exc}")
            else:
                built += 1
                verb = "ok" if args.check else "built"
                print(f"  {verb:5} {name}.zip ({count} file{'s' if count != 1 else ''})")

    print(f"\n{built} skill package{'s' if built != 1 else ''} "
          f"{'validated' if args.check else 'built'}.")
    if failures:
        print(f"{len(failures)} failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
