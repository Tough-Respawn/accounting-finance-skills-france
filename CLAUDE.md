# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **accounting-finance**, a Claude Code plugin that provides a French accounting and corporate finance research assistant. It covers 8 domains (general accounting, cost accounting, IFRS/consolidation, corporate finance, tax, audit, management control, payroll) with embedded reference materials, structured response templates, and user-role adaptation.

Installed via: `claude plugin install accounting-finance`

## Architecture

The plugin follows the Claude Code plugin structure with two layers:

### Plugin Manifest (root)
- `.claude-plugin/marketplace.json` — Plugin registry entry (name, version, description, source path)
- `plugins/accounting-finance/.claude-plugin/plugin.json` — Plugin metadata

### Plugin Content (`plugins/accounting-finance/`)

**Commands** (`commands/`): 9 slash-command definitions (`.md` files with YAML frontmatter). Each command file specifies `description`, `argument-hint`, `allowed-tools`, and a workflow. Domain-specific commands (e.g., `general-accounting.md`) skip routing and load their domain file directly. The generic `/accounting` command auto-routes based on keywords.

**Skill** (`skills/accounting-finance/`):
- `SKILL.md` — Main skill definition. Contains: role detection logic (5 roles), domain routing table (keywords -> reference files), research protocol (5 steps), complex case protocol, response template selection priority, citation standards, and mandatory disclaimer rules.
- `methodology.md` — 8 response templates aligned with French accounting methodology (ecriture comptable, analyse financiere, note fiscale, exercice corrige, fiche de paie, tableau de bord, cas complexe, sortie structuree).

**References** (`skills/accounting-finance/references/`): ~387 KB of embedded reference material:
- 8 domain files (`generale.md`, `analytique.md`, `ifrs.md`, `finance.md`, `fiscalite.md`, `audit.md`, `controle-gestion.md`, `paie.md`) — key articles, standards, rates, rules per domain
- `pcg-index.md` — lightweight PCG index (classes 1-7, main accounts)
- `taux-baremes.md` — rates and thresholds (IS, TVA, SMIC, PASS, cotisations, taux directeurs)
- `glossaire.md` — ~150 accounting/finance terms (FR/EN)
- `sources.md` — official source URLs and descriptions
- `decisions-cles.md` — ~35 landmark decisions and regulations

## Key Design Decisions

- **Domain routing** is keyword-based (see table in SKILL.md). Multi-domain questions load multiple reference files.
- **Conditional loading**: `pcg-index.md` loaded only for domains 1, 2, 4, 5, 8 (where PCG accounts are referenced). `taux-baremes.md` loaded only for tax, payroll, and finance queries.
- **Response template selection** follows strict priority: command-triggered > user-role-based > request-nature-based. Complex cases override to template #7 unless a command was explicitly used.
- **Web verification is mandatory**: even when embedded references contain the answer, the skill must cross-check against Legifrance/BOFiP/URSSAF. If verification fails, a warning is displayed.
- **All responses must end with a legal disclaimer** — never omitted.
- **Language**: respond in the user's detected language; all reference material is in French.
- **Token budget**: ~80-150 KB per query via selective domain loading.

## Contributing to References

Add articles, rates, or standards to the relevant file under `plugins/accounting-finance/skills/accounting-finance/references/<domain>.md`, following the existing table-based format within each file.