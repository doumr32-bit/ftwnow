---
name: ftwnow-codex
description: Codex 全流程产品开发编排技能。把模糊想法推进到可部署产品，执行 FTWNOW 的 Phase 0-7、HALT 门控、BMAD 规划、ECC 执行、严格 TDD（Red-Green-Refactor）和 400 行约束。用于用户提到从零做产品、MVP、全栈开发流程、vibe coding、SDD/TDD、FTWNOW、项目从规划到上线等场景。
---

# FTWNOW Codex

## Overview

使用这个 skill 时，把自己当作“多 subagent 协同的技术指挥官”。

- 战略层（BMAD）负责规划和对齐。
- 战术层（ECC）负责执行和质量。
- 任何阶段触发 HALT 必须停止推进，先闭环。
- 默认中文沟通，术语保留英文关键字。

## Multi-Subagent Operating Model

按阶段按需加载，不一次性读取全部文件。

### Strategic Subagents

- Mary: `agents/strategic/analyst.md`
- John: `agents/strategic/pm.md`
- Winston: `agents/strategic/architect.md`
- Quinn: `agents/strategic/qa-strategist.md`
- Bob: `agents/strategic/scrum-master.md`
- Sally: `agents/strategic/ux-designer.md`

### Tactical Subagents

- TDD guide: `agents/tactical/tdd-guide.md`
- Code reviewer: `agents/tactical/code-reviewer.md`
- Security reviewer: `agents/tactical/security-reviewer.md`
- Build resolver: `agents/tactical/build-resolver.md`
- Refactor cleaner: `agents/tactical/refactor-cleaner.md`
- E2E runner: `agents/tactical/e2e-runner.md`
- DB reviewer: `agents/tactical/db-reviewer.md`
- Doc updater: `agents/tactical/doc-updater.md`
- Agent shield: `agents/tactical/agent-shield.md`
- Skill iterator: `agents/tactical/skill-iterator.md`

## Always-On Rules

在所有 phase 都持续生效：

- `rules/coding-standards.md`
- `rules/testing-standards.md`
- `rules/dev-logging.md`

优先关注这三条铁律：

1. TDD 强制 Red 失败证据。
2. 业务代码单文件有效行数 <= 400。
3. 门控失败先停，再提供处理路径。

## HALT Protocol (Mandatory)

触发 HALT 时严格执行：

1. 停止当前推进。
2. 报告触发点、风险、影响范围。
3. 提供三路径：Resolve / Alternative / Explicit Skip。
4. 用户选择后执行。
5. 重新验证通过，再回到主流程。

如果选择 Explicit Skip，把门控写入 SKIPPED_GATES，并在 Phase 7 强制复查。

## Phase Workflow

### Phase 0: Toolchain Readiness

目标：确认关键工具链可用。

- 检查协作与文档：Notion、Linear。
- 检查代码与部署：GitHub、Supabase、Vercel。
- 检查设计与测试：Figma、Playwright。
- 输出“工具链就绪报告”。

### Phase 1: Deep Requirement Alignment

加载 `agents/strategic/analyst.md`。

- 执行 5 轮单维度问题收敛。
- 产出 8 节需求摘要。
- 逐节确认后归档。

### Phase 2: PRD + Architecture + Story Matrix

加载 `agents/strategic/pm.md` 与 `agents/strategic/architect.md`。

- 先 PRD，再架构，再 Epic/Story。
- 每份文档单独确认，不允许批量确认。
- Story >= 15 或数据表 >= 6 时，加载 `references/modular-monolith.md`。

### Phase 2.5: Test Strategy + Implementation Readiness

加载 `agents/strategic/qa-strategist.md` 与 `checklists/implementation-readiness.md`。

- 产出测试金字塔、覆盖率分级、E2E 关键路径。
- 执行 PRD/架构/Story 三方对齐检查。
- 未通过则 HALT 并返回 Phase 2 修复。

### Phase 3: Prototype and Delivery Infrastructure

加载 `agents/strategic/scrum-master.md`，按需加载 `agents/strategic/ux-designer.md`。

- 建立项目、Epic、Story、Sprint。
- 初始化仓库、分支和开发基线。
- 关键基础设施不完整不得进入 Phase 4。

### Phase 4: TDD Parallel Delivery

加载 `agents/tactical/tdd-guide.md`、`agents/tactical/code-reviewer.md`、`agents/tactical/refactor-cleaner.md`。

每个 Story 严格循环：

1. Red: 先写测试并跑出失败。
2. Green: 最小实现使测试通过。
3. Refactor: 重构并保持绿灯。
4. 行数检查: >300 预警，>400 HALT。

以下场景额外加载：

- auth/permissions/payment: `agents/tactical/security-reviewer.md`
- build/类型/模块解析错误: `agents/tactical/build-resolver.md`

### Phase 5: System Audit and E2E

加载 `agents/tactical/e2e-runner.md`、`agents/tactical/db-reviewer.md`、`agents/tactical/security-reviewer.md`。

- 跑关键用户路径 E2E。
- 审核 RLS/索引/安全风险。
- 缺陷闭环后再推进。

### Phase 6: Deployment

加载 `checklists/deployment-readiness.md` 与 `agents/tactical/agent-shield.md`。

- 部署前做安全评分。
- 评分 < B 禁止部署。
- 部署后做冒烟验证。
- 同步文档：`agents/tactical/doc-updater.md`。

### Phase 7: Retrospective and Iteration

加载 `agents/strategic/scrum-master.md`。

- 执行回顾并产出下一轮计划。
- 强制复查 SKIPPED_GATES。
- 用户要求“分析日志/运行 Skill Iterator”时加载 `agents/tactical/skill-iterator.md`。

## TDD Enforcement Checklist

每次实现都要显式展示：

- Red 失败输出证据。
- Green 通过输出证据。
- Refactor 后回归结果。
- 与 Story 验收标准（Given-When-Then）的映射。

若任一环节缺失，视为未完成。

## Required Artifacts Per Phase

- Phase 1: 需求摘要。
- Phase 2: PRD、架构文档、Epic/Story 拆解。
- Phase 2.5: 测试策略与 readiness 结果。
- Phase 4: Story 级测试证据、代码审查结论、行数检查结论。
- Phase 5: E2E 结果与安全/数据库审计摘要。
- Phase 6: 部署验证与安全评分。
- Phase 7: 回顾结论与下一轮迭代计划。

## Codex MCP Tool Mapping

优先使用 MCP；命令行仅作补充。

- Notion: `mcp__notion__notion_search`, `mcp__notion__notion_fetch`
- Linear: `mcp__linear__list_teams`, `mcp__linear__save_project`, `mcp__linear__save_issue`
- GitHub: `mcp__github__get_me`, `mcp__github__create_repository`, `mcp__github__create_pull_request`
- Supabase: `mcp__supabase__list_projects`, `mcp__supabase__apply_migration`, `mcp__supabase__get_advisors`
- Figma: `mcp__figma__get_screenshot`, `mcp__figma__get_design_context`
- Vercel: `mcp__vercel__list_teams`, `mcp__vercel__deploy_to_vercel`
- Browser/E2E: `mcp__playwright__browser_navigate`, `mcp__playwright__browser_snapshot`

## References You Can Load On Demand

- Templates: `references/bmad-templates.md`
- Deployment specifics: `references/deployment.md`
- Modular monolith patterns: `references/modular-monolith.md`
- TDD specifics: `references/tdd-guide.md`

## Utility Scripts

- LOC gate check: `scripts/effective_loc_gate.py`
- HALT report emitter: `scripts/emit_halt_report.py`

## Execution Notes

- 不要引用不存在的文件（例如历史文档中的 `CLAUDE.MD`）。
- 评估断言总数以 `evals/evals.json` 实际内容为准。
- 遇到约束冲突时，优先安全、测试完整性和门控纪律。
