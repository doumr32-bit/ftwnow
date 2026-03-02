# BMAD 模板参考

## PRD 模板

```markdown
# 产品需求文档 (PRD) — [项目名称]

## 1. 产品概述
### 1.1 产品愿景
[一段话描述这个产品是什么、为谁服务、解决什么问题]

### 1.2 目标用户
| 用户角色 | 描述 | 核心需求 |
|---------|------|---------|
| [角色1] | [画像描述] | [他们最需要什么] |

### 1.3 成功标准
- [ ] [可量化指标1]
- [ ] [可量化指标2]

## 2. 功能需求

### 功能 1: [功能名称]
**用户故事**: 作为[角色]，我想要[做什么]，以便[获得什么价值]

**验收标准**:
- Given [前提条件], When [用户操作], Then [预期结果]
- Given [前提条件], When [用户操作], Then [预期结果]

**优先级**: P0 (MVP必须) / P1 (重要) / P2 (可选)

### 功能 2: [功能名称]
...

## 3. 非功能需求
- **性能**: 页面加载 < 3秒
- **安全**: 用户数据加密存储，HTTPS 强制
- **可访问性**: 支持键盘导航，合理的颜色对比度
- **响应式**: 支持桌面（1200px+）、平板（768px+）、手机（375px+）

## 4. 数据模型

| 实体 | 字段 | 类型 | 说明 |
|------|------|------|------|
| User | id | UUID | 唯一标识 |
| User | email | String | 登录邮箱 |
| ... | ... | ... | ... |

## 5. 页面路由

| 路由 | 页面 | 核心功能 | 是否需要登录 |
|------|------|---------|------------|
| / | 首页 | [描述] | 否 |
| /dashboard | 仪表盘 | [描述] | 是 |
| ... | ... | ... | ... |
```

## 技术架构模板

```markdown
# 技术架构文档 — [项目名称]

## 1. 技术栈

| 层级 | 技术选择 | 说明 |
|------|---------|------|
| 前端框架 | Next.js 15 (App Router) | React 全栈框架 |
| 语言 | TypeScript | 类型安全 |
| 样式 | Tailwind CSS | 工具类 CSS |
| UI 组件 | shadcn/ui | 可定制组件库 |
| 数据库 | Supabase (PostgreSQL) | 托管数据库 + 认证 |
| 部署 | ~~deploy platform | 自动部署 |
| 测试 | Vitest + Playwright | 单元测试 + E2E |

## 2. 项目结构

```
项目根目录/
├── src/
│   ├── app/              # Next.js App Router 页面
│   │   ├── (auth)/       # 需要登录的页面
│   │   ├── (public)/     # 公开页面
│   │   └── api/          # API 路由
│   ├── components/       # 可复用组件
│   │   ├── ui/           # shadcn/ui 基础组件
│   │   └── features/     # 业务功能组件
│   ├── lib/              # 工具函数和配置
│   │   ├── supabase/     # Supabase 客户端
│   │   └── utils/        # 通用工具
│   ├── hooks/            # 自定义 React Hooks
│   └── types/            # TypeScript 类型定义
├── tests/
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── e2e/              # 端到端测试
├── docs/                 # 项目文档
└── public/               # 静态资源
```

## 3. 架构决策记录 (ADR)

### ADR-001: 为什么选择 Next.js App Router
**背景**: 需要一个支持服务端渲染的 React 框架
**决策**: 使用 Next.js 15 的 App Router
**原因**: App Router 是 Next.js 推荐的新路由方案，支持 React Server Components，更好的性能和 SEO
**后果**: 需要学习 App Router 的 layout/page 约定

### ADR-002: 为什么选择 Supabase
**背景**: 需要数据库、用户认证和文件存储
**决策**: 使用 Supabase 作为 Backend-as-a-Service
**原因**: 一站式解决后端需求，免费额度够用，有 MCP 支持，开发者体验好
**后果**: 与 Supabase 平台绑定

## 4. 环境变量

| 变量名 | 用途 | 来源 |
|--------|------|------|
| NEXT_PUBLIC_SUPABASE_URL | Supabase 项目 URL | Supabase Dashboard |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | Supabase 公钥 | Supabase Dashboard |
| SUPABASE_SERVICE_ROLE_KEY | Supabase 服务端密钥 | Supabase Dashboard |
```

## Epic & Story 模板

```markdown
# Epic: [Epic 名称]

## 描述
[这个功能模块要实现什么]

## Stories

### Story 1: [Story 标题]
**优先级**: P0
**复杂度**: 简单 / 中等 / 复杂
**估算**: [Story Points 或时间]

**描述**: 作为[角色]，我想要[做什么]，以便[价值]

**验收标准**:
- [ ] Given [条件], When [操作], Then [结果]
- [ ] Given [条件], When [操作], Then [结果]

**技术备注**:
- 涉及文件: [列出需要修改/创建的文件]
- 依赖: [依赖哪些其他 Story]

**测试策略**:
- 单元测试: [测什么]
- 集成测试: [测什么]
```
