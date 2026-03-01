# Deployment Readiness Check — 部署就绪检查

> 执行时机: Phase 6 部署前

## 检查清单

### 1. 代码质量
- [ ] 所有单元测试通过 (`npx vitest run`)
- [ ] 所有 E2E 测试通过 (`npx playwright test`)
- [ ] 覆盖率达标 (`npx vitest run --coverage`)
- [ ] 无 400 行超限文件
- [ ] 构建成功 (`npm run build`)

### 2. 安全
- [ ] AgentShield 评分 ≥ B
- [ ] `npm audit --production` 无 Critical/High
- [ ] RLS 策略覆盖所有公共表
- [ ] 无硬编码密钥
- [ ] `.env.local` 在 `.gitignore`

### 3. 数据库
- [ ] 所有 migration 已应用
- [ ] Supabase `get_advisors` 安全+性能无 Critical
- [ ] 索引策略已实施
- [ ] 测试数据已清除

### 4. 配置
- [ ] Vercel 环境变量已设置
- [ ] Supabase Auth URL 已配置（Site URL + Redirect URLs）
- [ ] CORS 配置正确
- [ ] `.env.example` 已更新

### 5. 文档
- [ ] README.md 已更新
- [ ] CHANGELOG.md 已更新
- [ ] docs/ 反映实际实现

### 6. 部署验证（部署后）
- [ ] 网站可访问（HTTP 200）
- [ ] 首页正常渲染
- [ ] 登录页面可访问
- [ ] 核心功能冒烟测试
- [ ] 无控制台报错

## ⛔ HALT 条件

- AgentShield 评分 < B → 修复安全问题后重跑
- 任何测试失败 → 修复后重跑
- 构建失败 → 修复后重跑
