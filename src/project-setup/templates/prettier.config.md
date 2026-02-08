# Prettier 配置参考

本文档提供 Prettier 的安装和配置指南，适配不同的项目环境和已有工具链。

## 场景 1：独立使用 Prettier（推荐新项目）

### 安装

使用项目的包管理器安装 Prettier：

```bash
# pnpm
pnpm add -D prettier

# yarn
yarn add -D prettier

# npm
npm install -D prettier

# bun
bun add -D prettier
```

### 配置文件 `.prettierrc`

在项目根目录创建 `.prettierrc` 文件：

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

**配置说明**：
- `semi`: 不使用分号
- `singleQuote`: 使用单引号
- `tabWidth`: 缩进 2 个空格
- `trailingComma`: ES5 兼容的尾随逗号
- `printWidth`: 每行最大 100 字符
- `arrowParens`: 箭头函数参数始终使用括号
- `endOfLine`: 使用 LF 换行符

### 忽略文件 `.prettierignore`

在项目根目录创建 `.prettierignore` 文件：

```
# Dependencies
node_modules
.pnp
.pnp.js

# Build outputs
dist
build
out
.next
.vercel
.turbo

# Cache
.cache
.parcel-cache
.eslintcache

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Editor
.vscode
.idea
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Package manager
pnpm-lock.yaml
yarn.lock
package-lock.json
bun.lockb

# Generated files
*.min.js
*.min.css
coverage
.nyc_output
```

### Package.json Scripts

在 `package.json` 中添加以下 scripts：

```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

**使用方式**：
- `<PM> format` - 格式化所有文件
- `<PM> format:check` - 检查格式但不修改文件（用于 CI）

## 场景 2：Prettier 已通过 ESLint 集成

### 检测方式

检查 `package.json` 的 `devDependencies` 是否包含：
- `@antfu/eslint-config` + `eslint-plugin-format`
- `eslint-plugin-prettier` + `eslint-config-prettier`

### 配置方式

**如果使用 `@antfu/eslint-config`**：

在 `eslint.config.js` 中确认 `formatters: true`：

```js
import antfu from '@antfu/eslint-config'

export default antfu({
  formatters: true,  // 启用 Prettier 集成
  // ... 其他配置
})
```

**如果使用 `eslint-plugin-prettier`**：

在 `.eslintrc.js` 中确认配置：

```js
module.exports = {
  extends: [
    // ... 其他 extends
    'plugin:prettier/recommended',  // 必须放在最后
  ],
}
```

### Package.json Scripts

添加或确认以下 scripts：

```json
{
  "scripts": {
    "format": "eslint --fix .",
    "format:check": "eslint ."
  }
}
```

**注意**：使用 ESLint 集成时，格式化通过 `eslint --fix` 完成。

## 场景 3：项目已有 Prettier

### 检查清单

1. **检查配置文件**：
   - 是否存在 `.prettierrc`、`.prettierrc.json`、`.prettierrc.js` 或 `prettier.config.js`
   - 如果不存在，创建 `.prettierrc` 文件（参考场景 1）

2. **检查忽略文件**：
   - 是否存在 `.prettierignore`
   - 如果不存在，创建 `.prettierignore` 文件（参考场景 1）

3. **检查 Scripts**：
   - 是否有 `format` 和 `format:check` scripts
   - 如果没有，添加到 `package.json`（参考场景 1）

## 编辑器集成（可选但推荐）

### VS Code / Cursor

在项目根目录创建 `.vscode/settings.json`（如果不存在）：

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

**注意**：如果使用 ESLint 集成 Prettier，使用 ESLint 作为 formatter：

```json
{
  "editor.formatOnSave": false,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

## 常见配置选项

### 针对特定文件类型的配置

在 `.prettierrc` 中使用 `overrides`：

```json
{
  "semi": false,
  "singleQuote": true,
  "overrides": [
    {
      "files": "*.md",
      "options": {
        "printWidth": 80,
        "proseWrap": "always"
      }
    },
    {
      "files": "*.json",
      "options": {
        "tabWidth": 2
      }
    }
  ]
}
```

### 与 Tailwind CSS 配合

安装 Tailwind CSS 的 Prettier 插件（可选）：

```bash
<PM> add -D prettier-plugin-tailwindcss
```

在 `.prettierrc` 中添加：

```json
{
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

这会自动排序 Tailwind CSS 类名。

## 验证配置

安装和配置完成后，运行以下命令验证：

```bash
# 检查格式
<PM> format:check

# 格式化代码
<PM> format
```

如果没有错误，说明配置成功。

## 故障排除

### Prettier 与 ESLint 冲突

如果同时使用独立 Prettier 和 ESLint，可能出现格式规则冲突。解决方案：

1. **推荐**：使用 ESLint 集成 Prettier（场景 2）
2. 或者安装 `eslint-config-prettier` 禁用 ESLint 中与 Prettier 冲突的规则：

```bash
<PM> add -D eslint-config-prettier
```

在 `.eslintrc.js` 的 `extends` 数组最后添加：

```js
extends: [
  // ... 其他配置
  'prettier',  // 必须放在最后
]
```

### 格式化速度慢

对于大型项目，可以使用 `--cache` 选项加速：

```json
{
  "scripts": {
    "format": "prettier --write --cache .",
    "format:check": "prettier --check --cache ."
  }
}
```

### 忽略特定代码块

在代码中使用注释忽略格式化：

```js
// prettier-ignore
const matrix = [
  1, 0, 0,
  0, 1, 0,
  0, 0, 1
]
```

或忽略整个文件：

```js
// prettier-ignore-file
```

## 最佳实践

1. **提交前格式化**：配置 Git hooks（使用 husky + lint-staged）在提交前自动格式化
2. **CI 检查**：在 CI 中运行 `format:check` 确保代码格式一致
3. **团队协作**：将 `.prettierrc` 和 `.prettierignore` 纳入版本控制
4. **编辑器集成**：推荐团队成员配置保存时自动格式化
5. **避免混用**：选择独立 Prettier 或 ESLint 集成，不要混用
