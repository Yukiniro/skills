# AGENTS.md - Project Development Guide

> **Usage Notes**: This file is a general template. Adjust the following when using:
>
> - Replace `<PM>` with the actual package manager (pnpm/yarn/npm/bun)
> - Adjust commands and file structure descriptions based on the project type
> - Remove sections that don't apply (e.g., remove component conventions for non-React projects)
> - Add project-specific conventions and best practices

## Build & Development Commands

```bash
<PM> dev             # Start development server
<PM> build           # Production build
<PM> start           # Start production server
<PM> lint            # Run ESLint
<PM> lint:fix        # Auto-fix ESLint issues
<PM> type-check      # TypeScript compilation check (TypeScript projects only)
<PM> test            # Run tests in watch mode
<PM> test:run        # Run tests once
<PM> test:ui         # Run tests with UI
<PM> test:coverage   # Generate test coverage report
<PM> format          # Format code
<PM> format:check    # Check code formatting
```

Note: This project uses Vitest for unit testing and Prettier for code formatting.

## Code Style Conventions

### Imports

- Group: React/type imports first, then third-party libraries, then local imports
- Use `import type { ... }` for type-only imports
- Use `@/` path alias for absolute imports from the project root (if configured)

```ts
"use client";
import type { RefObject } from "react";
import { useAtom } from "jotai";
import { Button } from "@/components/ui/button";
```

### Components (React/Next.js Projects)

- Add `'use client'` at the top of all client components
- Define props interfaces above the component: `interface ComponentNameProps { ... }`
- Use named exports: `export function ComponentName({ prop }: Props) { ... }`
- Use function components and Hooks, not class components
- Destructure props in the function signature for readability

### State Management (Adjust Based on the Actual Project)

- Use [state management library] for global state, defined in `lib/atoms.ts` or `store/`
- Read/write state with `const [value, setValue] = use[Hook]()`
- Mark unused values with underscore: `const [_, setValue] = use[Hook]()`

### Styling

- Use Tailwind CSS (or whatever CSS approach the project uses)
- Merge classes with `cn()` from `lib/utils.ts`
- Use CVA (class-variance-authority) for component variants
- Use `dark:` prefix for dark mode
- Place color/option constants in `constants.ts` with `as const`

### TypeScript

- Enable strict mode, disallow `any`
- Define interfaces for all props and data structures
- Minimize `as` assertions, prefer correct types
- Use `?` optional chaining for null checks where appropriate

### Error Handling

- Wrap async logic with try-catch
- Include context in console errors: `console.error('[feature] Error:', error)`
- Explicitly set loading states in async operations
- Prefer returning null over throwing errors when data is missing

### File Organization

Adjust the following structure based on project type:

**Next.js App Router Projects**:

- `components/ui/` - Shared UI components (shadcn/ui)
- `components/feature-name/` - Feature components with index.tsx
- `hooks/` - Custom React Hooks
- `lib/` - Utilities, configuration, state management
- `lib/supabase/` - Supabase client variants: browser, server, middleware, admin (if using Supabase)
- `app/` - Next.js App Router pages
- `app/[locale]/` - Internationalized routes (if using next-intl)
- `app/auth/` - Auth callback and auth-related routes (if using Supabase Auth)
- `app/api/webhooks/` - Webhook handlers for payment providers (if using Creem)
- `app/actions/` - Server Actions for mutations

**Vite Projects**:

- `src/components/` - React components
- `src/hooks/` - Custom Hooks
- `src/lib/` - Utility functions
- `src/pages/` - Page components
- `src/assets/` - Static assets

**Generic Node.js Projects**:

- `src/` - Source code
- `tests/` or `__tests__/` - Test files
- `lib/` - Utility functions
- `config/` - Configuration files

### Internationalization (Next.js projects using next-intl only)

- Use the `useTranslations()` hook from next-intl
- Configure locale routing in `i18n/routing.ts`
- Place translation files in `languages/` directory
- Get translations with `t('key')`

### Authentication (SaaS projects using Supabase Auth)

- Use `createBrowserClient()` from `@supabase/ssr` for client-side auth operations (login, sign-up, OAuth)
- Use `createServerClient()` from `@supabase/ssr` for server-side auth checks (Server Components, Server Actions, Route Handlers)
- Never expose `SUPABASE_SERVICE_ROLE_KEY` to the client — only use `NEXT_PUBLIC_` prefix for URL and anon key
- Auth state on the client: use a custom `useAuth` hook for auth state management
- Protect routes in `proxy.ts` (Next.js 16+) or `middleware.ts` (Next.js 15) — redirect unauthenticated users
- OAuth callback: handle token exchange in `app/auth/callback/route.ts`
- Supabase clients: `lib/supabase/client.ts` (browser), `lib/supabase/server.ts` (server), `lib/supabase/middleware.ts` (middleware/proxy)

### Database (SaaS projects using Supabase)

- Query via Supabase client: `.from('table').select()`, `.insert()`, `.update()`, `.delete()`, `.upsert()`
- Always use the server client for database operations in Server Components and Server Actions
- Use admin client (`SUPABASE_SERVICE_ROLE_KEY`) only in trusted server contexts (webhooks, cron jobs)
- Enable Row-Level Security (RLS) on all tables — filter by `user_id`
- Use `.single()` when expecting exactly one row, `.maybeSingle()` when the row might not exist
- Always handle `{ data, error }` response pattern — check error before using data

### Subscription & Payments (SaaS projects using Creem)

- Product configuration lives in `lib/products.ts` — define tiers, limits, and pricing
- Use Server Actions for checkout flow (`createCheckout()`)
- Webhook handler at `app/api/webhooks/creem/route.ts` — always verify HMAC-SHA256 signature
- Client-side subscription status: use `useSubscription` hook
- Feature gating: check subscription tier before allowing premium features
- Never trust client-side subscription status for security-critical operations — always verify server-side

### Naming Conventions

- Components: kebab-case (`photo-editor.tsx`)
- Hooks: kebab-case (`use-image-upload.ts`)
- Utilities: kebab-case (`format-date.ts`)
- Constants: SCREAMING_SNAKE_CASE (`DEFAULT_CONFIG`)
- Component files use kebab-case; types/hooks use camelCase

### Package Management

- Use <PM> to manage dependencies
- Keep the lockfile in version control
- Regularly update dependencies, watch for breaking changes

### Testing

- Place test files alongside source code with `.test.ts` or `.spec.ts` suffix
- Write tests for core business logic and utility functions
- Use clear test descriptions: `it('should handle empty input', () => { ... })`
- Mock external dependencies in `vitest.setup.ts` or test files
- Target test coverage: 80% or above

### Code Formatting

- Use Prettier for automatic code formatting
- Run `<PM> format` before committing to ensure consistent code style
- Configure editor to format on save (recommended)

### Pre-commit Checklist

- [ ] Build passes: `<PM> build`
- [ ] Lint passes: `<PM> lint` (or run `<PM> lint:fix`)
- [ ] No TypeScript errors: `<PM> type-check` (TypeScript projects)
- [ ] Tests pass: `<PM> test:run`
- [ ] Code formatted: `<PM> format`
- [ ] Manually verify functionality in development environment

## Project-Specific Conventions

> **TODO**: Add project-specific conventions, practices, and best practices here.
> For example: API call conventions, database query conventions, security requirements, etc.
