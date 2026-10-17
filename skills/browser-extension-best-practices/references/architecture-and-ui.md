# 架构与界面

按 [优化流程](guide.md) 限定场景。以下是缺少对应能力时的默认推荐；已有等价实现按职责、缺陷和迁移成本决定是否替换。

## 推荐技术与模块边界

| 能力 | 推荐 | 接入条件 |
| --- | --- | --- |
| 扩展工程 | WXT + TypeScript | 新建或需要多入口、浏览器目标和产物管理时优先；现有框架迁移须有明确收益 |
| 复杂交互界面 | React | 多组件共享状态和复杂控件需要时采用；简单内容脚本可直接使用 DOM |
| React 共享状态 | Jotai | 设置、选中项和派生视图跨组件共享，详见状态管理 |
| 可访问交互原语 | Base UI（`@base-ui/react`） | React 下拉框、对话框、滑块等；样式沿用现有方案 |
| 扩展国际化 | WXT i18n（`@wxt-dev/i18n`） | 类型化翻译与浏览器语言、manifest 资源集成 |
| 设置持久化 | WXT Storage 或现有 browser.storage 适配层 | 集中读写、订阅和校验；演进格式时接版本机制 |
| 版本与变更记录 | Changesets | 用户可见变更、版本 PR 与发布追踪，见 [质量与演进](quality-and-evolution.md) |

仅在出现对应需求时增加 TanStack Query（远程缓存）、TanStack Form（复杂表单）、Zod（复杂运行时数据校验）或 Dexie（结构化 IndexedDB 数据）。简单字段可用局部状态和显式校验。依赖版本从项目及官方兼容要求确认，不在指南固定版本矩阵。

按运行环境组织模块：后台协调扩展能力，内容脚本操作所在页面，popup/options/sidepanel 组合界面，共享模块承载稳定的业务规则与消息类型。业务代码靠近功能，平台适配集中在边界；目录名称沿用项目习惯。只因出现多个入口而拆包通常没有收益，独立交付或依赖隔离才构成拆分理由。

## 状态管理

**推荐 Jotai 管理 React 共享客户端状态。** 用基础 atom 保存已加载视图，用派生 atom 或 `selectAtom` 订阅实际消费的字段；只读、只写组件分别使用 `useAtomValue`、`useSetAtom`。在稳定位置创建 atom 和 store，避免 render 时重建。需要 React 外访问时使用 `createStore` 的 `get/set/sub`；同一界面用 Provider 传入该 store。[Jotai Store 文档](https://jotai.org/docs/core/store)

| 数据 | 权威位置 | 更新边界 |
| --- | --- | --- |
| 短期 UI 状态 | 拥有交互的组件 | 关闭或卸载后可重建 |
| 已提交设置 | 扩展存储或负责它的服务 | atom 是内存视图，写成功后与持久值一致 |
| 表单草稿 | 当前编辑会话 | 校验与提交后才改变已提交值 |
| 远程数据 | 查询缓存 | 请求、失效和错误由查询层负责 |
| DOM/媒体状态 | 所在页面对象 | 消息读取快照，UI 副本不能独立充当真值 |

**最小接入：** 选择一个设置字段，统一存储 adapter、读取初始化、写入 action 与订阅，再迁移消费它的组件。只在多个入口需要同一契约时提取共享工厂，保持存储可替换以便验证失败行为。

持久化边界把外部值作为 `unknown` 校验。TypeScript 泛型不提供运行时校验；默认值补齐也不等于历史迁移。WXT 项目优先用 `storage.defineItem` 集中 key、fallback、watch 和需要时的版本配置；现有 adapter 已满足契约时保留。[WXT Storage 文档](https://wxt.dev/storage.html)

异步规则：

- 初始化读取须在消费者保存前完成，或定义兼容读路径，防止默认值覆盖旧设置。
- 同实例排队写入时，用最新持久值合并字段补丁；旧任务的成功或失败不能覆盖更新的乐观视图。失败回滚仅撤销该次尚未被后续修改取代的内容。
- 订阅通知可触发重读；用请求代次或版本丢弃过期结果，卸载时取消订阅。自动保存另定义校验、输入法组合输入及离开页面时的 flush 行为。
- popup、options、content、background 各有独立 JS 上下文。Jotai store、Promise 队列和 storage watch 均不提供跨上下文事务。出现竞争时，优先收敛为后台单一写入入口并按持久对象串行处理，或采用支持事务的存储；所有调用方都必须遵循同一协议。普通 storage 的“读版本再写”也不是原子比较交换。

**验收：** 快速连续编辑、初次读取与写入交错、旧写失败、新写成功、卸载后通知，以及两个独立上下文同时改不同字段。单 store 测试只能证明该实例内行为。后台队列重启后如何恢复，继续按下文生命周期处理。

## 组件与样式

**推荐 Base UI 提供交互原语。** 在现有样式体系中定义背景、文本、边框、品牌、危险、焦点与间距等语义 Token，再封装业务确实重复的控件和变体。Base UI 本身不提供视觉皮肤，可配合 CSS Modules、普通 CSS 或 Tailwind；需要预制组件时再选用基于 Base UI 的 shadcn 组件，按项目实际生成配置核对底层实现。[Base UI 概览](https://base-ui.com/react/overview/about)

**最小接入：** 替换一个重复或存在键盘缺陷的控件，保留业务 props，统一其加载、禁用、错误和焦点状态。引入组件库后仍验证可访问名称、键盘操作、焦点回归与屏幕阅读器语义。

独立扩展页面在文档根应用主题；注入网页的 UI 在自己的容器中应用主题。Shadow DOM 场景显式选择组件 Portal 容器，使样式、层级和交互范围一致；Base UI Dialog 的 Portal 默认挂到 body，可通过 `container` 指定 HTMLElement 或 ShadowRoot。[Dialog Portal 文档](https://base-ui.com/react/components/dialog)

Shadow DOM 仍需检查继承字体、CSS 变量、浮层定位、页面缩放与宿主快捷键。仅在确认冲突时增加变量前缀或单位转换，保留用户缩放与字体偏好的可用性。

**验收：** popup 尺寸限制、亮暗主题、长文案、键盘开关与返回焦点；注入 UI 另在冲突页面、滚动和全屏场景验证浮层。

## 国际化

**推荐 WXT i18n 作为 WXT 扩展的基础。** 安装 `@wxt-dev/i18n`，在 WXT 配置的 `modules` 中合并加入 `@wxt-dev/i18n/module`，设置 `manifest.default_locale`，将资源放在配置的 `srcDir` 下的 `locales/`。通过 `#i18n` 的 `i18n.t` 使用类型化键，构建生成 `_locales`；manifest 用 `__MSG_key__` 引用文案。[WXT i18n 文档](https://wxt.dev/i18n.html)

先区分两种语言契约：

| 需求 | 推荐方式 |
| --- | --- |
| UI 跟随浏览器语言 | WXT i18n 与浏览器 locale 回退，减少各入口重复打包语言资源 |
| 用户在扩展内独立切换语言 | 保留 WXT 生成 manifest 资源，增加 i18next 等运行时引擎和订阅，尽量复用同一资源源文件 |

WXT i18n 基于浏览器 i18n，单独使用不提供扩展内任意语言切换。运行时方案需明确语言设置、支持列表、默认回退、异步资源就绪与失败行为，每个 JS 上下文独立初始化。UI 语言与内容处理目标语言分别存储。背景菜单等创建时固定的文案需在语言变化后重建。

**最小接入：** 迁移一个页面和一组非 React 文案，检查全部支持语言的键、占位符与复数需求；统一资源格式或提供明确的生成转换。需要替换引擎时使用窄门面保留调用契约。Prompt 等模板的占位符应按消费阶段处理，翻译结果仍按文本或 HTML 输出边界转义。

**验收：** 首屏、缺键回退、占位符、manifest 与 `_locales` 产物、长文案；有应用内切换时验证草稿、焦点和编辑器实例保留。整棵子树改 key 会重置内部状态，优先订阅更新。mock 掉 i18n 的测试不能证明真实语言行为。

## 通信与生命周期

消息少时沿用 `runtime.sendMessage`；请求较多且需类型契约时推荐 [`@webext-core/messaging`](https://webext-core.aklinker1.io/messaging/installation)，流式或持续会话按需要使用 Port。静态类型不能替代接收端校验。

- 验证发送者身份、消息类型、目标对象与 payload 范围；优先使用浏览器提供的 tab/frame 身份。页面可控输入不能直接获得任意 URL 请求、脚本执行或存储能力。
- 多 frame 对象使用包含 frame 身份的稳定路由。广播汇总可以容忍局部失败，但需区分“目标已消失”和“该 frame 暂时不可读”；后者不应悄悄改变用户选中对象。
- 顺序敏感命令在第一次异步等待前入队，按真正共享资源选择队列粒度。单 tab 队列不保护跨 tab 共享设置。某项失败后保留错误结果并让后续任务继续；页面导航后旧任务通过会话标识失效或取消。
- 监听器同步注册。异步回复按目标浏览器契约保持通道；使用回调模式时同步返回 `true`，并为可处理消息提供成功或错误响应。Promise listener 支持需核对目标浏览器版本。[Chrome 消息文档](https://developer.chrome.com/docs/extensions/develop/concepts/messaging)
- MV3 worker 可终止，内存 Map、选中项和队列不能充当持久真值。为状态分别选择丢弃、重新发现、session/local 存储或事务恢复；重试有副作用的命令需定义幂等或去重。不要靠常驻计时器假定后台永存。[Worker 生命周期](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle)
- 内容脚本在失效或卸载时清理监听器、observer、计时器、storage watch 与 UI root。按需要处理 SPA 导航、重复注入和 frame 消失。

权限围绕功能声明：用户手动触发时评估 `activeTab` 与按需注入；持续自动处理网页时评估相应 host permissions，支持时按需申请 optional permissions。修改权限须验证实际入口和拒绝路径，不能为缩短审核擅自削弱已约定功能。MAIN world 仅在确需页面上下文能力时使用，桥接输入按不可信处理。

**验收：** 非法发送者与 payload、frame 失败、快速命令及失败后继续、导航后的旧任务、worker 冷启动与重启、重新注入和权限拒绝。产物层与浏览器层检查见 [工程质量](quality-and-evolution.md#工程质量)。
