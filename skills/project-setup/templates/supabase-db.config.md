# Supabase Database Configuration Reference

This document provides configuration guidance for using Supabase PostgreSQL database in Next.js projects.

**Note**: This configuration is only applicable to Next.js SaaS projects using Supabase.

## Prerequisites

- Supabase Auth configured (see `supabase-auth.config.md`)
- `@supabase/supabase-js` already installed

## Directory Structure

```
project-root/
├── lib/
│   └── supabase/
│       ├── client.ts         # Browser client (from auth step)
│       ├── server.ts         # Server client (from auth step)
│       ├── middleware.ts     # Middleware client (from auth step)
│       └── admin.ts          # Admin client (service role, server-only)
```

## Configuration Files

### 1. lib/supabase/admin.ts

Server-only admin client using the service role key. This client bypasses Row-Level Security and should only be used in trusted server-side contexts (webhooks, cron jobs, admin operations):

```ts
import { createClient } from "@supabase/supabase-js";

export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);
```

**Important**: Never import this file in client components or expose `SUPABASE_SERVICE_ROLE_KEY` to the browser.

### 2. Type Definitions

Generate TypeScript types from your Supabase schema:

```bash
npx supabase gen types typescript --project-id <project-id> > lib/supabase/types.ts
```

Or define types manually based on your tables:

```ts
// lib/types/database.ts

export interface Prompt {
  id: string;
  user_id: string;
  title: string;
  content: string;
  tags: string[];
  is_favorite: boolean;
  usage_count: number;
  category: string | null;
  created_at: string;
  updated_at: string;
}

export interface Subscription {
  id: string;
  user_id: string;
  creem_subscription_id: string;
  creem_customer_id: string;
  status: "active" | "canceled" | "expired" | "paused" | "past_due";
  product_id: string;
  current_period_start: string | null;
  current_period_end: string | null;
}
```

## Query Patterns

### Basic CRUD Operations

#### SELECT — Read data

```ts
// Select all rows (with user scope)
const { data, error } = await supabase
  .from("prompts")
  .select("*")
  .eq("user_id", user.id)
  .order("created_at", { ascending: false });

// Select with filtering
const { data, error } = await supabase
  .from("prompts")
  .select("*")
  .eq("is_favorite", true)
  .order("created_at", { ascending: false });

// Select a single row
const { data, error } = await supabase
  .from("prompts")
  .select("*")
  .eq("id", promptId)
  .single();

// Select with search (ilike for case-insensitive)
const { data, error } = await supabase
  .from("prompts")
  .select("*")
  .or(`title.ilike.%${query}%,content.ilike.%${query}%`);

// Select with maybe single (returns null if not found, no error)
const { data } = await supabase
  .from("subscriptions")
  .select("*")
  .eq("user_id", user.id)
  .eq("status", "active")
  .maybeSingle();
```

#### INSERT — Create data

```ts
// Insert a single row
const { data, error } = await supabase
  .from("prompts")
  .insert({
    user_id: user.id,
    title: title.trim(),
    content: content.trim(),
    tags: Array.isArray(tags) ? tags : [],
  })
  .select()
  .single();
```

#### UPDATE — Modify data

```ts
// Update by ID
const { data, error } = await supabase
  .from("prompts")
  .update({ is_favorite: true })
  .eq("id", promptId)
  .select()
  .single();

// Update subscription status
const { error } = await supabase
  .from("subscriptions")
  .update({ status: "canceled" })
  .eq("creem_subscription_id", subscriptionId);
```

#### DELETE — Remove data

```ts
// Delete by ID
const { error } = await supabase.from("prompts").delete().eq("id", promptId);
```

#### UPSERT — Insert or update

```ts
// Upsert with conflict resolution
const { error } = await supabase.from("subscriptions").upsert(
  {
    user_id: userId,
    creem_subscription_id: subscriptionId,
    status: "active",
    product_id: productId,
  },
  { onConflict: "creem_subscription_id" }
);
```

### Advanced Queries

```ts
// Pagination
const { data } = await supabase
  .from("prompts")
  .select("*")
  .range(0, 9) // First 10 rows
  .order("created_at", { ascending: false });

// Count only (no data)
const { count } = await supabase
  .from("prompts")
  .select("*", { count: "exact", head: true })
  .eq("user_id", user.id);

// Multiple filters
const { data } = await supabase
  .from("prompts")
  .select("*")
  .eq("user_id", user.id)
  .in("category", ["work", "personal"])
  .gte("created_at", "2024-01-01")
  .order("usage_count", { ascending: false })
  .limit(10);

// Array contains
const { data } = await supabase
  .from("prompts")
  .select("*")
  .contains("tags", ["javascript"]);
```

## Usage in Server Components

```tsx
import { createClient } from "@/lib/supabase/server";

export default async function PromptsPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) return null;

  const { data: prompts, error } = await supabase
    .from("prompts")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    console.error("[prompts] Fetch error:", error);
    return <div>Failed to load prompts</div>;
  }

  return (
    <div>
      {prompts.map((prompt) => (
        <div key={prompt.id}>{prompt.title}</div>
      ))}
    </div>
  );
}
```

## Usage in API Route Handlers

```ts
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

// GET /api/prompts
export async function GET(req: NextRequest) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const { data, error } = await supabase
    .from("prompts")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json(data);
}

// POST /api/prompts
export async function POST(req: NextRequest) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const body = await req.json();

  const { data, error } = await supabase
    .from("prompts")
    .insert({ user_id: user.id, ...body })
    .select()
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json(data, { status: 201 });
}
```

## Usage in Server Actions

```ts
"use server";

import { revalidatePath } from "next/cache";
import { createClient } from "@/lib/supabase/server";

export async function createPrompt(formData: FormData) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) throw new Error("Not authenticated");

  const title = formData.get("title") as string;
  const content = formData.get("content") as string;

  const { error } = await supabase.from("prompts").insert({
    user_id: user.id,
    title,
    content,
  });

  if (error) throw new Error(error.message);

  revalidatePath("/work");
}
```

## Usage with Admin Client (Webhook Handlers)

```ts
import { supabaseAdmin } from "@/lib/supabase/admin";

// In webhook handler — bypasses RLS
await supabaseAdmin.from("subscriptions").upsert(
  {
    user_id: userId,
    creem_subscription_id: subscriptionId,
    status: "active",
  },
  { onConflict: "creem_subscription_id" }
);
```

## Row-Level Security (RLS)

All tables should have RLS enabled. Create policies in the Supabase Dashboard SQL Editor:

### Enable RLS

```sql
ALTER TABLE prompts ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
```

### Common Policies

```sql
-- Users can read their own prompts
CREATE POLICY "Users can read own prompts"
  ON prompts FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own prompts
CREATE POLICY "Users can insert own prompts"
  ON prompts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own prompts
CREATE POLICY "Users can update own prompts"
  ON prompts FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can delete their own prompts
CREATE POLICY "Users can delete own prompts"
  ON prompts FOR DELETE
  USING (auth.uid() = user_id);

-- Users can read their own subscriptions
CREATE POLICY "Users can read own subscriptions"
  ON subscriptions FOR SELECT
  USING (auth.uid() = user_id);
```

**Note**: The admin client (`supabaseAdmin`) uses the service role key which bypasses RLS. This is used in webhook handlers where there is no authenticated user context.

## Environment Variables

Add the following to `.env.local` (in addition to auth env vars):

```bash
# Supabase (server-only — DO NOT prefix with NEXT_PUBLIC_)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

This value can be found in Supabase Dashboard → Project Settings → API → Service Role Key.

## Verification

1. Test a basic query in a Server Component — data should load correctly
2. Verify RLS policies: attempt to query another user's data — should return empty
3. Test the admin client in a webhook handler — should bypass RLS
4. Verify `.insert()` with `.select().single()` returns the created row

## Troubleshooting

### RLS Blocking Queries

- Verify the user is authenticated (`supabase.auth.getUser()` returns a user)
- Check that RLS policies exist for the operation (SELECT, INSERT, UPDATE, DELETE)
- Use the Supabase Dashboard SQL Editor to test policies manually
- The admin client bypasses RLS — if admin queries work but regular queries don't, it's a policy issue

### Type Mismatches

- Regenerate types: `npx supabase gen types typescript --project-id <id>`
- Ensure column names in queries match the database schema exactly

### "relation does not exist" Error

- Verify the table exists in Supabase Dashboard → Table Editor
- Check that you're querying the correct schema (public by default)
- Ensure the Supabase project URL and keys match the project containing the table

## Best Practices

1. **Always use the server client for database operations** — never use the browser client for writes in production
2. **Enable RLS on all tables** — this is the first line of defense for data isolation
3. **Use `.single()` when expecting exactly one row** — it returns the object directly instead of an array
4. **Use `.maybeSingle()` when the row might not exist** — returns `null` without throwing an error
5. **Use the admin client sparingly** — only for operations that must bypass RLS (webhooks, cron jobs)
6. **Keep database queries in utility functions** — avoid inline queries in components for reusability
7. **Always check for errors** — Supabase returns `{ data, error }`, always handle the error case
8. **Use `user_id` for data scoping** — even with RLS, explicitly filtering by `user_id` makes intent clear

## Resources

- [Supabase Database Documentation](https://supabase.com/docs/guides/database)
- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript/introduction)
- [Row Level Security Guide](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase CLI (Type Generation)](https://supabase.com/docs/guides/cli)
