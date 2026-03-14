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