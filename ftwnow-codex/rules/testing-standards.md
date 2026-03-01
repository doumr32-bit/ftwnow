# 测试标准（持续生效规则）

> 来源: ECC Rules + BMAD TEA Module

## TDD 纪律

1. **Red 必须失败** — 写完测试后必须运行，必须看到红色输出
2. **Green 最小实现** — 只写让测试通过的最少代码
3. **Refactor 保绿** — 每次重构后重跑测试
4. **覆盖率检查** — 每个 Sprint 结束跑 `npx vitest run --coverage`

## 覆盖率目标（分级）

| 模块风险等级 | 覆盖率目标 | 典型模块 |
|------------|-----------|---------|
| 🔴 高风险 | ≥ 90% | auth, payment, permissions |
| 🟡 中风险 | ≥ 80% | 核心业务模块 |
| 🟢 低风险 | ≥ 60% | UI 组件, 工具函数 |
| 全局 | ≥ 80% | 整个项目 |

## 测试文件组织

```
src/modules/[module]/__tests__/
├── [feature].test.ts       # 单元测试
├── [feature].integration.ts # 集成测试（含 DB 交互）
└── fixtures/
    └── seed.ts             # 测试数据
tests/
└── e2e/
    ├── [flow].e2e.ts       # E2E 测试
    └── helpers/
        └── auth.ts         # E2E 辅助函数
```

## 测试命名

```typescript
describe('[模块/功能名]', () => {
  test('should [预期行为] when [条件]', () => {})
  // 或
  test('Given [前提] When [操作] Then [结果]', () => {})
})
```

## Bug 修复规则

修复 Bug 时：
1. **先写回归测试**（Red — 复现 Bug）
2. 修复代码（Green — 测试通过）
3. 跑全量测试（确认无回归）
