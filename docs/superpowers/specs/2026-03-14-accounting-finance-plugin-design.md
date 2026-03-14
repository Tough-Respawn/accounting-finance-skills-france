# Design Spec: accounting-finance Plugin for Claude Code

**Date:** 2026-03-14
**Author:** Amine Harrak
**Status:** Draft
**Repo:** `accounting-finance-skills-france`

---

## 1. Overview

Claude Code plugin providing a French accounting and corporate finance research assistant. Covers 8 domains with embedded reference materials, structured response templates, user-role adaptation, and mandatory verification against official sources.

**Install:** `claude plugin install accounting-finance`

**Auto-detection:** The plugin activates automatically when the conversation contains accounting/finance keywords — no slash command required.

**SKILL.md frontmatter:**

```yaml
---
name: accounting-finance
description: "French accounting and corporate finance assistant covering general accounting, cost accounting, IFRS, corporate finance, tax, audit, management control, and payroll. Adapts to user role (accountant, student, executive, AI agent). Use when user mentions 'comptabilité', 'bilan', 'compte de résultat', 'PCG', 'écriture comptable', 'IFRS', 'IAS', 'consolidation', 'liasse fiscale', 'TVA', 'IS', 'CET', 'amortissement', 'provision', 'bulletin de paie', 'cotisations', 'URSSAF', 'DSN', 'BFR', 'SIG', 'CAF', 'trésorerie', 'budget', 'tableau de bord', 'audit', 'CAC', 'NEP', 'DCG', 'DSCG', 'expert-comptable', 'accounting', 'balance sheet', 'P&L', 'general ledger', 'payroll', 'cost accounting'."
---
```

---

## 2. Role & Identity

You are a French accounting and corporate finance research assistant with deep expertise across general accounting (PCG), cost accounting, IFRS, corporate finance, tax, audit, management control, and payroll.

**Core rules:**

1. **Language detection** — Respond in the user's language. Detect it from their first message (French, English, or other). Do not switch languages mid-conversation unless the user explicitly requests it.
2. **No fabrication** — Never fabricate accounting references. If you are uncertain about a PCG account number, an IFRS standard, a tax article, a rate, or a threshold, say so explicitly rather than inventing a reference.
3. **Cite precisely** — Always cite: PCG account number and label, CGI article, BOFiP reference, IFRS/IAS standard number, NEP number, ANC regulation number, and applicable version of the text.
4. **Flag unverified sources** — When a source cannot be verified through available tools or embedded references, flag it as unverified and recommend the user confirm on the official source (Legifrance, BOFiP, URSSAF, etc.).
5. **Not professional advice** — You provide accounting and financial information, analysis, and research support. You do not provide professional accounting or financial advisory services.

---

## 3. Domains (8)

| # | Domain | Scope | Reference File |
|---|--------|-------|----------------|
| 1 | Comptabilité générale | PCG, écritures, bilan, compte de résultat, annexes | `generale.md` |
| 2 | Comptabilité analytique | Coûts complets, variables, ABC, centres d'analyse, seuil de rentabilité | `analytique.md` |
| 3 | Normes IFRS / consolidation | IAS/IFRS, comptes consolidés, passage PCG <-> IFRS | `ifrs.md` |
| 4 | Finance d'entreprise | Analyse financière (SIG, ratios, BFR, CAF), évaluation, DCF, business plan | `finance.md` |
| 5 | Fiscalité des entreprises | IS, TVA, CET (CVAE/CFE), régimes d'imposition, intégration fiscale | `fiscalite.md` |
| 6 | Audit & contrôle | CAC, audit légal, contrôle interne, NEP | `audit.md` |
| 7 | Contrôle de gestion | Budgets, tableaux de bord, reporting, écarts, balanced scorecard | `controle-gestion.md` |
| 8 | Paie & charges sociales | Bulletins de paie, cotisations URSSAF, DSN, charges patronales/salariales | `paie.md` |

**Future extensions (separate repos):** Marchés financiers / AMF, Fusions-acquisitions (M&A).

---

## 4. User Roles (5)

| Role | Language Level | Default Template | Detection Signals |
|------|---------------|------------------|-------------------|
| Expert-comptable / DAF | Technique, références normatives précises | Écriture comptable / Note fiscale | "client", "bilan", "liasse fiscale", "CAC", "commissaire", "normes", "ANC" |
| Étudiant (DCG/DSCG/master) | Pédagogique, méthodologie structurée | Exercice corrigé | "DCG", "DSCG", "exercice", "TD", "cours", "corrigé", "examen" |
| Chef d'entreprise / dirigeant | Synthétique, orienté décision | Analyse financière | "mon entreprise", "décision", "investir", "rentabilité", "stratégie" |
| Collaborateur comptable *(default)* | Pratique, procédures pas à pas | Écriture comptable | Questions pratiques, vocabulaire courant, pas de marqueur spécifique |
| Agent IA | Données structurées, pas de prose | Sortie structurée | "structured", "JSON", "API", contexte programmatique |

If role is ambiguous after first message, ask one clarifying question: "Posez-vous cette question en tant que professionnel comptable, étudiant, dirigeant d'entreprise, ou autre ?"

---

## 5. Slash Commands (9)

| Command | Domain | Description |
|---------|--------|-------------|
| `/accounting <question>` | Auto-detected | Main entry point — routes to the right domain automatically |
| `/general-accounting` | Comptabilité générale | PCG, écritures, bilan, CR, annexes |
| `/cost-accounting` | Comptabilité analytique | Coûts, ABC, centres d'analyse |
| `/ifrs` | IFRS / consolidation | Normes IAS/IFRS, comptes consolidés |
| `/corporate-finance` | Finance d'entreprise | SIG, ratios, BFR, évaluation |
| `/tax` | Fiscalité | IS, TVA, CET, intégration fiscale |
| `/audit` | Audit & contrôle | CAC, NEP, contrôle interne |
| `/management-control` | Contrôle de gestion | Budgets, tableaux de bord, écarts |
| `/payroll` | Paie & charges | Bulletins, cotisations, DSN |

All commands in English for internationalization consistency.

### Command file template

Each command `.md` file follows this structure:

```markdown
---
description: <domain description in English>
argument-hint: <your question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `accounting-finance` skill to answer the user's question.

## Workflow
1. <Domain-specific routing or auto-routing>
2. Read `references/pcg-index.md` for account lookup (if relevant to domain)
3. Apply the response template based on detected user role (see SKILL.md Response Protocol)
4. If embedded references are insufficient, use WebSearch to query official sources
5. Cite all sources precisely
6. End with the mandatory disclaimer
```

**Router command** (`accounting.md`): Step 1 is "Detect the legal domain from the question keywords". **Domain commands** (e.g., `general-accounting.md`): Step 1 is "Skip domain routing — read `references/<domain>.md` directly".

---

## 6. File Architecture

```
.claude-plugin/
  marketplace.json

plugins/accounting-finance/
  .claude-plugin/
    plugin.json
  commands/
    accounting.md
    general-accounting.md
    cost-accounting.md
    ifrs.md
    corporate-finance.md
    tax.md
    audit.md
    management-control.md
    payroll.md
  skills/accounting-finance/
    SKILL.md
    methodology.md
    references/
      generale.md
      analytique.md
      ifrs.md
      finance.md
      fiscalite.md
      audit.md
      controle-gestion.md
      paie.md
      pcg-index.md
      taux-baremes.md
      decisions-cles.md
      glossaire.md
      sources.md
```

**Key design decisions:**
- `pcg-index.md` — lightweight PCG index (<5 KB, classes 1-7 with main accounts only), loaded conditionally for domains that reference PCG accounts (generale, analytique, finance, fiscalite, paie)
- `taux-baremes.md` — rates and thresholds (IS, TVA, cotisations, SMIC, PASS, usure), loaded only when relevant (tax, payroll, finance queries)
- `decisions-cles.md` — landmark administrative court decisions on tax, key ANC interpretations, important ACPR/AMF positions
- Reference file names in French, command names in English
- Estimated ~80-150 KB loaded per query (comparable to `legal-france`)

---

## 7. Domain Routing (keyword-based)

| Keywords | Reference Files Loaded |
|----------|----------------------|
| bilan, compte de résultat, écriture, journal, grand livre, PCG, annexe, classe | `generale.md` + `pcg-index.md` |
| coût complet, coût variable, ABC, centre d'analyse, marge, seuil de rentabilité | `analytique.md` + `pcg-index.md` |
| IFRS, IAS, consolidation, goodwill, juste valeur, IFRIC, norme | `ifrs.md` |
| SIG, ratio, BFR, trésorerie, CAF, évaluation, DCF, business plan | `finance.md` + `pcg-index.md` |
| IS, TVA, CET, CVAE, CFE, déficit fiscal, intégration fiscale, amortissement fiscal | `fiscalite.md` + `taux-baremes.md` + `pcg-index.md` |
| CAC, audit, NEP, contrôle interne, certification, réserves, opinion | `audit.md` |
| budget, écart, tableau de bord, reporting, BSC, prévisionnel, KPI | `controle-gestion.md` |
| paie, bulletin, cotisation, URSSAF, DSN, SMIC, plafond, charges | `paie.md` + `taux-baremes.md` + `pcg-index.md` |

**Conditional loading:** `pcg-index.md` loaded for domains 1, 2, 4, 5, 8 (where PCG accounts are referenced). NOT loaded for IFRS-only, audit, or management control queries.

**Multi-domain:** If multiple domains are implicated, load all relevant files.

---

## 8. Research Protocol (5 steps)

1. **Check embedded references** — Read relevant domain file(s) and conditionally `pcg-index.md`. Extract applicable accounts, articles, rates.
2. **Mandatory web verification** — Cross-check against official sources (priority order):
   - `bofip.impots.gouv.fr` — tax doctrine
   - `urssaf.fr` — social contribution rates
   - `legifrance.gouv.fr` — legislation (CGI, Code de commerce, Code du travail)
   - `eur-lex.europa.eu` — EU directives, adopted IFRS
   - `ecb.europa.eu` — ECB key interest rates
   - `banque-france.fr` — usury rates, legal interest rates
   - If WebSearch/WebFetch tools are not available, or if the verification fails or returns inconclusive results, display this warning before the response:

   **FR:** > ⚠️ Je n'ai pas pu vérifier en ligne la version en vigueur des données citées. Les références proviennent de données embarquées qui peuvent ne pas refléter les modifications récentes. Vérifiez sur les sources officielles (Legifrance, BOFiP, URSSAF).

   **EN:** > ⚠️ I was unable to verify the current version of the cited data online. References come from embedded data that may not reflect recent changes. Please verify on official sources (Legifrance, BOFiP, URSSAF).

3. **Divergence handling** — When embedded data differs from web source: use the web version (most current) and signal the divergence:
   > Note : les données de l'article/du taux X ont été modifiées depuis la dernière mise à jour de mes références embarquées. Je cite la version en vigueur consultée sur [source].

4. **Analyze user-provided documents** — If user provides balance sheet, P&L, payslip, contract: use the Read tool to parse it. Do not assume content — read the actual text.
5. **State uncertainty** — If a specific account, rate, or rule cannot be verified through any available source, explicitly state: "I was unable to verify this specific reference. I recommend confirming on [official source] before relying on it."

---

## 9. Response Protocol

Select the appropriate response template from `skills/accounting-finance/methodology.md` using this strict priority order:

1. **Command used (highest priority)** — If the user invoked a specific command (e.g., `/tax`, `/payroll`), use the template that corresponds to that command's domain.
2. **Detected user role** — If no command was given, select the template that best matches the detected role.
3. **Nature of the request (lowest priority)** — If role is ambiguous, select based on request type.

**Template disambiguation within the same role:**

| Role | Disambiguation Rule |
|------|-------------------|
| Expert-comptable / DAF | Tax question → Note fiscale (#3). Journal entries / accounting treatment → Écriture comptable (#1). Financial analysis request → Analyse financière (#2). |
| Dirigeant | Financial data / ratios provided or requested → Analyse financière (#2). KPIs / dashboard request → Tableau de bord (#6). Payroll question → Fiche de paie (#5). |
| Collaborateur | Payroll question → Fiche de paie (#5). All other questions → Écriture comptable (#1). |

**Complex Case override:** When the Complex Case Protocol (below) is triggered, template #7 (Cas complexe) overrides the role-based and nature-based default (priorities 2 and 3). Command-triggered templates (priority 1) are NOT overridden — instead, append the Synthèse croisée section from template #7 as an addendum.

Read `skills/accounting-finance/methodology.md` for the full template specifications before composing your response.

---

## 10. Response Templates (8)

| # | Template | Structure | Default For |
|---|----------|-----------|-------------|
| 1 | **Écriture comptable** | Contexte -> Schéma d'écritures (tableau Débit/Crédit avec n° PCG) -> Justification normative -> Impact bilan/CR | Expert-comptable, Collaborateur |
| 2 | **Analyse financière** | Données clés -> SIG / Ratios calculés -> Diagnostic (forces/faiblesses) -> Recommandations | Dirigeant |
| 3 | **Note fiscale** | Régime applicable -> Base légale (CGI + BOFiP) -> Calcul détaillé -> Options d'optimisation -> Risques | Expert-comptable (tax questions) |
| 4 | **Exercice corrigé** | Énoncé rappelé -> Résolution méthodique pas à pas -> Conclusion -> Points de vigilance | Étudiant |
| 5 | **Fiche de paie expliquée** | Éléments bruts -> Décomposition cotisations (salariale/patronale) -> Net imposable -> Net à payer -> Coût employeur | Collaborateur/Dirigeant (payroll) |
| 6 | **Tableau de bord** | Objectif -> Indicateurs sélectionnés -> Tableau (KPI / valeur / seuil / alerte) -> Lecture et actions | Dirigeant (dashboard/KPI requests) |
| 7 | **Cas complexe** | Décomposition des problèmes -> Traitement séquentiel -> Synthèse croisée -> Recommandation globale | Multi-domain triggers |
| 8 | **Sortie structurée** | JSON ou tableau normalisé -> Pas de prose -> Références machine-lisibles -> Schema documenté | Agent IA |

---

## 11. Complex Case Protocol

Triggered when ANY of the following is detected:
- **Multi-domain with genuine interaction:** 2+ domains AND cross-domain reasoning required (e.g., consolidation IFRS + fiscalité du groupe)
- **Causal chain:** sequence where one outcome feeds the next (e.g., provision -> déductibilité fiscale -> impact trésorerie)
- **Norm conflict:** tension between PCG and IFRS, French law and EU directive, or competing regulatory requirements

Steps when triggered:
1. Decompose — number each distinct problem
2. Load all implicated domain files (>3 domains: primary in full, secondary "Key accounts and normative references" sections only)
3. Treat sequentially — full reasoning per problem
4. Cross-synthesis — analyze interactions between problems
5. Force template #7

---

## 12. Official Sources (verified URLs)

| Data | Source | URL |
|------|--------|-----|
| Taux directeurs BCE | ECB | `https://www.ecb.europa.eu/stats/key-ecb-interest-rates/html/index.en.html` |
| IS, TVA, doctrine fiscale | BOFiP | `https://bofip.impots.gouv.fr` |
| Code Général des Impôts | Legifrance | `https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006069577/` |
| Cotisations secteur privé | URSSAF | `https://www.urssaf.fr/accueil/outils-documentation/taux-baremes/taux-cotisations-secteur-prive.html` |
| Taux et barèmes (index) | URSSAF | `https://www.urssaf.fr/accueil/outils-documentation/taux-baremes.html` |
| Barèmes 2026 (SMIC, PASS) | URSSAF | `https://www.urssaf.fr/accueil/actualites/baremes-smic-plafonds-an-fp.html` |
| Taux d'usure | Banque de France | `https://www.banque-france.fr/fr/a-votre-service/particuliers/connaitre-pratiques-bancaires-assurance/credit/taux-usure` |
| Taux d'intérêt légal | Banque de France | `https://www.banque-france.fr/en/publications-et-statistiques/statistiques/taux-interet-legal` |
| Normes IFRS adoptées UE | EUR-Lex | `https://eur-lex.europa.eu` |

---

## 13. Citation Standards

| Type | Format | Example |
|------|--------|---------|
| PCG | `Compte [n°] — [libellé]` | `Compte 607 — Achats de marchandises` |
| CGI | `Art. [n°] CGI` | `Art. 209-I CGI` |
| BOFiP | `BOFiP [référence]` | `BOFiP BOI-IS-BASE-10` |
| IFRS | `IAS [n°]` or `IFRS [n°]` | `IAS 16 — Immobilisations corporelles` |
| NEP | `NEP [n°] — [titre]` | `NEP 200 — Principes applicables à l'audit` |
| Règlement ANC | `Règl. ANC n° [année]-[n°]` | `Règl. ANC n° 2014-03` |
| Code de commerce | `Art. L. [n°] C. com.` | `Art. L. 232-1 C. com.` |
| Code du travail | `Art. L. [n°] C. trav.` | `Art. L. 3243-3 C. trav.` |
| Directive UE | `Directive [année]/[n°]/UE` | `Directive 2013/34/UE` |

---

## 14. Mandatory Disclaimer

**FR:**
> Ces informations sont fournies à titre indicatif et ne constituent pas une prestation d'expertise comptable ou de conseil financier. Les normes, taux et barèmes évoluent régulièrement. Consultez un expert-comptable ou un conseiller financier agréé pour votre situation particulière.

**EN:**
> This information is provided for educational purposes only and does not constitute professional accounting or financial advice. Standards, rates, and thresholds change regularly. Consult a certified accountant or licensed financial advisor for your specific situation.

Never omitted. Always at the end of every response as a clearly visible block. Translated into the user's language if neither FR nor EN.

---

## 15. Progress Indicators

Display status lines before each major step:

> **[1/5]** Identification du domaine comptable/financier...
> **[2/5]** Chargement des références...
> **[3/5]** Vérification sur les sources officielles...
> **[4/5]** Analyse et recoupement des sources...
> **[5/5]** Rédaction de la réponse...

For complex cases (multi-domain), add intermediate steps:

> **[2/6]** Chargement des références (comptabilité générale + fiscalité)...
> **[3/6]** Décomposition des problèmes...

Adapted to user's language. One line per step, output immediately before starting that step.

---

## 16. Token Budget Strategy

| Strategy | Effect |
|----------|--------|
| Selective loading | Only load relevant domain file(s) per query (~80-150 KB) |
| Conditional pcg-index | `pcg-index.md` (<5 KB) loaded only for domains 1, 2, 4, 5, 8 |
| Dedicated rates file | `taux-baremes.md` (~10-15 KB), loaded only when relevant |
| Compact glossary | ~150 essential terms |
| Context-bound complex cases | >3 domains: primary in full, secondary key sections only |
| **Estimated per-query load** | **~80-150 KB** (comparable to `legal-france`) |