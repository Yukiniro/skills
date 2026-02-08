# next-intl 配置参考

本文档提供 next-intl 的安装和配置指南，用于在 Next.js 项目中实现国际化（i18n）。

**注意**：此配置仅适用于 Next.js 项目。

## 安装依赖

使用项目的包管理器安装 next-intl：

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

## 目录结构

创建以下目录和文件：

```
project-root/
├── i18n/
│   ├── routing.ts          # 路由配置
│   ├── request.ts          # 请求处理
│   └── navigation.ts       # 导航组件
├── languages/
│   ├── en.json             # 英文翻译
│   ├── zh-CN.json          # 简体中文翻译
│   ├── zh-TW.json          # 繁体中文翻译（可选）
│   └── ja.json             # 日文翻译（可选）
└── middleware.ts           # Next.js 中间件
```

## 配置文件

### 1. i18n/routing.ts

定义支持的语言和默认语言：

```ts
import { defineRouting } from 'next-intl/routing'

export const routing = defineRouting({
  // 支持的语言列表
  locales: ['en', 'zh-CN', 'zh-TW', 'ja'],
  
  // 默认语言
  defaultLocale: 'en',
  
  // 可选：路径名配置
  // pathnames: {
  //   '/': '/',
  //   '/about': {
  //     en: '/about',
  //     'zh-CN': '/guanyu',
  //   },
  // },
})
```

**配置说明**：
- `locales` - 支持的语言代码数组
- `defaultLocale` - 默认语言，当检测不到用户语言时使用
- `pathnames` - 可选，为不同语言配置不同的路径名

### 2. i18n/request.ts

配置请求处理和消息加载：

```ts
import { getRequestConfig } from 'next-intl/server'
import { routing } from './routing'

export default getRequestConfig(async ({ requestLocale }) => {
  // 获取请求的语言
  let locale = await requestLocale

  // 验证语言是否支持
  if (!locale || !routing.locales.includes(locale as any)) {
    locale = routing.defaultLocale
  }

  return {
    locale,
    // 动态导入翻译文件
    messages: (await import(`../languages/${locale}.json`)).default,
  }
})
```

### 3. i18n/navigation.ts

导出国际化导航组件：

```ts
import { createNavigation } from 'next-intl/navigation'
import { routing } from './routing'

// 创建国际化导航工具
export const { Link, redirect, usePathname, useRouter } =
  createNavigation(routing)
```

**使用方式**：
- `Link` - 替代 Next.js 的 `next/link`，自动处理语言前缀
- `redirect` - 服务端重定向
- `usePathname` - 获取当前路径（不含语言前缀）
- `useRouter` - 路由操作

### 4. middleware.ts

在项目根目录创建 `middleware.ts`：

```ts
import createMiddleware from 'next-intl/middleware'
import { routing } from './i18n/routing'

export default createMiddleware(routing)

export const config = {
  // 匹配所有路径，除了以下：
  matcher: [
    // 排除 API 路由
    '/((?!api|_next|_vercel|.*\\..*).*)',
  ],
}
```

**配置说明**：
- `matcher` - 定义中间件应用的路径
- 排除 `/api`、`/_next`、静态文件等不需要国际化的路径

## 翻译文件

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

### languages/zh-TW.json（可选）

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

### languages/ja.json（可选）

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

## 更新 next.config.js

在 `next.config.js` 中添加 next-intl 配置（Next.js 15+）：

```js
import createNextIntlPlugin from 'next-intl/plugin'

const withNextIntl = createNextIntlPlugin('./i18n/request.ts')

/** @type {import('next').NextConfig} */
const nextConfig = {
  // 你的其他配置
}

export default withNextIntl(nextConfig)
```

**或者** 对于 CommonJS 格式（Next.js 14）：

```js
const createNextIntlPlugin = require('next-intl/plugin')

const withNextIntl = createNextIntlPlugin('./i18n/request.ts')

/** @type {import('next').NextConfig} */
const nextConfig = {
  // 你的其他配置
}

module.exports = withNextIntl(nextConfig)
```

## 更新 App Router 布局

### app/[locale]/layout.tsx

```tsx
import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'
import { notFound } from 'next/navigation'
import { routing } from '@/i18n/routing'

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }))
}

export default async function LocaleLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode
  params: { locale: string }
}) {
  // 验证语言参数
  if (!routing.locales.includes(locale as any)) {
    notFound()
  }

  // 获取翻译消息
  const messages = await getMessages()

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
```

### app/[locale]/page.tsx

```tsx
import { useTranslations } from 'next-intl'
import { Link } from '@/i18n/navigation'

export default function HomePage() {
  const t = useTranslations('home')

  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
      
      <nav>
        <Link href="/">{t('nav.home')}</Link>
        <Link href="/about">{t('nav.about')}</Link>
      </nav>
    </div>
  )
}
```

## 使用示例

### 在服务端组件中使用

```tsx
import { useTranslations } from 'next-intl'

export default function ServerComponent() {
  const t = useTranslations('common')

  return (
    <div>
      <h1>{t('welcome')}</h1>
      <p>{t('hello', { name: 'John' })}</p>
    </div>
  )
}
```

### 在客户端组件中使用

```tsx
'use client'

import { useTranslations } from 'next-intl'

export default function ClientComponent() {
  const t = useTranslations('common')

  return (
    <div>
      <button>{t('loading')}</button>
    </div>
  )
}
```

### 使用国际化导航

```tsx
import { Link, useRouter } from '@/i18n/navigation'

export default function Navigation() {
  const router = useRouter()

  const handleNavigate = () => {
    router.push('/about')
  }

  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <button onClick={handleNavigate}>Go to About</button>
    </nav>
  )
}
```

### 语言切换器

```tsx
'use client'

import { useLocale } from 'next-intl'
import { useRouter, usePathname } from '@/i18n/navigation'
import { routing } from '@/i18n/routing'

export default function LanguageSwitcher() {
  const locale = useLocale()
  const router = useRouter()
  const pathname = usePathname()

  const handleChange = (newLocale: string) => {
    router.replace(pathname, { locale: newLocale })
  }

  return (
    <select value={locale} onChange={(e) => handleChange(e.target.value)}>
      {routing.locales.map((loc) => (
        <option key={loc} value={loc}>
          {loc.toUpperCase()}
        </option>
      ))}
    </select>
  )
}
```

## 高级功能

### 富文本格式化

```tsx
const t = useTranslations('messages')

// 在翻译文件中
{
  "messages": {
    "rich": "This is <bold>bold</bold> and <link>a link</link>"
  }
}

// 在组件中
<p>
  {t.rich('rich', {
    bold: (chunks) => <strong>{chunks}</strong>,
    link: (chunks) => <a href="/link">{chunks}</a>,
  })}
</p>
```

### 日期和数字格式化

```tsx
import { useFormatter } from 'next-intl'

export default function FormattedContent() {
  const format = useFormatter()

  const date = new Date('2024-01-15')
  const number = 1234567.89

  return (
    <div>
      <p>{format.dateTime(date, { dateStyle: 'long' })}</p>
      <p>{format.number(number, { style: 'currency', currency: 'USD' })}</p>
    </div>
  )
}
```

### 复数形式

```tsx
// 在翻译文件中
{
  "items": {
    "count": "{count, plural, =0 {No items} one {One item} other {# items}}"
  }
}

// 在组件中
const t = useTranslations('items')
<p>{t('count', { count: 5 })}</p>  // "5 items"
```

## 验证配置

1. 启动开发服务器：`<PM> dev`
2. 访问 `http://localhost:3000/en` 查看英文版本
3. 访问 `http://localhost:3000/zh-CN` 查看中文版本
4. 测试语言切换功能

## 故障排除

### 翻译文件找不到

确保翻译文件路径正确：
- 文件名必须与 `locales` 配置中的语言代码完全匹配
- 文件必须是有效的 JSON 格式
- 检查 `i18n/request.ts` 中的导入路径

### 中间件不生效

检查 `middleware.ts` 的 `matcher` 配置：
- 确保没有排除需要国际化的路径
- 确保文件位于项目根目录

### 类型错误

在 `tsconfig.json` 中添加类型定义：

```json
{
  "compilerOptions": {
    "types": ["next-intl"]
  }
}
```

## 最佳实践

1. **翻译文件组织**：按功能模块组织翻译键，使用嵌套结构
2. **翻译完整性**：确保所有语言文件包含相同的键
3. **变量命名**：使用描述性的变量名，如 `{userName}` 而非 `{x}`
4. **默认语言**：选择最常用的语言作为默认语言
5. **SEO 优化**：为每个语言版本配置正确的 `lang` 属性和 meta 标签
6. **性能优化**：使用动态导入按需加载翻译文件
7. **版本控制**：将翻译文件纳入版本控制，便于团队协作

## 参考资源

- [next-intl 官方文档](https://next-intl-docs.vercel.app/)
- [Next.js 国际化指南](https://nextjs.org/docs/app/building-your-application/routing/internationalization)
- [ICU 消息格式](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
