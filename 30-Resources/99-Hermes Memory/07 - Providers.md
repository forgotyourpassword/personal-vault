---
tags:
  - resource
---

# Providers

## Current Default
- Model: `qwen/qwen3.6-plus:free`
- Provider: OpenRouter (`https://openrouter.ai/api/v1`)
- Status: Free tier, working

## MiniMax (custom provider, added to config.yaml)
- Base URL: `https://api.minimax.chat/v1`
- Env var: `MINIMAX_API_KEY`
- Models:
  - `minimax-m2` (1M context)
  - `minimax-text-01` (1M context)
- Status: Config needs API key from https://platform.minimax.io/
- To use: `export MINIMAX_API_KEY="your-key"` then `hermes model` to select

## LM Studio (local)
- Base URL: `http://localhost:1234/v1`
- API key: `lm-studio`
- Default model: `google/gemma-3-4b` via `office` device (LM Link)
- Gotcha: `lms` daemon must be running

## OpenAI Codex
- Provider key: `openai-codex`
- Correct lightweight Codex model for Michael's ChatGPT Codex account: `gpt-5.4-mini`
- Do **not** use `gpt-4-mini` for Codex cron jobs; it fails with: `model is not supported when using Codex with a ChatGPT account`.

## Fallback Providers
- Current config has `fallback_providers: []` to prevent stale LM Studio fallback from hijacking cron jobs when local models are not loaded.
- Config comment supports: openrouter, openai-codex (OAuth), nous (OAuth), zai, kimi-coding, minimax, minimax-cn.

```yaml
# fallback_model:
#   provider: openrouter
#   model: anthropic/claude-sonnet-4
```
Quartz: http://192.168.1.223:8080/30-Resources/99-Hermes-Memory/07---Providers
