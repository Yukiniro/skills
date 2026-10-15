# 技术栈 项目结构 国际化 组件样式与状态管理

用于需要选择依赖、调整业务边界或重构界面基础设施的任务。先按 [主文档](guide.md) 确认问题，只采用与目标项目约束匹配的部分。

## 技术栈

### 来源实现

来源项目是单包浏览器扩展。主要技术及职责如下；版本为来源快照声明的版本范围或主版本。

| 职责 | 技术 | 实际用途 |
| --- | --- | --- |
| 扩展构建 | WXT 0.21.4、Vite 8、Manifest V3 | 多入口和多浏览器构建 |
| 界面与语言 | React 19、TypeScript 7、React Router 8 | 扩展页面、类型检查、设置页 Hash Router 与懒加载 |
| 样式 | Tailwind CSS 4、Base UI、shadcn、CVA、Motion | 基础交互、组件变体、主题及动画 |
| 状态与表单 | Jotai、TanStack Query、Form、React Store | 本地共享状态、远程数据、表单及表单状态订阅 |
| 服务接入 | AI SDK 7、多种 Provider 适配器、oRPC | 模型调用与托管服务契约 |
| 扩展通信 | webext-core messaging、runtime Port | 类型化消息与流式通道 |
| 持久化 | WXT Storage、Dexie | 配置、IndexedDB 缓存与术语表 |
| 校验与国际化 | Zod 4、i18next、WXT i18n、YAML | 运行时数据边界与多语言资源 |
| 工具链 | pnpm、Nx、Vitest、Oxlint、Oxfmt | 安装、任务缓存、测试和检查 |

定义、契约和布局由相邻仓库的外部包提供。开发配置允许别名指向这些源码，并阻止这种模式下生成发布 ZIP。

依据：`package.json`、`wxt.config.ts`。

### 接入建议

先比较职责，再比较库名。已有路由、状态、表单或校验库能够履行相同契约时，沿用现有实现。WXT 适用于扩展构建；服务端框架、SSR 应用或桌面工具应依据自身入口和部署方式选择工具。

为每个新增依赖写出直接使用它的模块和替代方案。只有独立发布、复用或依赖隔离确实需要时才拆包；出现 workspace 配置或 Nx 并不自动意味着需要 monorepo。

**最小接入：** 选一个场景，接入一个缺失能力，核对生产构建及依赖变化。完成条件是业务能力可达、依赖职责清晰、原有检查仍成立。

## 项目结构

### 来源实现

| 位置 | 职责 |
| --- | --- |
| `src/entrypoints/background` | 请求队列、缓存、消息处理、配置初始化与后台服务 |
| `host.content`、`selection.content`、`subtitles.content` | 网页翻译、划词操作和字幕运行时 |
| MAIN world 拦截入口 | 在页面环境中对接播放器等能力 |
| `popup`、`options`、`sidepanel`、`translation-hub` | 独立扩展界面 |
| `offscreen` | 后台音频播放 |
| `src/components`、`hooks`、`types` | 共享组件、React 逻辑、消息及配置类型 |
| `src/utils` | 翻译、Provider、存储、迁移及其他业务实现 |

网页翻译的一条主路径是：内容脚本准备文本，通过类型化消息请求后台；后台处理缓存、排队与服务调用，再返回结果，由内容脚本更新 DOM。后台同步注册监听，再异步初始化配置和语言资源，以适应 MV3 唤醒。

依据：`src/entrypoints/background/index.ts`、`src/entrypoints/background/page-translation.ts`、`src`。

### 接入建议

按运行环境、生命周期、数据所有者与依赖方向建立边界。页面只使用的业务留在该业务附近；多个入口共享且语义稳定的能力再提取。来源项目的 `utils` 包含大量业务代码，目标项目可依据真实职责使用领域目录，无需复刻名称。

优先整理一条调用链：入口只负责组装，业务模块表达规则，适配器处理平台差异。已有函数能承载单一职责时直接复用；只有稳定差异出现后再增加接口或策略层。

**最小重构：** 抽出一个重复的服务适配或业务规则，迁移相关调用方。完成条件是状态所有权和副作用位置清晰，依赖方向可解释，没有为预想平台增加空实现。

## 国际化

### 来源实现

同一份 `src/locales/*.yml` 服务于两条路径：WXT 生成 manifest 使用的 `_locales` 产物和翻译键类型；运行时通过 YAML 插件载入资源，由 i18next 提供可切换语言的 UI 文案。

`utils/i18n` 提供兼容门面，保留 `i18n.t(key, substitutions)` 调用方式，将 `$1` 等占位符转换为 i18next 插值。Prompt 中的命名占位符单独保留，避免翻译阶段提前消费。语言由 `uiLanguage` 解析，“auto”跟随浏览器，不支持的语言回退到默认语言；内容目标语言与界面语言另行处理。

每个 JS 上下文分别初始化国际化。React 的 `LocaleBoundary` 根据解析后的 locale 给子树重新设置 key，使文案重新计算；Jotai 与 Query Provider 位于该边界外。背景菜单等创建时固定的文案需要显式重建。

依据：`src/utils/i18n/index.ts`、`src/utils/i18n/resources.ts`、`src/utils/i18n/locale-boundary.tsx`、`wxt.config.ts`。

### 接入建议

| 目标需求 | 合适做法 |
| --- | --- |
| 当前国际化已支持所需行为 | 保留库、资源格式与订阅机制 |
| 替换引擎但调用方很多 | 用窄门面适配旧 API，按模块迁移调用方 |
| 需要运行时语言切换 | 定义语言来源、回退和订阅，更新依赖语言的派生值 |
| 同时存在 UI 文案和 Prompt 模板 | 明确各阶段消费的占位符，分别验证 |
| 语言资源较大，需要异步加载 | 等待目标资源就绪后切换，定义加载与错误行为 |

整棵子树重新挂载会重置其内部组件状态、草稿和编辑器实例。只有这些状态可以重建时才采用 来源项目的方式；需要保留编辑会话时，优先使用现有国际化订阅或更小刷新边界。其同步资源假设也需要与目标项目核对。

`escapeValue: false` 是来源配置，不能视为任意 HTML 渲染授权；输出到 React 文本、HTML 或 Prompt 时仍按各自边界处理。

**最小接入：** 迁移一个页面及一组非 React 文案。完成条件是首屏、切换、回退和占位符结果正确，并验证草稿、焦点与持久状态符合产品契约。通用测试若把 i18n 和语言边界 mock 掉，需要另做真实切换验证。

## 组件与样式

### 来源实现

`theme.css` 将背景、文本、边框、品牌、危险状态、圆角和阴影组织为语义 Token，通过 `--rf-*` 变量映射到 Tailwind。Base UI 提供交互原语，组件通过 CVA 定义 `variant` 与 `size`，业务组件消费统一基础组件。`components.json` 指定 shadcn 的生成目录和样式入口。

独立扩展页面把主题应用到文档根；注入 UI 可以指定容器，在 Shadow DOM 内使用主题。PostCSS 将 Tailwind 内部 `--tw-*` 属性改名前缀，并将 rem 转成 px，以降低宿主网页环境影响。Shadow DOM 仍会涉及继承变量、字体、Portal 与定位边界，需要配套处理。

依据：`src/assets/styles/theme.css`、`src/components/ui/base-ui/button.tsx`、`src/components/providers/theme-provider.tsx`、`postcss.config.cjs`。

### 接入建议

先统一语义 Token，再统一重复组件，最后按需要调整工具链。CSS Modules、现有组件库或其他样式方案也可以消费同一组 CSS 变量。优先为真实交互增加明确的组件变体；业务编排与无业务含义的基础组件分别维护。

普通 Web 应用无需为扩展宿主兼容而整体引入 Shadow DOM、变量重命名或 rem 转 px。嵌入第三方页面的项目应在冲突页面上验证隔离方案；单位策略需要同时检查浏览器缩放、用户字体偏好和布局要求。

**最小接入：** 选择高频按钮与一个表单，统一其 Token、状态和用法。完成条件是亮暗主题、禁用、错误、键盘焦点及浮层定位符合预期，并能删除被替代的重复样式。

## 状态管理

### 来源实现

| 数据 | 来源项目的主要承载方式 | 可借鉴的边界 |
| --- | --- | --- |
| 组件短期交互 | React 局部状态 | 由拥有交互的组件管理 |
| 共享配置视图与派生值 | Jotai、selectAtom、atomFamily | 订阅实际消费的数据 |
| 远程数据与 mutation | TanStack Query、oRPC 工具 | 查询键、失效、请求和错误归远程数据层 |
| 表单草稿、校验和保存状态 | TanStack Form、相关 Store 订阅、自动保存会话 | 草稿与已提交状态分开 |
| 持久配置 | WXT Storage 与 Zod adapter | 对外部数据校验，集中管理写入 |
| 翻译缓存与术语数据 | Dexie/IndexedDB | 按查询、容量及持久性需求组织 |

`writeConfigAtom` 先乐观更新，再通过当前上下文内的 Promise 队列重新读存储、合并并保存；数组更新采用覆盖语义。版本计数避免旧任务覆盖较新的本地视图。Storage watch 被用作重新读取的通知，另在页面重新可见时刷新。队列属于当前 JS 上下文，不能提供多个标签页或扩展页面之间的原子写入保证。

依据：`src/utils/atoms/config.ts`、`src/utils/tanstack-query.ts`、`src/entrypoints/options/pages/custom-actions/action-config-form/form.ts`、`src/utils/db/dexie/app-db.ts`。

### 接入建议

先为每类数据确定唯一权威来源、读者、写者、生命周期和恢复方式，再决定是否新增 Store。已有状态库可承担共享客户端状态；远程响应可以直接由已有查询层消费，避免再复制到全局 Store。

自动保存需定义校验失败、写入失败、输入法组合输入、路由切换和退出时的 flush 行为。乐观更新的回退必须与正在进行的新写入相容。多个上下文会竞争写入时，评估单一后台写入者、版本检查或存储事务，依据目标平台选一种明确机制。

**最小重构：** 选择一个存在丢更新或状态重复的字段，收敛写入入口和订阅路径。完成条件是快速连续编辑、失败回退、切页再返回和跨上下文更新都可解释，临时副本不再承担独立真值。
