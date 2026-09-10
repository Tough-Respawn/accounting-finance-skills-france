---
description: Ask any question about French accounting or corporate finance — routes to the right domain automatically
argument-hint: <your accounting/finance question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Read `${CLAUDE_PLUGIN_ROOT}/skills/accounting-finance/SKILL.md` and follow that skill to answer the request below.

Select the relevant domains using the skill's routing table.

Resolve all supporting resources relative to that SKILL.md directory. Apply its verification, response-selection and uncertainty rules, including when embedded references already contain an answer. Preserve an explicit output format such as JSON; include warnings and the professional-information notice inside its metadata.

## User request

$ARGUMENTS
