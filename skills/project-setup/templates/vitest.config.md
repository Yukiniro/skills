# Vitest Configuration Reference

This document provides installation and configuration guidance for Vitest, adapted to different project types and build tools.

## Install Dependencies

Install Vitest and coverage tools using the project's package manager:

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

**Optional dependencies** (install as needed):

```bash
# UI interface
<PM> add -D @vitest/ui

# Browser environment testing
<PM> add -D jsdom
# or
<PM> add -D happy-dom

# React component testing
<PM> add -D @testing-library/react @testing-library/jest-dom
```

## Configuration 1: Vite Projects (Recommended)

### Integrate in vite.config.ts

If the project already has a `vite.config.ts`, add test configuration directly:

```ts
/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    css: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "dist/",
        "**/*.d.ts",
        "**/*.config.*",
        "**/mockData",
        "tests/",
      ],
    },
  },
});
```

### Or Create Standalone vitest.config.ts

If you want to separate the configuration, create a standalone `vitest.config.ts`:

```ts
/// <reference types="vitest" />
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    css: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "dist/",
        "**/*.d.ts",
        "**/*.config.*",
        "**/mockData",
        "tests/",
      ],
    },
  },
  resolve: {
    alias: {
      "@": "/src",
    },
  },
});
```

## Configuration 2: Next.js Projects

Next.js projects require special configuration to support Next.js features.

### vitest.config.ts

```ts
/// <reference types="vitest" />
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    css: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        ".next/",
        "out/",
        "**/*.d.ts",
        "**/*.config.*",
        "**/mockData",
        "tests/",
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@/components": path.resolve(__dirname, "./src/components"),
      "@/lib": path.resolve(__dirname, "./src/lib"),
      "@/hooks": path.resolve(__dirname, "./src/hooks"),
    },
  },
});
```

## Configuration 3: Generic Node.js Projects

### vitest.config.ts (TypeScript Projects)

```ts
/// <reference types="vitest" />
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    setupFiles: "./vitest.setup.ts",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "dist/",
        "**/*.d.ts",
        "**/*.config.*",
        "tests/",
      ],
    },
  },
});
```

### vitest.config.mjs (JavaScript Projects)

```js
/// <reference types="vitest" />
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    setupFiles: "./vitest.setup.js",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["node_modules/", "dist/", "**/*.config.*", "tests/"],
    },
  },
});
```

## Setup File (Optional but Recommended)

### vitest.setup.ts

Create `vitest.setup.ts` for global configuration:

```ts
import { expect, afterEach } from "vitest";
import { cleanup } from "@testing-library/react";
import * as matchers from "@testing-library/jest-dom/matchers";

// Extend Vitest's expect assertions
expect.extend(matchers);

// Clean up after each test
afterEach(() => {
  cleanup();
});

// Mock browser APIs
Object.defineProperty(window, "matchMedia", {
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
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return [];
  }
  unobserve() {}
} as any;
```

### vitest.setup.js (JavaScript Projects)

```js
import { expect, afterEach } from "vitest";
import { cleanup } from "@testing-library/react";
import * as matchers from "@testing-library/jest-dom/matchers";

expect.extend(matchers);

afterEach(() => {
  cleanup();
});

// Mock browser APIs
Object.defineProperty(window, "matchMedia", {
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
});
```

## Package.json Scripts

Add the following scripts to `package.json`:

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

**Usage**:

- `<PM> test` - Run tests in watch mode (for development)
- `<PM> test:run` - Run all tests once (for CI)
- `<PM> test:coverage` - Generate test coverage report
- `<PM> test:ui` - View test results in the browser (requires @vitest/ui)

## Configuration Options Explained

### globals

```ts
globals: true;
```

Enables global test APIs (`describe`, `it`, `expect`, etc.) without importing them in each test file.

### environment

```ts
environment: "node"; // Node.js environment (default)
environment: "jsdom"; // Browser environment (using jsdom)
environment: "happy-dom"; // Browser environment (using happy-dom, faster)
```

Choose the test execution environment:

- `node` - For backend code, utility functions
- `jsdom` - For frontend components, DOM operations
- `happy-dom` - Lightweight alternative to jsdom, faster

### setupFiles

```ts
setupFiles: "./vitest.setup.ts";
```

Setup file executed before each test file runs, used for global configuration and mocks.

### coverage

```ts
coverage: {
  provider: 'v8',                    // Use V8 engine's coverage tool
  reporter: ['text', 'json', 'html'], // Output formats
  exclude: [                          // Excluded files
    'node_modules/',
    'dist/',
    '**/*.d.ts',
    '**/*.config.*',
  ],
  thresholds: {                       // Coverage thresholds (optional)
    lines: 80,
    functions: 80,
    branches: 80,
    statements: 80,
  },
}
```

## Test File Examples

### Utility Function Tests

```ts
// lib/utils.test.ts
import { describe, it, expect } from "vitest";
import { formatDate, cn } from "./utils";

describe("formatDate", () => {
  it("should format date correctly", () => {
    const date = new Date("2024-01-15");
    expect(formatDate(date)).toBe("2024-01-15");
  });

  it("should handle invalid date", () => {
    expect(formatDate(null)).toBe("");
  });
});

describe("cn", () => {
  it("should merge class names", () => {
    expect(cn("foo", "bar")).toBe("foo bar");
  });

  it("should handle conditional class names", () => {
    expect(cn("foo", false && "bar", "baz")).toBe("foo baz");
  });
});
```

### React Component Tests

```tsx
// components/button.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./button";

describe("Button", () => {
  it("should render button text", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });

  it("should respond to click events", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText("Click me"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("should not respond to clicks when disabled", () => {
    const handleClick = vi.fn();
    render(
      <Button disabled onClick={handleClick}>
        Click me
      </Button>,
    );

    fireEvent.click(screen.getByText("Click me"));
    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

### Async Tests

```ts
// api/users.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { fetchUser } from "./users";

// Mock fetch
global.fetch = vi.fn();

describe("fetchUser", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should successfully fetch user", async () => {
    const mockUser = { id: 1, name: "John" };
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const user = await fetchUser(1);
    expect(user).toEqual(mockUser);
  });

  it("should handle errors", async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 404,
    });

    await expect(fetchUser(999)).rejects.toThrow("User not found");
  });
});
```

## Verification

After installation and configuration, run the following commands to verify:

```bash
# Run tests
<PM> test:run

# View coverage
<PM> test:coverage
```

If tests run successfully, the configuration is correct.

## Troubleshooting

### Module Not Found

If you encounter module resolution errors, check the `resolve.alias` configuration:

```ts
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

### TypeScript Type Errors

Add Vitest types in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  }
}
```

### Slow Test Execution

1. Use `happy-dom` instead of `jsdom` (faster)
2. Enable parallel tests (enabled by default)
3. Use `--no-coverage` to skip coverage collection

### Mocks Not Working

Ensure mocks are defined before importing the module under test:

```ts
import { vi } from "vitest";

// Mocks must be before imports
vi.mock("./api", () => ({
  fetchData: vi.fn(),
}));

import { myFunction } from "./my-module";
```

## Best Practices

1. **Test file location**: Co-locate with source code, use `.test.ts` or `.spec.ts` suffix
2. **Test descriptions**: Use clear descriptions stating what is being tested and expected results
3. **AAA pattern**: Arrange, Act, Assert
4. **Independent tests**: Each test should be independent and not rely on other tests' results
5. **Mock external dependencies**: Mock API calls, databases, and other external dependencies
6. **Coverage target**: Aim for 80% or above code coverage
7. **CI integration**: Run `test:run` in CI to ensure code quality

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [Testing Library Documentation](https://testing-library.com/)
- [Vitest UI](https://vitest.dev/guide/ui.html)
