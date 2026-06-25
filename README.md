# aifr-spec

AIFR Spec（AI-Friendly Requirements Specification）是一个用于需求结构化、版本解释、稳定命名与质量检查的 Codex skill。

它的第一个版本聚焦这些能力：

- 和用户讨论并补全模糊需求，把需求 grill 到可评审、可实现、可测试。
- 将自然语言需求描述转换为 AIFR YAML Spec。
- 检查 AIFR Spec 的结构完整性、规则可追溯性、场景质量和评审就绪度。
- 为单条需求维护语义版本、变更集和影响分析。
- 用稳定路径、manifest、index 和 canonical path 让 AI 与人类可靠找到需求文件。
- 给代码入口补充需求 ID 注释，让实现入口与 AIFR 需求可追溯对齐。
- 审计需求实现状态，区分计划测试、已实现测试和已验证覆盖。

## 如何使用

README 只保留能力概览和核心约定。每种能力应该如何向 Codex 提出、需要提供什么输入、会得到什么输出，见 [docs/usage.md](docs/usage.md)。

最短用法示例：

```text
用 AIFR 帮我把下面这段需求转成 spec：...
```

```text
对这个 AIFR spec 做质量检查：aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

## 需求 grill

当用户说“帮我完成某个需求”但需求还不够清楚时，该 skill 会优先围绕需求层面讨论：

- 业务目标和用户结果
- 明确包含与排除的范围
- 业务规则、边界场景和失败场景
- 可测试的验收标准
- 必要的接口、数据、风险和非功能约束
- 必须现在决定的技术或运营限制

讨论目标不是无限追问，而是把需求边界 grill 清楚：哪些必须做、哪些明确不做、哪些还是开放问题、哪些可以延期。

grill 有两种模式：

- 交互式 grill：每次只问用户一个阻塞问题，给出推荐答案，等待用户确认后再继续。
- 自我 grill：AI 自我拷问需求边界，内部提出最多 50 轮问题并基于已有事实回答，记录假设、缺口和延期项。

当用户只说“用 grill”但没有说明是哪一种时，必须先解释自我 grill，并询问用户选择交互式 grill 还是自我 grill。用户明确说“自我 grill”时，不再反问，直接执行自我 grill。

## 需求转 Spec

当输入是一段产品需求、业务规则、会议纪要、issue 描述或功能说明时，该 skill 会提取并组织：

- 需求意图与业务价值
- 范围边界
- 参与者和外部系统
- 领域术语
- 前置条件
- 业务规则和计算公式
- Given/When/Then 场景
- 验收标准
- 接口影响
- 代码和测试追踪目标
- 机器可更新的实现状态与逐规则覆盖
- 风险与非功能要求

输出目标是可评审、可实现、可测试的 AIFR YAML Spec。

## 实现审计

当已有代码或测试需要和 AIFR 对齐时，该 skill 会把 `trace.expected_code` 和 `trace.expected_tests.planned` 当作查找线索，而不是覆盖证明。审计后可以更新：

- `implementation.status`：`not_started`、`partial`、`implemented` 或 `verified`
- `implementation.rule_coverage` / `implementation.acceptance_coverage`
- `trace.expected_tests.implemented`
- 复用接口的 `reuse_existing_endpoint` 和 `authorization_source`
- 跨需求影响的 `trace.related_requirements` 或反向索引提示

只有相关验证命令通过后，才能把需求标记为 `verified`。

## 稳定命名协议

AIFR 的路径和文件名是长期协议，应该像 API 一样稳定。需求身份由稳定 `id` 决定，路径只负责定位，slug 只负责可读性。

推荐 canonical requirement path：

```text
aifr/requirements/items/<domain-path>/<requirement-id>--<frozen-slug>/spec.aifr.yaml
```

示例：

```text
aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

核心规则：

- 当前权威需求文件固定为 `spec.aifr.yaml`。
- 版本写在 `aifr_spec.version` 和可选 `versions/` 快照中，不进入主路径。
- 状态写在 `aifr_spec.status` 中，不通过移动目录表达。
- 标题、状态、负责人、团队或业务域理解变化，不自动改 ID、移动文件或重命名目录。
- 废弃和被替代的需求不删除、不移动，使用 `status: deprecated` 或 `status: superseded` 表达。
- Codex 和其他 AI 应优先读取 `aifr/manifest.aifr.yaml`、`aifr/indexes/`、`aifr_spec.id` 和 `identity.canonical_path`，不要靠模糊路径猜测。

完整命名标准见 `references/naming.md`。

## 质量检查

当输入是已有 AIFR Spec 时，该 skill 会检查：

- 必填字段是否完整
- 标识符格式是否一致
- 验收标准是否引用了存在的规则
- 场景是否包含清晰的 Given/When/Then
- 高风险需求是否包含审计、安全、合规或明确评审控制
- 接口、测试和代码追踪信息是否足够指导实现
- canonical path、identity、slug、baseline 和 index 是否符合命名标准

检查结果会优先指出阻塞问题，再给出警告和建议修复方式。

## 代码入口注释

当输入是代码入口、实现目标或 `trace.expected_code` 映射时，该 skill 会帮助在稳定入口补充 AIFR 需求 ID 注释，例如服务方法、Controller/Handler、命令、Job、策略或工作流编排函数。

注释应只标识需求契约，例如 `REQ-PAY-0012` 或更细粒度的 `REQ-PAY-0012/RULE-001`，不要把整段需求复制进代码。若找不到唯一需求 ID 或入口位置，应先报告缺口，而不是猜测。

## Smoke Check

```bash
python3 scripts/validate_aifr_spec.py .
python3 scripts/validate_aifr_spec.py . --spec path/to/spec.yaml
python3 scripts/validate_aifr_spec.py . --spec path/to/spec.yaml --strict
python3 scripts/validate_aifr_spec.py . --strict
```

默认命令只做仓库结构和轻量 YAML 质量 smoke check。`--spec` 会检查单个需求文件的轻量 schema 规则；`--strict` 会检查跨文件一致性，例如 id、路径、index 和 update ledger。评审就绪仍需按 `references/quality-checklist.md`、`references/schema.md`、`references/naming.md`、`references/output-format.md` 和 `references/traceability.md` 人工检查。
