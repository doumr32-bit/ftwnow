# Implementation Readiness Check — 开发就绪检查

> 来源: BMAD Framework | 执行时机: Phase 2 → Phase 3 之间

## 目的

确保 PRD、架构文档、Epic/Story 三方对齐。避免"文档说一套，开发做一套"。

## 检查清单

### 1. PRD ↔ 架构对齐
- [ ] 每个 PRD P0/P1 功能在架构文档中有对应的技术方案
- [ ] 数据模型（PRD 版本）与数据库设计（架构版本）一致
- [ ] 页面路由（PRD）与项目结构（架构）对应
- [ ] 非功能需求有对应的技术实现方案

### 2. 权限矩阵完整性
- [ ] 每个角色定义明确
- [ ] 每个资源（表/API/页面）对每个角色有 CRUD 权限定义
- [ ] RLS 策略草案覆盖权限矩阵中的所有规则
- [ ] 前端路由权限与后端权限一致

### 3. Story 可开发性
- [ ] 每个 Story 有 Given-When-Then 验收标准
- [ ] 每个 Story 有预估的文件变更范围
- [ ] Story 之间的依赖关系已标记
- [ ] Sprint 1 的所有 Story 没有外部阻塞依赖

### 4. 技术可行性
- [ ] 所有需要的 Supabase 功能已确认可用（Auth, Storage, RLS, Edge Functions）
- [ ] 第三方集成方案已确认（如有）
- [ ] 性能瓶颈已识别并有应对方案

### 5. 安全方案
- [ ] 认证方案完整（注册/登录/登出/忘记密码）
- [ ] RLS SELECT 策略设计覆盖所有表（v3.1 拆细）
- [ ] RLS INSERT 策略设计覆盖所有表（v3.1 拆细）
- [ ] RLS UPDATE 策略设计覆盖所有表（v3.1 拆细）
- [ ] RLS DELETE 策略设计覆盖所有表（v3.1 拆细 — 最易遗漏）
- [ ] 敏感数据处理方案已定义
- [ ] API 权限检查方案已定义
- [ ] 涉及支付的金额字段有服务端验证方案（v3.1 新增）

### 6. Modular Monolith（如触发）
- [ ] 模块边界已定义
- [ ] Module Contract 已写入架构文档
- [ ] 每个模块的 public API 已设计
- [ ] shared/ 的内容已确定

## ⛔ HALT 条件

任何检查项未通过 → ⛔ HALT → 回到 Phase 2 补充对应文档 → 重新检查

## 执行方式

Architect (Winston) 执行此检查，对比 PRD 和架构文档，逐项验证。如发现不一致，指出具体矛盾点并提供修复建议。
