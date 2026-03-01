# 编码标准（持续生效规则）

> 来源: ECC Rules | 在所有开发阶段持续执行

## 文件结构

- **单文件 ≤ 400 有效代码行**（空行、注释不计）
- 纯类型文件 (.d.ts, types.ts) ≤ 600 行
- 测试文件、配置文件、生成文件不受限制
- 单函数 ≤ 50 行（建议），≤ 80 行（硬限）

## TypeScript

- 严格模式 (`strict: true`)
- 禁止 `any`（使用 `unknown` + 类型收窄）
- 优先 `interface` 定义对象形状，`type` 用于联合/交叉
- 导出的函数必须有返回类型标注
- 使用 `as const` 替代字符串枚举

## React / Next.js

- 函数式组件 + Hooks，不用 class 组件
- 明确 `"use client"` / `"use server"` 边界
- Server Component 作为默认，Client Component 仅在需要交互时使用
- 状态管理: URL state > React Context > Zustand（按需升级）
- 避免 prop drilling > 3 层

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件/文件夹 | kebab-case | `user-profile.tsx` |
| React 组件 | PascalCase | `UserProfile` |
| 函数 | camelCase | `getUserById` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| 类型/接口 | PascalCase | `UserProfile` |
| 环境变量 | UPPER_SNAKE | `NEXT_PUBLIC_API_URL` |

## Import 顺序

```typescript
// 1. 框架/库
import { useState } from 'react'
import { createClient } from '@supabase/supabase-js'

// 2. 内部模块 (公共 API)
import { authService } from '@/modules/auth'

// 3. 同模块相对路径
import { validateEmail } from './lib/validators'
import { UserCard } from './components/user-card'

// 4. 类型 (type-only import)
import type { User } from '@/modules/shared/types'
```

## 错误处理

- Server Action: try-catch + 返回 `{ error: string } | { data: T }`
- React: ErrorBoundary 包裹关键路由
- 异步操作: 始终处理 loading/error/success 三状态
- 用户可见错误信息用中/英文（根据项目语言），不暴露技术细节

## Git 规范

- Commit message: `feat(scope): description` / `fix(scope): description` / `refactor(scope): description`
- 每个 Story 一个 feature branch: `feature/[story-name-kebab]`
- PR 合并用 squash merge
- develop 分支永远可构建
