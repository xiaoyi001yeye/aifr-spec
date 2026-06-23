# AIFR Schema 中文版

AIFR 规范是 YAML 文档，用于描述一条需求。它需要包含足够的业务上下文、确定性规则、可执行场景、验收标准、接口、可追溯关系、风险、非功能要求和语义版本元数据，方便实现和评审。

> 本文档是 `references/schema.md` 的中文镜像。未来更新 schema 时，必须同时更新英文版和中文版。

## V1 使用场景

- 在起草或实现前，将模糊需求请求 grill 为明确范围、边界、规则、验收标准和开放问题。
- 将自然语言需求描述转换为结构化的 AIFR YAML 规范。
- 检查已有 AIFR YAML 规范的结构质量、可追溯性和评审就绪度。
- 生成、比较和解释需求语义版本变更。
- 将某个发布或产品版本描述为一组需求版本的快照。
- 通过稳定 id、manifest、index 和 canonical path 查找需求。
- 给稳定代码入口补充 AIFR 需求 id 注释，支持实现可追溯。

## 顶层字段

单条需求使用 `aifr_spec` 对象包裹。下面只展示 wrapper 和 identity 字段；完整输出示例见 `references/output-format.md`。

```yaml
aifr_spec:
  schema_version: "1.0.0"
  id: REQ-PAY-0012
  version: "1.0.0"
  title: 退款金额计算规则
  type: functional
  status: draft
  priority: high

  identity:
    primary_domain: PAY
    domain_path: pay
    frozen_slug: refund-amount-calculation
    canonical_path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
    naming_standard_version: "1.0.0"
```

必填字段：

- `schema_version`：AIFR Spec 格式本身的版本，例如 `1.0.0`。
- `id`：稳定的需求标识符。使用大写领域前缀和固定位宽序号，例如 `REQ-PAY-0012`。
- `version`：单条需求的语义版本，例如 `1.2.0`。
- `title`：人类可读的需求标题。
- `type`：需求类别。常用值：`functional`、`non_functional`、`constraint`、`interface`、`data`。
- `status`：评审状态。常用值：`draft`、`review`、`approved`、`deprecated`、`superseded`。
- `priority`：交付或业务优先级。常用值：`low`、`medium`、`high`、`critical`。
- `identity`：稳定命名和 canonical path 身份元数据。
- `lifecycle`：负责人、评审人和更新时间等生命周期元数据。
- `versioning`：当前版本的变更元数据。
- `revision_history`：需求语义版本历史。
- `intent`：需求意图对象。
- `scope`：包含范围和排除范围。
- `actors`：主要参与者和次要参与者。
- `domain_terms`：需求使用的领域词汇。
- `preconditions`：需求适用前必须满足的前置条件。
- `rules`：确定性的业务规则。
- `scenarios`：Given/When/Then 形式的行为示例。
- `acceptance_criteria`：可评审的验收标准，需关联规则或场景。
- `interfaces`：受需求影响的 API、事件、任务或其他系统边界。
- `trace`：预期实现位置和测试目标。
- `risk`：风险等级和原因。
- `non_functional`：性能、可审计性、可靠性、安全性或合规性约束。

## 字段细节

### schema_version

使用 `schema_version` 表示 AIFR Spec 格式版本，不表示产品版本或需求版本。V1 文档应使用：

```yaml
schema_version: "1.0.0"
```

### version

使用 `version` 表示单条需求的语义版本。完整需求引用由 id 和 version 组成：

```text
REQ-PAY-0012@1.2.0
```

版本号升级判定规则和更新报告字段以 `references/output-format.md` 为准。

### identity

使用 `identity` 将需求 id 和稳定 canonical path 连接起来。路径数据是定位元数据；`aifr_spec.id` 仍然是需求身份的最终依据。

- `primary_domain`：来自需求 id 的大写领域代码，例如 `PAY`。
- `domain_path`：小写路径代码，例如 `pay`。
- `frozen_slug`：需求目录中的稳定 kebab-case slug。
- `canonical_path`：当前权威 `spec.aifr.yaml` 的预期 canonical path。
- `naming_standard_version`：AIFR 命名标准版本，例如 `1.0.0`。
- `related_domains`：可选。当需求影响其他领域时记录相关大写领域代码。

规则：

- `canonical_path` 应与实际路径一致。
- `domain_path` 应与 `aifr/requirements/items/` 下的领域目录一致。
- `frozen_slug` 应与 `<requirement-id>--<frozen-slug>` 目录中的 slug 一致。
- `primary_domain` 应与 `REQ-<DOMAIN>-<NUMBER>` 中的 `DOMAIN` 一致，除非明确记录迁移原因。
- 文件路径和 `aifr_spec.id` 冲突时，以 `aifr_spec.id` 为准，但必须输出高严重度 warning。

### lifecycle

使用 `lifecycle` 记录负责人和评审元数据：

- `created_at`：创建时间；未知时为 `null`。
- `updated_at`：最近一次语义更新时间；未知时为 `null`。
- `owner`：负责人、角色、团队；未知时为 `null`。
- `reviewers`：评审角色或人员。

### versioning

使用 `versioning` 描述当前版本和其它需求版本的关系：

- `change_type`：`initial`、`patch`、`minor`、`major`、`deprecated` 或 `needs_review`。
- `previous_version`：上一个需求版本；没有时为 `null`。
- `supersedes`：当前版本替代的需求版本引用。
- `superseded_by`：替代当前版本的需求版本引用；没有时为 `null`。
- `breaking_change`：已有实现、测试或业务行为必须改变时为 `true`。
- `change_summary`：简洁的语义变更摘要。

### revision_history

使用 `revision_history` 总结需求语义版本，而不是 Git commit。每个条目应包含：

- `version`
- `change_type`
- `summary`

### intent

使用 `intent` 说明需求为什么存在。

- `user_goal`：面向用户的结果。
- `business_value`：业务原因或运营价值。

### scope

使用 `scope` 防止需求范围蔓延。

- `in`：明确包含的场景。
- `out`：明确排除的场景。

### actors

使用 `actors` 命名参与该行为的系统或角色。

- `primary`：触发或接收该行为的主要参与者。
- `secondary`：支撑系统、服务或角色。

### domain_terms

使用映射结构记录术语及其定义。术语应与规则、公式、场景和验收标准中使用的名称保持一致。

### rules

每条规则必须包含：

- `id`：稳定的规则标识符，例如 `RULE-001`。
- `description`：业务可读的规则说明。

每条规则应至少包含一个确定性表达：

- `invariant`：必须始终成立的条件。
- `formula`：计算或推导规则。

### scenarios

每个场景必须包含：

- `id`：稳定的场景标识符，例如 `SCN-001`。
- `name`：场景名称。
- `given`：初始事实或状态。
- `when`：触发动作。
- `then`：预期结果。

当计算、状态流转、权限或集成行为很重要时，场景中应使用具体数值。

### acceptance_criteria

每条验收标准必须包含：

- `id`：稳定的验收标准标识符，例如 `AC-001`。
- `text`：可测试的验收描述。
- `verifies`：一个或多个被验证的 `rules.id`。

### interfaces

使用 `interfaces` 描述受影响的集成点。对于 API，应包含：

- `method`
- `path`
- `request_schema`
- `response_schema`

### trace

使用 `trace` 指导实现和测试。

- `expected_code`：预期的服务、模块、方法、处理器或命令目标。
- `expected_tests`：预期的自动化测试类、文件或套件。

代码入口注释是实现可追溯辅助信息。它应使用 `aifr_spec.id` 中已有的需求 id，并放在 `trace.expected_code` 标识的稳定入口处；V1 不把它建模为单独 schema 字段。

### risk

使用 `risk` 标记实现和评审的敏感度。

- `level`：`low`、`medium`、`high` 或 `critical`。
- `reasons`：风险等级的具体原因。

### non_functional

使用 `non_functional` 描述以下约束：

- `performance`
- `auditability`
- `security`
- `reliability`
- `compliance`

## 质量规则

人工质量评审使用这些规则。`scripts/validate_aifr_spec.py` 只覆盖 smoke-check 子集，不能当作完整 schema 校验。

- `aifr_spec.schema_version` 必须存在。
- `aifr_spec.id` 必须稳定并符合需求标识符格式。
- `aifr_spec.version` 必须存在并符合语义版本格式。
- canonical `spec.aifr.yaml` 文件中应包含 `aifr_spec.identity`。
- `aifr_spec.identity.canonical_path` 应与实际路径一致。
- `aifr_spec.versioning.change_type` 必须存在。
- `aifr_spec.revision_history` 至少包含一条记录。
- 必填顶层字段必须存在。
- 标识符应符合预期前缀：`REQ-`、`RULE-`、`SCN-` 和 `AC-`。
- `acceptance_criteria[].verifies` 的值必须引用已存在的 `rules[].id`。
- 场景必须包含非空的 `given`、`when` 和 `then` 列表。
- 公式或不变量中引用的领域术语必须在 `domain_terms` 中定义。
- 高风险或关键风险需求必须至少包含 `non_functional.auditability`、`security`、`compliance` 或明确的评审说明。

## Baseline 文档

baseline 用于表达某个产品版本、发布版本或需求快照中包含的一组需求版本。它不是数据库，也不替代 Git 文件历史。

baseline id 格式：

```text
BL-<SCOPE>-<PERIOD_OR_RELEASE>
```

```yaml
baseline:
  id: BL-PAY-2026-Q3
  product_version: "payment-service-v3.4"
  status: approved
  created_at: "2026-06-22"
  requirements:
    - id: REQ-PAY-0012
      version: "1.2.0"
      path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
    - id: REQ-PAY-0018
      version: "1.0.0"
      path: aifr/requirements/items/pay/REQ-PAY-0018--coupon-refund-policy/spec.aifr.yaml
```

baseline 规则：

- `baseline.id` 应使用 `BL-<SCOPE>-<PERIOD_OR_RELEASE>`。
- `requirements` 必须包含 id 和 version；`id@version` 是语义引用。
- `path` 只是定位辅助。
- baseline 不应只引用 path 而不引用 version。
- 未知需求版本必须明确标记，不能猜测。
- baseline 只描述快照；V1 不实现 baseline 存储、Git 集成或外部追踪系统同步。
- 强审计场景中，被 baseline 引用的版本必须存在于 `versions/`。

## 仓库 Manifest 和 Indexes

仓库入口文件是 `aifr/manifest.aifr.yaml`：

```yaml
aifr_repository:
  naming_standard_version: "1.0.0"
  schema_version: "1.0.0"

  canonical_requirement_glob: "aifr/requirements/items/*/*/spec.aifr.yaml"
  baseline_glob: "aifr/baselines/**/*.aifr-baseline.yaml"

  requirement_id_format: "REQ-<DOMAIN>-<NUMBER4>"
  canonical_requirement_path_format: "aifr/requirements/items/<domain-path>/<requirement-id>--<frozen-slug>/spec.aifr.yaml"

  default_current_file: "spec.aifr.yaml"
  version_snapshot_dir: "versions"
```

indexes 是 `aifr/indexes/` 下的生成型查找辅助文件，不是权威来源。index 中的信息必须能从 `spec.aifr.yaml` 还原。

```yaml
requirements:
  - id: REQ-PAY-0012
    title: 退款金额计算规则
    domain: PAY
    version: "1.2.0"
    status: approved
    path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

详细命名和查找规则见 `references/naming.md`。
