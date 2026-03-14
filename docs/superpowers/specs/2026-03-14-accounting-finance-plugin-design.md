# Design Spec: accounting-finance Plugin for Claude Code

**Date:** 2026-03-14
**Author:** Amine Harrak
**Status:** Draft
**Repo:** `accounting-finance-skills-france`

---

## 1. Overview

Claude Code plugin providing a French accounting and corporate finance research assistant. Covers 8 domains with embedded reference materials, structured response templates, user-role adaptation, and mandatory verification against official sources.

**Install:** `claude plugin install accounting-finance`

**Auto-detection:** The plugin activates automatically when the conversation contains accounting/finance keywords (comptabilité, bilan, PCG, IFRS, TVA, IS, bulletin de paie, BFR, SIG, amortissement, budget, accounting, balance sheet, P&L, etc.) — no slash command required.

---

## 2. Domains (8)

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

## 3. User Roles (5)

| Role | Language Level | Default Template | Detection Signals |
|------|---------------|------------------|-------------------|
| Expert-comptable / DAF | Technique, références normatives précises | Écriture comptable / Note fiscale | "client", "bilan", "liasse fiscale", "CAC", "commissaire", "normes", "ANC" |
| Étudiant (DCG/DSCG/master) | Pédagogique, méthodologie structurée | Exercice corrigé | "DCG", "DSCG", "exercice", "TD", "cours", "corrigé", "examen" |
| Chef d'entreprise / dirigeant | Synthétique, orienté décision | Analyse financière | "mon entreprise", "décision", "investir", "rentabilité", "stratégie" |
| Collaborateur comptable *(default)* | Pratique, procédures pas à pas | Écriture comptable | Questions pratiques, vocabulaire courant, pas de marqueur spécifique |
| Agent IA | Données structurées, pas de prose | Sortie structurée | "structured", "JSON", "API", contexte programmatique |

If role is ambiguous after first message, ask one clarifying question.

---

## 4. Slash Commands (9)

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

---

## 5. File Architecture

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
      glossaire.md
      sources.md
```

**Key design decisions:**
- `pcg-index.md` — hierarchical PCG index (classes 1-7, main accounts), loaded with every query
- `taux-baremes.md` — rates and thresholds (IS, TVA, cotisations, SMIC, PASS, usure), loaded only when relevant (tax, payroll, finance queries)
- Reference file names in French, command names in English
- Estimated ~80-150 KB loaded per query (comparable to `legal-france`)

---

## 6. Domain Routing (keyword-based)

| Keywords | Reference Files Loaded |
|----------|----------------------|
| bilan, compte de résultat, écriture, journal, grand livre, PCG, annexe, classe | `generale.md` + `pcg-index.md` |
| coût complet, coût variable, ABC, centre d'analyse, marge, seuil de rentabilité | `analytique.md` |
| IFRS, IAS, consolidation, goodwill, juste valeur, IFRIC, norme | `ifrs.md` |
| SIG, ratio, BFR, trésorerie, CAF, évaluation, DCF, business plan | `finance.md` |
| IS, TVA, CET, CVAE, CFE, déficit fiscal, intégration fiscale, amortissement fiscal | `fiscalite.md` + `taux-baremes.md` |
| CAC, audit, NEP, contrôle interne, certification, réserves, opinion | `audit.md` |
| budget, écart, tableau de bord, reporting, BSC, prévisionnel, KPI | `controle-gestion.md` |
| paie, bulletin, cotisation, URSSAF, DSN, SMIC, plafond, charges | `paie.md` + `taux-baremes.md` |

**Always loaded:** `pcg-index.md` (every query).
**Multi-domain:** If multiple domains are implicated, load all relevant files.

---

## 7. Research Protocol (5 steps)

1. **Check embedded references** — Read `pcg-index.md` + relevant domain file(s). Extract applicable accounts, articles, rates.
2. **Mandatory web verification** — Cross-check against official sources (priority order):
   - `bofip.impots.gouv.fr` — tax doctrine
   - `urssaf.fr` — social contribution rates
   - `legifrance.gouv.fr` — legislation (CGI, Code de commerce, Code du travail)
   - `eur-lex.europa.eu` — EU directives, adopted IFRS
   - `ecb.europa.eu` — ECB key interest rates
   - `banque-france.fr` — usury rates, legal interest rates
   - If verification fails, display warning before response.
3. **Divergence handling** — When embedded data differs from web source: use web version (most current), signal the divergence.
4. **Analyze user-provided documents** — If user provides balance sheet, P&L, payslip, contract: read actual text, don't assume.
5. **State uncertainty** — If a specific account, rate, or rule cannot be verified, say so explicitly.

---

## 8. Response Templates (8)

| # | Template | Structure | Default For |
|---|----------|-----------|-------------|
| 1 | **Écriture comptable** | Contexte -> Schéma d'écritures (tableau Débit/Crédit avec n° PCG) -> Justification normative -> Impact bilan/CR | Expert-comptable, Collaborateur |
| 2 | **Analyse financière** | Données clés -> SIG / Ratios calculés -> Diagnostic (forces/faiblesses) -> Recommandations | Dirigeant |
| 3 | **Note fiscale** | Régime applicable -> Base légale (CGI + BOFiP) -> Calcul détaillé -> Options d'optimisation -> Risques | Expert-comptable |
| 4 | **Exercice corrigé** | Énoncé rappelé -> Résolution méthodique pas à pas -> Conclusion -> Points de vigilance | Étudiant |
| 5 | **Fiche de paie expliquée** | Éléments bruts -> Décomposition cotisations (salariale/patronale) -> Net imposable -> Net à payer -> Coût employeur | Collaborateur, Dirigeant |
| 6 | **Tableau de bord** | Objectif -> Indicateurs sélectionnés -> Tableau (KPI / valeur / seuil / alerte) -> Lecture et actions | Dirigeant |
| 7 | **Cas complexe** | Décomposition des problèmes -> Traitement séquentiel -> Synthèse croisée -> Recommandation globale | Multi-domain triggers |
| 8 | **Sortie structurée** | JSON ou tableau normalisé -> Pas de prose -> Références machine-lisibles -> Schema documenté | Agent IA |

**Template selection priority:**
1. Command used (highest)
2. Detected user role
3. Nature of request (lowest)

**Complex case override:** Template #7 overrides role/nature defaults. Does NOT override command-triggered templates — instead appends Synthèse croisée as addendum.

---

## 9. Complex Case Protocol

Triggered when ANY of the following is detected:
- **Multi-domain with genuine interaction:** 2+ domains AND cross-domain reasoning required (e.g., consolidation IFRS + fiscalité du groupe)
- **Causal chain:** sequence where one outcome feeds the next (e.g., provision -> déductibilité fiscale -> impact trésorerie)
- **Norm conflict:** tension between PCG and IFRS, French law and EU directive, or competing regulatory requirements

Steps when triggered:
1. Decompose — number each distinct problem
2. Load all implicated domain files (>3 domains: primary in full, secondary key sections only)
3. Treat sequentially — full reasoning per problem
4. Cross-synthesis — analyze interactions between problems
5. Force template #7

---

## 10. Official Sources (verified URLs)

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

## 11. Citation Standards

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

## 12. Mandatory Disclaimer

**FR:**
> Ces informations sont fournies à titre indicatif et ne constituent pas une prestation d'expertise comptable ou de conseil financier. Les normes, taux et barèmes évoluent régulièrement. Consultez un expert-comptable ou un conseiller financier agréé pour votre situation particulière.

**EN:**
> This information is provided for educational purposes only and does not constitute professional accounting or financial advice. Standards, rates, and thresholds change regularly. Consult a certified accountant or licensed financial advisor for your specific situation.

Never omitted. Always at the end of every response as a clearly visible block. Translated into the user's language if neither FR nor EN.

---

## 13. Progress Indicators

Display status lines before each major step:

> **[1/5]** Identification du domaine comptable/financier...
> **[2/5]** Chargement des références...
> **[3/5]** Vérification sur les sources officielles...
> **[4/5]** Analyse et recoupement des sources...
> **[5/5]** Rédaction de la réponse...

Adapted to user's language. One line per step, output immediately before starting that step.

---

## 14. Token Budget Strategy

| Strategy | Effect |
|----------|--------|
| Selective loading | Only load relevant domain + pcg-index per query (~80-150 KB) |
| Lightweight index | `pcg-index.md` = summary (classes 1-7, main accounts), not full 900-account PCG |
| Dedicated rates file | `taux-baremes.md` (~10-15 KB), loaded only when relevant |
| Compact glossary | ~150 essential terms |
| **Estimated per-query load** | **~80-150 KB** (comparable to `legal-france`) |