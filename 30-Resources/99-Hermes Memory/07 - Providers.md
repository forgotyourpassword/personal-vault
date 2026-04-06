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

## Fallback Providers
- None configured yet. Config comment supports: openrouter, openai-codex (OAuth), nous (OAuth), zai, kimi-coding, minimax, minimax-cn.

```yaml
# fallback_model:
#   provider: openrouter
#   model: anthropic/claude-sonnet-4
```
