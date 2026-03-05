---
name: project-setup
description: Initialize development toolchains and conventions for new projects. Includes AGENTS.md, Prettier formatting, Vitest testing, AI agent skills, and next-intl internationalization. Use when initializing new projects, scaffolding project structure, or configuring development toolchains.
---

# Project Setup

Quickly configure development toolchains, code standards, and AI agent skills for new projects. Automatically detects the project environment and adapts to the host project's package manager, framework, and existing toolchain.

## Use Cases

- Initialize development environment for new projects
- Add standardized toolchain to existing projects
- Configure code formatting, test framework, and AI skills
- Configure internationalization for Next.js projects

## Workflow

When executing the following steps, always detect the environment first, then adjust configuration based on the actual setup.

### Step 1: Environment Detection

Before performing any operations, gather host project information:

**Check package manager** (determine by lockfile):

- `pnpm-lock.yaml` → use `pnpm add -D`
- `yarn.lock` → use `yarn add -D`
- `package-lock.json` → use `npm install -D`
- `bun.lockb` → use `bun add -D`

**Check project type** (read `package.json` dependencies):

- Contains `next` → Next.js project
- Contains `vite` → Vite project
- Other → Generic Node.js project

**Check TypeScript**:

- `tsconfig.json` exists → TypeScript project (config files use `.ts`)
- Does not exist → JavaScript project (config files use `.js` or `.mjs`)

**Check existing toolchain** (read `package.json` devDependencies):

- `@antfu/eslint-config` + `eslint-plugin-format` → Prettier already integrated via ESLint
- `eslint-plugin-prettier` → Prettier already integrated via ESLint
- `prettier` → Standalone Prettier already exists
- `vitest` → Vitest already exists

**Check build tools**:

- Vite project: check for `vite.config.ts` / `vite.config.js`

### Step 2: Create AGENTS.md

Read the template from `templates/AGENTS.md` and adjust based on detection results:

1. Replace package manager commands (`pnpm` / `yarn` / `npm` / `bun`)
2. Adjust build commands and file structure descriptions based on project type
3. If TypeScript project, ensure `type-check` command is included
4. Write the adjusted content to `AGENTS.md` in the project root

### Step 3: Configure Prettier

Refer to `templates/prettier.config.md`.

**If Prettier is already integrated via ESLint** (`@antfu/eslint-config` or `eslint-plugin-prettier`):

- Skip installation and config file creation
- Only verify `package.json` has `format` and `format:check` scripts
- If missing, add scripts suitable for the ESLint integration approach

**If no Prettier**:

1. Install using the detected package manager: `<pm> add -D prettier`
2. Create `.prettierrc` config file
3. Create `.prettierignore` file
4. Add scripts to `package.json`:
   ```json
   {
     "format": "prettier --write .",
     "format:check": "prettier --check ."
   }
   ```

**If Prettier already exists**:

- Check for config file, create one if missing
- Check for scripts, add them if missing

### Step 4: Configure Vitest

Refer to `templates/vitest.config.md`.

**If Vitest already exists**:

- Check for config file, create one if missing
- Check for test scripts, add them if missing

**If no Vitest**:

1. Install using the detected package manager:

   ```bash
   <pm> add -D vitest @vitest/coverage-v8
   ```

2. Create config file:
   - **Vite project**: Add test config to `vite.config.ts`, or create standalone `vitest.config.ts`
   - **Next.js / other projects**: Create standalone `vitest.config.ts` or `vitest.config.mjs`
   - Use `.ts` extension (TypeScript project) or `.mjs` extension (JavaScript project)

3. Add scripts to `package.json`:

   ```json
   {
     "test": "vitest",
     "test:run": "vitest run",
     "test:coverage": "vitest run --coverage",
     "test:ui": "vitest --ui"
   }
   ```

4. Optional: Create `vitest.setup.ts` for global test configuration

### Step 5: Install AI Agent Skills

Use the `npx skills add` command to install third-party skills into project-level `.cursor/`, `.claude/`, and `.agents/` directories.

**Important**: Ensure you run these commands from the project root.

Execute the following commands sequentially (run each command individually, wait for completion before running the next):

```bash
# 1. Vercel React best practices + web design guidelines
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices web-design-guidelines --agent cursor claude-code agents -y

# 2. Frontend design guidelines
npx skills add anthropics/skills --skill frontend-design --agent cursor claude-code agents -y

# 3. shadcn/ui component patterns
npx skills add giuseppe-trisciuoglio/developer-kit --skill shadcn-ui --agent cursor claude-code agents -y

# 4. Vitest testing framework
npx skills add antfu/skills --skill vitest --agent cursor claude-code agents -y
```

**Notes**:

- These commands will automatically create `.cursor/skills/`, `.claude/skills/`, and `.agents/skills/` directories
- If a command fails, check network connectivity and npm configuration
- Once installed, these skills will be available in all supported AI agents

### Step 6: Configure next-intl (Next.js projects only)

Refer to `templates/next-intl.config.md`.

**Only execute this step if the project type is Next.js.**

1. Install using the detected package manager:

   ```bash
   <pm> add next-intl
   ```

2. Create `i18n/` directory and config files:
   - `i18n/routing.ts` - Define supported locales and default locale
   - `i18n/request.ts` - Configure request handling
   - `i18n/navigation.ts` - Export internationalized navigation components

3. Create `languages/` directory and translation files:
   - `languages/en.json` - English translations
   - `languages/zh-CN.json` - Simplified Chinese translations
   - Add other languages as needed

4. Use `proxy.ts` instead of `middleware.ts`, otherwise you will get a warning: `The "middleware" file convention is deprecated. Please use "proxy" instead. Learn more: https://nextjs.org/docs/messages/middleware-to-proxy`

5. Update `AGENTS.md` to add internationalization-related instructions

### Step 7: Configure Lint

Configure ESLint based on https://github.com/antfu/eslint-config. The config should include:

```js
import antfu from "@antfu/eslint-config";

export default antfu({
  formatters: true,
  react: true,
  stylistic: false,
  ignores: [
    ".agents/**/*",
    ".claude/**/*",
    ".cursor/**/*",
    ".vscode/**/*",
    "components/ai-elements/**/*",
    "components/ui/**/*",
  ],
});
```

### Step 8: Verification Checklist

After completing all configurations, present the following checklist to the user:

```
✓ Project Setup Complete

Environment Info:
- Package manager: <detected-pm>
- Project type: <detected-type>
- TypeScript: <yes/no>

Completed Configurations:
- [x] AGENTS.md created
- [x] Prettier configured (<standalone/ESLint-integrated/already existed>)
- [x] Vitest configured (<newly installed/already existed>)
- [x] AI Skills installed (4 skills)
- [x] next-intl configured (Next.js only)

Next Steps:
1. Run `<pm> install` to install dependencies
2. Run `<pm> run format` to format code
3. Run `<pm> run test` to verify test configuration
4. Review AGENTS.md for project conventions
```

## Template Files

This skill includes the following template files in the `templates/` directory:

- `AGENTS.md` - Project development conventions template
- `prettier.config.md` - Prettier configuration reference
- `vitest.config.md` - Vitest configuration reference
- `next-intl.config.md` - next-intl configuration reference

Read these template files for detailed configuration content when executing setup.

## Troubleshooting

### Prettier and ESLint Conflicts

If the project uses both Prettier and ESLint, ensure:

- When using `@antfu/eslint-config`, the formatters option is enabled
- When using `eslint-plugin-prettier`, extends is configured correctly
- When using standalone Prettier, add `.prettierignore` to avoid formatting conflicts

### Vitest Configuration in Next.js

Next.js projects require special Vitest configuration:

- Use the `next()` helper to handle Next.js-specific features
- Configure path alias mapping (`@/` → `./src/`)
- Set the correct test environment (usually `node` or `jsdom`)

### Skills Installation Failure

If `npx skills add` fails:

- Check network connectivity
- Try clearing npm cache: `npm cache clean --force`
- Manually set npm registry: `npm config set registry https://registry.npmjs.org/`
- Review detailed error messages and follow the instructions

## Best Practices

1. **Environment detection first**: Always detect the environment first to avoid assumptions about project configuration
2. **Avoid overwriting**: Check for existing configurations; only create new files when missing
3. **Adapt to package manager**: Use the project's existing package manager for consistency
4. **Incremental configuration**: Configure basic tools first, then add advanced features
5. **Verify configuration**: After setup, suggest users run relevant commands to verify
