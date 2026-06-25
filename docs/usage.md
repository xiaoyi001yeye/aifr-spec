# AIFR Spec 使用指南

本文面向使用者，说明每种能力适合什么时候用、可以怎么向 Codex 提出、需要提供什么输入，以及通常会得到什么输出。

README 负责说明 AIFR Spec 是什么和核心约定；本文件负责说明怎么用。更底层的格式、命名、质量标准和示例仍放在 `references/` 中。

## 快速选择

| 你想做什么 | 应使用的能力 | 可以怎么说 |
| --- | --- | --- |
| 把模糊需求问清楚 | 需求 grill | `用 AIFR 交互式 grill 这个需求：...` |
| 不想来回回答，先让 AI 自查需求边界 | 自我 grill | `用 AIFR 自我 grill 这个需求：...` |
| 把自然语言需求变成 YAML | 需求转 Spec | `把下面需求转成 AIFR spec：...` |
| 修改已有需求并判断版本号 | 版本更新 | `这个变更应该升 patch/minor/major 吗？请更新 spec。` |
| 检查 spec 是否可评审 | 质量检查 | `检查这个 AIFR spec：path/to/spec.aifr.yaml` |
| 审计实现覆盖状态 | 实现审计 | `审计 REQ-PAY-0012 的实现状态，并更新 implemented tests。` |
| 查找某条需求文件 | 定位需求 | `找到 REQ-PAY-0012 对应的 AIFR spec。` |
| 给代码入口补需求追踪注释 | 代码入口注释 | `给这个实现入口补 AIFR 追踪注释，需求是 REQ-PAY-0012。` |
| 记录外部事实来源 | Source Snapshot | `这个需求依赖外部赛程/价格/政策，请建立 source snapshot。` |
| 比较两个需求版本 | 版本比较 | `比较这两个 AIFR spec 的语义变化。` |
| 描述一次发布包含哪些需求版本 | Baseline | `为这个 release 生成 AIFR baseline。` |

## 需求 Grill

适合在需求还没清楚到可以实现或写 spec 时使用。它会先围绕业务目标、范围、规则、边界场景、验收标准、接口影响和风险补齐需求。

可以这样说：

```text
用 AIFR 交互式 grill 这个需求：用户可以申请退款。
```

```text
用 AIFR 自我 grill 这个需求，然后给我结论：用户可以预测世界杯冠军。
```

交互式 grill 每次只问一个阻塞问题，并给出推荐答案；自我 grill 会由 AI 内部连续追问和回答，最后列出已确定决策、假设、开放问题和延期项。

## 需求转 Spec

适合把产品需求、业务规则、会议纪要、issue 或功能说明整理成 AIFR YAML Spec。

可以这样说：

```text
把下面这段需求转成 AIFR spec：...
```

最好提供：

- 需求目标和业务价值
- 明确的包含范围和排除范围
- 业务规则、计算公式或限制
- 关键场景和验收标准
- 涉及的接口、数据、代码入口或测试目标

输出通常包括需求身份、版本、范围、参与者、术语、前置条件、规则、场景、验收标准、接口影响、追踪目标、风险和开放问题。

## 版本更新

适合已有 AIFR Spec 后，要根据新变更判断语义版本并生成更新说明。

可以这样说：

```text
基于这个变更更新 REQ-PAY-0012，并判断应该升 patch、minor 还是 major：...
```

Codex 会区分文字澄清和真正的业务语义变化，输出更新后的 spec、`version_update`、`change_set`、`impact_analysis`，并在需要时创建 `changes/v<version>.aifr-update.yaml`。

## 质量检查

适合在评审、实现或合并前检查 AIFR Spec 是否完整。

可以这样说：

```text
检查这个 AIFR spec 是否 review-ready：aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

检查会覆盖必填字段、命名、规则可追溯性、Given/When/Then 场景、验收标准、接口影响、风险、非功能要求、版本字段和代码追踪信息。结果会优先列阻塞问题，再列警告和建议。

本地 smoke check：

```bash
python3 scripts/validate_aifr_spec.py .
python3 scripts/validate_aifr_spec.py . --strict
python3 scripts/validate_aifr_spec.py . --spec path/to/spec.yaml
python3 scripts/validate_aifr_spec.py . --spec path/to/spec.yaml --strict
```

默认命令检查仓库结构和轻量 YAML 质量。`--spec` 检查单个需求文件；`--strict` 增加 id、路径、index 和 update ledger 等跨文件一致性检查。validator 不是完整人工评审，仍要结合 `references/quality-checklist.md`。

## 实现审计

适合在实现中或实现后确认 AIFR 和代码是否对齐。

可以这样说：

```text
审计 REQ-ORG-0004 的实现覆盖，区分 planned tests 和 implemented tests。
```

Codex 会读取需求、根据 `trace.expected_code` 查找主要服务或仓储，再检查测试是否真的存在并覆盖对应规则。审计结果可以更新 `implementation.status`、逐条规则覆盖、`trace.expected_tests.implemented`，并列出仍缺失的计划测试。

状态含义：

- `not_started`：没有找到匹配实现。
- `partial`：已有部分代码或测试，但覆盖不完整。
- `implemented`：代码看起来完整，但尚未通过验证证明。
- `verified`：代码和测试覆盖需求，且相关验证命令已通过。

## 定位需求文件

适合只知道需求 ID、标题、关键词、baseline 或 canonical path，需要找到权威 spec 文件时使用。

可以这样说：

```text
找到 REQ-PAY-0012 的 AIFR spec。
```

```text
查一下 refund amount calculation 对应的需求文件。
```

Codex 会优先读取 `aifr/manifest.aifr.yaml` 和 `aifr/indexes/`，再打开候选 `spec.aifr.yaml` 确认 `aifr_spec.id`。如果发现多个匹配或身份冲突，会报告歧义而不是猜一个。

## 代码入口注释

适合实现已经存在，想让代码入口能追溯到需求 ID 时使用。

可以这样说：

```text
给退款金额计算入口补 AIFR 追踪注释，需求是 REQ-PAY-0012。
```

注释应该放在稳定入口，例如 Controller、Handler、Service 方法、命令、Job、策略或工作流编排函数。注释只写需求 ID 或规则 ID，例如 `REQ-PAY-0012`、`REQ-PAY-0012/RULE-001`，不要把整段需求复制进代码。

## Source Snapshot

适合需求或实现依赖外部事实时使用，例如赛程、赛果、价格、政策、公开注册表或网页数据。

可以这样说：

```text
这个需求依赖 2026 世界杯赛程，请建立 AIFR source snapshot。
```

输出应包含来源、抓取或整理方式、稳定记录键、时区处理、规范化结果和可复现的更新方式。无法确认的映射应该作为阻塞缺口列出。

## 版本比较

适合比较两个 spec 或两个版本之间到底改变了什么。

可以这样说：

```text
比较这两个 AIFR spec 的语义变化，并告诉我实现和测试影响。
```

Codex 会分开列出未变、仅文字变化、新增、修改、删除和不确定的语义项，并给出版本建议、影响分析和迁移提示。

## Baseline

适合描述某个产品版本、发布、里程碑或快照包含哪些需求版本。

可以这样说：

```text
为 v1.4 release 生成一个 AIFR baseline，包含这些需求：...
```

Baseline 中每个条目都应该有需求 ID 和明确版本；不知道版本时使用 `unknown`，不要把 baseline 当数据库或注册中心。

## 推荐工作流

新需求：

```text
自我 grill -> 需求转 Spec -> 质量检查 -> 实现 -> 实现审计 -> 代码入口注释
```

已有需求变更：

```text
读取旧 spec -> 描述变更 -> 版本更新 -> strict validation -> 质量检查
```

依赖外部事实的需求：

```text
Source Snapshot -> 需求转 Spec 或版本更新 -> 实现读取 snapshot -> 质量检查
```
