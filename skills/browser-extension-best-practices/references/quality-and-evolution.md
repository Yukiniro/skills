# 工程质量 Changesets 与配置升级迁移

用于建立检查、调整发布流程或演进已持久化配置的任务。先确认 [主文档](guide.md) 中的业务问题和最小范围。发布版本与配置 Schema 版本分别表示交付批次和数据兼容边界。

## 工程质量管理

### 来源实现

来源项目使用 pnpm 锁定依赖，Node 和 pnpm 版本从包配置声明。Oxlint 承担规则与类型检查，Oxfmt 处理格式、导入与 Tailwind 类排序；`lint` 和 `type-check` 当前调用相同命令。Husky 在提交前运行 lint-staged，在 commit-msg 阶段执行 commitlint。

PR CI 执行格式检查、Lint/类型检查、构建和 Vitest，另检查调试工具导入。PR 标题通过 Conventional Commits 校验并映射标签。Nx 用于任务缓存；当前 PR 流程只在部分步骤显式通过 Nx 执行。

测试默认使用 Node，部分测试使用 jsdom；免费翻译服务测试依赖外部网络，Agent 本地通过 `SKIP_FREE_API=true` 跳过，PR CI 则通过 exclude 排除。测试 setup mock 了国际化及 `LocaleBoundary`，这类通用测试不能证明真实语言切换行为。

依据：`package.json`、`.github/workflows/pr-test.yml`、`vitest.config.ts`、`vitest.setup.ts`、`AGENTS.md`。

### 接入建议

| 已有问题 | 最小可用改进 | 验收 |
| --- | --- | --- |
| 本地与 CI 命令不一致 | 由项目脚本提供唯一入口 | 相同安装条件可重现检查结果 |
| 类型或核心业务错误进入主分支 | 增加对应类型检查或行为回归 | 代表性错误能被识别，正确实现通过 |
| 实网测试不稳定 | 区分确定性回归与外部服务验证 | 跳过项明确，实网能力另有验证入口 |
| 多人提交格式频繁冲突 | 在现有工具中统一格式配置 | 修改范围可控，本地与 CI 一致 |
| 检查成本已成为瓶颈 | 先测量，再评估任务缓存 | 缓存命中有收益，输入变化能正确失效 |

保留目标项目已工作的 ESLint、Prettier、测试框架和 CI。需要替换时，先比较规则覆盖、插件兼容与耗时，再迁移一个可独立验证的范围。任务缓存应覆盖源码、依赖、工具配置和会影响输出的环境变量。

测试围绕用户行为、边界契约和数据兼容选择；低风险的机械编辑用相称检查即可。报告分别说明目标检查、全量检查、跳过项与人工验证，避免用 mock 覆盖的结果代替浏览器证明。

## Changesets 设计

### 来源实现

来源根包为 `private: true`。`.changeset/config.json` 允许私有包参与版本更新和打标签，基准分支为 main，使用 GitHub changelog 生成器；`fixed`、`linked` 为空，适配单包发布。

每次面向用户的功能或修复通常附带一条记录：

```markdown
---
"package-name": patch
---

fix(subtitles): preserve the selected caption track
```

包名对应实际 workspace 包。Conventional Commit 描述变更性质，frontmatter 决定升级级别；两者分别维护。来源 PR 技能将修复、小增强和单个开关等归为 patch，完整新功能或新 Provider 等归为 minor，major 则用于需要用户适应的不兼容变化并要求显式批准。这是该项目的产品政策。

发布过程为：业务 changeset 合入 main，Action 聚合并创建版本 PR，更新版本与 CHANGELOG、消费记录；版本 PR 合入后执行 `changeset git-tag`，创建 GitHub Release，再构建并上传 Chrome、Edge、Firefox 和源码 ZIP。商店提交由另一个手动工作流触发，当前提交 Chrome 与 Edge。

来源流程的边界：PR 技能要求 `changeset status`，但 PR CI 没有该步骤，也没有完整的遗漏记录检查；major 工作流对同仓库 PR 留评论，对 fork 的 major 变更使检查失败。Release 创建早于 ZIP 构建，构建失败可能留下缺少附件的 Release。

依据：`.changeset/config.json`、`.agents/skills/prepare-pr/SKILL.md`、`.github/workflows/release.yml`、`.github/workflows/submit.yml`、`.github/workflows/changeset-major-warning.yml`。

### 接入建议

先确定发布单元与发布渠道：单个应用可以聚合为一个产品版本；公共库要考虑消费者兼容和包注册表；真正多包项目才需要评估联动依赖策略。已有发布工具能提供人工变更意图、版本审核和可追溯产物时，可以保留。

团队应明确 patch、minor、major 的产品与 API 语义，特别是库项目按消费者兼容性判定。`feat` 不自动等于 minor，小功能用 patch 也需要符合项目自己的版本契约。配置 Schema 升级独立判断。

**渐进接入：** 先在一个发布单元引入变更记录与 release PR，再接自动产物，最后按授权接发布渠道。CI 校验记录可解析、包名和升级级别正确，并提供明确的免发布理由。人工发布边界由目标项目交付要求决定。

**完成条件：** 一条修复和一条功能变更能汇总成预期版本与日志；校验或构建失败时发布流程停在可恢复的位置；产物对应明确提交，版本来源唯一，重复运行能恢复而不重复发版。对外公开 Release 前可先构建验证，或通过草稿 Release 等机制保证完整产物后再公开。

## 配置升级迁移

### 来源实现

当前 `CONFIG_SCHEMA_VERSION = 112`。配置存于 `local:config`，`schemaVersion` 与 `lastModifiedAt` 放在 WXT metadata。迁移脚本按 `vNNN-to-vNNN.ts` 排列，每步只升级一级，导出 `migrate(oldConfig)`。

Vite glob 收集脚本；注册表校验起点、单级递增、重复目标、连续性及终点。v109 配置升级到 v112 时，依次执行 109→110→111→112，最终通过当前 Zod Schema 校验。普通配置读取只校验，迁移注册表由需要迁移的入口引入。

| 入口 | 行为与失败策略 |
| --- | --- |
| 后台 `initializeConfig` | 无配置时生成最新默认值；缺少版本时按 v1；逐步迁移后写配置和 metadata；保留已有修改时间 |
| 启动迁移异常 | 单步报错后推进版本并继续；最终校验失败时重建默认值；没有统一的未来版本拒绝检查 |
| `migrateConfig` | 未来版本直接拒绝；单步失败或最终校验失败抛错；函数本身不持久化 |
| 导入与恢复 | 先完成迁移和相关输入检查，再备份当前配置并应用结果 |
| 云端与同步基线 | 读取历史数据时迁移；云端未来版本错误向上传递，其他远端迁移错误按远端不可用处理 |

启动通过后台共享 Promise 避免同一实例并发初始化；配置与 metadata 分别写入，不构成整体原子事务。自动备份是独立定时机制，启动迁移本身没有迁移前备份步骤。

两种脚本展示了 Schema 版本的用途：v111→112 为缺失的段落快捷键补 `Alt+Q` 并保留用户已有值；v110→111 不改数据，仅提高兼容边界，使旧客户端同步时拒绝新配置，避免旧 Schema 丢弃新字段后再上传。

依据：`src/utils/config/migration.ts`、`src/utils/config/init.ts`、`src/utils/google-drive/storage.ts`、`src/utils/config/migration-scripts/v111-to-v112.ts`、`src/utils/config/migration-scripts/v110-to-v111.ts`。

### 接入建议

有已发布持久数据、导入文件或多客户端同步时，优先建立明确版本与恢复契约。只有可丢弃缓存、且重建成本可接受时，可以选择失效重建。

1. **定义版本与入口。** 发布版本、配置 Schema、IndexedDB 数据库版本分别管理，列出启动、导入、恢复、同步全部入口。完成条件：每种历史数据都能找到唯一版本解释。
2. **固定历史转换。** 每步只负责一个明确版本差异，历史默认值在脚本内固定。完成条件：未来业务常量变化不改变旧迁移结果；已有用户值按规则保留。
3. **验证连续链。** 依据平台选择显式注册表或构建时发现。完成条件：缺步、重复、跨级和终点不一致可在交付前发现。
4. **先完成内存转换。** 从保留的原始数据生成候选值，拒绝不支持的未来版本，再做最终校验。完成条件：失败时原数据和可恢复信息仍存在。
5. **定义提交与恢复。** 选择事务、临时槽位或其他平台支持的方式协调配置与版本写入。完成条件：中断后能识别已完成状态并安全重试。
6. **统一错误契约。** 所有入口明确拒绝、恢复或重建的条件。完成条件：失败步骤不会被静默标为成功，重要用户数据的恢复行为可预测。
7. **控制首次访问。** 让需要稳定配置的消费者等待初始化或使用明确的兼容读路径。完成条件：首次读取不会把旧配置误判为损坏并提前覆盖。
8. **验证真实历史。** 覆盖单步、最旧支持版本到最新、已有值保留、重复执行、未来版本和失败恢复。完成条件：代表性历史样本通过，数据写入失败有可重现的处理结果。

脚本应隔离变化中的业务代码。来源项目用 `any` 表达历史形状，目标项目也可用 `unknown` 加局部历史类型和校验，依据现有类型规范决定。幂等是脚本需要验证的性质，不能从顺序执行自然推出。

迁移中存在“缺失”和“用户显式选择”的区别时，在转换完成前保留该信息；过早由 Schema 默认值补齐，可能让迁移无法判断来源。迁移也可能早于国际化初始化，新增实体的持久字段应按当时契约完整生成。

来源已有注册表检查、v1 到最新全链测试和逐版本样本；部分单步测试会依据历史样本是否存在决定验证范围。新增迁移应补自己的历史样本与预期，不能仅以框架存在断言覆盖完整。

依据：`.agents/skills/migration-scripts/SKILL.md`、`src/utils/config/__tests__/migration-scripts/all-migrations.test.ts`、`src/utils/config/__tests__/migration-scripts/v111-to-v112.test.ts`。
