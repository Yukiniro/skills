---
name: project-setup
description: 为新项目初始化开发工具链和规范配置。包括 AGENTS.md、Prettier 格式化、Vitest 测试、AI agent skills 和 next-intl 国际化。使用场景：初始化新项目、搭建项目脚手架、配置开发工具链。
---

# Project Setup

为新项目快速配置开发工具链、代码规范和 AI agent skills。自动探测项目环境并适配宿主项目的包管理器、框架和已有工具链。

## 使用场景

- 初始化新项目的开发环境
- 为现有项目添加标准化工具链
- 配置代码格式化、测试框架和 AI skills
- 为 Next.js 项目配置国际化支持

## 工作流程

执行以下步骤时，始终先探测环境，再根据实际情况调整配置。

### 步骤 1：环境探测

在执行任何操作前，先收集宿主项目信息：

**检查包管理器**（根据 lockfile 判断）：
- `pnpm-lock.yaml` → 使用 `pnpm add -D`
- `yarn.lock` → 使用 `yarn add -D`
- `package-lock.json` → 使用 `npm install -D`
- `bun.lockb` → 使用 `bun add -D`

**检查项目类型**（读取 `package.json` dependencies）：
- 包含 `next` → Next.js 项目
- 包含 `vite` → Vite 项目
- 其他 → 通用 Node.js 项目

**检查 TypeScript**：
- 存在 `tsconfig.json` → TypeScript 项目（配置文件用 `.ts`）
- 不存在 → JavaScript 项目（配置文件用 `.js` 或 `.mjs`）

**检查已有工具链**（读取 `package.json` devDependencies）：
- `@antfu/eslint-config` + `eslint-plugin-format` → Prettier 已通过 ESLint 集成
- `eslint-plugin-prettier` → Prettier 已通过 ESLint 集成
- `prettier` → 已有独立 Prettier
- `vitest` → 已有 Vitest

**检查构建工具**：
- Vite 项目：检查是否有 `vite.config.ts` / `vite.config.js`

### 步骤 2：创建 AGENTS.md

从 `templates/AGENTS.md` 读取模板，根据探测结果调整：

1. 替换包管理器命令（`pnpm` / `yarn` / `npm` / `bun`）
2. 根据项目类型调整构建命令和文件结构说明
3. 如果是 TypeScript 项目，确保包含 `type-check` 命令
4. 将调整后的内容写入项目根目录的 `AGENTS.md`

### 步骤 3：配置 Prettier

参考 `templates/prettier.config.md`。

**如果已有 ESLint 集成 Prettier**（`@antfu/eslint-config` 或 `eslint-plugin-prettier`）：
- 跳过安装和配置文件创建
- 仅确认 `package.json` 中有 `format` 和 `format:check` scripts
- 如果没有，添加适合 ESLint 集成方案的 scripts

**如果没有 Prettier**：
1. 使用探测到的包管理器安装：`<pm> add -D prettier`
2. 创建 `.prettierrc` 配置文件
3. 创建 `.prettierignore` 忽略文件
4. 在 `package.json` 添加 scripts：
   ```json
   {
     "format": "prettier --write .",
     "format:check": "prettier --check ."
   }
   ```

**如果已有 Prettier**：
- 检查是否有配置文件，如果没有则创建
- 检查是否有 scripts，如果没有则添加

### 步骤 4：配置 Vitest

参考 `templates/vitest.config.md`。

**如果已有 Vitest**：
- 检查是否有配置文件，如果没有则创建
- 检查是否有 test scripts，如果没有则添加

**如果没有 Vitest**：

1. 使用探测到的包管理器安装：
   ```bash
   <pm> add -D vitest @vitest/coverage-v8
   ```

2. 创建配置文件：
   - **Vite 项目**：在 `vite.config.ts` 中添加 test 配置，或创建独立 `vitest.config.ts`
   - **Next.js / 其他项目**：创建独立 `vitest.config.ts` 或 `vitest.config.mjs`
   - 使用 `.ts` 后缀（TypeScript 项目）或 `.mjs` 后缀（JavaScript 项目）

3. 在 `package.json` 添加 scripts：
   ```json
   {
     "test": "vitest",
     "test:run": "vitest run",
     "test:coverage": "vitest run --coverage",
     "test:ui": "vitest --ui"
   }
   ```

4. 可选：创建 `vitest.setup.ts` 用于全局测试配置

### 步骤 5：安装 AI Agent Skills

使用 `npx skills add` 命令安装第三方 skills 到项目级别的 `.cursor/`、`.claude/` 和 `.agents/` 目录。

**重要**：确保在项目根目录执行这些命令。

依次执行以下命令（每条命令单独执行，等待完成后再执行下一条）：

```bash
# 1. Vercel React 最佳实践 + Web 设计指南
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices web-design-guidelines --agent cursor claude-code agents -y

# 2. Frontend 设计指南
npx skills add anthropics/skills --skill frontend-design --agent cursor claude-code agents -y

# 3. shadcn/ui 组件模式
npx skills add giuseppe-trisciuoglio/developer-kit --skill shadcn-ui --agent cursor claude-code agents -y

# 4. Vitest 测试框架
npx skills add antfu/skills --skill vitest --agent cursor claude-code agents -y
```

**注意事项**：
- 这些命令会自动创建 `.cursor/skills/`、`.claude/skills/` 和 `.agents/skills/` 目录
- 如果命令失败，检查网络连接和 npm 配置
- 安装完成后，这些 skills 会在所有支持的 AI agents 中可用

### 步骤 6：配置 next-intl（仅 Next.js 项目）

参考 `templates/next-intl.config.md`。

**仅当项目类型为 Next.js 时执行此步骤。**

1. 使用探测到的包管理器安装：
   ```bash
   <pm> add next-intl
   ```

2. 创建 `i18n/` 目录和配置文件：
   - `i18n/routing.ts` - 定义支持的语言和默认语言
   - `i18n/request.ts` - 配置请求处理
   - `i18n/navigation.ts` - 导出国际化导航组件

3. 创建 `languages/` 目录和翻译文件：
   - `languages/en.json` - 英文翻译
   - `languages/zh-CN.json` - 简体中文翻译
   - 根据需要添加其他语言

4. 更新 `AGENTS.md` 添加国际化相关说明

### 步骤 7：验证清单

完成所有配置后，向用户展示以下清单：

```
✓ 项目设置完成检查清单

环境信息：
- 包管理器：<detected-pm>
- 项目类型：<detected-type>
- TypeScript：<yes/no>

已完成配置：
- [x] AGENTS.md 已创建
- [x] Prettier 已配置（<独立/ESLint集成/已存在>）
- [x] Vitest 已配置（<新安装/已存在>）
- [x] AI Skills 已安装（4 个 skills）
- [x] next-intl 已配置（仅 Next.js）

下一步建议：
1. 运行 `<pm> install` 安装依赖
2. 运行 `<pm> run format` 格式化代码
3. 运行 `<pm> run test` 验证测试配置
4. 查看 AGENTS.md 了解项目规范
```

## 模板文件

本 skill 包含以下模板文件，位于 `templates/` 目录：

- `AGENTS.md` - 项目开发规范模板
- `prettier.config.md` - Prettier 配置参考
- `vitest.config.md` - Vitest 配置参考
- `next-intl.config.md` - next-intl 配置参考

在执行配置时，读取这些模板文件获取详细配置内容。

## 故障排除

### Prettier 与 ESLint 冲突

如果项目同时使用 Prettier 和 ESLint，确保：
- 使用 `@antfu/eslint-config` 时，formatters 选项已启用
- 使用 `eslint-plugin-prettier` 时，已正确配置 extends
- 独立使用 Prettier 时，添加 `.prettierignore` 避免格式化冲突

### Vitest 在 Next.js 中的配置

Next.js 项目需要特殊的 Vitest 配置：
- 使用 `next()` helper 处理 Next.js 特定功能
- 配置路径别名映射（`@/` → `./src/`）
- 设置正确的 test environment（通常是 `node` 或 `jsdom`）

### Skills 安装失败

如果 `npx skills add` 失败：
- 检查网络连接
- 尝试清除 npm 缓存：`npm cache clean --force`
- 手动指定 npm registry：`npm config set registry https://registry.npmjs.org/`
- 查看详细错误信息并根据提示操作

## 最佳实践

1. **环境探测优先**：始终先探测环境，避免假设项目配置
2. **避免覆盖**：检查已有配置，只在缺失时创建新文件
3. **适配包管理器**：使用项目已有的包管理器，保持一致性
4. **渐进式配置**：先配置基础工具，再添加高级功能
5. **验证配置**：配置完成后建议用户运行相关命令验证
