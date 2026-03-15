---
name: project-setup
description: Initialize development toolchains and conventions for new projects. Includes AGENTS.md, Prettier formatting, Vitest testing, AI agent skills, next-intl internationalization, and optional SaaS features (Supabase Auth/DB, Creem payments). Use when initializing new projects, scaffolding project structure, or configuring development toolchains.
---

# Project Setup

Quickly configure development toolchains, code standards, and AI agent skills for new projects. Automatically detects the project environment and adapts to the host project's package manager, framework, and existing toolchain. For Next.js SaaS projects, optionally configures Supabase authentication, database access, and Creem payment/subscription integration.

## Use Cases

- Initialize development environment for new projects
- Add standardized toolchain to existing projects
- Configure code formatting, test framework, and AI skills
- Configure internationalization for Next.js projects
- Configure Supabase Auth, Database, and Creem subscription for Next.js SaaS projects

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

**Check SaaS dependencies** (read `package.json` dependencies):

- `@supabase/supabase-js` or `@supabase/ssr` → Supabase project (auth and/or database)
- Check for `.env.local` or `.env.example` containing `CREEM_API_KEY` → Creem payment configured

**Check SaaS file structure**:

- `lib/supabase/` directory exists → Supabase client layer already set up
- `app/api/webhooks/creem/` directory exists → Creem webhook handler already present
- `lib/products.ts` or `lib/plans.ts` exists → Payment/subscription product config present

### Step 2: Feature Selection

After environment detection, ask the user which optional features they want to configure. If the user has already specified the modules in their initial request, skip the inquiry and proceed directly.

Present the following options to the user:

```
Please select the features to configure (multiple selections allowed):

Default (always enabled):
- [x] AGENTS.md project conventions
- [x] Prettier code formatting
- [x] Vitest testing framework
- [x] AI Agent Skills
- [x] ESLint code linting

Optional (select as needed):
- [ ] next-intl internationalization (Next.js projects)
- [ ] Supabase Auth authentication
- [ ] Supabase Database
- [ ] Creem Subscription payments
```

If environment detection found existing modules, annotate the options accordingly (e.g., "Supabase Auth (already detected)").

The following steps 3-6 and 11 are always executed. Steps 7-10 are only executed if the user selected them.

### Step 3: Create AGENTS.md

Read the template from `templates/AGENTS.md` and adjust based on detection results:

1. Replace package manager commands (`pnpm` / `yarn` / `npm` / `bun`)
2. Adjust build commands and file structure descriptions based on project type
3. If TypeScript project, ensure `type-check` command is included
4. Write the adjusted content to `AGENTS.md` in the project root

### Step 4: Configure Prettier

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

### Step 5: Configure Vitest

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

### Step 6: Install AI Agent Skills

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

### Step 7: Configure next-intl (User selected)

Refer to `templates/next-intl.config.md`.

**Only execute this step if the user selected next-intl in Step 2.**

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

### Step 8: Configure Supabase Auth (User selected)

Refer to `templates/supabase-auth.config.md`.

**Only execute this step if the user selected Supabase Auth in Step 2.**

**If Supabase Auth is already configured** (`lib/supabase/client.ts` exists):

- Verify all three client variants exist (browser, server, middleware)
- Check for auth callback route
- Check for auth middleware/proxy configuration
- Skip to the next step

**If no Supabase Auth**:

1. Install using the detected package manager:

   ```bash
   <pm> add @supabase/supabase-js @supabase/ssr
   ```

2. Create `lib/supabase/` directory with client files:
   - `lib/supabase/client.ts` - Browser client (uses `createBrowserClient`)
   - `lib/supabase/server.ts` - Server client (uses `createServerClient` with cookie management)
   - `lib/supabase/middleware.ts` - Middleware client (for auth in proxy/middleware)

3. Create auth callback route:
   - `app/auth/callback/route.ts` - OAuth callback handler (exchanges code for session)

4. Configure auth middleware:
   - Next.js 16+: Add auth logic to `proxy.ts` (not `middleware.ts`)
   - Next.js 15 and earlier: Add auth logic to `middleware.ts`
   - Protect authenticated routes (e.g., `/work`, `/dashboard`)
   - Redirect unauthenticated users to login page

5. Add environment variables to `.env.example`:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

6. Optional: Create `hooks/use-auth.ts` custom hook for client-side auth state

### Step 9: Configure Supabase Database (User selected)

Refer to `templates/supabase-db.config.md`.

**Only execute this step if the user selected Supabase Database in Step 2.**

**If Supabase database queries already exist** (grep for `.from(` in `lib/` or `app/`):

- Verify server client is configured for database operations
- Check for admin client if webhook handlers exist
- Skip to the next step

**If no Supabase Database setup**:

1. Ensure `@supabase/supabase-js` is installed (should be done in Step 8)

2. Verify server client in `lib/supabase/server.ts` supports database queries

3. Create admin client for server-side operations requiring elevated privileges:
   - `lib/supabase/admin.ts` - Uses `SUPABASE_SERVICE_ROLE_KEY` (server-only, never exposed to client)

4. Create database type definitions:
   - Define TypeScript types for your database tables
   - Or use `npx supabase gen types typescript` to auto-generate from schema

5. Add environment variables to `.env.example`:
   - `SUPABASE_SERVICE_ROLE_KEY` (server-only)

6. Document Row-Level Security (RLS) conventions:
   - All tables should have RLS enabled
   - Filter by `user_id` for user-scoped data
   - Use service role key only in trusted server-side contexts

### Step 10: Configure Creem Subscription (User selected)

Refer to `templates/creem-subscription.config.md`.

**Only execute this step if the user selected Creem Subscription in Step 2.**

**If Creem is already configured** (`app/api/webhooks/creem/` exists):

- Verify webhook handler, product config, and checkout flow
- Skip to the next step

**If no Creem setup**:

1. Create product/plan configuration:
   - `lib/products.ts` - Define product tiers, pricing, feature limits, Creem product IDs
   - `lib/constants.ts` - Define free/pro tier limits, optional whitelist

2. Create checkout server action:
   - `app/actions/subscription.ts` - `createCheckout()` and `getSubscriptionStatus()` server actions
   - Calls Creem API to create checkout session
   - Returns checkout URL for client-side redirect

3. Create webhook handler:
   - `app/api/webhooks/creem/route.ts` - POST handler for Creem webhook events
   - Implement HMAC-SHA256 signature verification
   - Handle events: `checkout.completed`, `subscription.active`, `subscription.paid`, `subscription.canceled`, `subscription.expired`, `subscription.paused`, `subscription.past_due`, `subscription.scheduled_cancel`
   - Update subscription status in Supabase database using admin client

4. Create subscription utilities:
   - `hooks/use-subscription.ts` - Client-side hook for subscription status (uses SWR)
   - Implement tier-based feature gating (free vs pro limits)

5. Add environment variables to `.env.example`:
   - `CREEM_API_KEY` - Creem API key
   - `CREEM_WEBHOOK_SECRET` - Webhook signature verification secret
   - `NODE_TARGET` - Environment target (production/staging)
   - `NEXT_PUBLIC_SITE_URL` - Site URL for checkout redirect
   - `NEXT_PUBLIC_PROJECT_ID` - Creem product ID

6. Create `subscriptions` table in Supabase (provide SQL to user):
   - Columns: `id`, `user_id`, `creem_subscription_id`, `creem_customer_id`, `status`, `product_id`, `current_period_start`, `current_period_end`
   - Enable RLS with user-scoped read policy

### Step 11: Configure Lint

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

### Step 12: Verification Checklist

After completing all configurations, present the following checklist to the user. Only include items that were actually configured based on the user's selection in Step 2:

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
- [x] ESLint configured
- [x] next-intl configured (if selected)
- [x] Supabase Auth configured (if selected)
- [x] Supabase Database configured (if selected)
- [x] Creem Subscription configured (if selected)

Next Steps:
1. Run `<pm> install` to install dependencies
2. Run `<pm> run format` to format code
3. Run `<pm> run test` to verify test configuration
4. Review AGENTS.md for project conventions
5. Set up Supabase project at https://supabase.com and add env vars (if Supabase selected)
6. Configure Creem account at https://creem.io and add env vars (if Creem selected)
```

## Template Files

This skill includes the following template files in the `templates/` directory:

- `AGENTS.md` - Project development conventions template
- `prettier.config.md` - Prettier configuration reference
- `vitest.config.md` - Vitest configuration reference
- `next-intl.config.md` - next-intl configuration reference
- `supabase-auth.config.md` - Supabase Auth configuration reference
- `supabase-db.config.md` - Supabase Database configuration reference
- `creem-subscription.config.md` - Creem payment/subscription configuration reference

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

### Supabase Auth Issues

If authentication is not working:

- Verify `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` are set correctly
- Check that the auth callback route matches the redirect URL in Supabase dashboard
- Ensure `proxy.ts` (Next.js 16) or `middleware.ts` correctly refreshes the session
- For OAuth providers, verify the callback URL is registered in Supabase Auth settings

### Creem Webhook Issues

If webhooks are not being received:

- Verify `CREEM_WEBHOOK_SECRET` matches the secret in Creem dashboard
- Ensure the webhook URL is publicly accessible (use ngrok for local development)
- Read the request body as raw text (`req.text()`) before parsing for signature verification
- Check HMAC-SHA256 signature verification logic
- Review webhook event payload structure against Creem API documentation

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
