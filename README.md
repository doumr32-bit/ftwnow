# FTWNOW Plugin v3.2.0

Zero-to-production full-stack development methodology — from idea to deployment.

Combines **BMAD** (Spec-Driven Development) with **TDD** to guide anyone from idea to deployed product using **TypeScript + Next.js + Supabase + Vercel**.

## What's Included

| Component | Description |
|-----------|-------------|
| **Skill** | 9-Phase methodology (Phase 0–7 + 2.5) with 16 Agents (6 strategic + 10 tactical) |
| **Command** | `/FTW <project>` — project wake-up slash command |
| **Hook** | SessionStart auto-activation message |
| **MCP Servers** | Notion, Linear, Figma, Supabase, GitHub (pre-configured) |
| **Connectors** | 4 swappable tool categories + 2 fixed tools |

## Quick Start

### Install (Cowork)

1. Drop the `ftwnow.plugin` file into Cowork
2. Connect your MCP tools when prompted (Notion, Linear, Figma, Supabase, GitHub)
3. Type `/FTW MyProject` to start

### Install (Claude Code CLI)

```bash
claude plugin add /path/to/ftwnow.plugin
```

## Phases

| Phase | Name | Gate |
|-------|------|------|
| 0 | Discovery & Research | — |
| 1 | Specification (PRD + Architecture) | ⛔ Hard Gate 1 |
| 2 | Sprint Planning | — |
| 2.5 | Supabase Schema Bootstrap | ⛔ Hard Gate 2 |
| 3 | TDD Implementation | — |
| 4 | Code Review & QA | — |
| 5 | Deployment | — |
| 6 | Sprint Retrospective | — |
| 7 | Skill Self-Iteration | ⛔ Hard Gate 3 |

## Agents (16)

**Strategic (6):** Product Manager, Architect, Scrum Master, Agent Shield, Skill Iterator, Doc Updater

**Tactical (10):** Frontend Dev, Backend Dev, Supabase Admin, UX Designer, TDD Coach, Code Reviewer, E2E Runner, Performance Auditor, DevOps Engineer, Bug Hunter

## Tool Connectors

FTWNOW uses `~~category` placeholders so you can swap tools to match your team's stack:

| Category | Placeholder | Default | Alternatives |
|----------|-------------|---------|--------------|
| Docs | `~~docs` | Notion | Confluence, Google Docs, Coda |
| Project Tracker | `~~project tracker` | Linear | Jira, Asana, Monday, Shortcut |
| Design Tool | `~~design tool` | Figma | Sketch, Penpot, Adobe XD |
| Deploy Platform | `~~deploy platform` | Vercel | Netlify, Cloudflare Pages, Railway |

**Fixed tools** (not swappable): **Supabase** (backend infrastructure) and **GitHub** (source control).

Use the `cowork-plugin-customizer` skill to swap defaults after installation.

## Repository

Source: [github.com/doumr32-bit/ftwnow](https://github.com/doumr32-bit/ftwnow)

## License

MIT
