---
name: deep-research
description: Plan and execute comprehensive, source-backed research with GPT/OpenAI, Perplexity, and Gemini using five differentiated research strategies, adversarial comparison, synthesis, citation verification, source-quality auditing, and optional iterative deepening. Use for deep research, literature reviews, evidence maps, state-of-knowledge reports, policy or market scans, contested questions, and authoritative research briefs where accuracy, provenance, current sources, and disagreement analysis matter more than speed. Supports direct API orchestration and import of Deep Research reports produced in consumer apps; Claude is an optional future provider and Grok is not required.
---

# Deep Research

Run five research strategies through the user's three available provider families, then verify and synthesize the evidence. Preserve a distinction between strategy diversity and model diversity.

## Operating principles

- Treat a ChatGPT, Gemini, or Perplexity subscription as different from API access. Never assume a consumer plan includes an API key or API credits.
- Never expose, print, commit, or write API keys into the skill. Prefer environment variables or a user-controlled config outside a synced project.
- Never claim that five strategy reports are five independent model confirmations. Report both `strategy_count` and `provider_count`.
- Count support once per independent provider family when describing cross-model agreement. Count multiple strategies from one provider separately only as strategy agreement.
- Preserve disagreement, uncertainty, source provenance, and date sensitivity. Do not average conflicting figures silently.
- Treat citations as leads until mechanically or manually verified. A plausible citation is not a verified citation.
- Prefer primary sources, controlling authority, official statistics, peer-reviewed work, and direct institutional documents over summaries.
- Stamp current or time-sensitive claims with `[as of: YYYY-MM-DD]`.
- Mark unresolved items `UNVERIFIED`; never invent a DOI, URL, title, author, quotation, or date.

## Choose the execution mode

Run from the skill directory unless a command states otherwise.

1. Run `python scripts/check_setup.py`.
2. Use **API mode** only when at least one provider API is configured. Three providers are preferred.
3. Use **report-import mode** when the user has consumer subscriptions but no API keys, or when they want to control Deep Research runs in each product UI.
4. Permit a mixed run: import consumer-app reports and generate missing roles through configured APIs. Record every origin in the manifest.

Read [three-provider-setup.md](references/three-provider-setup.md) when configuring providers, selecting current model IDs, diagnosing access, or preparing consumer-app prompts.

## Default three-provider role map

Use the following deliberate spread when all three providers are available:

| Strategy | Provider | Purpose |
|---|---|---|
| academic | Gemini | Canonical literature, theory, empirical debates, long documents |
| practitioner | GPT | Applied methods, implementation, industry evidence, explainers |
| real-time | Perplexity | Current web evidence, recent data, news, filings, live citations |
| grey-literature | Gemini | Government, IGO, legal, standards, datasets, primary documents |
| contrarian | GPT | Rival hypotheses, dissent, boundary conditions, missing perspectives |

If a provider is missing, remap roles explicitly and record the reduced provider count. Do not label a knowledge-cutoff model as real-time unless it has live web search.

## Round 0: frame and scope

Before calling providers:

1. Restate the question, decision context, audience, time horizon, geography, exclusions, and desired deliverable.
2. Identify claims that are current, contested, causal, quantitative, or high stakes.
3. Classify the domain and establish source priorities.
4. Define inclusion and exclusion criteria and a stopping rule.
5. Create a topic slug under `research/<topic-slug>/`.

Run:

```text
python scripts/scope.py --topic "<topic>" --scope "<scope>" --output research/<slug>/round0/scope.md --use-llm
```

Omit `--use-llm` when no API provider is configured. Preserve `scope.json` for downstream prompts.

## Round 1A: API dispatch

Always preview assignments and costs before paid calls:

```text
python dispatch.py --topic "<topic>" --scope "<scope>" --output-dir research/<slug>/round1 --scope-file research/<slug>/round0/scope.json --estimate-only
```

Do not treat a cost estimate as enforceable when it says provider pricing is unknown. Add current pricing in `deep-research.toml`, reduce the run, or obtain user confirmation of the uncertainty.

After the user has authorized the run or supplied a trustworthy cap:

```text
python dispatch.py --topic "<topic>" --scope "<scope>" --output-dir research/<slug>/round1 --scope-file research/<slug>/round0/scope.json --languages en --resume
```

Use `--agents`, `--max-cost-usd`, and additional languages when appropriate. If `--max-cost-usd` is supplied while any pricing is unknown, stop rather than offering a false hard cap.

## Round 1B: consumer-app report import

Give each product only its assigned role prompt from [synthesis-prompts.md](references/synthesis-prompts.md). Ask the user to export or attach the complete reports as Markdown or plain text. Do not imply that Codex can use their consumer accounts through an API.

Normalize reports with:

```text
python scripts/import_reports.py --topic "<topic>" --scope "<scope>" --output-dir research/<slug>/round1 --report academic=gemini:<path> --report practitioner=chatgpt:<path> --report real-time=perplexity:<path> --report grey-literature=gemini:<path> --report contrarian=chatgpt:<path>
```

Preserve the original exports outside `round1` when feasible. If one consumer report covers two strategies, either import it under the dominant role and flag the missing role, or deliberately reuse it while marking the reports as non-independent.

## Round 2: adversarial comparison

Read every Round 1 report and `manifest.json`. Produce `round2/adversarial-comparison.md` using the Round 2 contract in [synthesis-prompts.md](references/synthesis-prompts.md).

Build:

- a claim-by-provider matrix;
- a strategy-coverage matrix;
- a contradiction and discrepancy ledger;
- a citation-laundering map showing reports that rely on the same underlying source;
- a completeness map of unanswered or weakly answered questions;
- a risk register for high-stakes or time-sensitive claims.

Tag support as `[provider support: n/N; strategy support: s/S]`. A shared secondary source is one evidence chain, regardless of how many reports cite it.

## Round 3: plan and synthesize

Create three independent section plans, reconcile them, then draft sections. Use subagents only when available and permitted; give each one the raw Round 1 reports, Round 2 comparison, scope, and a bounded section assignment. Do not give a validator the intended conclusion.

For each section:

1. Lead with the answer or controlling finding.
2. Separate established findings, disputed findings, gaps, and inference.
3. Use direct citations and retain exact source identifiers.
4. Attach provider/strategy support tags only to consequential claims.
5. Include counterevidence and boundary conditions.
6. Avoid combining different denominators, populations, jurisdictions, or as-of dates.

Write integrated sections under `research/<slug>/sections/` and a deduplicated `bibliography.md`.

## Round 4: verification and correction

Run the mechanical checks from the skill directory:

```text
python scripts/dedup_bib.py research/<slug>/round1/agent-*.md --output research/<slug>/sections/bibliography.md
python scripts/verify_citations.py research/<slug>/sections --output research/<slug>/round4/citation-verification.md --check-urls
python scripts/classify_sources.py research/<slug>/sections/bibliography.md --output research/<slug>/round4/tier-report.md
python scripts/lit_search.py --topic "<topic>" --limit 50 --compare-bib research/<slug>/sections/bibliography.md --output research/<slug>/round4/missing-lit.md
```

Then perform a source-to-claim audit:

- Open sources supporting the key findings and confirm that each source entails the claim.
- Verify quotations, numbers, units, dates, populations, and jurisdiction.
- Replace secondary citations with primary sources when possible.
- Downgrade, qualify, or remove claims that remain unresolved.
- Record every material correction in `round4/fix-log.md`.

Never equate successful title/DOI resolution with claim-level verification.

## Round 5: deepen selectively

Run at most two deepening passes. Target only sections that have low provider support, unresolved contradictions, missing canonical literature, weak source tiers, or stale evidence. Keep the original reports and log what changed.

Stop when the stated stopping rule is met, new searches produce mostly duplicate evidence, and remaining uncertainty is explicitly bounded.

## Export and handoff

Run:

```text
python scripts/export.py --sections research/<slug>/sections --bibliography research/<slug>/sections/bibliography.md --output-dir research/<slug>/export
python scripts/search.py index
```

Deliver:

- a concise hub file with question, scope, as-of date, provider/strategy counts, key findings, important disagreements, limitations, and section links;
- integrated sections;
- verified bibliography plus BibTeX;
- machine-readable claims JSONL;
- Round 0–5 provenance and correction logs.

State which providers actually ran, whether each came from API or consumer export, which checks completed, and what remains unverified.

## Failure handling

- Resume partial API runs with `--resume`; do not discard successful reports.
- If a provider fails, continue with remaining providers but reduce the denominator and disclose the loss of independence.
- If live search is unavailable, remove or relabel the real-time pass.
- If a model ID fails, verify the current official provider documentation before changing it; avoid guessing aliases.
- If API access is absent, switch to report-import mode instead of asking for secrets in chat.
- If mechanical resolvers disagree or cannot resolve a citation, inspect the source manually and retain `UNVERIFIED` until resolved.

## Maintenance note

This skill is adapted from `nraford7/deep-research` under the included MIT license. The tailored default is GPT + Perplexity + Gemini; Claude may be added later through TOML, and Grok is neither expected nor required.
