---
name: browser-extension-best-practices
description: 诊断并优化浏览器插件的架构、状态、UI、国际化、通信、测试和版本发布。用于插件优化、技术选型、设置同步、Changesets 接入、发布流程和配置升级。Use when diagnosing or improving browser extension architecture, shared state, UI, i18n, messaging, quality checks, releases, or data migrations.
---

# 浏览器插件优化

先读 [优化流程](references/guide.md)，定位当前问题，再按需读取专题。

| 当前问题 | 读取 |
| --- | --- |
| 技术选型、Jotai 状态、Base UI 组件、WXT i18n、跨上下文通信、MV3 生命周期 | [架构与界面](references/architecture-and-ui.md) |
| 测试与产物验证、Changesets、版本 PR、Release、商店提交、配置升级 | [质量与演进](references/quality-and-evolution.md) |
| README、Agent 入口、发布与开发文档分工 | [文档](references/documentation.md) |

缺少对应能力时给出明确的推荐库与最小接入路径；已有等价能力时按实际缺陷和迁移成本判断保留或替换。实现 API 以项目安装版本和官方文档为准。

分析请求交付决策与验收标准；实现请求在已授权范围内完成修改和验证。优化授权不自动包含提交商店或对外发布。
