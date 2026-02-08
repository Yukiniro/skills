# Vitest 配置参考

本文档提供 Vitest 的安装和配置指南，适配不同的项目类型和构建工具。

## 安装依赖

使用项目的包管理器安装 Vitest 和覆盖率工具：

```bash
# pnpm
pnpm add -D vitest @vitest/coverage-v8

# yarn
yarn add -D vitest @vitest/coverage-v8

# npm
npm install -D vitest @vitest/coverage-v8

# bun
bun add -D vitest @vitest/coverage-v8
```

**可选依赖**（根据需要安装）：

```bash
# UI 界面
<PM> add -D @vitest/ui

# 浏览器环境测试
<PM> add -D jsdom
# 或
<PM> add -D happy-dom

# React 组件测试
<PM> add -D @testing-library/react @testing-library/jest-dom
```

## 配置方式 1：Vite 项目（推荐）

### 在 vite.config.ts 中集成

如果项目已有 `vite.config.ts`，直接在其中添加 test 配置：

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.ts',
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        'tests/',
      ],
    },
  },
})
```

### 或创建独立 vitest.config.ts

如果想分离配置，创建独立的 `vitest.config.ts`：

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.ts',
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        'tests/',
      ],
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
```

## 配置方式 2：Next.js 项目

Next.js 项目需要特殊配置以支持 Next.js 特性。

### vitest.config.ts

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.ts',
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        '.next/',
        'out/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        'tests/',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/components': path.resolve(__dirname, './src/components'),
      '@/lib': path.resolve(__dirname, './src/lib'),
      '@/hooks': path.resolve(__dirname, './src/hooks'),
    },
  },
})
```

## 配置方式 3：通用 Node.js 项目

### vitest.config.ts（TypeScript 项目）

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    setupFiles: './vitest.setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/*.config.*',
        'tests/',
      ],
    },
  },
})
```

### vitest.config.mjs（JavaScript 项目）

```js
/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    setupFiles: './vitest.setup.js',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.config.*',
        'tests/',
      ],
    },
  },
})
```

## Setup 文件（可选但推荐）

### vitest.setup.ts

创建 `vitest.setup.ts` 用于全局配置：

```ts
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

// 扩展 Vitest 的 expect 断言
expect.extend(matchers)

// 每个测试后清理
afterEach(() => {
  cleanup()
})

// Mock 浏览器 API
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
})

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return []
  }
  unobserve() {}
} as any
```

### vitest.setup.js（JavaScript 项目）

```js
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

afterEach(() => {
  cleanup()
})

// Mock 浏览器 API
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
})
```

## Package.json Scripts

在 `package.json` 中添加以下 scripts：

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

**使用方式**：
- `<PM> test` - 监听模式运行测试（开发时使用）
- `<PM> test:run` - 单次运行所有测试（CI 使用）
- `<PM> test:coverage` - 生成测试覆盖率报告
- `<PM> test:ui` - 在浏览器中查看测试结果（需要安装 @vitest/ui）

## 配置选项说明

### globals

```ts
globals: true
```

启用全局测试 API（`describe`、`it`、`expect` 等），无需在每个测试文件中导入。

### environment

```ts
environment: 'node'        // Node.js 环境（默认）
environment: 'jsdom'       // 浏览器环境（使用 jsdom）
environment: 'happy-dom'   // 浏览器环境（使用 happy-dom，更快）
```

选择测试运行环境：
- `node` - 适用于后端代码、工具函数
- `jsdom` - 适用于前端组件、DOM 操作
- `happy-dom` - jsdom 的轻量级替代，速度更快

### setupFiles

```ts
setupFiles: './vitest.setup.ts'
```

在每个测试文件运行前执行的设置文件，用于全局配置和 mock。

### coverage

```ts
coverage: {
  provider: 'v8',                    // 使用 V8 引擎的覆盖率工具
  reporter: ['text', 'json', 'html'], // 输出格式
  exclude: [                          // 排除文件
    'node_modules/',
    'dist/',
    '**/*.d.ts',
    '**/*.config.*',
  ],
  thresholds: {                       // 覆盖率阈值（可选）
    lines: 80,
    functions: 80,
    branches: 80,
    statements: 80,
  },
}
```

## 测试文件示例

### 工具函数测试

```ts
// lib/utils.test.ts
import { describe, it, expect } from 'vitest'
import { formatDate, cn } from './utils'

describe('formatDate', () => {
  it('应该正确格式化日期', () => {
    const date = new Date('2024-01-15')
    expect(formatDate(date)).toBe('2024-01-15')
  })

  it('应该处理无效日期', () => {
    expect(formatDate(null)).toBe('')
  })
})

describe('cn', () => {
  it('应该合并类名', () => {
    expect(cn('foo', 'bar')).toBe('foo bar')
  })

  it('应该处理条件类名', () => {
    expect(cn('foo', false && 'bar', 'baz')).toBe('foo baz')
  })
})
```

### React 组件测试

```tsx
// components/button.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './button'

describe('Button', () => {
  it('应该渲染按钮文本', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('应该响应点击事件', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('禁用状态下不应响应点击', () => {
    const handleClick = vi.fn()
    render(<Button disabled onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).not.toHaveBeenCalled()
  })
})
```

### 异步测试

```ts
// api/users.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchUser } from './users'

// Mock fetch
global.fetch = vi.fn()

describe('fetchUser', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('应该成功获取用户', async () => {
    const mockUser = { id: 1, name: 'John' }
    ;(fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    })

    const user = await fetchUser(1)
    expect(user).toEqual(mockUser)
  })

  it('应该处理错误', async () => {
    ;(fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 404,
    })

    await expect(fetchUser(999)).rejects.toThrow('User not found')
  })
})
```

## 验证配置

安装和配置完成后，运行以下命令验证：

```bash
# 运行测试
<PM> test:run

# 查看覆盖率
<PM> test:coverage
```

如果测试运行成功，说明配置正确。

## 故障排除

### 找不到模块

如果遇到模块解析错误，检查 `resolve.alias` 配置是否正确：

```ts
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

### TypeScript 类型错误

在 `tsconfig.json` 中添加 Vitest 类型：

```json
{
  "compilerOptions": {
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  }
}
```

### 测试运行缓慢

1. 使用 `happy-dom` 替代 `jsdom`（更快）
2. 启用并行测试（默认启用）
3. 使用 `--no-coverage` 跳过覆盖率收集

### Mock 不生效

确保 mock 在导入被测试模块之前定义：

```ts
import { vi } from 'vitest'

// Mock 必须在 import 之前
vi.mock('./api', () => ({
  fetchData: vi.fn(),
}))

import { myFunction } from './my-module'
```

## 最佳实践

1. **测试文件位置**：与源码同目录，使用 `.test.ts` 或 `.spec.ts` 后缀
2. **测试描述**：使用清晰的描述，说明测试的内容和预期结果
3. **AAA 模式**：Arrange（准备）、Act（执行）、Assert（断言）
4. **独立测试**：每个测试应该独立，不依赖其他测试的结果
5. **Mock 外部依赖**：对 API 调用、数据库等外部依赖进行 mock
6. **覆盖率目标**：建议达到 80% 以上的代码覆盖率
7. **CI 集成**：在 CI 中运行 `test:run` 确保代码质量

## 参考资源

- [Vitest 官方文档](https://vitest.dev/)
- [Testing Library 文档](https://testing-library.com/)
- [Vitest UI](https://vitest.dev/guide/ui.html)
