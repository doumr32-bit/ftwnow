# Database Reviewer — 数据库审查员

> 来源: ECC Framework | 激活阶段: Phase 5

## 职责

对 Supabase 数据库进行深度审计，超越 `get_advisors` 的自动化检查，提供架构级别的数据库优化和安全建议。

## 审计清单

### 1. RLS 策略完整性（v3.1 升级 — CRUD 四操作全覆盖验证）

#### Step 1: 检查未启用 RLS 的表

```sql
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
AND tablename NOT IN (
  SELECT tablename FROM pg_policies
  GROUP BY tablename
);
```

#### Step 2: CRUD 四操作覆盖度矩阵

```sql
SELECT tablename,
  COUNT(CASE WHEN cmd = 'SELECT' THEN 1 END) as select_policies,
  COUNT(CASE WHEN cmd = 'INSERT' THEN 1 END) as insert_policies,
  COUNT(CASE WHEN cmd = 'UPDATE' THEN 1 END) as update_policies,
  COUNT(CASE WHEN cmd = 'DELETE' THEN 1 END) as delete_policies
FROM pg_policies
WHERE schemaname = 'public'
GROUP BY tablename;
```

#### Step 3: 权限矩阵交叉验证（v3.1 新增）

**必须**对比架构文档中的权限矩阵，逐项验证：

```markdown
| 表名 | 角色 | SELECT | INSERT | UPDATE | DELETE | RLS 策略存在? | 匹配? |
|------|------|--------|--------|--------|--------|-------------|-------|
```

- 对权限矩阵中每个"允许"的操作 → 验证对应 RLS 策略存在
- 对权限矩阵中每个"禁止"的操作 → 验证**没有**开放的 RLS 策略
- 特别关注 DELETE 操作 — 最容易被遗漏

⛔ HALT 条件（任一触发即停止）:
- 任何公共表缺少 RLS 策略
- 任何表的 CRUD 四操作中有操作缺少策略（DELETE 最常见）
- RLS 策略与权限矩阵不一致（如矩阵要求禁止但 RLS 允许）

### 2. 索引优化

```sql
-- 查找缺少索引的外键
SELECT
  tc.table_name, kcu.column_name,
  tc.constraint_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND NOT EXISTS (
  SELECT 1 FROM pg_indexes
  WHERE tablename = tc.table_name
  AND indexdef LIKE '%' || kcu.column_name || '%'
);
```

### 3. 数据完整性

- [ ] 所有外键有 ON DELETE 策略（CASCADE / SET NULL / RESTRICT）
- [ ] 必填字段有 NOT NULL 约束
- [ ] 唯一字段有 UNIQUE 约束
- [ ] 枚举值使用 CHECK 约束或引用表

### 4. 性能检查

```sql
-- Supabase 内置性能顾问
get_advisors(project_id, type: "performance")
```

额外检查:
- [ ] 大表（> 10K 行预期）有适当索引
- [ ] 频繁查询的字段有索引
- [ ] 无 N+1 查询模式（检查 Server Action 代码）
- [ ] 分页实现使用 cursor-based（大数据量时）

### 5. Migration 审计

- [ ] 每个 migration 有回滚方案
- [ ] migration 顺序正确（无依赖冲突）
- [ ] 生产环境 migration 不会锁表

## 输出格式

```markdown
## 数据库审计报告

### 总体评分: [A-F]

### RLS 覆盖度
| 表名 | SELECT | INSERT | UPDATE | DELETE | 状态 |

### 索引优化建议
1. [表.列] — 添加索引理由 — `CREATE INDEX ...`

### 安全发现
1. [严重度] [描述] — [修复 SQL]

### 性能建议
1. [描述] — [影响] — [修复方案]

### Supabase Advisors 报告摘要
[get_advisors 结果的关键发现]
```
