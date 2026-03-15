# Supabase Auth Configuration Reference

This document provides installation and configuration guidance for Supabase Auth in Next.js projects.

**Note**: This configuration is only applicable to Next.js SaaS projects.

## Install Dependencies

Install Supabase packages using the project's package manager:

```bash
# pnpm
pnpm add @supabase/supabase-js @supabase/ssr

# yarn
yarn add @supabase/supabase-js @supabase/ssr

# npm
npm install @supabase/supabase-js @supabase/ssr

# bun
bun add @supabase/supabase-js @supabase/ssr
```

## Directory Structure

Create the following directories and files:

```
project-root/
├── lib/
│   └── supabase/
│       ├── client.ts         # Browser client
│       ├── server.ts         # Server client (cookie management)
│       └── middleware.ts     # Middleware client (route protection)
├── app/
│   ├── auth/
│   │   └── callback/
│   │       └── route.ts     # OAuth callback handler
│   └── [locale]/
│       └── auth/
│           ├── login/
│           │   └── page.tsx  # Login page
│           └── sign-up/
│               └── page.tsx  # Sign-up page
├── hooks/
│   └── use-auth.ts          # Custom auth hook (optional)
└── proxy.ts                  # Next.js 16+ middleware (or middleware.ts for Next.js 15)
```

## Configuration Files

### 1. lib/supabase/client.ts

Browser-side Supabase client for client components:

```ts
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### 2. lib/supabase/server.ts

Server-side Supabase client with cookie management for Server Components, Server Actions, and Route Handlers:

```ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // The "setAll" method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
          }
        },
      },
    }
  );
}
```

### 3. lib/supabase/middleware.ts

Middleware Supabase client for session refresh and route protection:

```ts
import type { NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";
import { NextResponse } from "next/server";

// Regex pattern for protected routes — adjust to match your app's routes
const protectedPattern = /^\/[a-z]{2}(?:-[a-zA-Z]+)?\/work/;

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({
            request,
          });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  const {
    data: { user },
  } = await supabase.auth.getUser();

  // Redirect unauthenticated users to login for protected routes
  const pathname = request.nextUrl.pathname;
  if (protectedPattern.test(pathname) && !user) {
    const locale = pathname.split("/")[1];
    const url = request.nextUrl.clone();
    url.pathname = `/${locale}/auth/login`;
    return NextResponse.redirect(url);
  }

  return supabaseResponse;
}
```

### 4. app/auth/callback/route.ts

OAuth callback handler that exchanges the authorization code for a session:

```ts
import type { NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/work";

  if (!code) {
    return NextResponse.redirect(`${origin}/en/auth/error?error=missing_code`);
  }

  const cookieStore = await cookies();
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Ignore errors when called from Server Component
          }
        },
      },
    }
  );

  const { error } = await supabase.auth.exchangeCodeForSession(code);

  if (error) {
    console.error("[auth/callback] OAuth exchange error:", error);
    return NextResponse.redirect(
      `${origin}/en/auth/error?error=${error.message}`
    );
  }

  const forwardedHost = request.headers.get("x-forwarded-host");
  const isLocalEnv = process.env.NODE_ENV === "development";

  if (isLocalEnv) {
    return NextResponse.redirect(`${origin}${next}`);
  } else if (forwardedHost) {
    return NextResponse.redirect(`https://${forwardedHost}${next}`);
  } else {
    return NextResponse.redirect(`${origin}${next}`);
  }
}
```

### 5. Auth Middleware

#### Next.js 16+ (proxy.ts)

For Next.js 16+, use `proxy.ts` instead of `middleware.ts`:

```ts
import type { NextRequest } from "next/server";
import createIntlMiddleware from "next-intl/middleware";
import { updateSession } from "@/lib/supabase/middleware";
import { routing } from "./i18n/routing";

const intlMiddleware = createIntlMiddleware(routing);

export async function proxy(request: NextRequest) {
  // Run i18n middleware first
  const intlResponse = intlMiddleware(request);

  // Then run Supabase session update
  const supabaseResponse = await updateSession(request);

  // If Supabase middleware wants to redirect (e.g., unauthenticated user),
  // return its response immediately
  if (supabaseResponse.headers.has("location")) {
    return supabaseResponse;
  }

  // Copy Supabase cookies to the i18n response
  supabaseResponse.cookies.getAll().forEach((cookie) => {
    intlResponse.cookies.set(cookie.name, cookie.value);
  });

  return intlResponse;
}

export const config = {
  matcher: ["/((?!api|auth/callback|_next|_vercel|.*\\..*).*)"],
};
```

#### Next.js 15 (middleware.ts)

For Next.js 15 projects, use `middleware.ts`:

```ts
import type { NextRequest } from "next/server";
import createIntlMiddleware from "next-intl/middleware";
import { updateSession } from "@/lib/supabase/middleware";
import { routing } from "./i18n/routing";

const intlMiddleware = createIntlMiddleware(routing);

export default async function middleware(request: NextRequest) {
  const intlResponse = intlMiddleware(request);
  const supabaseResponse = await updateSession(request);

  if (supabaseResponse.headers.has("location")) {
    return supabaseResponse;
  }

  supabaseResponse.cookies.getAll().forEach((cookie) => {
    intlResponse.cookies.set(cookie.name, cookie.value);
  });

  return intlResponse;
}

export const config = {
  matcher: ["/((?!api|auth/callback|_next|_vercel|.*\\..*).*)"],
};
```

**Note**: If the project does not use `next-intl`, remove the i18n middleware and use `updateSession` directly:

```ts
import type { NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/middleware";

export async function proxy(request: NextRequest) {
  return await updateSession(request);
}

export const config = {
  matcher: ["/((?!api|auth/callback|_next|_vercel|.*\\..*).*)"],
};
```

### 6. hooks/use-auth.ts (Optional)

Custom hook for client-side auth state management:

```ts
"use client";

import { useAtom } from "jotai";
import { useCallback, useEffect } from "react";
import { useRouter } from "@/i18n/navigation";
import { userAtom } from "@/lib/atoms/auth";
import { createClient } from "@/lib/supabase/client";

export function useAuth() {
  const [user, setUser] = useAtom(userAtom);
  const router = useRouter();

  useEffect(() => {
    const supabase = createClient();

    const getUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      setUser(user);
    };
    getUser();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, [setUser]);

  const signOut = useCallback(async () => {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push("/");
  }, [router]);

  return { user, signOut };
}
```

**Note**: This example uses Jotai for state management. If your project uses a different state library (e.g., Zustand, React Context), adapt the state management accordingly. The key patterns to preserve are:

- Fetch the initial user on mount
- Listen for auth state changes with `onAuthStateChange`
- Clean up the subscription on unmount
- Provide a `signOut` function

If not using Jotai, you can use a simpler approach with `useState`:

```ts
"use client";

import type { User } from "@supabase/supabase-js";
import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const supabase = createClient();

    const getUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      setUser(user);
    };
    getUser();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signOut = useCallback(async () => {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push("/");
  }, [router]);

  return { user, signOut };
}
```

## Environment Variables

Add the following to `.env.local` (and `.env.example` without values):

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your-supabase-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

These values can be found in Supabase Dashboard → Project Settings → API.

## Usage Examples

### In Server Components

```tsx
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";

export default async function ProtectedPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/auth/login");
  }

  return <div>Welcome, {user.email}</div>;
}
```

### In Client Components

```tsx
"use client";

import { createClient } from "@/lib/supabase/client";

export function LoginButton() {
  const handleLogin = async () => {
    const supabase = createClient();
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
  };

  return <button onClick={handleLogin}>Sign in with Google</button>;
}
```

### In Server Actions

```ts
"use server";

import { createClient } from "@/lib/supabase/server";

export async function updateProfile(formData: FormData) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) throw new Error("Not authenticated");

  // Proceed with authenticated operation...
}
```

## Verification

1. Start the development server: `<PM> dev`
2. Navigate to the login page and test email/password sign-up
3. Verify OAuth flow (if configured): click OAuth button → redirect → callback → session created
4. Access a protected route while unauthenticated → should redirect to login
5. Access a protected route while authenticated → should render the page

## Troubleshooting

### Session Not Persisting

- Ensure the middleware/proxy is refreshing sessions on every request
- Check that `getAll` and `setAll` cookie methods are implemented correctly
- Verify that the middleware matcher is not excluding routes that need session refresh

### OAuth Redirect URL Mismatch

- The callback URL must be registered in Supabase Dashboard → Authentication → URL Configuration
- For local development, add `http://localhost:3000/auth/callback`
- For production, add `https://your-domain.com/auth/callback`

### Cookie Issues with SSR

- The server client uses `cookies()` from `next/headers`, which is only available in Server Components, Server Actions, and Route Handlers
- The middleware client uses `NextRequest`/`NextResponse` cookies, which is only available in middleware
- Never use the server client in client components — use the browser client instead

## Best Practices

1. **Always refresh sessions in middleware/proxy** — this ensures tokens are valid on every request
2. **Never expose `SUPABASE_SERVICE_ROLE_KEY` to the client** — use `NEXT_PUBLIC_` prefix only for URL and anon key
3. **Use `supabase.auth.getUser()` instead of `getSession()`** — `getUser()` validates the JWT with Supabase servers
4. **Handle auth state changes** — subscribe to `onAuthStateChange` to keep the UI in sync
5. **Implement proper error pages** — create `app/[locale]/auth/error/page.tsx` for auth error display
6. **Use Row-Level Security (RLS)** — always pair Supabase Auth with RLS policies on database tables

## Resources

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Supabase SSR Guide for Next.js](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [@supabase/ssr Package](https://www.npmjs.com/package/@supabase/ssr)
