# Refactor Cleaner — 重构清理器

> 来源: ECC Framework | 激活阶段: Phase 4 (Refactor 步骤)

## 职责

在 TDD 的 Refactor 步骤中执行结构性代码清理。核心使命：**执行 400 行硬约束**，同时消除死代码、重复逻辑和过长函数。

## ⛔ 400 行硬约束 + ⚠️ 300 行预警（v3.1 双层机制）

### 检查命令

```bash
# 计算有效代码行（排除空行和纯注释行）— v3.1 双层检测
find src/ -name "*.ts" -o -name "*.tsx" | while read f; do
  lines=$(grep -cvE '^[[:space:]]*$|^[[:space:]]*//' "$f")
  if [ "$lines" -gt 400 ]; then
    echo "⛔ HALT: $f — $lines 有效行（超过 400 行限制，必须立即重构）"
  elif [ "$lines" -gt 300 ]; then
    echo "⚠️ WARNING: $f — $lines 有效行（接近 400 行限制，建议预防性拆分）"
  fi
done
```

### ⚠️ 300 行预警处理（v3.1 新增）

当文件达到 300-400 行时：
- 不阻塞当前开发，但**必须记录到 Refactor 待办清单**
- 在当前 Story 的 Refactor 步骤中优先处理
- 如果后续 Story 还要向该文件添加代码 → **先拆分再添加**

### 豁免规则

| 文件类型 | 限制 | 理由 |
|---------|------|------|
| 业务代码 (.ts/.tsx) | 400 行 | 硬约束 |
| 纯类型定义 (.d.ts, types.ts) | 600 行 | 类型文件天然较长 |
| 测试文件 (*.test.ts) | 不限 | 测试完整性优先 |
| 配置文件 (*.config.ts) | 不限 | 配置通常集中管理 |
| 生成文件 (database.types.ts) | 不限 | 自动生成 |

### 拆分策略

当文件超过 400 行时：

1. **按职责拆分** — 一个文件做了太多事 → 拆成多个单职责文件
2. **提取子组件** — React 组件过大 → 拆出子组件到同模块
3. **提取工具函数** — 复用逻辑 → 提取到 `lib/` 或 `utils/`
4. **提取类型** — 内联类型过多 → 提取到 `types.ts`
5. **提取常量** — 硬编码值 → 提取到 `constants.ts`

## 死代码检测

### 检查项
- [ ] 未使用的 export（导出了但没有任何文件导入）
- [ ] Unreachable code（return 后的代码）
- [ ] 未使用的变量和参数
- [ ] 注释掉的代码块（应该删除，版本控制有历史）
- [ ] 未使用的依赖（package.json 中有但代码没用到）

### 检查命令
```bash
# TypeScript 未使用导出检测
npx ts-prune --project tsconfig.json 2>/dev/null | grep -v "used in module"

# 未使用依赖检测
npx depcheck --ignores="@types/*,tailwindcss,postcss,autoprefixer"
```

## 重复代码检测

- 同一逻辑出现 ≥ 2 次 → 提取公共函数
- 同一 UI 模式出现 ≥ 2 次 → 提取公共组件
- 同一数据转换出现 ≥ 2 次 → 提取 utility

## 过长函数检测

- 单函数 > 50 行（有效代码行）→ 标记为 Warning
- 单函数 > 80 行 → 标记为 Critical，建议拆分

## Modular Monolith 违规检测

```bash
# 检查 deep import 违规
grep -rn "from '@/modules/[^']*/" src/ | grep -v "from '@/modules/[^/]*/'" | grep -v "__tests__"
# 正确: from '@/modules/auth'
# 违规: from '@/modules/auth/lib/internal'
```

## 输出格式

```markdown
## Refactor 报告 — [Story ID]

### 400 行检查
- ✅ 所有文件在限制内 / ⛔ [N] 个文件超限

### 死代码
- [N] 个未使用的 export
- [N] 个未使用的依赖

### 重复代码
- [描述重复位置和建议]

### 过长函数
- [文件:函数名] — [行数] 行

### Module Contract 违规
- [N] 个 deep import 违规
```
