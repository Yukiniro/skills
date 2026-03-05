# next-intl Configuration Reference

This document provides installation and configuration guidance for next-intl to implement internationalization (i18n) in Next.js projects.

**Note**: This configuration is only applicable to Next.js projects.

## Install Dependencies

Install next-intl using the project's package manager:

```bash
# pnpm
pnpm add next-intl

# yarn
yarn add next-intl

# npm
npm install next-intl

# bun
bun add next-intl
```

## Directory Structure

Create the following directories and files:

```
project-root/
├── i18n/
│   ├── routing.ts          # Routing configuration
│   ├── request.ts          # Request handling
│   └── navigation.ts       # Navigation components
├── languages/
│   ├── en.json             # English translations
│   ├── zh-CN.json          # Simplified Chinese translations
│   ├── zh-TW.json          # Traditional Chinese translations (optional)
│   └── ja.json             # Japanese translations (optional)
└── middleware.ts           # Next.js middleware
```

## Configuration Files

### 1. i18n/routing.ts

Define supported locales and default locale:

```ts
import { defineRouting } from "next-intl/routing";

export const routing = defineRouting({
  // Supported locales
  locales: ["en", "zh-CN", "zh-TW", "ja"],

  // Default locale
  defaultLocale: "en",

  // Optional: pathname configuration
  // pathnames: {
  //   '/': '/',
  //   '/about': {
  //     en: '/about',
  //     'zh-CN': '/guanyu',
  //   },
  // },
});
```

**Options explained**:

- `locales` - Array of supported locale codes
- `defaultLocale` - Default locale used when user's locale cannot be detected
- `pathnames` - Optional, configure different pathnames for different locales

### 2. i18n/request.ts

Configure request handling and message loading:

```ts
import { getRequestConfig } from "next-intl/server";
import { routing } from "./routing";

export default getRequestConfig(async ({ requestLocale }) => {
  // Get the requested locale
  let locale = await requestLocale;

  // Validate locale is supported
  if (!locale || !routing.locales.includes(locale as any)) {
    locale = routing.defaultLocale;
  }

  return {
    locale,
    // Dynamically import translation files
    messages: (await import(`../languages/${locale}.json`)).default,
  };
});
```

### 3. i18n/navigation.ts

Export internationalized navigation components:

```ts
import { createNavigation } from "next-intl/navigation";
import { routing } from "./routing";

// Create internationalized navigation utilities
export const { Link, redirect, usePathname, useRouter } =
  createNavigation(routing);
```

**Usage**:

- `Link` - Replaces Next.js `next/link`, automatically handles locale prefix
- `redirect` - Server-side redirect
- `usePathname` - Get current path (without locale prefix)
- `useRouter` - Router operations

### 4. middleware.ts

Create `middleware.ts` in the project root:

```ts
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export default createMiddleware(routing);

export const config = {
  // Match all paths except:
  matcher: [
    // Exclude API routes
    "/((?!api|_next|_vercel|.*\\..*).*)",
  ],
};
```

**Options explained**:

- `matcher` - Define paths where the middleware applies
- Excludes `/api`, `/_next`, static files, and other paths that don't need internationalization

## Translation Files

### languages/en.json

```json
{
  "common": {
    "welcome": "Welcome",
    "hello": "Hello, {name}!",
    "loading": "Loading...",
    "error": "An error occurred"
  },
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "home": {
    "title": "Welcome to our website",
    "description": "This is a multilingual website built with Next.js and next-intl"
  }
}
```

### languages/zh-CN.json

```json
{
  "common": {
    "welcome": "欢迎",
    "hello": "你好，{name}！",
    "loading": "加载中...",
    "error": "发生错误"
  },
  "nav": {
    "home": "首页",
    "about": "关于",
    "contact": "联系"
  },
  "home": {
    "title": "欢迎访问我们的网站",
    "description": "这是一个使用 Next.js 和 next-intl 构建的多语言网站"
  }
}
```

### languages/zh-TW.json (Optional)

```json
{
  "common": {
    "welcome": "歡迎",
    "hello": "你好，{name}！",
    "loading": "載入中...",
    "error": "發生錯誤"
  },
  "nav": {
    "home": "首頁",
    "about": "關於",
    "contact": "聯絡"
  },
  "home": {
    "title": "歡迎訪問我們的網站",
    "description": "這是一個使用 Next.js 和 next-intl 構建的多語言網站"
  }
}
```

### languages/ja.json (Optional)

```json
{
  "common": {
    "welcome": "ようこそ",
    "hello": "こんにちは、{name}さん！",
    "loading": "読み込み中...",
    "error": "エラーが発生しました"
  },
  "nav": {
    "home": "ホーム",
    "about": "について",
    "contact": "お問い合わせ"
  },
  "home": {
    "title": "私たちのウェブサイトへようこそ",
    "description": "これは Next.js と next-intl で構築された多言語ウェブサイトです"
  }
}
```

## Update next.config.js

Add next-intl configuration in `next.config.js` (Next.js 15+):

```js
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your other config
};

export default withNextIntl(nextConfig);
```

**Or** for CommonJS format (Next.js 14):

```js
const createNextIntlPlugin = require("next-intl/plugin");

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your other config
};

module.exports = withNextIntl(nextConfig);
```

## Update App Router Layout

### app/[locale]/layout.tsx

```tsx
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "@/i18n/routing";

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  // Validate locale parameter
  if (!routing.locales.includes(locale as any)) {
    notFound();
  }

  // Get translation messages
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

### app/[locale]/page.tsx

```tsx
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export default function HomePage() {
  const t = useTranslations("home");

  return (
    <div>
      <h1>{t("title")}</h1>
      <p>{t("description")}</p>

      <nav>
        <Link href="/">{t("nav.home")}</Link>
        <Link href="/about">{t("nav.about")}</Link>
      </nav>
    </div>
  );
}
```

## Usage Examples

### In Server Components

```tsx
import { useTranslations } from "next-intl";

export default function ServerComponent() {
  const t = useTranslations("common");

  return (
    <div>
      <h1>{t("welcome")}</h1>
      <p>{t("hello", { name: "John" })}</p>
    </div>
  );
}
```

### In Client Components

```tsx
"use client";

import { useTranslations } from "next-intl";

export default function ClientComponent() {
  const t = useTranslations("common");

  return (
    <div>
      <button>{t("loading")}</button>
    </div>
  );
}
```

### Using Internationalized Navigation

```tsx
import { Link, useRouter } from "@/i18n/navigation";

export default function Navigation() {
  const router = useRouter();

  const handleNavigate = () => {
    router.push("/about");
  };

  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <button onClick={handleNavigate}>Go to About</button>
    </nav>
  );
}
```

### Language Switcher

```tsx
"use client";

import { useLocale } from "next-intl";
import { useRouter, usePathname } from "@/i18n/navigation";
import { routing } from "@/i18n/routing";

export default function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const handleChange = (newLocale: string) => {
    router.replace(pathname, { locale: newLocale });
  };

  return (
    <select value={locale} onChange={(e) => handleChange(e.target.value)}>
      {routing.locales.map((loc) => (
        <option key={loc} value={loc}>
          {loc.toUpperCase()}
        </option>
      ))}
    </select>
  );
}
```

## Advanced Features

### Rich Text Formatting

```tsx
const t = useTranslations('messages')

// In the translation file
{
  "messages": {
    "rich": "This is <bold>bold</bold> and <link>a link</link>"
  }
}

// In the component
<p>
  {t.rich('rich', {
    bold: (chunks) => <strong>{chunks}</strong>,
    link: (chunks) => <a href="/link">{chunks}</a>,
  })}
</p>
```

### Date and Number Formatting

```tsx
import { useFormatter } from "next-intl";

export default function FormattedContent() {
  const format = useFormatter();

  const date = new Date("2024-01-15");
  const number = 1234567.89;

  return (
    <div>
      <p>{format.dateTime(date, { dateStyle: "long" })}</p>
      <p>{format.number(number, { style: "currency", currency: "USD" })}</p>
    </div>
  );
}
```

### Plurals

```tsx
// In the translation file
{
  "items": {
    "count": "{count, plural, =0 {No items} one {One item} other {# items}}"
  }
}

// In the component
const t = useTranslations('items')
<p>{t('count', { count: 5 })}</p>  // "5 items"
```

## Verification

1. Start the development server: `<PM> dev`
2. Visit `http://localhost:3000/en` to see the English version
3. Visit `http://localhost:3000/zh-CN` to see the Chinese version
4. Test the language switching functionality

## Troubleshooting

### Translation File Not Found

Ensure translation file paths are correct:

- Filenames must exactly match the locale codes in the `locales` configuration
- Files must be valid JSON format
- Check the import path in `i18n/request.ts`

### Middleware Not Working

Check the `matcher` configuration in `middleware.ts`:

- Ensure paths that need internationalization are not excluded
- Ensure the file is in the project root directory

### Type Errors

Add type definitions in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["next-intl"]
  }
}
```

## Best Practices

1. **Organize translation files**: Organize translation keys by feature module, use nested structures
2. **Translation completeness**: Ensure all language files contain the same keys
3. **Variable naming**: Use descriptive variable names, e.g., `{userName}` instead of `{x}`
4. **Default locale**: Choose the most commonly used language as the default locale
5. **SEO optimization**: Configure correct `lang` attributes and meta tags for each locale version
6. **Performance optimization**: Use dynamic imports to load translation files on demand
7. **Version control**: Keep translation files in version control for team collaboration

## Resources

- [next-intl Documentation](https://next-intl-docs.vercel.app/)
- [Next.js Internationalization Guide](https://nextjs.org/docs/app/building-your-application/routing/internationalization)
- [ICU Message Format](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
