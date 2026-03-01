# TDD 开发指南 v2

## TDD 是什么？（给零基础用户的解释）

TDD（测试驱动开发）就像先写考试答案，再去学习怎么答题：

1. 🔴 **Red**：先写一个"考试题目"（测试），**运行它，看到失败** — 这很重要！如果题目还没学就能答对，说明题目太简单了
2. 🟢 **Green**：写最少的代码让"考试"通过
3. 🔄 **Refactor**：答案对了以后，把代码整理得更漂亮，**再跑一次确认还是对的**

为什么这样做？因为这样写出来的每一行代码都有明确的目的，不会写出没用的代码，也不会遗漏功能。

---

## Red 阶段的三个微步骤

Red 是 TDD 的灵魂。很多团队号称做 TDD 但其实只是"写了测试" — 如果你不运行测试看到失败，你就不知道测试是否真的在检查什么。

### 微步骤 1: 写测试
根据 Story 的 Given-When-Then 验收标准编写测试用例。

### 微步骤 2: 运行测试
```bash
npx vitest run --reporter=verbose [测试文件路径]
```

### 微步骤 3: 确认失败
你必须看到类似这样的输出：
```
❌ FAIL  tests/unit/todo-list.test.tsx
  ✗ renders todo items — Error: Cannot find module '@/components/todo-list'
  ✗ adds new todo — Error: Cannot find module '@/components/todo-list'

Tests: 2 failed, 0 passed
```

**如果测试意外全部通过**，说明：
- 测试引用了已存在的代码（不是新功能）
- 测试的断言太宽松（比如只检查组件存在，没检查内容）
- 测试文件路径有误

此时 ⛔ HALT，修改测试直到看到失败。

---

## TypeScript + Next.js 的 TDD 工具栈

### 单元测试和集成测试：Vitest

```bash
# 安装
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom @vitejs/plugin-react

# vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'text-summary', 'html'],
      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80,
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    }
  }
})
```

### 覆盖率检查

Phase 4 完成时必须运行覆盖率报告：

```bash
npx vitest run --coverage
```

预期看到类似输出：
```
------------|---------|----------|---------|---------|
File        | % Stmts | % Branch | % Funcs | % Lines |
------------|---------|----------|---------|---------|
All files   |   85.2  |   82.1   |   88.5  |   84.7  |
------------|---------|----------|---------|---------|
```

如果任何指标低于 80%，⛔ HALT 补充测试。

### E2E 测试：Playwright

```bash
# 安装
npm install -D @playwright/test
npx playwright install chromium

# playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  webServer: {
    command: 'npx next start',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 30000,
  },
})
```

注意：使用 `npx next start`（预构建的生产服务器）而不是 `npm run dev`（开发服务器），因为开发服务器在 CI 或受限环境中可能启动超时。

### Playwright 选择器最佳实践

优先使用语义化选择器，避免 `text=//` 格式（会被 Playwright 解析为正则表达式）：

```typescript
// ✅ 推荐
page.getByText('登录')
page.getByRole('button', { name: '提交' })
page.getByLabel('邮箱')
page.getByPlaceholder('请输入密码')

// ❌ 避免
page.locator('text=// 登录')  // 会被解析为正则
page.locator('.btn-primary')   // 脆弱的 CSS 选择器
```

---

## TDD 实战模式

### 模式 1：React 组件 TDD

**Story**: "用户可以看到一个登录表单，包含邮箱和密码输入框和提交按钮"

**🔴 Red**: 写测试
```typescript
// tests/unit/login-form.test.tsx
import { render, screen } from '@testing-library/react'
import { LoginForm } from '@/components/features/login-form'

describe('LoginForm', () => {
  it('renders email input', () => {
    render(<LoginForm />)
    expect(screen.getByLabelText(/邮箱/i)).toBeInTheDocument()
  })

  it('renders password input', () => {
    render(<LoginForm />)
    expect(screen.getByLabelText(/密码/i)).toBeInTheDocument()
  })

  it('renders submit button', () => {
    render(<LoginForm />)
    expect(screen.getByRole('button', { name: /登录/i })).toBeInTheDocument()
  })
})
```

运行 → 看到 `Cannot find module '@/components/features/login-form'` → ✅ 确认 Red

**🟢 Green**: 写最少的代码让测试通过

**🔄 Refactor**: 优化组件结构 → 重跑测试确认仍然通过

### 模式 2：API 路由 TDD

**🔴 Red**:
```typescript
// tests/integration/api/users.test.ts
describe('POST /api/users', () => {
  it('creates a user and returns id', async () => {
    const res = await fetch('http://localhost:3000/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@test.com', name: 'Test' }),
    })
    const data = await res.json()
    expect(res.status).toBe(201)
    expect(data.id).toBeDefined()
  })
})
```

### 模式 3：Supabase 数据操作 TDD

```typescript
// tests/integration/supabase/profiles.test.ts
import { createClient } from '@supabase/supabase-js'

describe('Profiles table', () => {
  it('can insert and retrieve a profile', async () => {
    const { data, error } = await supabase
      .from('profiles')
      .insert({ username: 'testuser', bio: 'Hello' })
      .select()
      .single()

    expect(error).toBeNull()
    expect(data.username).toBe('testuser')
  })
})
```

---

## 并行开发 Agent Team 模式

当项目有多个独立的 Epic 时，可以启动多个 Agent 并行开发：

```
主 Agent（你）
├── Sub-Agent 1: Epic A — 用户认证模块
│   └── feature/auth 分支 → TDD 循环 → PR
├── Sub-Agent 2: Epic B — 仪表盘模块
│   └── feature/dashboard 分支 → TDD 循环 → PR
└── Sub-Agent 3: Epic C — 设置页面
    └── feature/settings 分支 → TDD 循环 → PR
```

每个 Sub-Agent 收到的指令应包含：
1. 需要实现的 Story 列表（含验收标准）
2. 相关的架构文档片段
3. 分支名称
4. TDD 流程要求（强调 Red 必须看到失败）

合并顺序：按 Story 的依赖关系，先合并被依赖的模块。

---

## 覆盖率目标

| 测试类型 | 目标覆盖率 | 说明 |
|---------|-----------|------|
| 单元测试 | ≥ 80% | 核心业务逻辑（vitest --coverage 验证） |
| 集成测试 | 关键路径 | API 路由 + 数据库操作 |
| E2E 测试 | 核心用户流程 | 注册→使用→退出 |

运行覆盖率报告：
```bash
npx vitest run --coverage
```

⛔ 低于 80% 时不能进入 Phase 5。
