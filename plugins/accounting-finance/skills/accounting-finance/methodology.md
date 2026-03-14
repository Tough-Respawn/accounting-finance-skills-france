# Response Templates — accounting-finance

This file defines the eight structured response templates used by the accounting-finance skill. Each template includes trigger conditions, section structure, tone guidance, and an example skeleton. The template to use is selected by `SKILL.md`’s Response Protocol (command > role > request nature).

---

## Core Principle

The **rigueur comptable** (accounting rigor) is the backbone of all professional response formats:

- **Norme** — The applicable accounting/tax/financial standard (“Selon le PCG / l’art. X CGI / IAS Y...”)
- **Application** — The application to the specific situation (“En l’espèce, l’opération se traduit par...”)
- **Vérification** — The cross-check and impact assessment (“L’impact au bilan/CR est... La cohérence avec [norme] est vérifiée.”)

Every response must be anchored in normative references, with precise account numbers or article citations.

---

## Template 1 — Écriture comptable (Journal Entry)

**Trigger conditions:**
- User role is `expert-comptable` or `collaborateur`
- User invokes `/compta` (or any domain command) and role is detected as `expert-comptable` or `collaborateur`
- User describes a transaction and asks for the journal entry or accounting treatment
- Question requires identification of PCG accounts, debit/credit logic, and normative justification
- User mentions “écriture”, “comptabiliser”, “enregistrement”, “journal”, “OD”

**Tone:** Formal, precise, technical. Use PCG account numbers systematically. Reference the applicable PCG article, ANC regulation, or IFRS standard. Every entry must balance and be justified. No approximation — this is a professional working document.

**Section structure:**

### 1. Contexte de l’opération (Transaction Context)
Restate the transaction as described by the user, with accounting qualification. Identify the nature of the operation (purchase, sale, payroll, fixed asset, provision, etc.), the relevant parties, the applicable tax regime (TVA collectée, déductible, non-déductible), and any temporal considerations (exercice, rattachement, cut-off). Distinguish between the economic event and the accounting event if they differ.

### 2. Schéma d’écritures (Journal Entries)
Present the journal entries in a structured debit/credit table:

| Date | Compte | Libellé | Débit | Crédit |
|------|--------|---------|-------|--------|
| JJ/MM/AAAA | NNN — Intitulé PCG | Description | X,XX | |
| JJ/MM/AAAA | NNN — Intitulé PCG | Description | | X,XX |

Rules: always include the PCG account number and its official label. Show TVA on a separate line. If the entry spans multiple journals (achats, ventes, banque, OD), indicate which journal each entry belongs to. Group multi-line entries logically. The table must balance (total debits = total credits).

### 3. Justification normative (Normative Basis)
Cite the applicable accounting standard for each significant line:
- PCG article (e.g., art. 944-46 for account classification)
- ANC regulation (e.g., ANC 2014-03 for general accounting rules)
- CGI article for tax treatment (e.g., art. 271-I CGI for TVA deduction)
- IFRS/IAS if the entity reports under international standards

Explain the accounting principle at play: principe de prudence, rattachement des charges aux produits, non-compensation, coût historique, image fidèle. If there is a choice of method (e.g., composant vs. structure, amortissement linéaire vs. dégressif), state the options and their impact.

### 4. Impact bilan et compte de résultat (Financial Statement Impact)
Describe the effect of the entry on the balance sheet (actif/passif) and income statement (charges/produits). Specify which aggregates are affected: immobilisations, stocks, créances, dettes, trésorerie, capitaux propres. If the entry affects the résultat fiscal differently from the résultat comptable (e.g., réintégrations, déductions extra-comptables), note the divergence and the relevant CGI provision.

**Example skeleton:**

```
## Écriture comptable — Achat de marchandises

**Contexte de l’opération**
La société X, assujettie à la TVA (régime réel normal), achète des marchandises auprès du fournisseur Y pour un montant HT de 10 000 EUR, TVA 20 %. La facture est datée du 15/03/N. Règlement à 30 jours.

**Schéma d’écritures**

Journal : Achats

| Date | Compte | Libellé | Débit | Crédit |
|------|--------|---------|-------|--------|
| 15/03/N | 607 — Achats de marchandises | Fact. Y n° 2024-001 | 10 000,00 | |
| 15/03/N | 44566 — TVA déductible sur ABS | TVA 20 % | 2 000,00 | |
| 15/03/N | 401 — Fournisseurs | Fournisseur Y | | 12 000,00 |

**Total : 12 000,00 = 12 000,00** ✓

**Justification normative**
- Compte 607 : art. 946-60 PCG, charges d’exploitation — achats de marchandises destinées à la revente en l’état.
- Compte 44566 : art. 271-I CGI — la TVA sur achats de biens est déductible dès lors que le bien est affecté à une opération taxable.
- Compte 401 : dette fournisseur constatée à la date de réception de la facture (art. 944-40 PCG).
- Règle ANC 2014-03, art. 512-2 : les charges sont comptabilisées à la date du fait générateur.

**Impact bilan/CR**
- Bilan : Actif — augmentation du poste “Créances fiscales” (TVA déductible) de 2 000 EUR. Passif — augmentation du poste “Dettes fournisseurs” de 12 000 EUR.
- Compte de résultat : Charge d’exploitation de 10 000 EUR (diminution du résultat d’exploitation).
- Résultat fiscal : pas de divergence — la charge est déductible fiscalement à l’exercice de rattachement (art. 39-1-1° CGI).
```

---

## Template 2 — Analyse financière (Financial Analysis)

**Trigger conditions:**
- User role is `dirigeant`, `DAF`, or `analyste`
- User invokes `/finance` and the request involves diagnostic, ratios, or financial health
- User provides financial data (bilan, compte de résultat, liasse fiscale) and asks for interpretation
- User mentions “analyse financière”, “diagnostic”, “SIG”, “soldes intermédiaires”, “ratios”, “rentabilité”
- Question requires computation and interpretation of financial indicators

**Tone:** Professional, analytical, decision-oriented. Present numbers in structured tables. Interpret every ratio — never present a ratio without commentary. Be direct about weaknesses. Recommendations must be actionable with concrete levers. Use formal financial vocabulary but avoid unnecessary jargon when the user is not a finance specialist.

**Section structure:**

### 1. Données clés (Key Data)
Summarize the financial data provided or extracted. Present in a compact table:
- Chiffre d’affaires HT (revenue)
- Résultat d’exploitation, résultat courant, résultat net
- Total bilan (balance sheet total)
- Capitaux propres, endettement financier net
- Effectif moyen, secteur d’activité

If data is missing, explicitly note what is absent and how it limits the analysis. If comparative data (N-1, N-2) is available, include it for trend analysis.

### 2. Soldes Intermédiaires de Gestion — SIG (Intermediate Management Balances)
Present the full SIG cascade in a table:

| SIG | Montant N | Montant N-1 | Variation | % CA |
|-----|-----------|-------------|-----------|------|
| Marge commerciale | | | | |
| Production de l’exercice | | | | |
| Valeur ajoutée | | | | |
| EBE (EBITDA) | | | | |
| Résultat d’exploitation | | | | |
| Résultat courant avant impôts | | | | |
| Résultat exceptionnel | | | | |
| Résultat net | | | | |

For each SIG, provide a one-line interpretation: “La valeur ajoutée représente X % du CA, en progression de Y points, ce qui traduit une amélioration de l’efficacité productive.”

### 3. Ratios significatifs (Key Ratios)
Present ratios grouped by category, with formula, value, benchmark, and interpretation:

**Rentabilité :**
- Rentabilité économique (ROCE) = Résultat d’exploitation / Capitaux engagés
- Rentabilité financière (ROE) = Résultat net / Capitaux propres
- Marge nette = Résultat net / CA HT

**Structure financière :**
- Ratio d’endettement = Dettes financières / Capitaux propres
- Capacité d’autofinancement (CAF)
- Ratio de solvabilité = Capitaux propres / Total bilan

**Liquidité :**
- Fonds de roulement (FR) = Ressources stables — Emplois stables
- Besoin en fonds de roulement (BFR)
- Trésorerie nette = FR — BFR

**Activité :**
- Délai de rotation des stocks (jours)
- Délai de règlement clients (jours)
- Délai de règlement fournisseurs (jours)

For each ratio: state the formula, compute the value, compare to sector benchmarks or N-1, and interpret the result.

### 4. Diagnostic forces / faiblesses (Strengths / Weaknesses Assessment)
Structured SWOT-style assessment, limited to financial dimensions:
- **Forces :** what the numbers show is going well (e.g., strong EBE margin, improving BFR)
- **Faiblesses :** what is concerning (e.g., deteriorating solvency, negative trésorerie)
- **Points de vigilance :** risks not yet materialized but visible in trends (e.g., rising client payment delays)

### 5. Recommandations (Recommendations)
Concrete, prioritized action plan:
- For each recommendation: what to do, expected financial impact, timeline, and level of urgency
- Link recommendations to specific weaknesses identified in section 4
- Distinguish between short-term corrective actions and medium-term strategic initiatives

**Example skeleton:**

```
## Analyse financière — Société Z (exercice N)

**Données clés**

| Élément | N | N-1 | Variation |
|---------|---|-----|-----------|
| CA HT | 5 200 000 | 4 800 000 | +8,3 % |
| Résultat d’exploitation | 390 000 | 310 000 | +25,8 % |
| Résultat net | 245 000 | 195 000 | +25,6 % |
| Capitaux propres | 1 200 000 | 1 050 000 | +14,3 % |
| Endettement financier net | 800 000 | 900 000 | -11,1 % |

**Soldes Intermédiaires de Gestion**

| SIG | N | N-1 | Var. | % CA |
|-----|---|-----|------|------|
| Marge commerciale | 2 080 000 | 1 872 000 | +11,1 % | 40,0 % |
| Valeur ajoutée | 1 560 000 | 1 392 000 | +12,1 % | 30,0 % |
| EBE | 624 000 | 528 000 | +18,2 % | 12,0 % |
| Résultat d’exploitation | 390 000 | 310 000 | +25,8 % | 7,5 % |
| Résultat net | 245 000 | 195 000 | +25,6 % | 4,7 % |

L’EBE progresse de 18,2 %, signe d’une amélioration opérationnelle supérieure à la croissance du CA...

**Ratios significatifs**

| Ratio | Formule | Valeur N | Valeur N-1 | Interprétation |
|-------|---------|----------|------------|----------------|
| ROE | RN / CP | 20,4 % | 18,6 % | Rentabilité financière en hausse, supérieure au coût du capital estimé |
| ROCE | Rex / CE | 19,5 % | 16,3 % | Amélioration de l’efficacité des capitaux engagés |
| Endettement | DF / CP | 66,7 % | 85,7 % | Désendettement significatif, structure plus saine |
| Trésorerie nette | FR - BFR | +120 000 | -50 000 | Retour à une trésorerie positive |

**Diagnostic**
Forces : Croissance rentable, désendettement rapide, trésorerie restaurée.
Faiblesses : Marge nette encore faible (4,7 %), dépendance à un client > 30 % du CA.
Vigilance : Délai client en augmentation (52 j. vs 45 j. en N-1).

**Recommandations**
1. Réduire le délai client : mettre en place une relance systématique à J+30, objectif 45 jours — impact trésorerie estimé +80 000 EUR. Urgence : haute.
2. Diversifier le portefeuille clients : lancer une prospection commerciale pour réduire la dépendance au client principal sous 20 %. Horizon : 12 mois.
3. Améliorer la marge nette : analyser les charges exceptionnelles et financières pour identifier des leviers de réduction. Horizon : 6 mois.
```

---

## Template 3 — Note fiscale (Tax Memorandum)

**Trigger conditions:**
- User role is `expert-comptable`, `fiscaliste`, or `DAF`
- User invokes `/fiscal` or `/impôts` and asks a tax question
- Question involves corporate tax (IS), VAT (TVA), CET (CFE/CVAE), income tax (IR), or specific tax regime
- User mentions “IS”, “TVA”, “CGI”, “BOFiP”, “optimisation fiscale”, “plus-value”, “déficit”, “intégration fiscale”, “crédit d’impôt”
- Question requires identifying the applicable tax regime, computing a tax liability, or evaluating tax options

**Tone:** Rigorous, systematic, risk-aware. Tax advice must be anchored in CGI articles and BOFiP references. Present options objectively with associated risks. Distinguish clearly between legal optimization and aggressive positions. Flag any area where the tax administration’s interpretation differs from taxpayer-favorable readings.

**Section structure:**

### 1. Régime applicable (Applicable Tax Regime)
Identify the tax at issue and the applicable regime. State the taxpayer’s status (assujetti TVA, redevable IS, etc.), the applicable rate or regime (régime réel, micro, simplifié), and any relevant exemptions or special regimes (ZFU, JEI, régime mère-fille, etc.). If the question involves multiple taxes, treat each one.

### 2. Base légale (Legal Basis)
Cite the relevant legal sources in hierarchical order:
- **CGI articles** (primary legal source): full article reference with paragraph and alinéa
- **Annexes CGI** (regulatory details): relevant annexe provisions
- **BOFiP references** (administrative doctrine): BOI reference number, paragraph, date of last update
- **Jurisprudence fiscale** (tax case law): CE (Conseil d’État) or CAA decisions, with date and decision number
- **Doctrine administrative** (rescrits, réponses ministérielles): if applicable

For each source, state its legal authority: loi > règlement > doctrine administrative (opposable under art. L. 80 A LPF).

### 3. Calcul détaillé (Detailed Computation)
Present the tax computation step by step, showing all intermediate calculations:
- Base imposable (taxable base): how it is determined, what is included/excluded
- Deductions and abatements: applicable deductions with legal basis
- Taux applicable (applicable rate): standard rate, reduced rate, progressive scale
- Crédits d’impôt: applicable credits with conditions and caps
- Impôt dû (tax due): final amount

Use a clear computational layout. Show formulas. If multiple scenarios exist, compute each one.

### 4. Options d’optimisation (Optimization Options)
Present legally available tax planning options:
- For each option: description, legal basis, conditions, expected tax savings, implementation steps
- Compare options in a summary table
- Note any option that requires prior approval (agrément, rescrit) or declaration

### 5. Risques et contentieux (Risks and Disputes)
Flag potential tax risks:
- Positions that the tax administration might challenge (with reference to BOFiP contrary positions)
- Risk of reclassification (abus de droit, acte anormal de gestion)
- Applicable penalties (art. 1728, 1729 CGI) and interest (art. 1727 CGI)
- Prescription periods (art. L. 169 et seq. LPF)
- Any pending legislative changes that could affect the analysis

### 6. Délais et obligations déclaratives (Deadlines and Filing Requirements)
List all relevant deadlines:
- Filing dates (déclarations, paiements, acomptes)
- Option exercise deadlines
- Statute of limitations
- Specific notification or documentation requirements

**Example skeleton:**

```
## Note fiscale — Calcul de l’IS (exercice N)

**Régime applicable**
La société A, SA au capital de 500 000 EUR, est soumise à l’IS de droit commun (art. 205 CGI). Elle ne bénéficie pas du taux réduit PME (CA > 10 M EUR). Exercice clos le 31/12/N.

**Base légale**
- Art. 209-I CGI : détermination du bénéfice imposable à l’IS — “les bénéfices passibles de l’impôt sur les sociétés sont déterminés en tenant compte uniquement des bénéfices réalisés dans les entreprises exploitées en France...”
- Art. 39-1 CGI : charges déductibles — les charges sont admises en déduction du bénéfice net à condition d’être engagées dans l’intérêt direct de l’exploitation.
- Art. 219-I CGI : taux de l’IS — taux normal de 25 % pour les exercices ouverts à compter du 1er janvier 2022.
- BOI-IS-BASE-10 : commentaires administratifs sur la détermination du résultat fiscal.
- CE, 30/12/2003, n° 233894, SA Andritz : sur la déductibilité des provisions pour risques.

**Calcul détaillé**
Résultat comptable avant impôt : 800 000 EUR
(+) Réintégrations extra-comptables :
  - Amende pénale non déductible (art. 39-2 CGI) : +15 000
  - Amortissement excédentaire véhicule (art. 39-4 CGI, plafond 18 300 EUR) : +5 200
(-) Déductions extra-comptables :
  - Produit de participation mère-fille (art. 216 CGI) : -50 000 (quote-part de frais de 5 % réintégrée : +2 500)
Résultat fiscal : 772 700 EUR
IS dû (25 %) : 193 175 EUR

**Options d’optimisation**
1. Suramortissement : vérifier si des investissements de l’exercice sont éligibles au suramortissement (art. 39 decies CGI) — économie potentielle estimée selon actifs concernés.
2. Crédit d’impôt recherche (CIR) : si des dépenses de R&D sont engagées, le CIR (art. 244 quater B CGI) permettrait un crédit de 30 % sur les dépenses éligibles.
3. Report de déficits antérieurs : vérifier l’existence de déficits reportables (art. 209-I al. 3 CGI, plafond 1 M EUR + 50 % au-delà).

**Risques**
- La provision pour risques de 120 000 EUR pourrait être contestée si le fait générateur n’est pas suffisamment probable (CE, 30/12/2003, Andritz).
- La requalification de la convention d’assistance avec la filiale étrangère en acte anormal de gestion (art. 57 CGI, prix de transfert) n’est pas exclue si le prix n’est pas conforme au principe de pleine concurrence.
- Pénalité applicable en cas de rectification : 40 % pour manquement délibéré (art. 1729-a CGI).

**Délais**
- Déclaration de résultat (liasse fiscale) : dans les 3 mois de la clôture, soit le 31/03/N+1 (art. 223-1 CGI).
- Solde d’IS : au plus tard le 15/05/N+1 (art. 1668-1 CGI).
- Prescription : droit de reprise de l’administration jusqu’au 31/12/N+3 (art. L. 169 LPF).
```

---

## Template 4 — Exercice corrigé (Corrected Exercise)

**Trigger conditions:**
- User role is `étudiant` (student)
- User invokes `/compta` or `/finance` and role is detected as `étudiant`
- User describes an exercise, problem set, or case study and asks for the solution
- User mentions “exercice”, “TD”, “partiel”, “examen”, “correction”, “corrigé”, “calculer”
- Question involves applying a formula, method, or accounting rule to given data

**Tone:** Pedagogical, methodical, encouraging. Show every reasoning step explicitly — never skip intermediate calculations. Explain the “why” behind each step, not just the “how.” Use clear variable naming. The student must be able to reproduce the method on a different set of numbers. Flag common mistakes and traps at the end.

**Section structure:**

### 1. Énoncé rappelé (Problem Restated)
Restate the exercise in a clean, structured format. Extract the given data into a summary (table or bullet list). Identify the question(s) to answer. If the problem statement is ambiguous, note the interpretation chosen and why.

### 2. Résolution pas à pas (Step-by-Step Solution)
For each question or sub-question, solve methodically:
- **Étape 1 :** State the formula or rule to apply. Cite the source (PCG, manual, financial theory).
- **Étape 2 :** Substitute the given values into the formula. Show the numerical substitution explicitly.
- **Étape 3 :** Compute the result. Show intermediate calculations when the formula involves multiple steps.
- **Étape 4 :** Interpret the result in context (“Ce ratio signifie que l’entreprise dispose de X EUR de marge de sécurité...”).

Number each step clearly. If a later step depends on an earlier result, reference it explicitly (“En reprenant le résultat de l’étape 2...”).

### 3. Conclusion (Summary of Results)
Present all final answers in a compact summary table or list. Restate the key results with their units. Provide a one-paragraph synthesis: what does the overall result tell us about the situation?

### 4. Points de vigilance (Common Pitfalls)
List 3-5 common mistakes students make on this type of exercise:
- Typical calculation errors (e.g., confusing HT and TTC, forgetting to annualize a rate)
- Conceptual confusions (e.g., confusing charges fixes and charges variables)
- Methodological traps (e.g., applying a formula outside its validity conditions)
- Presentation errors (e.g., missing units, insufficient decimal places)

For each pitfall: state the mistake, explain why it is wrong, and give the correct approach.

**Example skeleton:**

```
## Exercice corrigé — Seuil de rentabilité

**Énoncé rappelé**
La société ABC présente les données suivantes pour l’exercice N :
- Chiffre d’affaires : 500 000 EUR
- Charges variables : 300 000 EUR
- Charges fixes : 150 000 EUR

Questions :
1. Calculer la marge sur coût variable (MCV) et le taux de MCV.
2. Déterminer le seuil de rentabilité (SR) en valeur et en volume.
3. Calculer le point mort (date d’atteinte du SR) en supposant un CA régulier.
4. Déterminer la marge de sécurité et l’indice de sécurité.

**Résolution pas à pas**

*Question 1 — Marge sur coût variable*
Étape 1 : MCV = CA - Charges variables
Étape 2 : MCV = 500 000 - 300 000
Étape 3 : **MCV = 200 000 EUR**
Taux de MCV = MCV / CA = 200 000 / 500 000 = **0,40 soit 40 %**
Interprétation : sur chaque euro de CA, 40 centimes contribuent à couvrir les charges fixes puis à générer du bénéfice.

*Question 2 — Seuil de rentabilité*
Étape 1 : SR = Charges fixes / Taux de MCV (formule du point d’équilibre où RN = 0)
Étape 2 : SR = 150 000 / 0,40
Étape 3 : **SR = 375 000 EUR**
Interprétation : l’entreprise doit réaliser 375 000 EUR de CA pour couvrir l’ensemble de ses charges. Au-delà, chaque euro supplémentaire génère du profit.

*Question 3 — Point mort*
Étape 1 : Point mort = (SR / CA) × 365 jours
Étape 2 : (375 000 / 500 000) × 365
Étape 3 : **Point mort = 273,75 jours soit environ le 1er octobre de l’exercice N**
Interprétation : le SR est atteint début octobre ; l’entreprise dispose de 3 mois de marge.

*Question 4 — Marge et indice de sécurité*
Marge de sécurité = CA - SR = 500 000 - 375 000 = **125 000 EUR**
Indice de sécurité = Marge de sécurité / CA = 125 000 / 500 000 = **0,25 soit 25 %**
Interprétation : le CA peut baisser de 25 % avant que l’entreprise ne devienne déficitaire.

**Conclusion**

| Indicateur | Valeur |
|------------|--------|
| MCV | 200 000 EUR |
| Taux de MCV | 40 % |
| Seuil de rentabilité | 375 000 EUR |
| Point mort | 1er octobre (274e jour) |
| Marge de sécurité | 125 000 EUR |
| Indice de sécurité | 25 % |

L’entreprise ABC est rentable avec une marge de sécurité confortable de 25 %. La structure de coûts (60 % variable, 30 % fixe) est équilibrée.

**Points de vigilance**
1. Ne pas confondre charges fixes et charges variables : un loyer est fixe même si l’activité varie ; les matières premières sont variables.
2. Le taux de MCV doit être calculé sur le CA HT, jamais TTC — sinon le SR est faussé.
3. Le point mort suppose un CA linéaire sur l’année. Si l’activité est saisonnière, il faut recalculer mois par mois.
4. Ne pas oublier les unités : le SR est en euros (pas en quantités sauf si le prix unitaire est connu).
5. L’indice de sécurité s’exprime en pourcentage — ne pas le confondre avec la marge de sécurité (en valeur absolue).
```

---

## Template 5 — Fiche de paie expliquée (Payslip Breakdown)

**Trigger conditions:**
- User asks about payroll, payslip, cotisations sociales, net à payer, coût employeur
- User invokes `/paie` or `/social` and the request involves salary computation
- User role is `expert-comptable`, `collaborateur`, `RH`, or `salarié`
- User mentions “bulletin de paie”, “fiche de paie”, “cotisations”, “net imposable”, “net à payer”, “Urssaf”, “charges patronales”, “charges salariales”
- Question requires decomposing gross salary into net salary through social contributions

**Tone:** Precise, systematic, exhaustive. Every contribution line must be identified with its rate, base, and regulatory reference. Use the official Urssaf contribution names and rates. Distinguish clearly between employee and employer contributions. The result must be verifiable against an actual payslip. For non-specialist users (role `salarié`), add plain-language explanations of what each line means.

**Section structure:**

### 1. Éléments bruts (Gross Salary Components)
Decompose the gross salary:
- Salaire de base (basic salary): monthly rate or hourly rate × hours
- Heures supplémentaires: number of hours, rate of increase (25 %, 50 %), legal basis (art. L. 3121-22 C. trav.)
- Primes: nature (ancienneté, 13e mois, performance), base, taxability
- Avantages en nature: valuation (real or forfaitaire), social contribution base

State the total brut (gross total) which serves as the base for most contributions.

### 2. Cotisations salariales (Employee Contributions)
Present each employee contribution on a separate line:

| Cotisation | Base | Taux | Montant | Référence |
|------------|------|------|---------|-----------|
| Sécurité sociale — Maladie | Totalité | 0,00 % | 0,00 | art. L. 241-1 CSS |
| Sécurité sociale — Vieillesse plafonnée | Tranche 1 | 6,90 % | ... | art. L. 241-3 CSS |
| Sécurité sociale — Vieillesse déplafonnée | Totalité | 0,40 % | ... | art. L. 241-3 CSS |
| CSG déductible | 98,25 % du brut | 6,80 % | ... | art. L. 136-1-1 CSS |
| CSG non déductible + CRDS | 98,25 % du brut | 2,90 % | ... | art. L. 136-8 CSS |
| Retraite complémentaire (Agirc-Arrco) T1 | Tranche 1 | 3,15 % | ... | ANI Agirc-Arrco |
| Retraite complémentaire T2 | Tranche 2 | 8,64 % | ... | ANI Agirc-Arrco |
| Assurance chômage | Totalité (plafond 4 PMSS) | 0,00 % | 0,00 | depuis 01/10/2018 |

State the total des cotisations salariales.

### 3. Cotisations patronales (Employer Contributions)
Present each employer contribution:

| Cotisation | Base | Taux | Montant | Référence |
|------------|------|------|---------|-----------|
| Sécurité sociale — Maladie | Totalité | 7,00 % (ou 13 %) | ... | art. L. 241-1 CSS |
| Sécurité sociale — Vieillesse plafonnée | Tranche 1 | 8,55 % | ... | art. L. 241-3 CSS |
| Sécurité sociale — Vieillesse déplafonnée | Totalité | 2,02 % | ... | art. L. 241-3 CSS |
| Allocations familiales | Totalité | 3,45 % (ou 5,25 %) | ... | art. L. 241-6-1 CSS |
| Assurance chômage | Totalité (plafond 4 PMSS) | 4,05 % | ... | Unédic |
| AGS | Totalité (plafond 4 PMSS) | 0,20 % | ... | art. L. 3253-18 C. trav. |
| Retraite complémentaire T1 | Tranche 1 | 4,72 % | ... | ANI Agirc-Arrco |
| Accidents du travail | Totalité | Variable | ... | art. L. 241-5 CSS |
| Réduction Fillon (si applicable) | | | (-...) | art. L. 241-13 CSS |

State the total des cotisations patronales.

### 4. Net imposable (Taxable Net Income)
Compute: Brut - Cotisations salariales (hors CSG non déductible et CRDS) + CSG non déductible + CRDS + Part patronale mutuelle.
Explain why the net imposable differs from the net à payer. State the net imposable which is reported on the déclaration de revenus.

### 5. Net à payer (Take-Home Pay)
Compute: Brut - Total cotisations salariales = Net à payer avant PAS.
Apply the prélèvement à la source (PAS) if the taux is known:
Net à payer après PAS = Net avant PAS - PAS.
This is the amount actually received by the employee.

### 6. Coût employeur (Total Employer Cost)
Compute: Brut + Total cotisations patronales = Coût total employeur.
Express as a ratio of the net à payer: “Pour 1 EUR versé au salarié, l’employeur débourse X,XX EUR au total.”
Note any applicable exonérations (réduction Fillon, exonération ZRR, aide à l’embauche) that reduce the cost.

**Example skeleton:**

```
## Fiche de paie expliquée — Cadre, salaire brut 3 500 EUR

**Éléments bruts**
- Salaire de base : 3 500,00 EUR (151,67 h × 23,08 EUR/h)
- Heures supplémentaires : néant
- Primes : néant
- Avantages en nature : néant
- **Total brut : 3 500,00 EUR**

Plafond de la Sécurité sociale (PMSS) mensuel : 3 864 EUR (2025)
Tranche 1 : de 0 à 3 864 EUR → base T1 = 3 500,00 EUR
Tranche 2 : de 3 864 à 30 912 EUR → base T2 = 0,00 EUR (brut < PMSS)

**Cotisations salariales**

| Cotisation | Base | Taux | Montant |
|------------|------|------|---------|
| SS Vieillesse plafonnée | 3 500,00 | 6,90 % | 241,50 |
| SS Vieillesse déplafonnée | 3 500,00 | 0,40 % | 14,00 |
| Retraite Agirc-Arrco T1 | 3 500,00 | 3,15 % | 110,25 |
| CEG T1 | 3 500,00 | 0,86 % | 30,10 |
| CSG déductible | 3 438,75 | 6,80 % | 233,84 |
| CSG + CRDS non déductible | 3 438,75 | 2,90 % | 99,72 |
| **Total cotisations salariales** | | | **729,41** |

**Cotisations patronales**

| Cotisation | Base | Taux | Montant |
|------------|------|------|---------|
| SS Maladie | 3 500,00 | 7,00 % | 245,00 |
| SS Vieillesse plafonnée | 3 500,00 | 8,55 % | 299,25 |
| SS Vieillesse déplafonnée | 3 500,00 | 2,02 % | 70,70 |
| Allocations familiales | 3 500,00 | 3,45 % | 120,75 |
| Chômage | 3 500,00 | 4,05 % | 141,75 |
| AGS | 3 500,00 | 0,20 % | 7,00 |
| Retraite Agirc-Arrco T1 | 3 500,00 | 4,72 % | 165,20 |
| CEG T1 | 3 500,00 | 1,29 % | 45,15 |
| AT/MP | 3 500,00 | 1,10 % | 38,50 |
| **Total cotisations patronales** | | | **1 133,30** |

**Net imposable**
Brut (3 500,00) - Cotisations salariales hors CSG/CRDS non déd. (629,69) + CSG/CRDS non déductible (99,72) = **2 970,03 EUR**

**Net à payer**
Brut (3 500,00) - Total cotisations salariales (729,41) = **2 770,59 EUR** (avant PAS)
PAS (taux 7,5 %) : 2 770,59 × 7,5 % = 207,79 EUR
**Net à payer après PAS : 2 562,80 EUR**

**Coût employeur**
Brut (3 500,00) + Cotisations patronales (1 133,30) = **4 633,30 EUR**
Ratio : pour 1 EUR net versé au salarié, l’employeur débourse 1,67 EUR au total.
```

---

## Template 6 — Tableau de bord (Dashboard / KPI Report)

**Trigger conditions:**
- User role is `dirigeant`, `DAF`, or `contrôleur-de-gestion`
- User invokes `/gestion` or `/pilotage` and requests a dashboard, KPIs, or performance indicators
- User mentions “tableau de bord”, “KPI”, “indicateurs”, “pilotage”, “reporting”, “balanced scorecard”
- Question requires defining, computing, or interpreting performance metrics for management decision-making

**Tone:** Concise, action-oriented, visual. The dashboard must be scannable — a manager should grasp the situation in 30 seconds. Use tables as the primary format. Color-code alerts (textual: VERT/ORANGE/ROUGE or symbols). Minimize prose — every word must earn its place. Recommendations must be directly tied to alert states.

**Section structure:**

### 1. Objectif du tableau de bord (Dashboard Purpose)
State the management objective this dashboard serves. Identify the decision-maker (DG, DAF, responsable de BU), the reporting period (mensuel, trimestriel), and the scope (entire company, business unit, project). Specify the strategic or operational question the dashboard answers.

### 2. Indicateurs (KPI Table)
Present the KPIs in a single structured table:

| KPI | Formule | Valeur actuelle | Objectif / Seuil | Écart | Alerte |
|-----|---------|-----------------|-------------------|-------|--------|
| [Nom du KPI] | [Formule de calcul] | [Valeur] | [Cible ou seuil] | [+/- %] | VERT / ORANGE / ROUGE |

For each KPI:
- **Formule :** the exact computation formula, with variable names matching the available data
- **Valeur actuelle :** the current period’s computed value
- **Objectif / Seuil :** the target or threshold value, with source (budget, N-1, benchmark sectoriel)
- **Écart :** deviation from target, in absolute and percentage terms
- **Alerte :** VERT (on target), ORANGE (deviation < 10 %, requires monitoring), ROUGE (deviation > 10 %, requires action)

Group KPIs by dimension if there are more than 5 (financier, commercial, opérationnel, RH).

### 3. Lecture du tableau de bord (Dashboard Reading)
For each ORANGE or ROUGE indicator, provide a brief diagnostic:
- What does the deviation mean concretely?
- What is the likely cause (if identifiable from the data)?
- What is the trend (improving, stable, deteriorating vs N-1 or previous period)?

For VERT indicators, note if they are at risk of deterioration (leading indicators).

### 4. Actions recommandées (Recommended Actions)
For each alert, propose a concrete action:

| Priorité | KPI concerné | Action | Responsable | Délai | Impact attendu |
|----------|-------------|--------|-------------|-------|----------------|
| 1 | [KPI ROUGE] | [Action concrète] | [Fonction] | [Date] | [Chiffre] |
| 2 | [KPI ORANGE] | [Action concrète] | [Fonction] | [Date] | [Chiffre] |

Prioritize by severity (ROUGE first) and financial impact. Each action must be specific, measurable, and time-bound.

**Example skeleton:**

```
## Tableau de bord — Direction Générale (T1 N)

**Objectif**
Pilotage trimestriel de la performance globale. Destinataire : DG. Périmètre : société consolidée. Question clé : la trajectoire budgétaire est-elle respectée ?

**Indicateurs**

| KPI | Formule | Réel T1 | Budget T1 | Écart | Alerte |
|-----|---------|---------|-----------|-------|--------|
| CA HT | Facturation HT | 1 180 000 | 1 250 000 | -5,6 % | ORANGE |
| Marge brute | (CA - Achats consommés) / CA | 42,1 % | 45,0 % | -2,9 pts | ROUGE |
| EBE | CA - Consommations - Charges de personnel | 95 000 | 140 000 | -32,1 % | ROUGE |
| Trésorerie nette | Disponibilités - CBC | +45 000 | +80 000 | -43,8 % | ROUGE |

**Lecture**
- **Marge brute (ROUGE)** : la hausse du coût des matières premières (+8 % vs budget) n’a pas été répercutée sur les prix de vente. Tendance : détérioration depuis janvier (44 % → 42 %).
- **EBE (ROUGE)** : combine l’effet marge brute et un dépassement des charges de personnel (+12 000 EUR d’intérim non budgété). L’écart est significatif et compromet l’objectif annuel.
- **Trésorerie (ROUGE)** : conséquence directe de l’érosion de l’EBE, aggravée par un allongement du délai client (58 j. vs 45 j. budgétés).
- **CA (ORANGE)** : retard de facturation sur deux contrats signés mais non encore livrés. Rattrapage prévu en T2.

**Actions recommandées**

| Prio | KPI | Action | Resp. | Délai | Impact |
|------|-----|--------|-------|-------|--------|
| 1 | Marge brute | Réviser la grille tarifaire (+5 % sur gamme A) | Dir. Commercial | 30/04/N | +1,5 pt de marge |
| 2 | EBE | Geler le recours à l’intérim et reprioriser les missions | DRH | Immédiat | -12 000 EUR/mois |
| 3 | Trésorerie | Relance systématique clients > 45 jours | DAF | 15/04/N | +30 000 EUR encaissés |
| 4 | CA | Accélérer la livraison des 2 contrats en attente | Dir. Opérations | 30/04/N | +70 000 EUR de CA |
```


---

## Template 7 — Cas complexe (Complex Case)

**Trigger conditions:**
- The question involves interaction between multiple domains (comptabilité + fiscalité, paie + gestion, audit + normes IFRS, etc.)
- There is a causal chain where the treatment in one domain affects the treatment in another (e.g., un retraitement IFRS modifie la base imposable à l'IS)
- There is a norm conflict or divergence (PCG vs IFRS, droit français vs droit européen, doctrine administrative vs jurisprudence)
- The question requires synthesizing positions from multiple reference files
- The SKILL.md complex case protocol has been activated (multi-domain interaction detected)
- User mentions «restructuration», «fusion», «acquisition», «groupe», «consolidation», «intégration fiscale», «opération transfrontalière», «changement de méthode comptable»

**Tone:** Rigorous, systematic, multi-perspective. Each sub-problem must be treated exhaustively before synthesis. Highlight tensions between norms explicitly — never hide a conflict. The final recommendation must account for all dimensions simultaneously. Use cross-references between sections to show causal links. This is the most demanding template: precision and completeness are paramount.

**Section structure:**

### 1. Décomposition des problèmes (Problem Decomposition)
Identify and list each distinct sub-problem raised by the question. For each sub-problem, state:
- The domain concerned (comptabilité, fiscalité, paie, audit, finance, gestion, normes IFRS, droit des sociétés)
- The normative framework applicable (PCG, CGI, Code du travail, IFRS, Code de commerce, etc.)
- The reference files to consult
- The dependencies: which sub-problems must be resolved first because others depend on their outcome

Present the decomposition in a structured table:

| # | Sous-problème | Domaine | Cadre normatif | Dépendances |
|---|--------------|---------|----------------|-------------|
| 1 | [Description] | [Domaine] | [Norme] | — |
| 2 | [Description] | [Domaine] | [Norme] | Dépend de #1 |
| 3 | [Description] | [Domaine] | [Norme] | Dépend de #1, #2 |

If a norm conflict exists, flag it here with a brief description: «Conflit identifié : le PCG impose [X] tandis que la norme IAS [Y] requiert [Z].»

### 2. Traitement séquentiel (Sequential Treatment)
Treat each sub-problem in dependency order. For each one, apply the methodology of the most appropriate template (Template 1 for an accounting entry, Template 3 for a tax question, etc.) but in a condensed form. Each treatment must include:
- **Norme applicable :** the specific article, regulation, or standard
- **Analyse :** application to the facts of the case
- **Conclusion intermédiaire :** the answer to this sub-problem, stated clearly
- **Impact sur les autres sous-problèmes :** how this conclusion affects subsequent analyses

Use numbered sub-sections matching the decomposition table:

**Sous-problème #1 — [Titre]**
- Norme applicable : [citation]
- Analyse : [raisonnement]
- Conclusion intermédiaire : [réponse]
- Impact : [effet sur #2, #3, etc.]

**Sous-problème #2 — [Titre]**
- Norme applicable : [citation]
- Analyse : [raisonnement, intégrant la conclusion de #1]
- Conclusion intermédiaire : [réponse]
- Impact : [effet sur #3, etc.]

Continue until all sub-problems are resolved.

### 3. Synthèse croisée (Cross-Synthesis)
This is the critical section that distinguishes the complex case template. Present:
- **Interactions identifiées :** a matrix showing how each sub-problem's conclusion affects the others

| | SP #1 | SP #2 | SP #3 |
|---|-------|-------|-------|
| SP #1 | — | [effet] | [effet] |
| SP #2 | [effet] | — | [effet] |
| SP #3 | [effet] | [effet] | — |

- **Conflits normatifs :** for each identified conflict, state the two positions, the hierarchy of norms, and the recommended resolution. If the conflict has no clear resolution (e.g., pending case law), state the risk associated with each position.
- **Cohérence globale :** verify that the combined treatment across all domains is internally consistent. Flag any circular dependency or paradox. If a choice in one domain constrains choices in another, make this explicit.
- **Impact financier consolidé :** compute the total financial impact across all domains (accounting result, tax liability, cash flow, social contributions) in a summary table.

### 4. Recommandation globale (Overall Recommendation)
Provide a unified recommendation that accounts for all dimensions:
- **Stratégie recommandée :** the overall approach, with justification
- **Plan d'action :** sequenced steps, each tied to a specific domain and sub-problem
- **Risques résiduels :** risks that remain after following the recommended strategy, with mitigation measures
- **Points nécessitant un avis spécialisé :** if any sub-problem exceeds the scope of the analysis (e.g., requires a formal tax ruling, external audit, or legal counsel), flag it explicitly

| Étape | Action | Domaine | Responsable | Délai | Risque résiduel |
|-------|--------|---------|-------------|-------|-----------------|
| 1 | [Action] | [Domaine] | [Qui] | [Quand] | [Risque] |
| 2 | [Action] | [Domaine] | [Qui] | [Quand] | [Risque] |

**Example skeleton:**

```
## Cas complexe — Changement de méthode comptable avec impact fiscal et IFRS

**Décomposition des problèmes**

| # | Sous-problème | Domaine | Cadre normatif | Dépendances |
|---|--------------|---------|----------------|-------------|
| 1 | Changement de méthode d'évaluation des stocks (CMUP → FIFO) | Comptabilité | PCG art. 213-2, ANC 2014-03 art. 122-2 | — |
| 2 | Impact fiscal du changement de méthode | Fiscalité | Art. 38-2 CGI, BOI-BIC-BASE-40-10 | Dépend de #1 |
| 3 | Retraitement en normes IFRS (IAS 8) | Normes IFRS | IAS 8 §§ 14-27, IAS 2 | Dépend de #1 |
| 4 | Impact sur les comptes consolidés | Consolidation | ANC 2020-01, IFRS 10 | Dépend de #1, #3 |

Conflit identifié : en PCG, le changement de méthode est comptabilisé dans le résultat de l'exercice du changement ; en IFRS (IAS 8), il est comptabilisé de manière rétrospective avec ajustement des capitaux propres d'ouverture.

**Traitement séquentiel**

*Sous-problème #1 — Changement de méthode comptable*
- Norme applicable : ANC 2014-03, art. 122-2 — «un changement de méthode comptable n'est possible que s'il existe un choix entre plusieurs méthodes conformes et que le changement conduit à une meilleure information financière.»
- Analyse : le passage de CMUP à FIFO est autorisé. L'impact sur le stock au 01/01/N est une augmentation de 150 000 EUR (le FIFO valorise le stock plus haut en période de hausse des prix).
- Conclusion intermédiaire : l'ajustement de +150 000 EUR est comptabilisé en report à nouveau (PCG, compte 11 — Report à nouveau) dans les comptes sociaux, conformément à l'ANC 2014-03 art. 122-3.
- Impact : cet ajustement modifie le résultat fiscal (SP #2) et le bilan d'ouverture consolidé (SP #4).

*Sous-problème #2 — Impact fiscal*
- Norme applicable : art. 38-2 CGI — le bénéfice imposable est déterminé d'après les résultats d'ensemble des opérations.
- Analyse : l'augmentation de stock de 150 000 EUR augmente le résultat fiscal de l'exercice N. IS supplémentaire : 150 000 × 25 % = 37 500 EUR.
- Conclusion intermédiaire : surcoût fiscal de 37 500 EUR sur N.
- Impact : le surcoût affecte la trésorerie et les soldes de gestion (SP #4).

*Sous-problème #3 — Retraitement IFRS*
- Norme applicable : IAS 8 §§ 19-22 — un changement de méthode comptable doit être appliqué de manière rétrospective, sauf impraticabilité.
- Analyse : l'ajustement est porté en capitaux propres d'ouverture de la première période présentée. Les comparatifs sont retraités.
- Conclusion intermédiaire : dans les comptes IFRS, le stock d'ouverture N-1 et N est retraité.
- Impact : divergence de traitement avec les comptes sociaux (SP #1).

**Synthèse croisée**

Impact consolidé :

| Élément | Comptes sociaux (PCG) | Comptes consolidés (IFRS) |
|---------|----------------------|---------------------------|
| Stock au 01/01/N | +150 000 EUR | +150 000 EUR (et comparatifs retraités) |
| Résultat N | Neutre (via report à nouveau) | Neutre (rétrospectif) |
| IS supplémentaire | +37 500 EUR | +37 500 EUR |
| Capitaux propres nets | +112 500 EUR | +112 500 EUR |

**Recommandation globale**
1. Procéder au changement de méthode au 01/01/N après approbation par l'organe compétent.
2. Constituer une provision pour IS de 37 500 EUR.
3. Documenter la justification dans l'annexe des comptes sociaux et la note IFRS.
4. Retraiter les comparatifs dans les comptes consolidés IFRS conformément à IAS 8.
5. Informer le commissaire aux comptes en amont.

Risques résiduels : l'administration fiscale pourrait contester le changement (art. L. 64 LPF, abus de droit).
```

---

## Template 8 — Sortie structurée (Structured Output)

**Trigger conditions:**
- User role is `ai-agent` (machine consumer, API integration, downstream automation)
- User explicitly requests JSON, CSV, structured data, or machine-readable output
- User mentions "JSON", "API", "structured", "export", "données structurées", "tableau normalisé", "intégration"
- The request comes from an automated pipeline or the user specifies a target schema
- Another AI agent is consuming the output for further processing

**Tone:** Zero prose. Pure data. Every field must be documented. Use JSON as the default format; use normalized tables when the user requests tabular output. No introductory paragraphs, no commentary embedded in the data — all metadata goes in dedicated fields. The output must be directly parseable by a machine without post-processing.

**Section structure:**

### 1. Schéma de sortie (Output Schema)
Before emitting data, declare the schema. The schema documents every field:

```json
{
  "": "accounting-finance/v1",
  "type": "[output_type]",
  "description": "[what this output represents]",
  "fields": {
    "field_name": {
      "type": "[string|number|date|boolean|array|object]",
      "description": "[field description]",
      "unit": "[EUR|%|days|null]",
      "source": "[PCG|CGI|IFRS|computed|user_input]"
    }
  }
}
```

### 2. Données (Data Payload)
Emit the data conforming to the declared schema. Use consistent formatting:
- Dates: ISO 8601 (`YYYY-MM-DD`)
- Amounts: numbers without currency symbols (currency in metadata)
- Rates: decimal form (`0.25` not `25 %`)
- Null values: explicit `null`, never empty strings
- References: structured objects with `type`, `code`, and `label` fields

### 3. Références normatives (Normative References)
Machine-readable array of all norms cited:

```json
{
  "references": [
    {
      "type": "CGI",
      "article": "219-I",
      "description": "Taux de l'impôt sur les sociétés",
      "url": "https://www.legifrance.gouv.fr/codes/article_lc/..."
    }
  ]
}
```

### 4. Métadonnées (Metadata)
Include provenance and reliability information:

```json
{
  "metadata": {
    "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
    "skill_version": "accounting-finance/v1",
    "data_freshness": "YYYY-MM",
    "confidence": "high|medium|low",
    "verification_required": true,
    "warnings": ["[any caveats]"]
  }
}
```


**Common output schemas:**

**A. Écriture comptable (Journal Entry)**

```json
{
  "$schema": "accounting-finance/v1",
  "type": "journal_entry",
  "description": "Écriture comptable au format structuré",
  "currency": "EUR",
  "journal": "string — code journal (ACH, VTE, BQ, OD)",
  "date": "YYYY-MM-DD",
  "piece_ref": "string",
  "lines": [
    {
      "account_code": "string — numéro de compte PCG",
      "account_label": "string — intitulé du compte",
      "debit": "number|null",
      "credit": "number|null",
      "label": "string — libellé de la ligne",
      "analytical_code": "string|null",
      "tax_code": "string|null"
    }
  ],
  "total_debit": "number",
  "total_credit": "number",
  "balanced": "boolean",
  "normative_basis": [
    {
      "type": "PCG|CGI|ANC|IFRS",
      "reference": "string",
      "description": "string"
    }
  ]
}
```

**Exemple :**

```json
{
  "type": "journal_entry",
  "journal": "ACH",
  "date": "2026-03-15",
  "piece_ref": "FA-2026-0042",
  "lines": [
    {
      "account_code": "607",
      "account_label": "Achats de marchandises",
      "debit": 10000.0,
      "credit": null,
      "label": "Achat marchandises fournisseur Y",
      "analytical_code": "AXE1-COMM",
      "tax_code": "TVA20"
    },
    {
      "account_code": "44566",
      "account_label": "TVA déductible sur ABS",
      "debit": 2000.0,
      "credit": null,
      "label": "TVA 20 %",
      "analytical_code": null,
      "tax_code": null
    },
    {
      "account_code": "401",
      "account_label": "Fournisseurs",
      "debit": null,
      "credit": 12000.0,
      "label": "Fournisseur Y — FA-2026-0042",
      "analytical_code": null,
      "tax_code": null
    }
  ],
  "total_debit": 12000.0,
  "total_credit": 12000.0,
  "balanced": true,
  "normative_basis": [
    {
      "type": "PCG",
      "reference": "art. 946-60",
      "description": "Achats de marchandises"
    },
    {
      "type": "CGI",
      "reference": "art. 271-I",
      "description": "TVA déductible sur achats"
    },
    {
      "type": "ANC",
      "reference": "2014-03 art. 512-2",
      "description": "Fait générateur des charges"
    }
  ]
}
```

**B. Ratios financiers (Financial Ratios)**

```json
{
  "$schema": "accounting-finance/v1",
  "type": "financial_ratios",
  "entity": "string",
  "period": "YYYY ou YYYY-MM",
  "currency": "EUR",
  "ratios": [
    {
      "category": "rentabilite|structure|liquidite|activite",
      "name": "string",
      "formula": "string",
      "numerator": "number",
      "denominator": "number",
      "value": "number",
      "unit": "%|days|ratio",
      "benchmark": "number|null",
      "benchmark_source": "string|null",
      "interpretation": "positive|negative|neutral",
      "alert": "green|orange|red"
    }
  ]
}
```

**Exemple :**

```json
{
  "type": "financial_ratios",
  "entity": "Société Z",
  "period": "2025",
  "currency": "EUR",
  "ratios": [
    {
      "category": "rentabilite",
      "name": "ROE",
      "formula": "resultat_net / capitaux_propres",
      "numerator": 245000,
      "denominator": 1200000,
      "value": 0.2042,
      "unit": "%",
      "benchmark": 0.15,
      "benchmark_source": "Banque de France — statistiques sectorielles",
      "interpretation": "positive",
      "alert": "green"
    },
    {
      "category": "structure",
      "name": "ratio_endettement",
      "formula": "dettes_financieres / capitaux_propres",
      "numerator": 800000,
      "denominator": 1200000,
      "value": 0.6667,
      "unit": "ratio",
      "benchmark": 1.0,
      "benchmark_source": "Norme sectorielle",
      "interpretation": "positive",
      "alert": "green"
    }
  ]
}
```

**C. Calcul d’impôt (Tax Computation)**

```json
{
  "$schema": "accounting-finance/v1",
  "type": "tax_computation",
  "description": "Calcul détaillé",
  "tax_type": "IS|IR|TVA|CET|PV",
  "entity": "string",
  "fiscal_year": "YYYY",
  "currency": "EUR",
  "steps": [
    {
      "step": "number",
      "label": "string",
      "operation": "base|add|subtract|multiply|result",
      "amount": "number",
      "legal_basis": "string",
      "detail": "string|null"
    }
  ],
  "result": {
    "taxable_base": "number",
    "rate": "number",
    "tax_due": "number",
    "credits": "number",
    "net_tax": "number"
  },
  "optimization_options": [
    {
      "option": "string",
      "legal_basis": "string",
      "potential_saving": "number",
      "conditions": "string",
      "risk_level": "low|medium|high"
    }
  ]
}
```

**Exemple :**

```json
{
  "type": "tax_computation",
  "tax_type": "IS",
  "entity": "Société A",
  "fiscal_year": "2025",
  "currency": "EUR",
  "steps": [
    {
      "step": 1,
      "label": "Résultat comptable",
      "operation": "base",
      "amount": 800000,
      "legal_basis": "art. 38 CGI",
      "detail": null
    },
    {
      "step": 2,
      "label": "Réintégration amende",
      "operation": "add",
      "amount": 15000,
      "legal_basis": "art. 39-2 CGI",
      "detail": "Non déductible"
    },
    {
      "step": 3,
      "label": "Amort. VP",
      "operation": "add",
      "amount": 5200,
      "legal_basis": "art. 39-4 CGI",
      "detail": "Plafond VP"
    },
    {
      "step": 4,
      "label": "Mère-fille",
      "operation": "subtract",
      "amount": 50000,
      "legal_basis": "art. 216 CGI",
      "detail": "95%"
    },
    {
      "step": 5,
      "label": "QPFC",
      "operation": "add",
      "amount": 2500,
      "legal_basis": "art. 216 CGI",
      "detail": "5%"
    },
    {
      "step": 6,
      "label": "Résultat fiscal",
      "operation": "result",
      "amount": 772700,
      "legal_basis": "art. 209-I CGI",
      "detail": null
    }
  ],
  "result": {
    "taxable_base": 772700,
    "rate": 0.25,
    "tax_due": 193175,
    "credits": 0,
    "net_tax": 193175
  },
  "optimization_options": [
    {
      "option": "CIR",
      "legal_basis": "art. 244 quater B CGI",
      "potential_saving": null,
      "conditions": "R&D",
      "risk_level": "low"
    }
  ]
}
```

**D. Fiche de paie synthétique (Payslip Summary)**

```json
{
  "$schema": "accounting-finance/v1",
  "type": "payslip_summary",
  "period": "YYYY-MM",
  "currency": "EUR",
  "employee": {
    "status": "cadre|non_cadre|dirigeant",
    "contract": "CDI|CDD|interim",
    "hours": "number"
  },
  "gross": {
    "base_salary": "number",
    "overtime": "number",
    "bonuses": "number",
    "benefits_in_kind": "number",
    "total_gross": "number"
  },
  "employee_contributions": [
    {
      "name": "string",
      "base": "number",
      "rate": "number",
      "amount": "number",
      "legal_ref": "string"
    }
  ],
  "employer_contributions": [
    {
      "name": "string",
      "base": "number",
      "rate": "number",
      "amount": "number",
      "legal_ref": "string"
    }
  ],
  "net_taxable": "number",
  "net_before_tax": "number",
  "withholding_tax_rate": "number|null",
  "withholding_tax_amount": "number|null",
  "net_pay": "number",
  "total_employer_cost": "number"
}
```

**Rules for structured output:**
1. Never mix prose and data. Use a separate `"notes"` array field if needed.
2. Always include the schema declaration at the top of the output.
3. All monetary amounts use 2 decimal places.
4. All rates use decimal form (0.25, not 25 %).
5. Dates use ISO 8601.
6. Include `metadata` block with generation timestamp, data freshness, and confidence level.
7. If verification needed, set `"verification_required": true` and list URLs in `"warnings"`.
8. For multiple output types, wrap in array under `"results"` key.
