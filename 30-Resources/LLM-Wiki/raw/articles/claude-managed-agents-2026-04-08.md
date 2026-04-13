---
title: "Claude Managed Agents: get to production 10x faster"
source_url: https://claude.com/blog/claude-managed-agents
date: 2026-04-08
type: raw
---

# Claude Managed Agents: get to production 10x faster

Published: April 8, 2026 | Anthropic Blog | Product Announcement

## Summary

Anthropic launched Claude Managed Agents — a suite of composable APIs for building and deploying cloud-hosted agents at scale. Available in public beta on the Claude Platform.

## What It Is

Before this, building a production AI agent required:
- Sandboxed code execution
- State management / checkpointing
- Credential management
- Scoped permissions
- End-to-end tracing
...all of which could take months before shipping anything users see.

Managed Agents handles all of that. You define tasks, tools, and guardrails — Anthropic runs the infrastructure.

## Key Features

- **Production-grade agents** — secure sandboxing, authentication, and tool execution handled
- **Long-running sessions** — operate autonomously for hours, persist through disconnections
- **Multi-agent coordination** — agents spin up and direct other agents for parallel complex work (research preview)
- **Trusted governance** — scoped permissions, identity management, execution tracing built in
- **Self-evaluation loop** — define outcomes and success criteria; Claude iterates until it gets there (research preview)
- **Console visibility** — session tracing, integration analytics, troubleshooting in Claude Console

## Performance Claims

- Up to 10-point improvement in task success over standard prompting loop (internal testing)
- Largest gains on hardest problems
- "Get to production 10x faster"

## Designed for Claude

Purpose-built for Claude models which are themselves built for agentic work. The built-in orchestration harness decides when to call tools, manages context, and recovers from errors.

## Early Customers

- **Notion** — lets teams delegate work to Claude inside their workspace; engineers use it to ship code, knowledge workers produce websites/presentations (private alpha: Notion Custom Agents)
- **Rakuten** — shipped enterprise agents across product, sales, marketing, finance; plugged into Slack and Teams; each specialist agent deployed within a week
- **Asana** — built AI Teammates (collaborative agents working alongside humans inside projects); used Managed Agents to add advanced features dramatically faster
- **Vibecode** — prompt-to-deployed-app platform; using Managed Agents as default integration
- **Sentry** — Seer debugging agent paired with Claude-powered agent that writes the patch and opens the PR; shipped in weeks not months

## Access

- Public beta: Claude Platform
- Multi-agent coordination: research preview (request access at claude.com/form/claude-managed-agents)
- Self-evaluation loop: research preview
