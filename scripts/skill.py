#!/usr/bin/env python3
"""Install the portable skill or export selected resources; Python 3.10+, stdlib only."""

import argparse
from pathlib import Path
import stat
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins/accounting-finance/skills/accounting-finance"
NAME = "accounting-finance"

# Project paths, verified against the official sources linked in COMPATIBILITY.md.
AGENTS = {
    "claude-code": ".claude/skills",
    "codex": ".agents/skills",
    "cursor": ".cursor/skills",
    "github-copilot": ".github/skills",
    "gemini-cli": ".gemini/skills",
    "opencode": ".opencode/skills",
    "windsurf": ".windsurf/skills",
    "cline": ".cline/skills",
    "roo-code": ".roo/skills",
    "amp": ".agents/skills",
    "universal": ".agents/skills",
}
DOMAINS = (
    "generale", "analytique", "ifrs", "finance", "fiscalite", "audit",
    "controle-gestion", "paie",
)
PCG_DOMAINS = {"generale", "analytique", "finance", "fiscalite", "paie"}
RATES_DOMAINS = {"finance", "fiscalite", "paie"}
EXTRA_REFERENCES = ("glossaire", "decisions-cles")


def is_link(path):
    """Detect symlinks and Windows junctions on Python 3.10+ without following them."""
    try:
        status = path.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return False
    return stat.S_ISLNK(status.st_mode) or getattr(status, "st_reparse_tag", None) in {
        getattr(stat, "IO_REPARSE_TAG_SYMLINK", -1),
        getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", -2),
    }


def checked_path(path):
    """Reject links/junctions before resolving a destination, including its parents."""
    path = Path(path).expanduser().absolute()
    for component in (path, *path.parents):
        if is_link(component):
            raise ValueError(f"Destination uses a symlink or junction: {component}")
    return path.resolve()


def skill_files():
    if not (SOURCE / "SKILL.md").is_file():
        raise ValueError(f"Skill source is missing: {SOURCE}")
    files = {}
    for source_file in sorted(SOURCE.rglob("*")):
        if is_link(source_file):
            raise ValueError(f"Source must contain regular files: {source_file}")
        if source_file.is_file() and source_file.suffix in {".md", ".yaml"}:
            files[source_file.relative_to(SOURCE)] = source_file.read_bytes()
    files[Path("LICENSE")] = (ROOT / "LICENSE").read_bytes()
    return files


def write_files(plan, force=False, dry_run=False):
    """Preflight all conflicts before writing. Never remove directories or extra files."""
    pending = []
    for target, content in plan.items():
        target = checked_path(target)
        if target.is_relative_to(SOURCE):
            raise ValueError(f"Refusing to overwrite the canonical skill: {target}")
        for parent in target.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Parent is not a directory: {parent}")
        if target.exists():
            if not target.is_file():
                raise ValueError(f"Destination is not a regular file: {target}")
            if target.read_bytes() == content:
                continue
            if not force:
                raise ValueError(f"Different file already exists: {target}. Use --force to replace it.")
        pending.append((target, content))
    if not dry_run:
        for target, content in pending:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    verb = "Would write" if dry_run else "Wrote"
    print(f"{verb} {len(pending)} file(s); {len(plan) - len(pending)} unchanged.")


def install(args):
    if args.skills_dir is not None:
        if args.project is not None:
            raise ValueError("Use --skills-dir alone, without --project.")
        roots = [checked_path(args.skills_dir)]
    else:
        project = checked_path(args.project or Path.cwd())
        if not project.is_dir():
            raise ValueError(f"Project directory does not exist: {project}")
        roots = [checked_path(project / AGENTS[agent]) for agent in args.agent]
    destinations = list(dict.fromkeys(root / NAME for root in roots))
    files = skill_files()
    plan = {}
    for destination in destinations:
        if destination == SOURCE or destination.is_relative_to(SOURCE) or SOURCE.is_relative_to(destination):
            raise ValueError(f"Installation overlaps the canonical skill: {destination}")
        for relative, content in files.items():
            plan[destination / relative] = content
        print(f"Skill directory: {destination}")
    write_files(plan, args.force, args.dry_run)


def export_resources(domains, extras=()):
    selected = set(DOMAINS) if "all" in domains else set(domains)
    resources = ["SKILL.md", "methodology.md", "references/sources.md"]
    resources.extend(f"references/{domain}.md" for domain in DOMAINS if domain in selected)
    if selected & PCG_DOMAINS:
        resources.append("references/pcg-index.md")
    if selected & RATES_DOMAINS:
        resources.append("references/taux-baremes.md")
    resources.extend(f"references/{extra}.md" for extra in dict.fromkeys(extras))
    return resources


def export(args):
    resources = export_resources(args.domain, args.extra or ())
    header = (
        "# accounting-finance — portable context bundle\n\n"
        "Apply the included SKILL.md to the user's accounting/finance request. "
        "Follow the host's instructions and the user's requested output format.\n\n"
        "Each RESOURCE section below is the content of the named skill-relative file. "
        "References to those paths can be resolved within this document. "
        "Other referenced files are not included: request an extract when needed. "
        "This bundle does not grant filesystem access, web access or tools. "
        "Embedded rates and examples have not been verified as current by this export.\n\n"
        "Included resources:\n" + "".join(f"- `{name}`\n" for name in resources)
    )
    sections = [header]
    for resource in resources:
        content = (SOURCE / resource).read_text(encoding="utf-8")
        sections.append(f"\n---\n\n# RESOURCE: {resource}\n\n{content.rstrip()}\n")
    sections.append("\n---\n\n# License\n\n" + (ROOT / "LICENSE").read_text(encoding="utf-8"))
    payload = "".join(sections).encode("utf-8")
    target = checked_path(args.output)
    write_files({target: payload}, args.force, args.dry_run)
    print(f"Bundle: {target} ({len(payload):,} UTF-8 bytes, {len(resources)} resources)")
    print("Check your host's context/upload limit; bytes are not a token count.")


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List supported project installation targets")
    install_parser = commands.add_parser("install", help="Copy the complete skill to a discovery directory")
    target = install_parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--agent", nargs="+", choices=AGENTS, help="One or more agent applications")
    target.add_argument("--skills-dir", type=Path, help="Custom skills parent directory; NAME is appended")
    install_parser.add_argument("--project", type=Path, help="Existing project root; default: working directory")
    export_parser = commands.add_parser("export", help="Create a standalone Markdown context bundle")
    export_parser.add_argument("--domain", nargs="+", choices=(*DOMAINS, "all"), required=True)
    export_parser.add_argument("--extra", nargs="+", choices=EXTRA_REFERENCES)
    export_parser.add_argument("--output", type=Path, required=True)
    for command in (install_parser, export_parser):
        command.add_argument("--force", action="store_true", help="Replace conflicting shipped files; keep extra files")
        command.add_argument("--dry-run", action="store_true", help="Preflight and report without writing")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "list":
            for agent, directory in AGENTS.items():
                print(f"{agent:16} {directory}/{NAME}/")
        elif args.command == "install":
            install(args)
        else:
            export(args)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
