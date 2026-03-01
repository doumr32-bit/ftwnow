# FTWNOW 开发日志系统

## 概述

本目录存储使用 FTWNOW 方法论开发真实项目时自动生成的结构化日志。日志数据用于驱动 Skill Iterator Agent 对 FTWNOW 进行数据驱动的迭代优化。

## 目录结构

```
logs/
├── README.md                     # 本文件
├── projects/                     # 按项目组织的日志
│   └── {project-name}/           # 项目名（kebab-case）
│       └── sprint-{N}/           # Sprint 编号
│           ├── phase-log.jsonl   # 阶段时间线
│           ├── halt-log.jsonl    # HALT 事件记录
│           ├── decision-log.jsonl # 用户决策记录
│           └── metrics.json      # Sprint 量化指标汇总
└── skill-iterations/             # Skill Iterator 分析报告
    └── iter-{NNN}.md             # 迭代分析报告
```

## 日志类型

| 文件 | 格式 | 写入时机 | 用途 |
|------|------|---------|------|
| `phase-log.jsonl` | JSONL | 每个 Phase 完成 + Phase 4 每个 Story 完成 | 流程效率分析 |
| `halt-log.jsonl` | JSONL | 每次 HALT 触发 + 300行预警 | HALT 模式识别 |
| `decision-log.jsonl` | JSONL | 用户做关键决策时 | 决策模式分析 |
| `metrics.json` | JSON | Sprint 结束时 | 量化趋势追踪 |

## 如何使用

### 自动记录

使用 FTWNOW 开发项目时，日志按 `rules/dev-logging.md` 的规则自动写入。无需手动操作。

### 触发迭代分析

当你希望根据日志优化 FTWNOW 时：
1. 确保至少有 1 个项目的 1 个 Sprint 完整日志
2. 告诉 Claude："分析日志，运行 Skill Iterator"
3. Skill Iterator Agent 会读取全部 skill 文件 + 日志数据
4. 输出带证据链的修改建议报告

### 数据积累建议

- 1-2 个项目：定性分析，参考价值有限
- 3+ 个项目或 5+ 个 Sprint：趋势分析可用
- 10+ Sprint / 3+ 项目：全面统计分析 + 跨项目对比

## 隐私

日志中**不包含**：密码、API Key、Token、完整代码片段、用户私人对话内容。详见 `rules/dev-logging.md` 的"禁止记录"节。
