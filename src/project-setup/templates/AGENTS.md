# AGENTS.md - 项目开发指南

> **使用说明**：此文件是通用模板，使用时需根据实际项目调整以下内容：
> - 将 `<PM>` 替换为实际包管理器（pnpm/yarn/npm/bun）
> - 根据项目类型调整命令和文件结构说明
> - 删除不适用的章节（如非 React 项目删除组件规范）
> - 添加项目特定的规范和约定

## 构建与开发命令

```bash
<PM> dev             # 启动开发服务器
<PM> build           # 生产环境构建
<PM> start           # 启动生产服务器
<PM> lint            # 运行 ESLint
<PM> lint:fix        # 自动修复 ESLint 问题
<PM> type-check      # TypeScript 编译检查（仅 TypeScript 项目）
<PM> test            # 监听模式运行测试
<PM> test:run        # 单次运行测试
<PM> test:ui         # 带 UI 运行测试
<PM> test:coverage   # 生成测试覆盖率报告
<PM> format          # 格式化代码
<PM> format:check    # 检查代码格式
```

说明：本项目使用 Vitest 做单元测试，使用 Prettier 做代码格式化。

## 代码风格规范

### 导入

- 分组：先 React/类型导入，再第三方库，最后本地导入
- 仅类型导入使用 `import type { ... }`
- 使用 `@/` 路径别名表示项目根目录的绝对导入（如果配置）

```ts
'use client'
import type { RefObject } from 'react'
import { useAtom } from 'jotai'
import { Button } from '@/components/ui/button'
```

### 组件（React/Next.js 项目）

- 所有客户端组件顶部添加 `'use client'`
- 在组件上方定义 props 接口：`interface ComponentNameProps { ... }`
- 使用命名导出：`export function ComponentName({ prop }: Props) { ... }`
- 使用函数组件和 Hooks，不用类组件
- 在函数签名中解构 props，便于阅读

### 状态管理（根据项目实际情况调整）

- 全局状态使用 [状态管理库名称]，定义在 `lib/atoms.ts` 或 `store/`
- 用 `const [value, setValue] = use[Hook]()` 读写状态
- 不使用的值用下划线标记：`const [_, setValue] = use[Hook]()`

### 样式

- 使用 Tailwind CSS（或项目实际使用的 CSS 方案）
- 用 `lib/utils.ts` 中的 `cn()` 合并 class
- 组件变体使用 CVA（class-variance-authority）
- 暗色模式用 `dark:` 前缀
- 颜色/选项等常量放在 `constants.ts`，使用 `as const`

### TypeScript

- 开启严格模式，禁止 `any`
- 为所有 props 和数据结构定义接口
- 少用 `as` 断言，优先正确类型
- 适当使用 `?` 可选链做空值检查

### 错误处理

- 异步逻辑用 try-catch 包裹
- 控制台错误带上下文：`console.error('[feature] Error:', error)`
- 异步操作中显式设置 loading 状态
- 数据缺失时优先返回 null，而非抛错

### 文件组织

根据项目类型调整以下结构：

**Next.js App Router 项目**：
- `components/ui/` - 通用 UI 组件（shadcn/ui）
- `components/feature-name/` - 功能组件，带 index.tsx
- `hooks/` - 自定义 React Hooks
- `lib/` - 工具、配置、状态管理
- `app/` - Next.js App Router 页面
- `app/[locale]/` - 国际化路由（如果使用 next-intl）

**Vite 项目**：
- `src/components/` - React 组件
- `src/hooks/` - 自定义 Hooks
- `src/lib/` - 工具函数
- `src/pages/` - 页面组件
- `src/assets/` - 静态资源

**通用 Node.js 项目**：
- `src/` - 源代码
- `tests/` 或 `__tests__/` - 测试文件
- `lib/` - 工具函数
- `config/` - 配置文件

### 国际化（仅适用于使用 next-intl 的 Next.js 项目）

- 使用 next-intl 的 `useTranslations()` 钩子
- 在 `i18n/routing.ts` 配置 locale 路由
- 翻译文件放在 `languages/` 目录
- 用 `t('key')` 获取文案

### 命名约定

- 组件：kebab-case（`photo-editor.tsx`）
- Hooks：kebab-case（`use-image-upload.ts`）
- 工具函数：kebab-case（`format-date.ts`）
- 常量：SCREAMING_SNAKE_CASE（`DEFAULT_CONFIG`）
- 组件文件用 kebab-case，类型/钩子用 camelCase

### 包管理

- 使用 <PM> 管理依赖
- 保持 lockfile 在版本控制中
- 定期更新依赖，注意破坏性变更

### 测试

- 测试文件与源码同目录，后缀 `.test.ts` 或 `.spec.ts`
- 为核心业务逻辑和工具函数编写测试
- 测试描述使用清晰的语言：`it('should handle empty input', () => { ... })`
- 在 `vitest.setup.ts` 或测试文件中 mock 外部依赖
- 目标测试覆盖率：80% 以上

### 代码格式化

- 使用 Prettier 自动格式化代码
- 提交前运行 `<PM> format` 确保代码格式一致
- 配置编辑器保存时自动格式化（推荐）

### 提交前检查

- [ ] 构建通过：`<PM> build`
- [ ] 通过 Lint：`<PM> lint`（或执行 `<PM> lint:fix`）
- [ ] TypeScript 无报错：`<PM> type-check`（TypeScript 项目）
- [ ] 测试通过：`<PM> test:run`
- [ ] 代码已格式化：`<PM> format`
- [ ] 在开发环境中手动验证功能

## 项目特定规范

> **TODO**：在此添加项目特定的规范、约定和最佳实践。
> 例如：API 调用规范、数据库查询规范、安全要求等。
