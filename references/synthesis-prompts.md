# Research and synthesis prompt contracts

## Consumer-app research prompt

Use one copy per assigned strategy. Replace bracketed fields and paste the matching strategy text from `config.py`.

```text
Conduct a complete Deep Research pass.

Question: [QUESTION]
Scope: [SCOPE]
Decision/audience: [CONTEXT]
As-of date: [YYYY-MM-DD]
Inclusion criteria: [CRITERIA]
Exclusions: [EXCLUSIONS]

Your assigned strategy is: [STRATEGY NAME]
[STRATEGY TEXT]

Requirements:
- Search and cite real sources; prefer primary, official, institutional, and peer-reviewed evidence.
- Never invent a source, URL, DOI, quotation, author, or date. Mark uncertainty UNVERIFIED.
- Cite every consequential factual claim inline and include a full source list with URLs/identifiers.
- Add [as of: YYYY-MM-DD] to current claims.
- Separate evidence, interpretation, inference, dissent, and open questions.
- Identify conflicting estimates, denominators, populations, jurisdictions, and source dependencies.
- Return the full report in one response or exportable document.
```

## Round 2 adversarial comparison contract

```text
Compare all Round 1 reports as an adversarial evidence auditor.

Use manifest.json to distinguish provider families from strategy roles. Never count two reports from the same provider as two independent model confirmations. For every important claim, report [provider support: n/N; strategy support: s/S]. Trace apparently independent citations to the underlying source and collapse citation laundering into one evidence chain.

Produce:
1. claim-by-provider matrix;
2. strategy-coverage matrix;
3. agreements with strongest sources;
4. contradictions with exact values, definitions, dates, and jurisdictions;
5. unsupported or weakly supported claims;
6. citation-laundering/source-dependency map;
7. missing canonical sources and unanswered questions;
8. high-stakes verification priorities;
9. proposed section architecture.

Do not resolve disagreement by majority vote. State what evidence would discriminate among rival claims.
```

## Section synthesis contract

```text
Draft only the assigned section using the scope, raw reports, adversarial comparison, and verified sources. Lead with the controlling finding. Separate established findings, disputed findings, gaps, and inference. Preserve counterevidence and boundary conditions. Do not introduce uncited facts. Do not convert strategy agreement into provider agreement. Use exact as-of dates and reconcile units, populations, denominators, and jurisdictions. End with a short verification-needed list.
```
