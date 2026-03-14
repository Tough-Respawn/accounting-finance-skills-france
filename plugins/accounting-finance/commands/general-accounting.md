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