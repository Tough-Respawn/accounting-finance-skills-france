# accounting-finance — Claude Code Plugin

**Assistant comptable et financier pour la France et l'Europe.**
*French accounting and corporate finance assistant for Claude Code.*

---

## FR

### Description

Plugin Claude Code couvrant 8 domaines de la comptabilité, de la finance d'entreprise et de la fiscalité française :

| # | Domaine | Commande |
|---|---------|----------|
| 1 | Comptabilité générale (PCG) | `/general-accounting` |
| 2 | Comptabilité analytique | `/cost-accounting` |
| 3 | Normes IFRS / consolidation | `/ifrs` |
| 4 | Finance d'entreprise | `/corporate-finance` |
| 5 | Fiscalité des entreprises | `/tax` |
| 6 | Audit & contrôle (CAC, NEP) | `/audit` |
| 7 | Contrôle de gestion | `/management-control` |
| 8 | Paie & charges sociales | `/payroll` |

La commande `/accounting` auto-détecte le domaine et route automatiquement.

### Fonctionnalités

- **Auto-détection** : le plugin s'active automatiquement quand vous posez une question sur la comptabilité, la finance ou la fiscalité
- **Adaptation au rôle** : expert-comptable/DAF, étudiant, dirigeant, collaborateur, agent IA
- **8 templates de réponse** : écriture comptable, analyse financière, note fiscale, exercice corrigé, fiche de paie, tableau de bord, cas complexe, sortie structurée
- **Références embarquées** : ~387 KB de données structurées (PCG, CGI, IFRS, taux, barèmes, glossaire, décisions clés)
- **Vérification web obligatoire** : recoupement systématique avec Legifrance, BOFiP, URSSAF, EUR-Lex
- **Protocole cas complexe** : décomposition multi-domaines, synthèse croisée, détection de conflits normatifs

### Installation

```bash
claude plugin install accounting-finance
```

---

## EN

### Description

Claude Code plugin covering 8 domains of French accounting, corporate finance, and taxation.

Use `/accounting <question>` for auto-routing, or domain-specific commands listed above.

### Features

- **Auto-detection**: activates when the conversation involves accounting, finance, or tax topics
- **Role adaptation**: accountant/CFO, student, executive, collaborator, AI agent
- **8 response templates**: journal entry, financial analysis, tax memo, corrected exercise, payslip breakdown, dashboard, complex case, structured output
- **Embedded references**: ~387 KB of structured data (PCG, CGI, IFRS, rates, thresholds, glossary, landmark decisions)
- **Mandatory web verification**: cross-check against Legifrance, BOFiP, URSSAF, EUR-Lex
- **Complex case protocol**: multi-domain decomposition, cross-synthesis, norm conflict detection

### Installation

```bash
claude plugin install accounting-finance
```

---

## Architecture

```
.claude-plugin/marketplace.json          # Plugin registry
plugins/accounting-finance/
  .claude-plugin/plugin.json             # Plugin metadata
  commands/                              # 9 slash commands
    accounting.md                        # Auto-router
    general-accounting.md ... payroll.md # Domain-specific
  skills/accounting-finance/
    SKILL.md                             # Skill definition (13 sections)
    methodology.md                       # 8 response templates
    references/                          # ~387 KB embedded data
      generale.md      analytique.md     ifrs.md
      finance.md       fiscalite.md      audit.md
      controle-gestion.md  paie.md
      pcg-index.md     taux-baremes.md   glossaire.md
      sources.md       decisions-cles.md
```

## License

MIT