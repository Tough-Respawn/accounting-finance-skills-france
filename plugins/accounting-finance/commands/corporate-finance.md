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