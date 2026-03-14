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