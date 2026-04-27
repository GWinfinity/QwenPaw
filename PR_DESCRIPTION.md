# feat: Hermes Agent enhancement & Token Usage Cost Display

## Summary

This PR introduces **Hermes Agent enhancement modules** adapted from [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) and adds **USD/CNY cost display** to the Token Usage page, helping users track API spending alongside token consumption.

## Changes

### 1. feat: add Hermes Agent enhancement modules

Introduces `src/qwenpaw/agents/hermes_enhance/` with the following capabilities:

| Module | Description |
|--------|-------------|
| `ContextCompressor` | Smart context compression with rich summarization templates (Resolved/Pending tracking, Handoff framing, iterative summary updates, tool-output pruning) |
| `usage_pricing` | USD cost calculation (`CostResult`, `CanonicalUsage`) using a local pricing table — no network calls |
| `model_metadata` | Model context length metadata queries (dependency for pricing) |
| `auxiliary_client`, `context_engine`, `_compat` | Supporting dependencies |

> **Note:** After the initial import, modules duplicating existing QwenPaw functionality (`bedrock_adapter`, `memory_manager`, `memory_provider`, `prompt_builder`, `rate_limit_tracker`, `retry_utils`, `skill_utils`) were removed to keep the footprint minimal.

### 2. feat(token-usage): add USD cost display using Hermes pricing

**Backend:**
- Adds `cost_usd` to `TokenUsageStats` and `total_cost_usd` to `TokenUsageSummary`
- Adds `_calc_cost()` using the Hermes local pricing table (`_OFFICIAL_DOCS_PRICING`)
- Falls back to `0` for unknown models

**Frontend:**
- Extends `TokenUsageStats` / `TokenUsageSummary` types with cost fields
- Adds **Total Cost (USD)** summary card alongside Prompt / Completion cards
- Adds **Cost (USD)** column to both *By Model* and *By Date* tables
- Adds i18n keys: `cost`, `totalCost` (EN / ZH / JA / RU)

### 3. feat(token-usage): add CNY cost display for domestic models

**Backend:**
- Adds `_CNY_PRICING` table for domestic providers (**DeepSeek, DashScope/Qwen, Zhipu, Moonshot, Baidu**) with native CNY per-million-token rates
- Adds `_calc_costs()` returning `(usd, cny)`; CNY uses native pricing when available, falls back to `USD * 7.2` exchange rate for foreign models
- Extends `TokenUsageStats` with `cost_cny` and `TokenUsageSummary` with `total_cost_cny`

**Frontend:**
- Extends types with `cost_cny` / `total_cost_cny`
- Adds `formatCostCNY` helper (`¥` prefix)
- Adds **Total Cost (CNY)** summary card alongside the USD card
- Adds **Cost (CNY)** column to *By Model* and *By Date* tables
- Adds i18n keys for all 4 languages

## Files Changed

- `src/qwenpaw/agents/hermes_enhance/*` — new Hermes enhancement modules
- `src/qwenpaw/token_usage/manager.py` — cost calculation logic
- `console/src/api/types/tokenUsage.ts` — TypeScript type extensions
- `console/src/pages/Settings/TokenUsage/index.tsx` — UI components
- `console/src/locales/*.json` — i18n strings

## Checklist

- [x] Hermes modules deduplicated to retain only unique capabilities
- [x] USD pricing uses offline table (no external network calls)
- [x] CNY pricing covers major domestic providers
- [x] Frontend preserves existing Card / Table / layout style
- [x] i18n updated for EN, ZH, JA, RU

## Related

- Source: https://github.com/NousResearch/hermes-agent
