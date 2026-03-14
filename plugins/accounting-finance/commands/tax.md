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