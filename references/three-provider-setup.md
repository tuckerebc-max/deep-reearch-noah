# Three-provider setup

## Access modes

Consumer subscriptions and developer APIs are separate products. The API dispatcher requires developer credentials and may incur usage charges:

- `OPENAI_API_KEY` for GPT/OpenAI API
- `PERPLEXITY_API_KEY` for Perplexity Sonar API
- `GOOGLE_API_KEY` for the Gemini API

If only consumer subscriptions are available, use the report-import workflow in `SKILL.md`. Never request that a user paste a secret into chat, a tracked file, or a synced project folder.

## Install dependencies

From the skill directory:

```text
python -m pip install -r requirements.txt
```

Optional semantic indexing:

```text
python -m pip install -r requirements-search.txt
```

## Configure without embedding secrets

Set keys in the process environment or a user-controlled `~/.env`. The runtime also reads a project `.env`, but avoid that location when the project is synced or shared.

Copy `references/deep-research.toml.example` to `deep-research.toml` in the research project only when model or role overrides are needed. The example reads keys from environment-variable names; it contains no credential values.

Run:

```text
python scripts/check_setup.py
```

The expected full assignment is:

- academic → gemini
- practitioner → chatgpt
- real-time → perplexity
- grey-literature → gemini
- contrarian → chatgpt

The setup checker must report three independent providers and five strategies for full diversity.

## Model freshness

Defaults were reviewed against official provider documentation on 2026-08-04:

- OpenAI: `gpt-5.6-sol`
- Perplexity: `sonar-deep-research`
- Gemini: `gemini-3.5-flash`, with configured fallbacks

Model IDs, availability, output limits, and prices change. When a model fails or the user asks for the latest model, verify official documentation before editing config. For Gemini, prefer a stable identifier and use the Models API to confirm availability to the user's key. For Perplexity, keep the `web_search` capability on Sonar Deep Research. Do not invent price entries; unknown pricing must remain visibly excluded from estimates.

## Optional future Claude adapter

Install the Anthropic SDK only if Claude API access is added:

```text
python -m pip install anthropic
```

Then set `ANTHROPIC_API_KEY` and add explicit agent mappings in TOML. Do not change the three-provider defaults merely because the runtime supports Claude.

## Troubleshooting

- `API providers: none`: keys are absent from the environment/config. Use report-import mode or configure developer API keys.
- real-time warning: Perplexity is absent or the selected provider lacks `web_search`; do not present that report as current web research.
- budget not enforceable: one or more provider prices are unknown. Add current pricing overrides or obtain explicit approval for uncapped provider cost.
- model 404/invalid model: check the provider's current model list and account entitlement; do not cycle through guessed names.
