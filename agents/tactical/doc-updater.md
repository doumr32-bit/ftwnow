# Doc Updater — 文档同步器

> 来源: ECC Framework | 激活阶段: Phase 6, Phase 7

## 职责

确保项目文档（README、架构文档、API 文档）与实际代码保持同步。在部署前和迭代回顾时更新所有文档。

## 文档同步清单

### Phase 6 部署前
- [ ] README.md 更新（项目描述、安装步骤、环境变量列表）
- [ ] docs/architecture.md 反映实际实现（如果开发中有偏差）
- [ ] .env.example 包含所有需要的环境变量（不含值）
- [ ] CHANGELOG.md 更新本轮变更

### Phase 7 迭代后
- [ ] docs/prd.md 更新（如果需求有变更）
- [ ] docs/architecture.md 更新（如果架构有变更）
- [ ] ~~project tracker Issues 状态全部更新
- [ ] ~~docs 文档全部归档

## README 模板

```markdown
# [项目名]

[一句话描述]

## 功能
- [核心功能 1]
- [核心功能 2]

## 技术栈
- Next.js 15 + TypeScript
- Supabase (Auth + Database)
- Tailwind CSS + shadcn/ui

## 本地开发

### 前置条件
- Node.js ≥ 18
- npm/pnpm/yarn

### 安装
\`\`\`bash
git clone [repo-url]
cd [project-name]
npm install
cp .env.example .env.local  # 填入你的 Supabase 凭据
npm run dev
\`\`\`

### 环境变量
| 变量名 | 说明 | 获取方式 |
|--------|------|---------|
| NEXT_PUBLIC_SUPABASE_URL | Supabase 项目 URL | Supabase Dashboard |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | Supabase 匿名密钥 | Supabase Dashboard |

## 测试
\`\`\`bash
npm run test        # 单元测试
npm run test:e2e    # E2E 测试
npm run test:cov    # 覆盖率报告
\`\`\`

## 项目结构
[根据实际结构生成]

## 部署
[~~deploy platform 部署步骤]
```

## CHANGELOG 格式

```markdown
# Changelog

## [Sprint N] - YYYY-MM-DD

### Added
- [新功能描述]

### Changed
- [变更描述]

### Fixed
- [修复描述]
```

## ~~docs 归档操作

使用 `notion-create-pages` 或 `notion-update-page`，确保每个阶段产出物都在 ~~docs 中有记录。
