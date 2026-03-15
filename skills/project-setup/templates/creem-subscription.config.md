# Creem Payment/Subscription Configuration Reference

This document provides configuration guidance for integrating Creem payment and subscription management in Next.js SaaS projects.

**Note**: This configuration is only applicable to Next.js SaaS projects using Creem as the payment provider.

## Overview

Creem is a payment provider for SaaS subscriptions. Key features:

- Checkout sessions for one-time and recurring payments
- Subscription lifecycle management (create, cancel, pause, resume)
- Webhooks for real-time event notifications
- HMAC-SHA256 webhook signature verification

## Directory Structure

```
project-root/
├── lib/
│   ├── products.ts           # Product/plan configuration
│   └── constants.ts          # Feature limits, whitelist config
├── app/
│   ├── actions/
│   │   └── subscription.ts   # Checkout & subscription server actions
│   └── api/
│       └── webhooks/
│           └── creem/
│               └── route.ts  # Webhook handler
├── hooks/
│   └── use-subscription.ts   # Client-side subscription hook
└── components/
    └── upgrade-button.tsx    # Upgrade CTA component
```

## Configuration Files

### 1. lib/products.ts

Define product tiers, pricing, and Creem product IDs:

```ts
export interface Product {
  id: string;
  name: string;
  description: string;
  priceInCents: number;
  creemProductId: string;
  interval: "month" | "year";
}

export const PRODUCTS: Product[] = [
  {
    id: "pro",
    name: "Pro",
    description: "Unlimited items, advanced features, priority support",
    priceInCents: 600,
    creemProductId: process.env.NEXT_PUBLIC_PROJECT_ID!,
    interval: "month",
  },
];
```

### 2. lib/constants.ts

Define feature limits per tier and optional whitelist:

```ts
// Free tier limits
export const FREE_LIMITS = {
  maxItems: 30,
  maxTags: 5,
  maxContentLength: 1000,
} as const;

// Pro tier limits
export const PRO_LIMITS = {
  maxItems: Infinity,
  maxTags: Infinity,
  maxContentLength: 2000,
} as const;

// Optional: whitelist for testing or special access
const WHITELIST: string[] = [
  // Add emails for testing or special access
];

export function isEmailWhitelisted(email?: string | null): boolean {
  if (!email) return false;
  return WHITELIST.includes(email.toLowerCase());
}
```

### 3. app/actions/subscription.ts

Server actions for checkout creation and subscription status:

```ts
"use server";

import { PRODUCTS } from "@/lib/products";
import { createClient } from "@/lib/supabase/server";

export async function createCheckout(productId: string) {
  const product = PRODUCTS.find((p) => p.id === productId);
  if (!product) throw new Error(`Product "${productId}" not found`);

  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) throw new Error("Not authenticated");

  // Use production or test API based on environment
  const baseUrl =
    process.env.NODE_TARGET === "production"
      ? "https://api.creem.io/v1"
      : "https://test-api.creem.io/v1";

  const res = await fetch(`${baseUrl}/checkouts`, {
    method: "POST",
    headers: {
      "x-api-key": process.env.CREEM_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      product_id: product.creemProductId,
      success_url: `${process.env.NEXT_PUBLIC_SITE_URL}/work`,
      metadata: { userId: user.id },
    }),
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(`Failed to create checkout: ${error}`);
  }

  const data = await res.json();
  return data.checkout_url as string;
}

export async function getSubscriptionStatus() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return null;

  const { data } = await supabase
    .from("subscriptions")
    .select("*")
    .eq("user_id", user.id)
    .eq("status", "active")
    .maybeSingle();

  return data;
}
```

### 4. app/api/webhooks/creem/route.ts

Webhook handler with HMAC-SHA256 signature verification:

```ts
import crypto from "node:crypto";
import { createClient } from "@supabase/supabase-js";
import { NextResponse } from "next/server";

// Use admin client (service role) for webhook operations — bypasses RLS
const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

function verifySignature(
  payload: string,
  secret: string,
  signature: string
): boolean {
  return (
    crypto.createHmac("sha256", secret).update(payload).digest("hex") ===
    signature
  );
}

export async function POST(req: Request) {
  // Read raw body for signature verification
  const body = await req.text();
  const signature = req.headers.get("creem-signature");

  // Verify webhook signature
  const webhookSecret = process.env.CREEM_WEBHOOK_SECRET;
  if (webhookSecret && signature) {
    if (!verifySignature(body, webhookSecret, signature)) {
      return NextResponse.json({ error: "Invalid signature" }, { status: 401 });
    }
  }

  // Parse the event
  let event: { eventType: string; object: Record<string, unknown> };
  try {
    event = JSON.parse(body);
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const obj = event.object;

  switch (event.eventType) {
    case "checkout.completed": {
      const sub = obj.subscription as Record<string, unknown> | undefined;
      const customer = obj.customer as Record<string, unknown> | undefined;
      const metadata = (obj.metadata ?? sub?.metadata) as
        | Record<string, string>
        | undefined;
      const userId = metadata?.userId;
      if (!userId || !sub) break;

      await supabaseAdmin.from("subscriptions").upsert(
        {
          user_id: userId,
          creem_subscription_id: sub.id as string,
          creem_customer_id: (customer?.id as string) ?? "",
          status: (sub.status as string) ?? "active",
          product_id:
            ((obj.product as Record<string, unknown>)?.id as string) ?? "",
          current_period_start:
            (sub.current_period_start_date as string) ?? null,
          current_period_end: (sub.current_period_end_date as string) ?? null,
        },
        { onConflict: "creem_subscription_id" }
      );
      break;
    }

    case "subscription.active":
    case "subscription.paid": {
      const metadata = obj.metadata as Record<string, string> | undefined;
      const userId = metadata?.userId;
      if (!userId) break;

      const customer = obj.customer as Record<string, unknown> | undefined;
      const product = obj.product as Record<string, unknown> | undefined;

      await supabaseAdmin.from("subscriptions").upsert(
        {
          user_id: userId,
          creem_subscription_id: obj.id as string,
          creem_customer_id: (customer?.id as string) ?? "",
          status: obj.status as string,
          product_id: (product?.id as string) ?? "",
          current_period_start:
            (obj.current_period_start_date as string) ?? null,
          current_period_end: (obj.current_period_end_date as string) ?? null,
        },
        { onConflict: "creem_subscription_id" }
      );
      break;
    }

    case "subscription.canceled":
    case "subscription.expired":
    case "subscription.paused":
    case "subscription.past_due":
    case "subscription.scheduled_cancel": {
      await supabaseAdmin
        .from("subscriptions")
        .update({ status: obj.status as string })
        .eq("creem_subscription_id", obj.id as string);
      break;
    }
  }

  return NextResponse.json({ received: true });
}
```

### 5. hooks/use-subscription.ts

Client-side hook for checking subscription status:

```ts
"use client";

import useSWR from "swr";
import { getSubscriptionStatus } from "@/app/actions/subscription";
import { isEmailWhitelisted } from "@/lib/constants";
import { useAuth } from "./use-auth";

interface SubscriptionState {
  isWhitelisted: boolean;
  isSubscribed: boolean;
  isLoading: boolean;
}

export function useSubscription(): SubscriptionState {
  const { user } = useAuth();

  const isWhitelisted = isEmailWhitelisted(user?.email);

  const { data, isLoading } = useSWR(
    user ? "subscription-status" : null,
    () => getSubscriptionStatus()
  );

  return { isWhitelisted, isSubscribed: !!data, isLoading };
}
```

**Note**: This hook uses SWR for caching and revalidation. If your project doesn't use SWR, you can use `useEffect` + `useState` instead.

### 6. components/upgrade-button.tsx (Optional)

Example upgrade button component:

```tsx
"use client";

import { useState } from "react";
import { createCheckout } from "@/app/actions/subscription";

export function UpgradeButton() {
  const [loading, setLoading] = useState(false);

  const handleUpgrade = async () => {
    try {
      setLoading(true);
      const checkoutUrl = await createCheckout("pro");
      window.location.href = checkoutUrl;
    } catch (error) {
      console.error("[upgrade] Checkout error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleUpgrade} disabled={loading}>
      {loading ? "Loading..." : "Upgrade to Pro"}
    </button>
  );
}
```

## Checkout Flow

```
User clicks "Upgrade"
    ↓
Client calls createCheckout("pro") server action
    ↓
Server: verify auth → call Creem API → get checkout_url
    ↓
Client: redirect to checkout_url (Creem hosted checkout page)
    ↓
User completes payment on Creem
    ↓
Creem sends webhook (checkout.completed) → POST /api/webhooks/creem
    ↓
Webhook handler: verify signature → upsert subscription in DB
    ↓
User redirected to success_url → client revalidates subscription status
```

## Feature Gating

### Server-side Gating (in API Routes)

```ts
// Check subscription before allowing premium features
const { data: subscription } = await supabase
  .from("subscriptions")
  .select("id")
  .eq("user_id", user.id)
  .eq("status", "active")
  .maybeSingle();

const isPro = !!subscription || isEmailWhitelisted(user.email);
const contentLimit = isPro ? PRO_LIMITS.maxContentLength : FREE_LIMITS.maxContentLength;

if (content.length > contentLimit) {
  return NextResponse.json(
    { error: `Content exceeds ${contentLimit} character limit` },
    { status: 400 }
  );
}
```

### Client-side Gating (UI only — for display, not security)

```tsx
"use client";

import { useSubscription } from "@/hooks/use-subscription";

export function FeatureCard() {
  const { isSubscribed, isWhitelisted } = useSubscription();
  const isPro = isSubscribed || isWhitelisted;

  if (!isPro) {
    return (
      <div>
        <p>This feature requires a Pro subscription</p>
        <UpgradeButton />
      </div>
    );
  }

  return <div>{/* Premium feature content */}</div>;
}
```

**Important**: Client-side gating is for UI presentation only. Always enforce limits server-side (in API routes, Server Actions, or webhooks) for security.

## Database Schema

Create the `subscriptions` table in Supabase SQL Editor:

```sql
CREATE TABLE subscriptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  creem_subscription_id TEXT UNIQUE NOT NULL,
  creem_customer_id TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'active',
  product_id TEXT NOT NULL DEFAULT '',
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Users can read their own subscriptions
CREATE POLICY "Users can read own subscriptions"
  ON subscriptions FOR SELECT
  USING (auth.uid() = user_id);

-- Create index for common queries
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

## Environment Variables

Add the following to `.env.local`:

```bash
# Creem Payment
CREEM_API_KEY=your-creem-api-key
CREEM_WEBHOOK_SECRET=your-creem-webhook-secret

# Environment target (production or staging)
NODE_TARGET=staging

# Site URL (for checkout success redirect)
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Creem Product ID
NEXT_PUBLIC_PROJECT_ID=your-creem-product-id
```

## Local Development

### Testing Webhooks Locally

Use ngrok or a similar tool to expose your local server:

```bash
# Start ngrok tunnel
ngrok http 3000

# Copy the HTTPS URL and set it as the webhook URL in Creem dashboard
# Example: https://abc123.ngrok.io/api/webhooks/creem
```

### Creem Test Mode

- Use `https://test-api.creem.io/v1` for development/staging
- Use `https://api.creem.io/v1` for production
- Set `NODE_TARGET=staging` in `.env.local` for development

## Verification

1. Test checkout flow: click upgrade → redirect to Creem → complete payment → redirect back
2. Verify webhook receives events: check server logs for webhook handler output
3. Verify subscription status updates in database after payment
4. Test feature gating: free user should see limits, pro user should have full access
5. Test subscription cancellation: cancel in Creem → webhook → status updated in DB

## Troubleshooting

### Webhook Not Received

- Verify the webhook URL is publicly accessible (use ngrok for local development)
- Check that the webhook URL is registered in the Creem dashboard
- Ensure the API route path is correct: `app/api/webhooks/creem/route.ts`

### Signature Verification Failing

- Ensure `CREEM_WEBHOOK_SECRET` matches the secret in the Creem dashboard
- Read the request body as raw text (`req.text()`) before parsing — do not use `req.json()` first
- Verify the signature header name: `creem-signature`

### Subscription Status Not Updating

- Check the webhook handler logs for errors
- Verify the `userId` is included in the checkout metadata
- Ensure the admin client has the correct `SUPABASE_SERVICE_ROLE_KEY`
- Check RLS policies — webhook handler must use the admin client to bypass RLS

### Checkout Redirect Not Working

- Verify `CREEM_API_KEY` is set correctly
- Check `success_url` includes the full URL (including protocol)
- Verify the `product_id` matches a valid product in Creem dashboard

## Best Practices

1. **Always verify webhook signatures** — never process unverified webhook payloads
2. **Implement idempotent webhook handling** — the same event may be delivered multiple times, use `upsert` with `onConflict`
3. **Never trust client-side subscription status for security** — always verify server-side before granting access
4. **Store subscription data in your own database** — don't rely solely on Creem API for status checks
5. **Log webhook events** — add structured logging for debugging payment issues
6. **Handle edge cases** — payment pending, subscription lapsed, grace periods
7. **Use Server Actions for checkout** — keep API keys server-side, never expose to the client
8. **Test the full flow** — always test checkout → webhook → status update → feature access end-to-end

## Resources

- [Creem API Documentation](https://docs.creem.io)
- [Creem Webhooks Guide](https://docs.creem.io/webhooks)
- [Creem Dashboard](https://creem.io/dashboard)
