# AIFR Examples

Keep representative AIFR specification examples here. Examples should stay synchronized with `references/schema.md`, `references/naming.md`, and `references/output-format.md`.

## Recommended Repository Layout

```text
aifr/
  manifest.aifr.yaml
  registries/
    domains.aifr.yaml
  requirements/
    items/
      pay/
        REQ-PAY-0012--refund-amount-calculation/
          spec.aifr.yaml
          changelog.md
          versions/
            v1.0.0.aifr.yaml
            v1.1.0.aifr.yaml
          plans/
            test-plan.md
            implementation-plan.md
            review-checklist.md
          evidence/
            notes.md
      order/
        REQ-ORDER-0007--auto-cancel-unpaid-order/
          spec.aifr.yaml
          changelog.md
  baselines/
    pay/
      BL-PAY-2026-Q3.aifr-baseline.yaml
  indexes/
    requirements.aifr-index.yaml
    domains.aifr-index.yaml
    baselines.aifr-index.yaml
```

Canonical requirement path:

```text
aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

## Minimal Example

```yaml
aifr_spec:
  schema_version: "1.0.0"
  id: REQ-PAY-0001
  version: "1.0.0"
  title: 订单支付成功后更新支付状态
  type: functional
  status: draft
  priority: high

  identity:
    primary_domain: PAY
    domain_path: pay
    frozen_slug: update-paid-status
    canonical_path: aifr/requirements/items/pay/REQ-PAY-0001--update-paid-status/spec.aifr.yaml
    naming_standard_version: "1.0.0"

  lifecycle:
    created_at: null
    updated_at: null
    owner: payment
    reviewers:
      - backend
      - qa

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

  intent:
    user_goal: 用户完成支付后，可以看到订单已支付
    business_value: 保证交易状态准确，避免重复支付

  scope:
    in:
      - 普通订单支付
    out:
      - 跨境支付

  actors:
    primary:
      - buyer
    secondary:
      - payment_gateway

  domain_terms:
    paid_status: 订单已完成支付后的状态

  preconditions:
    - 订单状态为 pending_payment

  rules:
    - id: RULE-001
      description: 支付网关确认成功后，订单状态必须更新为 paid
      invariant: payment_gateway_result = success implies order_status = paid

  scenarios:
    - id: SCN-001
      name: 支付成功后订单变为已支付
      given:
        - 用户有一笔待支付订单
        - payment_gateway_result = success
      when:
        - 系统接收支付成功回调
      then:
        - order_status = paid

  acceptance_criteria:
    - id: AC-001
      text: 支付成功回调处理完成后，订单状态必须为 paid
      verifies:
        - RULE-001

  interfaces:
    apis:
      - method: POST
        path: /payments/callback
        request_schema: PaymentCallbackRequest
        response_schema: PaymentCallbackResponse

  trace:
    expected_code:
      - service: PaymentCallbackService
      - method_hint: handlePaymentSuccess
    expected_tests:
      planned:
        - PaymentCallbackServiceTest
      implemented: []

  implementation:
    status: not_started
    updated_at: null
    notes: []
    rule_coverage:
      - rule_id: RULE-001
        status: not_started
        code: []
        tests:
          planned:
            - PaymentCallbackServiceTest
          implemented: []

  risk:
    level: high
    reasons:
      - 涉及交易状态一致性

  non_functional:
    auditability:
      - 必须记录支付网关流水号和订单状态变更记录
```

## Complete Example

```yaml
aifr_spec:
  schema_version: "1.0.0"
  id: REQ-PAY-0012
  version: "1.2.0"
  title: 退款金额计算规则
  type: functional
  status: approved
  priority: high

  identity:
    primary_domain: PAY
    domain_path: pay
    frozen_slug: refund-amount-calculation
    canonical_path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
    naming_standard_version: "1.0.0"
    related_domains:
      - FINANCE

  lifecycle:
    created_at: "2026-06-01"
    updated_at: "2026-06-20"
    owner: payment
    reviewers:
      - backend
      - qa
      - finance

  versioning:
    change_type: minor
    previous_version: "1.1.0"
    supersedes:
      - REQ-PAY-0012@1.1.0
    superseded_by: null
    breaking_change: false
    change_summary: 新增部分退款时优惠券分摊规则

  revision_history:
    - version: "1.0.0"
      change_type: initial
      summary: 初始退款金额计算规则
    - version: "1.1.0"
      change_type: patch
      summary: 澄清优惠券不可现金退还的术语
    - version: "1.2.0"
      change_type: minor
      summary: 新增部分退款时优惠券按比例分摊的边界规则

  aliases:
    titles:
      - 退款金额计算规则
      - 退款金额与优惠券分摊计算规则
    slugs:
      - refund-amount-calculation
      - refund-coupon-allocation

  intent:
    user_goal: 用户申请退款时，系统应正确计算可退金额
    business_value: 避免多退、少退，保证财务一致性

  scope:
    in:
      - 普通订单退款
      - 部分退款
      - 使用优惠券的订单
    out:
      - 跨境支付退款
      - 人工客服补偿

  actors:
    primary:
      - buyer
    secondary:
      - payment_gateway
      - finance_system

  domain_terms:
    refund_amount: 实际退还给用户的金额
    paid_amount: 用户实际支付金额
    coupon_discount: 平台优惠券抵扣金额
    coupon_refund_share: 部分退款时按商品实付比例分摊的优惠券金额

  preconditions:
    - 订单状态为 paid 或 completed
    - 订单未被全额退款
    - 用户具备该订单的退款权限

  rules:
    - id: RULE-001
      description: 可退金额不得超过用户实际支付金额
      invariant: refund_amount <= paid_amount

    - id: RULE-002
      description: 部分退款按商品实付金额比例计算，并扣除不可退费用
      formula: refund_amount = item_paid_amount - non_refundable_fee

    - id: RULE-003
      description: 平台优惠券金额不可退还给用户
      invariant: coupon_discount is excluded_from cash_refund

    - id: RULE-004
      description: 部分退款时优惠券按退款商品实付比例分摊，仅用于财务对账，不作为现金退还
      formula: coupon_refund_share = coupon_discount * item_paid_amount / order_paid_amount

  scenarios:
    - id: SCN-001
      name: 普通订单全额退款
      given:
        - 用户有一笔已支付订单
        - paid_amount = 100
        - coupon_discount = 0
      when:
        - 用户申请全额退款
      then:
        - refund_amount = 100

    - id: SCN-005
      name: 使用优惠券的订单部分退款
      given:
        - 用户有一笔已支付订单
        - order_paid_amount = 80
        - item_paid_amount = 40
        - coupon_discount = 20
      when:
        - 用户申请退还该商品
      then:
        - refund_amount = 40
        - coupon_refund_share = 10
        - coupon_refund_share 仅用于财务对账

  acceptance_criteria:
    - id: AC-001
      text: 系统必须保证退款金额不超过用户实际支付金额
      verifies:
        - RULE-001

    - id: AC-006
      text: 部分退款时，系统必须计算优惠券分摊金额用于财务对账，且该金额不得作为现金退还
      verifies:
        - RULE-004

  interfaces:
    apis:
      - method: POST
        path: /refunds
        request_schema: RefundRequest
        response_schema: RefundResponse
        reuse_existing_endpoint: false

  recommended_vertical_slices:
    - id: SLICE-001
      name: 退款金额上限
      covers:
        rules:
          - RULE-001
        acceptance_criteria:
          - AC-001
      suggested_tests:
        planned:
          - RefundServiceTest
          - RefundControllerTest
        implemented:
          - RefundServiceTest.shouldCapRefundAtPaidAmount

  trace:
    related_requirements:
      - REQ-PAY-0018
      - REQ-FIN-0004
    expected_code:
      - service: RefundService
      - method_hint: calculateRefundAmount
      - policy_hint: CouponRefundPolicy
    expected_tests:
      planned:
        - RefundServiceTest
        - RefundControllerTest
        - CouponRefundPolicyTest
      implemented:
        - RefundServiceTest.shouldCapRefundAtPaidAmount

  implementation:
    status: partial
    updated_at: "2026-06-26"
    notes:
      - 退款上限规则已有服务层测试；优惠券分摊和 Controller 覆盖仍需补齐。
    rule_coverage:
      - rule_id: RULE-001
        status: verified
        code:
          - RefundService.calculateRefundAmount
        tests:
          planned:
            - RefundControllerTest
          implemented:
            - RefundServiceTest.shouldCapRefundAtPaidAmount
      - rule_id: RULE-004
        status: partial
        code:
          - CouponRefundPolicy
        tests:
          planned:
            - CouponRefundPolicyTest
          implemented: []

  risk:
    level: high
    reasons:
      - 涉及资金计算
      - 涉及外部支付网关
      - 影响财务对账

  non_functional:
    performance:
      - 退款金额计算应在 100ms 内完成
    auditability:
      - 每次退款金额计算必须记录需求版本、规则版本和输入参数
```

## Version Update Example

```yaml
version_update:
  requirement_id: REQ-PAY-0012
  from_version: "1.1.0"
  to_version: "1.2.0"
  recommended_bump: minor
  breaking_change: false
  reason: 新增边界场景和验收标准，不改变已有退款金额上限或优惠券不可现金退还行为

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
    - 优惠券仍不得作为现金退还给用户

impact_analysis:
  requirement_impact:
    related_requirements:
      - REQ-PAY-0018

  code_impact:
    level: medium
    reason: 修改了退款金额计算规则，需要在优惠券订单部分退款路径中增加分摊计算
    code_search_hints:
      - RefundService
      - calculateRefundAmount
      - CouponRefundPolicy

  test_impact:
    level: high
    reason: 新增优惠券部分退款规则，需要新增边界测试和回归测试
    recommended_tests:
      - shouldCalculatePartialRefundWithCoupon
      - shouldNotRefundCouponBeyondPaidAmount

  review_impact:
    recommended_reviewers:
      - backend
      - qa
      - finance
```

## Manifest And Registry Examples

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

```yaml
domains:
  - code: PAY
    path: pay
    name: Payment
    description: 支付、退款、结算、支付网关相关需求
    id_number_width: 4

  - code: ORDER
    path: order
    name: Order
    description: 订单创建、取消、状态流转相关需求
    id_number_width: 4
```

## Baseline Example

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

## Changelog Example

```markdown
# REQ-PAY-0012 Changelog

## 1.2.0
- 新增部分退款时优惠券分摊规则。
- 新增边界场景：优惠券金额大于商品实付金额。

## 1.1.0
- 新增优惠券全额退款场景。

## 1.0.0
- 初始版本。
```

## Status, Domain, And Title Changes

Do not move a requirement when its status changes:

```yaml
status: deprecated

versioning:
  superseded_by:
    - REQ-PAY-0041@1.0.0
  change_summary: 被新的统一退款规则替代
```

Do not move or rename `REQ-PAY-0012` when it later affects order behavior:

```yaml
identity:
  primary_domain: PAY
  related_domains:
    - ORDER
    - FINANCE

trace:
  related_requirements:
    - REQ-ORDER-0007
    - REQ-FIN-0004
```

Do not rename `REQ-PAY-0012--refund-amount-calculation/` when the title changes:

```yaml
title: 退款金额与优惠券分摊计算规则
aliases:
  titles:
    - 退款金额计算规则
    - 退款金额与优惠券分摊计算规则
  slugs:
    - refund-amount-calculation
    - refund-coupon-allocation
```

## Split And Merge Examples

Requirement split:

```yaml
status: superseded

versioning:
  superseded_by:
    - REQ-PAY-0041@1.0.0
    - REQ-PAY-0042@1.0.0
  change_summary: 原退款金额计算需求拆分为金额计算和优惠券分摊两个需求
```

New directories:

```text
aifr/requirements/items/pay/REQ-PAY-0041--refund-base-amount-calculation/spec.aifr.yaml
aifr/requirements/items/pay/REQ-PAY-0042--coupon-allocation-for-refund/spec.aifr.yaml
```

Requirement merge:

```yaml
versioning:
  supersedes:
    - REQ-PAY-0012@1.2.0
    - REQ-PAY-0018@1.0.0
```

Old requirement after merge:

```yaml
status: superseded
versioning:
  superseded_by:
    - REQ-PAY-0045@1.0.0
```

## Good And Bad Paths

Recommended:

```text
aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
aifr/requirements/items/order/REQ-ORDER-0007--auto-cancel-unpaid-order/spec.aifr.yaml
aifr/baselines/pay/BL-PAY-2026-Q3.aifr-baseline.yaml
```

Not recommended:

```text
requirements/payment/refund.yaml
requirements/payment/退款金额计算规则.yaml
requirements/payment/REQ-PAY-0012.v1.2.0.approved.yaml
requirements/approved/payment/REQ-PAY-0012.yaml
requirements/team-backend/REQ-PAY-0012.yaml
requirements/payment/latest.yaml
```

Reasons:

- Missing stable id.
- Path contains Chinese.
- Version and status appear in the current path.
- Status changes cause moves.
- Team changes cause moves.
- `latest` is ambiguous.

## Invalid Examples

### Acceptance criterion references a missing rule

```yaml
aifr_spec:
  schema_version: "1.0.0"
  id: REQ-PAY-0013
  version: "1.0.0"
  title: 无效示例
  type: functional
  status: draft
  priority: high
  identity:
    primary_domain: PAY
    domain_path: pay
    frozen_slug: invalid-example
    canonical_path: aifr/requirements/items/pay/REQ-PAY-0013--invalid-example/spec.aifr.yaml
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
  rules:
    - id: RULE-001
      description: 示例规则
      invariant: refund_amount <= paid_amount
  acceptance_criteria:
    - id: AC-001
      text: 引用了不存在的规则
      verifies:
        - RULE-999
```

This should fail because `AC-001` references `RULE-999`, but only `RULE-001` is defined.
