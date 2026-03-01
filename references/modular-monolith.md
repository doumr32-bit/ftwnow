# Modular Monolith 架构指南

## 触发条件

当项目满足以下任一条件时，**强制**使用 Modular Monolith 架构：
- ≥ 15 个 Story
- ≥ 6 张数据库表

## 项目结构

```
src/
├── modules/                    # 业务模块（核心）
│   ├── auth/                   # 认证模块
│   │   ├── index.ts            # Public API（唯一导出入口）
│   │   ├── actions/            # Server Actions
│   │   │   ├── login.ts
│   │   │   └── signup.ts
│   │   ├── components/         # 模块专属 UI
│   │   │   ├── login-form.tsx
│   │   │   └── signup-form.tsx
│   │   ├── lib/                # 业务逻辑
│   │   │   ├── validators.ts
│   │   │   └── auth-utils.ts
│   │   ├── hooks/              # 模块的 React Hooks
│   │   │   └── use-auth.ts
│   │   ├── types.ts            # 模块内部类型
│   │   └── __tests__/          # 模块测试
│   │       ├── login.test.ts
│   │       ├── signup.test.ts
│   │       └── fixtures/
│   │           └── seed.ts
│   │
│   ├── [domain-b]/             # 其他业务模块（同结构）
│   │   └── ...
│   │
│   └── shared/                 # 跨模块共享
│       ├── ui/                 # 公共 UI 组件
│       │   ├── button.tsx
│       │   └── form-field.tsx
│       ├── utils/              # 工具函数
│       │   ├── format-date.ts
│       │   └── cn.ts
│       ├── types/              # 共享类型
│       │   ├── database.types.ts  # Supabase 生成
│       │   └── common.ts
│       └── config/             # 共享配置
│           └── constants.ts
│
├── app/                        # Next.js 路由层（薄壳）
│   ├── layout.tsx              # 根布局
│   ├── page.tsx                # 首页
│   ├── (auth)/                 # 认证路由组
│   │   ├── login/page.tsx      # 仅组合 auth 模块组件
│   │   └── signup/page.tsx
│   ├── (dashboard)/            # 仪表盘路由组
│   │   ├── layout.tsx          # 含 auth guard
│   │   └── [feature]/page.tsx
│   └── api/                    # API Routes（如需要）
│
├── lib/                        # 全局基础设施
│   ├── supabase/
│   │   ├── client.ts           # Browser client
│   │   ├── server.ts           # Server client
│   │   └── middleware.ts       # Auth middleware
│   └── constants.ts
│
└── test-setup.ts               # 测试全局配置
```

## Module Contract（强制规则）

### 规则 1: 单一入口

每个模块通过 `index.ts` 导出 public API。外部只能通过此入口访问。

```typescript
// ✅ modules/auth/index.ts
export { loginAction, signupAction } from './actions/login'
export { LoginForm } from './components/login-form'
export { useAuth } from './hooks/use-auth'
export type { AuthUser } from './types'

// ✅ 其他模块使用
import { LoginForm, useAuth } from '@/modules/auth'

// ❌ 禁止 deep import
import { validateEmail } from '@/modules/auth/lib/validators'
```

### 规则 2: shared/ 准入

只有 **≥ 3 个模块** 使用的代码才放入 shared/。

```
2 个模块共用 → 放在其中一个模块中，另一个通过 public API 访问
3+ 个模块共用 → 提取到 shared/
```

### 规则 3: 独立可测

每个模块可以单独运行测试：

```bash
npx vitest run src/modules/auth    # 只跑 auth 模块
npx vitest run src/modules/team    # 只跑 team 模块
```

### 规则 4: app/ 是薄壳

`app/` 目录下的页面文件**只做组合**，不含业务逻辑：

```typescript
// ✅ app/(dashboard)/projects/page.tsx — 薄壳
import { ProjectList } from '@/modules/project'
import { requireAuth } from '@/modules/auth'

export default async function ProjectsPage() {
  await requireAuth()
  return <ProjectList />
}

// ❌ 不要在 app/ 里写业务逻辑
```

## tsconfig.json paths 配置

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/modules/*": ["./src/modules/*"]
    }
  }
}
```

## 模块间通信

模块之间不直接调用内部函数。通过以下方式通信：

1. **Public API 调用**（同步）— `import { X } from '@/modules/other'`
2. **数据库关系**（异步）— 通过外键关联，各模块独立查询
3. **共享类型**（类型层）— 通过 `shared/types/` 共享数据结构

禁止：Event Bus、Pub/Sub（MVP 阶段不需要这种复杂度）
