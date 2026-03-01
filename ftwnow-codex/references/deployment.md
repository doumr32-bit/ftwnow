# 部署指南 — Vercel + Supabase

## Supabase 设置流程

### 1. 创建项目

使用 Supabase MCP 工具：
- 确认用户的 Organization
- 选择就近区域
- 等待项目初始化完成

### 2. 数据库表创建

根据 architecture.md 中的数据模型，使用 `apply_migration` 创建表。

标准表结构示例：
```sql
-- 用户配置表（Supabase Auth 会自动创建 auth.users）
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE,
  display_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 启用 RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- RLS 策略：用户只能读写自己的数据
CREATE POLICY "用户可以查看所有公开资料"
  ON public.profiles FOR SELECT
  USING (true);

CREATE POLICY "用户只能编辑自己的资料"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);
```

### 3. RLS 策略原则

向用户解释："RLS 就像数据库的门禁系统 — 确保每个用户只能看到和修改属于自己的数据。"

核心原则：
- 每张表都要开启 RLS
- SELECT 策略：谁能看到这些数据？
- INSERT 策略：谁能添加数据？
- UPDATE 策略：谁能修改数据？
- DELETE 策略：谁能删除数据？

### 4. Authentication 配置

通过 Supabase Dashboard 引导用户：
- 启用邮箱/密码登录
- 可选：配置第三方登录（Google、GitHub 等）
- 设置邮件模板（确认邮件、重置密码邮件）

### 5. 环境变量

```env
# .env.local（本地开发）
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...  # 仅服务端使用
```

---

## Vercel 部署流程

### 1. 准备工作

确认以下文件存在且配置正确：
- `next.config.js` — Next.js 配置
- `package.json` — 依赖和脚本
- `.env.local` — 环境变量（不上传到 Git）

### 2. 连接部署

引导用户操作：

1. 访问 vercel.com，用 GitHub 账号登录
2. 点击 "Import Project"
3. 选择项目仓库
4. 配置环境变量（从 .env.local 复制）
5. 点击 Deploy

或者使用 Vercel CLI：
```bash
npm i -g vercel
vercel login
vercel --prod
```

### 3. 部署后验证清单

自动执行的检查：
```
✅ 网站可访问（HTTP 200）
✅ 首页正常渲染
✅ 登录页面可访问
✅ 注册流程正常
✅ 数据库连接正常（可读写）
✅ 静态资源加载正常
✅ 无控制台错误
✅ 移动端布局正常
```

### 4. 自定义域名

如果用户有自己的域名：
1. 在 Vercel 项目设置中添加域名
2. 按指引配置 DNS 记录
3. 等待 SSL 证书自动签发
4. 验证域名生效

---

## 部署故障排除

| 问题 | 常见原因 | 解决方案 |
|------|---------|---------|
| Build 失败 | TypeScript 类型错误 | 检查 build 日志，修复类型错误 |
| 环境变量缺失 | 未在 Vercel 配置 | 在 Project Settings → Environment Variables 添加 |
| 数据库连接失败 | Supabase URL 错误 | 确认环境变量值正确 |
| 页面 404 | 路由配置问题 | 检查 app/ 目录结构 |
| API 超时 | Serverless 函数超时 | 优化数据库查询或增加超时时间 |
