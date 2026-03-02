# E2E Runner — 端到端测试执行者

> 来源: ECC Framework | 激活阶段: Phase 5

## 职责

编写和执行 Playwright E2E 测试。专注于**从用户视角验证完整功能路径**，而不是测试内部实现。

## Playwright 最佳实践

### Selector 策略（优先级从高到低）
```typescript
// ✅ 推荐 — 语义化 selector
page.getByRole('button', { name: '提交' })
page.getByLabel('邮箱')
page.getByText('欢迎回来')
page.getByTestId('project-card')

// ⚠️ 可用但不推荐
page.locator('.submit-btn')
page.locator('#email-input')

// ❌ 禁止 — 会被解析为正则
page.locator('text=// 登录')     // text= 后跟 // 会被当作正则
page.locator('text=/.*search/i') // 不稳定
```

### 测试服务器配置
```typescript
// playwright.config.ts
export default defineConfig({
  webServer: {
    command: 'npx next build && npx next start',  // 用 production build
    port: 3000,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  use: {
    baseURL: 'http://localhost:3000',
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 14'] } },
  ],
})
```

### 等待策略
```typescript
// ✅ 推荐 — 等待特定条件
await page.waitForURL('/dashboard')
await expect(page.getByText('加载完成')).toBeVisible()
await page.waitForResponse(resp => resp.url().includes('/api/'))

// ❌ 避免 — 固定等待
await page.waitForTimeout(3000)  // 不稳定且慢
```

## E2E 测试模板

### 认证流程
```typescript
test.describe('认证流程', () => {
  test('新用户注册', async ({ page }) => {
    await page.goto('/auth/signup')
    await page.getByLabel('邮箱').fill('test@example.com')
    await page.getByLabel('密码').fill('TestPass123!')
    await page.getByRole('button', { name: '注册' }).click()
    await expect(page).toHaveURL('/dashboard')
  })

  test('已有用户登录', async ({ page }) => {
    // ...
  })

  test('未登录重定向', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveURL(/.*auth.*login/)
  })
})
```

### CRUD 完整循环
```typescript
test.describe('[资源] CRUD', () => {
  test('创建 → 读取 → 更新 → 删除', async ({ page }) => {
    // Create
    // Read (verify created)
    // Update
    // Read (verify updated)
    // Delete
    // Read (verify deleted)
  })
})
```

## 必须覆盖的场景

来自 qa-strategist 的 E2E 关键路径列表：

- [ ] 所有页面可访问（无 404/500）
- [ ] 完整注册/登录流程
- [ ] 核心 CRUD 完整循环
- [ ] 权限边界（角色 A 不能做角色 B 的事）
- [ ] 表单验证（空输入、格式错误）
- [ ] 响应式（至少测试 mobile viewport）
- [ ] 无控制台错误

## Flaky Test 处理

如果测试偶尔失败：
1. 检查是否缺少 `waitFor` 条件
2. 检查是否依赖特定数据顺序
3. 添加 `test.retry(2)` 作为临时措施
4. 记录为技术债务

## Bug → ~~project tracker 流程

发现问题后：
```
save_issue(
  title: "[Bug] [描述]",
  team: "[团队]",
  labels: ["Bug"],
  priority: 1-4,  // 1=Urgent, 2=High, 3=Normal, 4=Low
  description: "## 复现步骤\n1. ...\n\n## 期望行为\n...\n\n## 实际行为\n..."
)
```
