# AIFR Output Format

Use this reference when generating new requirements, updating existing requirements, comparing versions, or describing baselines.

Follow `references/naming.md` for canonical paths, frozen slugs, version snapshots, baselines, manifests, and indexes.

## New Requirement

When there is no old requirement input, generate an initial requirement version. Do not invent historical versions.

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

  lifecycle:
    created_at: null
    updated_at: null
    owner: null
    reviewers: []

  versioning:
    change_type: initial
    previous_version: null
    supersedes: []
    superseded_by: null
    breaking_change: false
    change_summary: 初始版本

  revision_history:
    - version: "1.0.0"
      change_type: initial
      summary: 初始版本
```

## Requirement Update

When updating an existing requirement, output the updated requirement and a separate semantic change report. Do not simply overwrite the old requirement.

```yaml
version_update:
  requirement_id: REQ-PAY-0012
  from_version: "1.1.0"
  to_version: "1.2.0"
  recommended_bump: minor
  breaking_change: false
  reason: 新增边界场景和验收标准，不改变已有行为

change_set:
  added_rules:
    - RULE-004
  modified_rules: []
  removed_rules: []

  added_scenarios:
    - SCN-005
  modified_scenarios: []
  removed_scenarios: []

  added_acceptance_criteria:
    - AC-006
  modified_acceptance_criteria: []
  removed_acceptance_criteria: []

  textual_changes:
    clarified_rules:
      - RULE-002
    clarified_scenarios: []
    clarified_acceptance_criteria:
      - AC-002
    terminology_changes:
      - 将优惠券退款表述澄清为不可现金退还

  semantic_summary:
    - 新增部分退款时优惠券分摊规则
    - 原有退款金额上限规则未改变

impact_analysis:
  requirement_impact:
    related_requirements:
      - REQ-PAY-0018

  code_impact:
    level: medium
    reason: 修改了退款金额计算规则
    code_search_hints:
      - RefundService
      - calculateRefundAmount
      - CouponRefundPolicy

  test_impact:
    level: high
    reason: 新增优惠券部分退款规则，需要新增边界测试
    recommended_tests:
      - shouldCalculatePartialRefundWithCoupon
      - shouldNotRefundCouponBeyondPaidAmount

  review_impact:
    recommended_reviewers:
      - backend
      - qa
      - finance
```

## Unknown Old Version

If the old requirement or old version number is missing, make uncertainty explicit.

```yaml
version_update:
  requirement_id: REQ-PAY-0012
  from_version: unknown
  to_version: "1.0.0"
  recommended_bump: needs_review
  breaking_change: false
  reason: 缺少旧版本输入，无法判断语义升级类型；只能生成初始版本或候选版本
```

## Bump Decision Rules

- `patch`: Wording, terminology, formatting, or explanatory changes only.
- `minor`: New rules, scenarios, acceptance criteria, or boundary conditions that preserve existing behavior.
- `major`: Modified or removed business behavior, formulas, acceptance criteria, or behavior that forces existing implementation or tests to change.
- `needs_review`: The old version, change intent, or semantic effect is not clear enough to choose a bump.

Always separate wording changes, structural changes, business semantic changes, test impact changes, and code impact changes when explaining an update.

`change_set.modified_rules`, `change_set.modified_scenarios`, and `change_set.modified_acceptance_criteria` are for business semantic changes only. Wording, terminology, formatting, or explanation-only changes must go under `change_set.textual_changes`.

## Baseline

Use a baseline to express a release, product version, or requirements snapshot.

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

Baselines are snapshots. V1 does not implement Git integration, database storage, Jira sync, CodeGraph sync, coverage sync, or baseline validation.

Baseline semantic references are `id@version`. Paths are location hints only.

## Canonical Path Output

When creating a requirement file, report the canonical path:

```yaml
canonical_output:
  requirement_id: REQ-PAY-0012
  path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
  current_file: spec.aifr.yaml
  version_snapshot:
    recommended: false
    path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/versions/v1.0.0.aifr.yaml
    reason: 普通项目可以先依赖 Git history；合规或 baseline 锁定版本时建议写入 versions/
```

`version_update`, `change_set`, and `impact_analysis` are update or comparison reports. They do not replace the authoritative `spec.aifr.yaml`.
