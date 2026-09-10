# Repository guidance

This repository distributes a portable French accounting and corporate finance Agent Skill, plus an optional Claude Code plugin.

- The canonical skill is `plugins/accounting-finance/skills/accounting-finance/`. Keep business instructions there; do not maintain separate copies for each host.
- All resource paths in the skill resolve relative to its `SKILL.md`. Keep host-specific tool names, variables and command syntax in adapters or installation documentation.
- `plugins/accounting-finance/commands/` contains Claude-specific adapters. Preserve their YAML metadata, plugin-root resource path and user argument forwarding.
- `scripts/skill.py` uses Python 3.10+ and only the standard library. No build step or runtime dependency is needed to read the skill.
- Preserve the eight domains, selective reference loading, official-source verification and explicit handling of unavailable capabilities. Never claim embedded rates are verified current.
- User-requested schemas take precedence over templates. JSON must be one parseable value; put notices and verification status inside permitted metadata.
- Keep `README.md`, `COMPATIBILITY.md` and installation targets consistent. Verify new host discovery paths against that host's official documentation.
- Keep the marketplace and plugin versions aligned when changing the distributed plugin.
- Run `python -m unittest discover -s tests -v` after changes to installation/export behavior. Validate edited JSON manifests and YAML frontmatter. New scripts must be exercised.
- When updating accounting references, cite the official source and applicable period. Portability changes do not imply a regulatory refresh.
