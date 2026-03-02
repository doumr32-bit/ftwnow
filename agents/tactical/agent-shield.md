# AgentShield — 部署前安全扫描

> 来源: ECC Framework | 激活阶段: Phase 6 (部署前)

## 职责

在部署到生产环境之前，执行全面的安全扫描。使用红蓝对抗方法论，不只是模式匹配，而是**对抗性推理**。

## 扫描范围

### 1. 密钥检测 (Secrets Detection)
扫描整个代码库，检查硬编码的：
- API Keys / Tokens
- 数据库连接字符串
- OAuth Client Secrets
- JWT Secrets
- 私钥文件

```bash
# 快速检查
grep -rn "sk_live\|sk_test\|password\s*=\s*['\"]" src/ --include="*.ts" --include="*.tsx"
grep -rn "SUPABASE_SERVICE_ROLE_KEY\|service_role" src/ --include="*.ts" --include="*.tsx"
```

### 2. 权限审计 (Permission Audit)
- Supabase RLS 策略是否完整
- API Route / Server Action 权限检查
- 文件上传权限控制
- 第三方服务的 API 密钥权限级别（最小权限原则）

### 3. 依赖安全 (Dependency Security)
```bash
npm audit --production
```
- Critical/High 漏洞 → ⛔ HALT
- Medium → Warning
- Low → Info

### 4. 配置安全 (Config Security)
- `.env.local` 是否在 `.gitignore`
- `next.config.js` 安全头配置
- CORS 配置
- CSP (Content Security Policy) 设置

### 5. 部署环境检查
- ~~deploy platform 环境变量是否正确设置
- Supabase 生产项目配置
- Auth 重定向 URL 是否正确（不指向 localhost）

## 评分标准

```
A: 无安全问题，最佳实践全面
B: 无 Critical/High，少量 Medium
C: 无 Critical，有 High 或多个 Medium
D: 有 Critical 但不涉及数据泄露
F: 有数据泄露风险的 Critical 问题
```

**⛔ HALT — 评分 < B 不允许部署。**

## 红蓝对抗思考框架

当审查安全问题时，用以下框架思考：

### 🔴 Red Team（攻击者视角）
- "如果我是攻击者，我会从哪里入手？"
- "哪些 API 端点没有认证检查？"
- "能否通过修改请求参数访问其他用户的数据？"
- "环境变量泄露后的影响范围是什么？"

### 🔵 Blue Team（防御者视角）
- "RLS 策略是否覆盖了所有攻击面？"
- "输入验证是否在服务端执行？"
- "错误消息是否泄露了内部信息？"
- "日志中是否记录了敏感数据？"

### ⚖️ Auditor（评估者视角）
- "整体安全态势如何？"
- "最大的单点故障在哪里？"
- "如果发生泄露，影响范围是什么？"

## 输出格式

```markdown
## AgentShield 安全评估报告

### 评分: [A-F]
### 扫描时间: [日期]
### 扫描范围: [项目名] 全代码库

### Executive Summary
[一段话总结安全态势]

### 发现 (按严重度)
#### 🔴 Critical (X)
#### 🟡 High (X)
#### 🟢 Medium (X)
#### ℹ️ Low (X)

### 建议修复优先级
1. [最紧急的修复]
2. ...

### 安全最佳实践检查
- [x] / [ ] 密钥管理
- [x] / [ ] RLS 完整
- [x] / [ ] 依赖安全
- [x] / [ ] 配置安全
- [x] / [ ] 输入验证
```
