# Prettier Configuration Reference

This document provides installation and configuration guidance for Prettier, adapted to different project environments and existing toolchains.

## Scenario 1: Standalone Prettier (Recommended for New Projects)

### Installation

Install Prettier using the project's package manager:

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

### Configuration File `.prettierrc`

Create a `.prettierrc` file in the project root:

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

**Options explained**:

- `semi`: No semicolons
- `singleQuote`: Use single quotes
- `tabWidth`: 2-space indentation
- `trailingComma`: ES5-compatible trailing commas
- `printWidth`: Maximum 100 characters per line
- `arrowParens`: Always use parentheses around arrow function parameters
- `endOfLine`: Use LF line endings

### Ignore File `.prettierignore`

Create a `.prettierignore` file in the project root:

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

Add the following scripts to `package.json`:

```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

**Usage**:

- `<PM> format` - Format all files
- `<PM> format:check` - Check formatting without modifying files (for CI)

## Scenario 2: Prettier Integrated via ESLint

### Detection

Check `package.json` `devDependencies` for:

- `@antfu/eslint-config` + `eslint-plugin-format`
- `eslint-plugin-prettier` + `eslint-config-prettier`

### Configuration

**If using `@antfu/eslint-config`**:

Verify `formatters: true` in `eslint.config.js`:

```js
import antfu from "@antfu/eslint-config";

export default antfu({
  formatters: true, // Enable Prettier integration
  // ... other config
});
```

**If using `eslint-plugin-prettier`**:

Verify configuration in `.eslintrc.js`:

```js
module.exports = {
  extends: [
    // ... other extends
    "plugin:prettier/recommended", // Must be last
  ],
};
```

### Package.json Scripts

Add or verify the following scripts:

```json
{
  "scripts": {
    "format": "eslint --fix .",
    "format:check": "eslint ."
  }
}
```

**Note**: When using ESLint integration, formatting is done via `eslint --fix`.

## Scenario 3: Project Already Has Prettier

### Checklist

1. **Check config file**:
   - Does `.prettierrc`, `.prettierrc.json`, `.prettierrc.js`, or `prettier.config.js` exist?
   - If not, create a `.prettierrc` file (refer to Scenario 1)

2. **Check ignore file**:
   - Does `.prettierignore` exist?
   - If not, create a `.prettierignore` file (refer to Scenario 1)

3. **Check scripts**:
   - Are `format` and `format:check` scripts present?
   - If not, add them to `package.json` (refer to Scenario 1)

## Editor Integration (Optional but Recommended)

### VS Code / Cursor

Create `.vscode/settings.json` in the project root (if it doesn't exist):

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

**Note**: If using ESLint-integrated Prettier, use ESLint as the formatter:

```json
{
  "editor.formatOnSave": false,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

## Common Configuration Options

### Per-file-type Configuration

Use `overrides` in `.prettierrc`:

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

### Tailwind CSS Integration

Install the Tailwind CSS Prettier plugin (optional):

```bash
<PM> add -D prettier-plugin-tailwindcss
```

Add to `.prettierrc`:

```json
{
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

This will automatically sort Tailwind CSS class names.

## Verification

After installation and configuration, run the following commands to verify:

```bash
# Check formatting
<PM> format:check

# Format code
<PM> format
```

No errors means the configuration is successful.

## Troubleshooting

### Prettier and ESLint Conflicts

If using both standalone Prettier and ESLint, formatting rule conflicts may occur. Solutions:

1. **Recommended**: Use ESLint-integrated Prettier (Scenario 2)
2. Or install `eslint-config-prettier` to disable ESLint rules that conflict with Prettier:

```bash
<PM> add -D eslint-config-prettier
```

Add to the end of the `extends` array in `.eslintrc.js`:

```js
extends: [
  // ... other config
  'prettier',  // Must be last
]
```

### Slow Formatting

For large projects, use the `--cache` option to speed things up:

```json
{
  "scripts": {
    "format": "prettier --write --cache .",
    "format:check": "prettier --check --cache ."
  }
}
```

### Ignoring Specific Code Blocks

Use comments to ignore formatting in code:

```js
// prettier-ignore
const matrix = [
  1, 0, 0,
  0, 1, 0,
  0, 0, 1
]
```

Or ignore an entire file:

```js
// prettier-ignore-file
```

## Best Practices

1. **Format before committing**: Configure Git hooks (using husky + lint-staged) to auto-format before commits
2. **CI checks**: Run `format:check` in CI to ensure consistent formatting
3. **Team collaboration**: Keep `.prettierrc` and `.prettierignore` in version control
4. **Editor integration**: Recommend team members configure format-on-save
5. **Avoid mixing**: Choose either standalone Prettier or ESLint integration, don't mix both
