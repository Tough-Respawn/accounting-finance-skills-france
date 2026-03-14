# accounting-finance Plugin Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code plugin providing a French accounting and corporate finance assistant with 8 domains, 5 user roles, 9 commands, and embedded reference materials.

**Architecture:** Claude Code plugin following the `legal-france` pattern — marketplace manifest at root, plugin content under `plugins/accounting-finance/` with commands, a SKILL.md, methodology.md, and domain-specific reference files. All content is markdown — no code, no build step.

**Tech Stack:** Claude Code plugin system (markdown-based), git

**Spec:** `docs/superpowers/specs/2026-03-14-accounting-finance-plugin-design.md`

**Reference model:** `legal-france` plugin at `c:\Users\Amine\Documents\legal-skills-france\`

---

## Chunk 1: Plugin scaffold and manifests

### Task 1: Create plugin manifest files

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/accounting-finance/.claude-plugin/plugin.json`

- [ ] **Step 1: Create root marketplace.json**

Create `.claude-plugin/marketplace.json`:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "accounting-finance",
  "description": "French accounting & corporate finance assistant — analytical accounting, financial reporting (PCG/IFRS), corporate finance, tax, and audit across France and EU",
  "owner": {
    "name": "Amine Harrak",
    "email": "amineharrak@proton.me"
  },
  "plugins": [
    {
      "name": "accounting-finance",
      "description": "French accounting and corporate finance assistant covering general accounting, cost accounting, IFRS, corporate finance, tax, audit, management control, and payroll. Adapts to user role (accountant, student, executive, AI agent). Use when user mentions 'comptabilité', 'bilan', 'compte de résultat', 'PCG', 'écriture comptable', 'IFRS', 'IAS', 'consolidation', 'liasse fiscale', 'TVA', 'IS', 'CET', 'amortissement', 'provision', 'bulletin de paie', 'cotisations', 'URSSAF', 'DSN', 'BFR', 'SIG', 'CAF', 'trésorerie', 'budget', 'tableau de bord', 'audit', 'CAC', 'NEP', 'DCG', 'DSCG', 'expert-comptable', 'accounting', 'balance sheet', 'P&L', 'general ledger', 'payroll', 'cost accounting'.",
      "version": "1.0.0",
      "author": {
        "name": "Amine Harrak"
      },
      "source": "./plugins/accounting-finance",
      "category": "knowledge",
      "homepage": "https://github.com/Tough-Respawn/accounting-finance-skills-france"
    }
  ]
}
```

- [ ] **Step 2: Create plugin.json**

Create `plugins/accounting-finance/.claude-plugin/plugin.json`:

```json
{
  "name": "accounting-finance",
  "description": "French accounting and corporate finance assistant with domain-specific expertise across general accounting, cost accounting, IFRS, corporate finance, tax, audit, management control, and payroll. Supports financial analysis, accounting entries, tax optimization, and document parsing.",
  "author": {
    "name": "Amine Harrak"
  }
}
```

- [ ] **Step 3: Create .gitignore and LICENSE**

Create `.gitignore`:

```
.claude/
docs/superpowers/
```

Copy `LICENSE` from the legal-france repo (MIT, same author).

- [ ] **Step 4: Commit scaffold**

```bash
git add .claude-plugin/ plugins/accounting-finance/.claude-plugin/ .gitignore LICENSE
git commit -m "chore: add plugin scaffold — marketplace.json, plugin.json, .gitignore, LICENSE"
```

---

### Task 2: Create all 9 command files

**Files:**
- Create: `plugins/accounting-finance/commands/accounting.md`
- Create: `plugins/accounting-finance/commands/general-accounting.md`
- Create: `plugins/accounting-finance/commands/cost-accounting.md`
- Create: `plugins/accounting-finance/commands/ifrs.md`
- Create: `plugins/accounting-finance/commands/corporate-finance.md`
- Create: `plugins/accounting-finance/commands/tax.md`
- Create: `plugins/accounting-finance/commands/audit.md`
- Create: `plugins/accounting-finance/commands/management-control.md`
- Create: `plugins/accounting-finance/commands/payroll.md`

- [ ] **Step 1: Create router command — accounting.md**

```markdown
---
description: Ask any question about French accounting or corporate finance — routes to the right domain automatically
argument-hint: <your accounting/finance question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Detect the accounting/finance domain from the question keywords
2. Read the relevant `references/<domain>.md` file from the skill directory
3. Also read `references/pcg-index.md` for account lookup (if domain uses PCG accounts)
4. Apply the response template matching the user's role (see SKILL.md Response Protocol)
5. If embedded references are insufficient, use WebSearch to query official sources (BOFiP, URSSAF, Legifrance)
6. Cite all sources precisely (account numbers, article references, standard numbers)
7. End with the mandatory disclaimer
```

- [ ] **Step 2: Create domain command — general-accounting.md**

```markdown
---
description: French general accounting — PCG, journal entries, balance sheet, income statement, annexes
argument-hint: <your general accounting question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/generale.md` directly
2. Also read `references/pcg-index.md` for account lookup
3. Apply the response template based on detected user role (see SKILL.md Response Protocol)
4. If embedded references are insufficient, use WebSearch to query official sources
5. Cite all sources precisely (account numbers, article references)
6. End with the mandatory disclaimer
```

- [ ] **Step 3: Create domain command — cost-accounting.md**

```markdown
---
description: French cost accounting — full costing, variable costing, ABC, cost centers, break-even analysis
argument-hint: <your cost accounting question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/analytique.md` directly
2. Also read `references/pcg-index.md` for account lookup
3. Apply the response template based on detected user role (see SKILL.md Response Protocol)
4. If embedded references are insufficient, use WebSearch to query official sources
5. Cite all sources precisely
6. End with the mandatory disclaimer
```

- [ ] **Step 4: Create domain command — ifrs.md**

```markdown
---
description: IFRS/IAS standards and consolidation — international accounting standards, consolidated accounts, PCG-IFRS conversion
argument-hint: <your IFRS question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/ifrs.md` directly
2. Apply the response template based on detected user role (see SKILL.md Response Protocol)
3. If embedded references are insufficient, use WebSearch to query EUR-Lex or IFRS Foundation
4. Cite all sources precisely (IAS/IFRS standard numbers, ANC regulation numbers)
5. End with the mandatory disclaimer
```

- [ ] **Step 5: Create domain command — corporate-finance.md**

```markdown
---
description: French corporate finance — financial analysis, SIG, ratios, working capital, valuation, DCF, business plan
argument-hint: <your corporate finance question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/finance.md` directly
2. Also read `references/pcg-index.md` for account lookup and `references/taux-baremes.md` for rates
3. Apply the response template based on detected user role (see SKILL.md Response Protocol)
4. If embedded references are insufficient, use WebSearch to query official sources
5. Cite all sources precisely
6. End with the mandatory disclaimer
```

- [ ] **Step 6: Create domain command — tax.md**

```markdown
---
description: French corporate tax — IS, TVA, CET, tax regimes, fiscal consolidation
argument-hint: <your tax question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/fiscalite.md` directly
2. Also read `references/taux-baremes.md` for current rates and `references/pcg-index.md` for account lookup
3. Apply the response template based on detected user role (see SKILL.md Response Protocol)
4. If embedded references are insufficient, use WebSearch to query BOFiP or Legifrance
5. Cite all sources precisely (CGI articles, BOFiP references)
6. End with the mandatory disclaimer
```

- [ ] **Step 7: Create domain command — audit.md**

```markdown
---
description: French audit and internal control — statutory audit (CAC), NEP standards, internal control frameworks
argument-hint: <your audit question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/audit.md` directly
2. Apply the response template based on detected user role (see SKILL.md Response Protocol)
3. If embedded references are insufficient, use WebSearch to query official sources
4. Cite all sources precisely (NEP numbers, Code de commerce articles)
5. End with the mandatory disclaimer
```

- [ ] **Step 8: Create domain command — management-control.md**

```markdown
---
description: French management control — budgeting, dashboards, reporting, variance analysis, balanced scorecard
argument-hint: <your management control question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/controle-gestion.md` directly
2. Apply the response template based on detected user role (see SKILL.md Response Protocol)
3. If embedded references are insufficient, use WebSearch to query official sources
4. Cite all sources precisely
5. End with the mandatory disclaimer
```

- [ ] **Step 9: Create domain command — payroll.md**

```markdown
---
description: French payroll and social contributions — pay slips, URSSAF contributions, DSN, employer/employee charges
argument-hint: <your payroll question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. Skip domain routing — read `references/paie.md` directly
2. Also read `references/taux-baremes.md` for current rates and `references/pcg-index.md` for account lookup
3. Apply the response template based on detected user role (see SKILL.md Response Protocol)
4. If embedded references are insufficient, use WebSearch to query URSSAF or Legifrance
5. Cite all sources precisely (Code du travail articles, URSSAF rates)
6. End with the mandatory disclaimer
```

- [ ] **Step 10: Commit all command files**

```bash
git add plugins/accounting-finance/commands/
git commit -m "feat: add 9 slash commands — router + 8 domain commands"
```

---

## Chunk 2: SKILL.md and methodology.md

### Task 3: Create SKILL.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/SKILL.md`
- Reference: spec sections 1-4, 7-9, 11, 13-16

- [ ] **Step 1: Write SKILL.md**

Target size: ~10-12 KB. The SKILL.md must contain all the following sections, in order, transcribed from the spec:

1. **Frontmatter** — exact YAML from spec Section 1
2. **Role & Identity** — from spec Section 2 (5 core rules)
3. **User Role Detection** — from spec Section 4 (5 roles table + detection signals + clarifying question)
4. **Domains** — from spec Section 3 (8-domain table with scope and reference file mapping)
5. **Domain Routing** — from spec Section 7 (keyword→file routing table + conditional pcg-index rules)
6. **Commands Reference** — from spec Section 5 (9 commands table + template mapping note)
7. **Progress Indicators** — from spec Section 15 (5 standard steps + complex case adaptation)
8. **Research Protocol** — from spec Section 8 (5 steps with warning texts)
9. **Complex Case Protocol** — from spec Section 11 (triggers + 5 steps)
10. **Response Protocol** — from spec Section 9 (priority order + disambiguation table + complex case override)
11. **Citation Standards** — from spec Section 13 (9-row citation format table)
12. **Mandatory Disclaimer** — from spec Section 14 (FR + EN text + rules)
13. **Token Budget Strategy** — from spec Section 16 (selective loading rules, conditional pcg-index policy, >3 domains rule)

Follow the exact structure and wording of the legal-france SKILL.md as closely as possible, substituting domain-specific content from the spec.

- [ ] **Step 2: Verify SKILL.md completeness**

Check that SKILL.md contains ALL 13 sections listed above. Verify:
- Frontmatter has `name` and `description` fields
- All 5 core rules are present
- All 5 user roles are in the detection table
- 8-domain table with scope and reference file mapping is present
- All 8 domain routing rows are present with correct file references
- Commands table has all 9 commands
- Warning text (FR + EN) is present in Research Protocol
- Divergence handling text is present
- Template disambiguation table has 3 rows (Expert-comptable, Dirigeant, Collaborateur)
- Complex Case override paragraph is present (command priority 1 not overridden, priorities 2-3 overridden by template #7)
- All 9 citation formats are present
- Disclaimer text (FR + EN) is present
- Token Budget Strategy section present with selective loading rules and >3 domains policy

- [ ] **Step 3: Commit SKILL.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/SKILL.md
git commit -m "feat: add SKILL.md — main skill definition with routing, protocols, and citation standards"
```

---

### Task 4: Create methodology.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/methodology.md`
- Reference: spec Section 10, legal-france methodology.md for structure

- [ ] **Step 1: Write methodology.md with all 8 templates**

The file starts with a header and core principle, then defines 8 templates. Each template must include:
- **Trigger conditions** (when to use this template)
- **Tone** (language style guidance)
- **Section structure** (numbered sections with descriptions)
- **Example skeleton** (concrete example in a code block)

**Template 1 — Écriture comptable (Accounting Entry)**
- Trigger: Expert-comptable or Collaborateur asking about accounting treatment / journal entries
- Structure: Contexte → Schéma d'écritures (Débit/Crédit table with PCG accounts) → Justification normative (PCG, ANC, Code de commerce) → Impact bilan/CR
- Skeleton: show a purchase of goods entry with Compte 607 / Compte 44566 / Compte 401

**Template 2 — Analyse financière (Financial Analysis)**
- Trigger: Dirigeant, or any role requesting financial diagnosis
- Structure: Données clés → SIG calculés → Ratios (liquidité, solvabilité, rentabilité) → Diagnostic forces/faiblesses → Recommandations
- Skeleton: show SIG table + 3-4 key ratios + commentary

**Template 3 — Note fiscale (Tax Note)**
- Trigger: Expert-comptable asking about tax, or `/tax` command
- Structure: Régime applicable → Base légale (CGI + BOFiP) → Calcul détaillé → Options d'optimisation → Risques fiscaux → Délais
- Skeleton: show IS calculation with Art. 209-I CGI reference

**Template 4 — Exercice corrigé (Corrected Exercise)**
- Trigger: Étudiant role, or mentions DCG/DSCG/exercice
- Structure: Énoncé rappelé → Résolution méthodique pas à pas → Conclusion → Points de vigilance
- Skeleton: show a break-even calculation exercise

**Template 5 — Fiche de paie expliquée (Payslip Explained)**
- Trigger: Payroll question from any role
- Structure: Éléments bruts (salaire de base, primes) → Cotisations salariales (détail par ligne) → Cotisations patronales → Net imposable → Net à payer → Coût employeur total
- Skeleton: show a sample payslip decomposition with URSSAF rates

**Template 6 — Tableau de bord (Dashboard)**
- Trigger: Dirigeant asking about KPIs/reporting/dashboards
- Structure: Objectif → Indicateurs sélectionnés (table: KPI / Formule / Valeur / Seuil / Alerte) → Lecture → Actions recommandées
- Skeleton: show a 4-KPI dashboard table

**Template 7 — Cas complexe (Complex Case)**
- Trigger: Complex Case Protocol activated (multi-domain, causal chain, norm conflict)
- Structure: Problèmes identifiés (numbered list) → Traitement séquentiel (full reasoning per problem) → Synthèse croisée (interactions between problems) → Recommandation globale
- Skeleton: show a consolidation + tax integration example

**Template 8 — Sortie structurée (Structured Output)**
- Trigger: Agent IA role
- Structure: JSON or normalized table → No prose → Machine-readable references → Documented schema
- Skeleton: show a JSON example with account entries

- [ ] **Step 2: Verify methodology.md completeness**

Check that all 8 templates have: trigger conditions, tone, section structure, and example skeleton. Verify that the core principle section explains the accounting methodology backbone (comparable to the legal syllogism in legal-france).

- [ ] **Step 3: Commit methodology.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/methodology.md
git commit -m "feat: add methodology.md — 8 response templates with triggers, structure, and skeletons"
```

---

## Chunk 3: Cross-cutting reference files

### Task 5: Create pcg-index.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/pcg-index.md`

- [ ] **Step 1: Write pcg-index.md**

Must be lightweight (<5 KB). Structure:

```markdown
# Index du Plan Comptable Général (PCG)

Quick-reference index of PCG account classes and main accounts. For detailed entries, see the relevant domain reference file.

## Classes

| Classe | Libellé |
|--------|---------|
| 1 | Comptes de capitaux |
| 2 | Comptes d'immobilisations |
| 3 | Comptes de stocks et en-cours |
| 4 | Comptes de tiers |
| 5 | Comptes financiers |
| 6 | Comptes de charges |
| 7 | Comptes de produits |

## Comptes principaux par classe

### Classe 1 — Capitaux
- 10 — Capital et réserves
  - 101 — Capital
  - 106 — Réserves
  - 108 — Compte de l'exploitant
- 11 — Report à nouveau
- 12 — Résultat de l'exercice
- 13 — Subventions d'investissement
- 15 — Provisions
- 16 — Emprunts et dettes assimilées
  - 164 — Emprunts auprès des établissements de crédit

### Classe 2 — Immobilisations
[... continue with main accounts for each class ...]
```

Include the most commonly referenced accounts per class (15-20 per class, not all 900). Target: ~4 KB.

Use WebSearch to verify the current PCG structure against ANC sources if needed.

- [ ] **Step 2: Commit pcg-index.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/pcg-index.md
git commit -m "feat: add pcg-index.md — lightweight PCG account class index"
```

---

### Task 6: Create taux-baremes.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/taux-baremes.md`

- [ ] **Step 1: Research current rates**

Use WebSearch to fetch the latest rates from official sources:
- IS rates (Art. 219 CGI) — current standard rate + PME rate
- TVA rates (Art. 278+ CGI) — 20%, 10%, 5.5%, 2.1%
- SMIC 2026 — from URSSAF baremes
- PASS 2026 — plafond annuel de la sécurité sociale
- Main social contribution rates — from URSSAF taux-cotisations-secteur-prive
- Taux d'usure Q1 2026 — from Banque de France
- Taux d'intérêt légal S1 2026 — from Banque de France
- ECB key rates — from ECB

- [ ] **Step 2: Write taux-baremes.md**

Structure with clear date stamps for each rate:

```markdown
# Taux et Barèmes — France

> ⚠️ Les taux ci-dessous sont ceux en vigueur au [date de dernière mise à jour]. Vérifiez systématiquement sur la source officielle avant toute utilisation.

## Impôt sur les sociétés (IS)

| Taux | Condition | Base légale |
|------|-----------|-------------|
| ...% | Taux normal (toutes entreprises) | Art. 219-I CGI |
| ...% | Taux réduit PME (bénéfice ≤ ... €, CA ≤ ... €) | Art. 219-I-b CGI |

Source: [BOFiP](https://bofip.impots.gouv.fr)

## TVA
[... table with 4 rates ...]

## SMIC et plafonds
[... SMIC horaire/mensuel, PASS ...]

## Cotisations sociales — secteur privé
[... main rates table: maladie, vieillesse, chômage, retraite complémentaire ...]

## Taux financiers
[... taux d'usure, taux d'intérêt légal, taux directeurs BCE ...]
```

Target: ~10-15 KB. Each rate with its legal basis and official source URL.

- [ ] **Step 3: Commit taux-baremes.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/taux-baremes.md
git commit -m "feat: add taux-baremes.md — current rates and thresholds with official sources"
```

---

### Task 7: Create glossaire.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/glossaire.md`

- [ ] **Step 1: Write glossaire.md**

Follow the same format as legal-france's glossaire.md: alphabetical, French term in bold, English translation in italics, concise definition. Target: ~150 terms covering all 8 domains.

Must include key terms like: Actif, Amortissement, Bilan, BFR, CAF, Capitaux propres, Charges, Classe (PCG), Consolidation, Coût complet, Coût variable, Crédit-bail, DCF, Débit/Crédit, DSN, EBITDA, Écriture comptable, Exercice comptable, Goodwill, IFRS, Immobilisation, Impôt différé, IS, Journal, Liasse fiscale, Marge, NEP, PCG, PASS, Passif, Provision, Résultat, SIG, SMIC, Solde, TVA, URSSAF, Valeur ajoutée...

- [ ] **Step 2: Commit glossaire.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/glossaire.md
git commit -m "feat: add glossaire.md — ~150 accounting/finance terms FR/EN"
```

---

### Task 8: Create sources.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/sources.md`

- [ ] **Step 1: Write sources.md**

Follow the same format as legal-france's sources.md: each source with URL, operator, what it contains, how to search it, URL patterns, and citation formats.

Sources to document (from spec Section 12):
1. BOFiP — tax doctrine
2. URSSAF — social contribution rates
3. Legifrance — CGI, Code de commerce, Code du travail
4. EUR-Lex — EU directives, adopted IFRS
5. ECB — key interest rates
6. Banque de France — usury rates, legal interest rates
7. ANC — Plan Comptable Général, accounting regulations
8. H3C / CNCC — audit standards (NEP)
9. OEC — professional recommendations

For each: URL, what it contains, how to search, citation format.

- [ ] **Step 2: Commit sources.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/sources.md
git commit -m "feat: add sources.md — official source guide with search instructions"
```

---

### Task 9: Create decisions-cles.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/decisions-cles.md`

- [ ] **Step 1: Research landmark decisions**

Use WebSearch to identify key decisions in:
- Tax law: CE landmark decisions on IS, TVA, abuse of law
- ANC: key interpretive positions and regulation changes
- Accounting: CAC liability decisions, financial reporting disputes
- ACPR/AMF: significant sanctions relevant to financial reporting

- [ ] **Step 2: Write decisions-cles.md**

Structure by domain, each decision with: court, date, reference number, short name, legal principle established, and significance.

Target: 30-50 key decisions.

- [ ] **Step 3: Commit decisions-cles.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/decisions-cles.md
git commit -m "feat: add decisions-cles.md — landmark decisions in accounting/tax/audit"
```

---

## Chunk 4: Domain reference files (Part 1 — Domains 1-4)

### Task 10: Create generale.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/generale.md`

- [ ] **Step 1: Research and write generale.md**

Follow the structure of legal-france domain files. Sections:

1. **Applicable texts** — PCG (Règl. ANC n° 2014-03), Code de commerce (Art. L. 123-12 to L. 123-28), directives comptables
2. **Key accounts** — Most important PCG accounts with numbers, labels, and usage rules
3. **Key rules** — Principles: image fidèle, prudence, permanence des méthodes, indépendance des exercices, intangibilité du bilan d'ouverture
4. **Journal entries patterns** — Common entry patterns (purchase, sale, payroll, depreciation, provision, closing)
5. **Financial statements** — Bilan (structure), Compte de résultat (structure), Annexe (required disclosures)
6. **Key ANC regulations** — Major regulations and their content

Use WebSearch to verify key article texts against Legifrance and ANC. Target: ~35-40 KB.

- [ ] **Step 2: Commit generale.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/generale.md
git commit -m "feat: add generale.md — general accounting reference (PCG, entries, financial statements)"
```

---

### Task 11: Create analytique.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/analytique.md`

- [ ] **Step 1: Research and write analytique.md**

Sections:
1. **Applicable framework** — PCG classe 9 (optional analytical accounts), ANC guidance
2. **Costing methods** — Coûts complets (full absorption), coûts variables, coûts directs, ABC (Activity-Based Costing), coûts standards
3. **Key concepts** — Centre d'analyse, unité d'œuvre, clé de répartition, charges directes/indirectes, charges fixes/variables
4. **Break-even analysis** — Seuil de rentabilité, point mort, marge sur coût variable, marge de sécurité
5. **Cost-volume-profit** — Formulas and methodology
6. **Inventory valuation** — CUMP, FIFO (PEPS), coût standard

Target: ~30-35 KB.

- [ ] **Step 2: Commit analytique.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/analytique.md
git commit -m "feat: add analytique.md — cost accounting reference (methods, analysis, break-even)"
```

---

### Task 12: Create ifrs.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/ifrs.md`

- [ ] **Step 1: Research and write ifrs.md**

Sections:
1. **Framework** — Cadre conceptuel IFRS, adoption UE (Règlement 1606/2002), ANC transposition
2. **Key standards** — For each major IAS/IFRS: number, title, scope, key principles, main differences with PCG
   - IAS 1 (Présentation des états financiers), IAS 2 (Stocks), IAS 7 (Tableau des flux), IAS 12 (Impôts sur le résultat), IAS 16 (Immobilisations corporelles), IAS 17→IFRS 16 (Contrats de location), IAS 19 (Avantages du personnel), IAS 36 (Dépréciation), IAS 37 (Provisions), IAS 38 (Immobilisations incorporelles), IFRS 3 (Regroupements d'entreprises), IFRS 9 (Instruments financiers), IFRS 10 (États financiers consolidés), IFRS 15 (Produits des activités ordinaires), IFRS 16 (Contrats de location)
3. **PCG ↔ IFRS conversion** — Main divergences table (fair value vs historical cost, lease treatment, provisions, goodwill amortization vs impairment)
4. **Consolidation** — Methods (intégration globale, proportionnelle, mise en équivalence), périmètre, goodwill, écarts d'évaluation

Use WebSearch on EUR-Lex to verify adopted IFRS standards. Target: ~40-45 KB.

- [ ] **Step 2: Commit ifrs.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/ifrs.md
git commit -m "feat: add ifrs.md — IFRS standards reference with PCG conversion guide"
```

---

### Task 13: Create finance.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/finance.md`

- [ ] **Step 1: Research and write finance.md**

Sections:
1. **Financial analysis framework** — Sources of data (bilan, CR, annexe, flux de trésorerie)
2. **SIG (Soldes Intermédiaires de Gestion)** — Complete cascade: marge commerciale → production de l'exercice → VA → EBE → résultat d'exploitation → résultat courant → résultat exceptionnel → résultat net. Formulas for each.
3. **Key ratios** — Table organized by category:
   - Liquidité: ratio de liquidité générale, réduite, immédiate
   - Solvabilité: taux d'endettement, autonomie financière, couverture des charges financières
   - Rentabilité: ROE, ROA, ROCE, marge nette, marge d'exploitation
   - Activité: rotation des stocks, délai clients, délai fournisseurs
4. **Working capital** — FR (Fonds de roulement), BFR (Besoin en fonds de roulement), Trésorerie nette. Formulas and interpretation.
5. **Cash flow** — CAF (Capacité d'autofinancement), tableau de flux (méthode directe/indirecte)
6. **Valuation** — DCF, multiples (PER, EV/EBITDA), patrimoniale (ANC, ANR)
7. **Business plan** — Structure, prévisionnel financier, plan de financement

Target: ~35-40 KB.

- [ ] **Step 2: Commit finance.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/finance.md
git commit -m "feat: add finance.md — corporate finance reference (SIG, ratios, BFR, valuation)"
```

---

## Chunk 5: Domain reference files (Part 2 — Domains 5-8)

### Task 14: Create fiscalite.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/fiscalite.md`

- [ ] **Step 1: Research and write fiscalite.md**

Sections:
1. **Applicable codes** — CGI, LPF (Livre des procédures fiscales), BOFiP references
2. **IS (Impôt sur les sociétés)** — Champ d'application, détermination du résultat fiscal (réintégrations, déductions), taux, paiement (acomptes, solde), Art. 209-I et seq. CGI
3. **TVA** — Champ (Art. 256+ CGI), taux, fait générateur, exigibilité, déduction, déclarations (CA3, CA12), régimes (réel normal, simplifié, franchise)
4. **CET (CFE + CVAE)** — Assiette, calcul, plafonnement VA
5. **Déficits fiscaux** — Report en avant (illimité, plafonné), report en arrière (carry-back), Art. 209-I al. 3 CGI
6. **Intégration fiscale** — Conditions, périmètre, détermination du résultat d'ensemble, Art. 223 A+ CGI
7. **Amortissements fiscaux** — Linéaire, dégressif, exceptionnel, suramortissement
8. **Provisions déductibles** — Conditions de déduction (Art. 39-1-5° CGI), provisions non déductibles

Use WebSearch on BOFiP and Legifrance to verify key articles. Target: ~38-42 KB.

- [ ] **Step 2: Commit fiscalite.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/fiscalite.md
git commit -m "feat: add fiscalite.md — corporate tax reference (IS, TVA, CET, deficits, integration)"
```

---

### Task 15: Create audit.md (reference)

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/audit.md`

- [ ] **Step 1: Research and write audit.md**

Sections:
1. **Legal framework** — Code de commerce (Art. L. 820-1+), loi de 2003, réforme de 2019 (loi PACTE)
2. **CAC mission** — Nomination, durée du mandat (6 exercices), incompatibilités, rotation
3. **NEP (Normes d'Exercice Professionnel)** — Key NEPs:
   - NEP 200 (Principes applicables), NEP 240 (Fraude), NEP 300 (Planification), NEP 315 (Risques), NEP 330 (Réponse aux risques), NEP 450 (Évaluation des anomalies), NEP 500 (Éléments probants), NEP 570 (Continuité d'exploitation), NEP 700 (Rapport)
4. **Audit opinions** — Certification sans réserve, avec réserve, refus de certifier, impossibilité de certifier
5. **Internal control** — COSO framework, référentiel AMF, contrôle interne comptable et financier
6. **CAC liability** — Responsabilité civile, pénale, disciplinaire
7. **Seuils d'audit** — Seuils de nomination obligatoire (post-loi PACTE)

Target: ~30-35 KB.

- [ ] **Step 2: Commit audit.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/audit.md
git commit -m "feat: add audit.md — statutory audit reference (CAC, NEP, internal control)"
```

---

### Task 16: Create controle-gestion.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/controle-gestion.md`

- [ ] **Step 1: Research and write controle-gestion.md**

Sections:
1. **Role and scope** — Distinction contrôle de gestion vs comptabilité analytique, place dans l'organisation
2. **Budgeting** — Budget commercial, production, approvisionnement, charges, trésorerie, investissement. Processus budgétaire.
3. **Variance analysis** — Écarts sur charges directes (quantité, prix), écarts sur charges indirectes (budget, activité, rendement), écart global
4. **Dashboards** — Tableau de bord prospectif (BSC: financial, customer, internal process, learning), indicateurs clés, construction
5. **Reporting** — Reporting financier, reporting de gestion, périodicité, consolidation de gestion
6. **Performance measurement** — EVA, ROI by division, prix de cession interne
7. **Forecasting** — Reprévision, rolling forecast, budget base zéro

Target: ~30-35 KB.

- [ ] **Step 2: Commit controle-gestion.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/controle-gestion.md
git commit -m "feat: add controle-gestion.md — management control reference (budgets, variances, dashboards)"
```

---

### Task 17: Create paie.md

**Files:**
- Create: `plugins/accounting-finance/skills/accounting-finance/references/paie.md`

- [ ] **Step 1: Research and write paie.md**

Sections:
1. **Legal framework** — Code du travail (Art. L. 3243-1+), mentions obligatoires du bulletin de paie
2. **Payslip structure** — Salaire brut, cotisations salariales, cotisations patronales, net imposable, net à payer, prélèvement à la source
3. **Social contributions detail** — Table by line: maladie, vieillesse plafonnée/déplafonnée, chômage, retraite complémentaire AGIRC-ARRCO, CSG/CRDS, prévoyance. For each: base, taux salarial, taux patronal, plafond.
4. **SMIC and thresholds** — SMIC horaire/mensuel, PASS, tranches de cotisations (T1, T2)
5. **Reduction générale** — RGDU (ex-réduction Fillon), calcul, coefficient
6. **DSN (Déclaration Sociale Nominative)** — Contenu, périodicité, événements déclarés
7. **Accounting entries for payroll** — Écritures types: salaires bruts (641), cotisations patronales (645), organismes sociaux (43), net à payer (421)

Use WebSearch on URSSAF to get current 2026 rates. Target: ~35-38 KB.

- [ ] **Step 2: Commit paie.md**

```bash
git add plugins/accounting-finance/skills/accounting-finance/references/paie.md
git commit -m "feat: add paie.md — payroll reference (payslip, contributions, DSN, accounting entries)"
```

---

## Chunk 6: Final assembly and README

### Task 18: Create README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README.md**

Follow the same bilingual (FR/EN) structure as the legal-france README.md. Include:
- Title and tagline (FR + EN)
- Installation command
- Commands table (9 commands with descriptions in FR + EN)
- User profiles section
- Response formats section
- Domains covered table (8 domains with reference file names)
- Cross-cutting references list
- Sources list with URLs
- Versions table (v1.0.0)
- Contributing section
- Disclaimer (FR + EN)
- License (MIT — Amine Harrak)

- [ ] **Step 2: Commit README.md**

```bash
git add README.md
git commit -m "docs: add bilingual README with v1.0 content"
```

---

### Task 19: Create CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write CLAUDE.md**

Same structure as the legal-france CLAUDE.md:
- Project overview
- Architecture (two layers: manifest + plugin content)
- Key design decisions
- Contributing guidance

- [ ] **Step 2: Commit CLAUDE.md**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md for future Claude Code sessions"
```

---

### Task 20: Final verification and push

- [ ] **Step 1: Verify file tree**

Run `find . -type f | grep -v .git | sort` and compare against the spec's file architecture (Section 6). Every file listed in the spec must exist.

Expected files:
```
.claude-plugin/marketplace.json
.gitignore
CLAUDE.md
LICENSE
README.md
plugins/accounting-finance/.claude-plugin/plugin.json
plugins/accounting-finance/commands/accounting.md
plugins/accounting-finance/commands/audit.md
plugins/accounting-finance/commands/corporate-finance.md
plugins/accounting-finance/commands/cost-accounting.md
plugins/accounting-finance/commands/general-accounting.md
plugins/accounting-finance/commands/ifrs.md
plugins/accounting-finance/commands/management-control.md
plugins/accounting-finance/commands/payroll.md
plugins/accounting-finance/commands/tax.md
plugins/accounting-finance/skills/accounting-finance/SKILL.md
plugins/accounting-finance/skills/accounting-finance/methodology.md
plugins/accounting-finance/skills/accounting-finance/references/analytique.md
plugins/accounting-finance/skills/accounting-finance/references/audit.md
plugins/accounting-finance/skills/accounting-finance/references/controle-gestion.md
plugins/accounting-finance/skills/accounting-finance/references/decisions-cles.md
plugins/accounting-finance/skills/accounting-finance/references/finance.md
plugins/accounting-finance/skills/accounting-finance/references/fiscalite.md
plugins/accounting-finance/skills/accounting-finance/references/generale.md
plugins/accounting-finance/skills/accounting-finance/references/glossaire.md
plugins/accounting-finance/skills/accounting-finance/references/ifrs.md
plugins/accounting-finance/skills/accounting-finance/references/paie.md
plugins/accounting-finance/skills/accounting-finance/references/pcg-index.md
plugins/accounting-finance/skills/accounting-finance/references/sources.md
plugins/accounting-finance/skills/accounting-finance/references/taux-baremes.md
```

- [ ] **Step 2: Verify plugin installs correctly**

```bash
claude plugin install .
```

- [ ] **Step 3: Push to remote**

```bash
git push -u origin main
```