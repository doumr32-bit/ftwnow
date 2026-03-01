# 开发日志规则（持续生效规则）

> 来源: FTWNOW v3.2 | 在所有开发阶段持续执行

## 目的

在使用 FTWNOW 开发真实项目时，自动记录详细的结构化日志，为 Skill 的自我迭代优化提供数据基础。

## 日志存储位置

所有日志存储在 FTWNOW 的 GitHub 仓库 `logs/` 目录下，按项目和 Sprint 组织：

```
logs/projects/{project-name}/sprint-{N}/
├── phase-log.jsonl      # 阶段时间线
├── halt-log.jsonl       # HALT 事件记录
├── decision-log.jsonl   # 用户决策记录
└── metrics.json         # Sprint 量化指标汇总
```

## 日志格式（JSONL — 每行一个 JSON 对象）

### 1. phase-log.jsonl — 阶段完成时写入

每个 Phase 完成后立即追加一条记录。Phase 4 的 TDD 循环按 Story 粒度记录子步骤。

```jsonl
{"ts":"ISO-8601","phase":"Phase N","agent":"agent-name","duration_min":25,"gates_total":3,"gates_passed":3,"gates_skipped":0,"halts":0,"artifacts":["产出物列表"],"notes":"简要备注"}
```

**Phase 4 增强记录**（每个 Story 完成时追加）：

```jsonl
{"ts":"ISO-8601","phase":"Phase 4","story_id":"STORY-ID","agent":"tdd-guide","red_duration_min":5,"green_duration_min":8,"refactor_duration_min":4,"review_result":"pass|critical|warning","halts":0,"files_changed":3,"max_file_lines":280,"coverage_delta":"+3%"}
```

### 2. halt-log.jsonl — HALT 触发时立即写入

```jsonl
{"ts":"ISO-8601","phase":"Phase N","trigger":"halt-type","detail":"具体触发信息","file":"涉及文件(可选)","lines":423,"resolution":"resolve|alternative|skip","resolution_detail":"具体解决方案","time_to_resolve_min":12}
```

**trigger 标准值**：
- `400-line-limit` — 文件超 400 行
- `300-line-warning` — 文件超 300 行预警（记录但不阻塞）
- `red-must-fail` — Red 阶段测试未失败
- `assertion-quality` — 断言质量不达标
- `coverage-below-threshold` — 覆盖率不达标
- `implementation-readiness` — 三方对齐检查未通过
- `agentshield-below-b` — 安全评分低于 B
- `critical-in-review` — Code Review 发现 Critical
- `rls-missing` — RLS 策略缺失
- `prd-mapping-gap` — PRD 功能映射缺失
- `crypto-banned` — 使用禁用密码学算法
- `amount-tampering` — 金额防篡改检查失败
- `user-confirmation-pending` — 等待用户确认

### 3. decision-log.jsonl — 用户做关键决策时写入

```jsonl
{"ts":"ISO-8601","phase":"Phase N","decision_type":"type","question":"面临的选择","options":["选项A","选项B"],"chosen":"选项A","reason":"选择原因","user_quote":"用户原话(如有)"}
```

**decision_type 标准值**：
- `architecture` — 架构决策（Modular Monolith、技术选型等）
- `mvp-scope` — MVP 范围决策（砍功能、排优先级）
- `halt-resolution` — HALT 处理方式选择（resolve/alternative/skip）
- `design` — 设计决策（UI 方案、交互模式）
- `security` — 安全方案选择
- `deploy` — 部署相关决策

### 4. metrics.json — Sprint 结束时汇总写入

```json
{
  "sprint": 1,
  "project": "project-name",
  "date": "2026-03-05",
  "duration_days": 5,
  "stories_planned": 8,
  "stories_done": 7,
  "stories_carried": 1,
  "halts_total": 3,
  "halts_by_type": {
    "400-line-limit": 1,
    "red-must-fail": 1,
    "coverage-below-threshold": 1
  },
  "halts_by_phase": {
    "Phase 2": 0,
    "Phase 4": 2,
    "Phase 5": 1
  },
  "coverage": {
    "global": 82,
    "modules": {
      "auth": 91,
      "booking": 85,
      "shared": 65
    }
  },
  "files_total": 24,
  "max_file_lines": 380,
  "files_above_300": 2,
  "security_grade": "B+",
  "deploy_success": true,
  "skipped_gates": [],
  "phase_durations_min": {
    "Phase 0": 5,
    "Phase 1": 25,
    "Phase 2": 40,
    "Phase 2.5": 15,
    "Phase 3": 30,
    "Phase 4": 180,
    "Phase 5": 45,
    "Phase 6": 20,
    "Phase 7": 15
  }
}
```

## 写入时机

| 事件 | 写入内容 | 目标文件 |
|------|---------|---------|
| Phase 完成 | phase-log 一条 | `phase-log.jsonl` |
| ⛔ HALT 触发 | halt-log 一条 | `halt-log.jsonl` |
| ⚠️ 300 行预警 | halt-log 一条（trigger=300-line-warning） | `halt-log.jsonl` |
| 用户关键决策 | decision-log 一条 | `decision-log.jsonl` |
| Phase 4 Story 完成 | phase-log 增强记录一条 | `phase-log.jsonl` |
| Sprint 结束 | metrics 汇总 | `metrics.json` |

## Git 提交策略

日志文件的 git 提交跟随 CLAUDE.MD 的 1000 行自动提交规则。但在以下额外时机也必须提交：

- Sprint 结束时（确保 metrics.json 已推送）
- 项目开发会话结束时（确保当前会话的日志不丢失）

Commit message 格式：`[FTWNOW-LOG] {project-name} Sprint {N} — {简要描述}`

## 禁止记录

- 密码、API Key、Token 等敏感信息
- 用户的私人对话内容（除非用户明确同意的 user_quote）
- 完整的代码片段（只记录文件名和行号）
