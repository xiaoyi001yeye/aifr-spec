# AIFR Traceability

Document how AIFR specs connect requirements, source materials, decisions, implementation, and tests.

## Trace Links

AIFR uses explicit identifiers to keep requirement intent, business rules, examples, acceptance criteria, implementation, and tests connected.

- Requirement ids use `REQ-<DOMAIN>-<NUMBER>`, for example `REQ-PAY-0012`.
- Rule ids use `RULE-<NUMBER>`, for example `RULE-001`.
- Scenario ids use `SCN-<NUMBER>`, for example `SCN-001`.
- Acceptance criterion ids use `AC-<NUMBER>`, for example `AC-001`.

Requirement file lookup should use `aifr/manifest.aifr.yaml`, indexes, `aifr_spec.id`, and `identity.canonical_path`. Paths help locate files; ids define requirement identity.

Acceptance criteria must list the rules they verify:

```yaml
acceptance_criteria:
  - id: AC-001
    text: 系统必须保证退款金额不超过用户实际支付金额
    verifies:
      - RULE-001
```

## Source Mapping

When a requirement comes from an external source, add source references in the requirement body or in a future `sources` section. Prefer stable references such as:

- Product requirement document ids
- Issue ids
- Design decision records
- Compliance policy ids
- Meeting note links

Keep source references close to the requirement or rule they justify.

## Test Mapping

Use `trace.expected_tests.planned` to name expected automated tests, and `trace.expected_tests.implemented` to name tests found in the repository:

```yaml
trace:
  expected_tests:
    planned:
      - RefundServiceTest
      - RefundControllerTest
    implemented:
      - tests/payment/RefundServiceTest.java
```

Test mapping expectations:

- Calculation rules should have unit tests.
- API behavior should have controller, handler, or integration tests.
- Risky financial or audit behavior should include boundary and regression tests.
- Each `acceptance_criteria[].verifies` target should be covered by at least one expected test.
- Planned tests are recommendations or gaps; implemented tests must correspond to files, classes, or cases that actually exist.
- Do not move a test from `planned` to `implemented` until repository inspection confirms it exists.

## Implementation Audit Mapping

Use `implementation` to record current implementation state, and keep it distinct from requirement review `status`.

```yaml
implementation:
  status: partial
  updated_at: "2026-06-26"
  notes: []
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
```

Implementation audit rules:

- `not_started` means no matching implementation was found.
- `partial` means at least one code target or test exists, but rule or acceptance coverage is incomplete.
- `implemented` means code coverage appears complete, but verification has not proved it yet.
- `verified` means relevant verification commands passed after code and tests were inspected.
- Per-rule and per-acceptance coverage may be updated by automation; do not use prose-only notes as the sole coverage record.
- If a requirement has no implementation yet, leave `trace.expected_tests.implemented` empty and keep missing tests under `planned`.

## Code Mapping

Use `trace.expected_code` to name likely implementation targets:

```yaml
trace:
  expected_code:
    - service: RefundService
    - method_hint: calculateRefundAmount
```

Code mapping should be specific enough for an implementer to find the change area without forcing an exact file path too early.

When an interface reuses an existing endpoint, trace the second authorization check explicitly:

```yaml
interfaces:
  apis:
    - method: GET
      path: /vocabularies/{id}
      reuse_existing_endpoint: true
      authorization_source: VocabularyAccessService.assertReadable
```

Reuse expectations:

- `reuse_existing_endpoint: true` means the requirement relies on an existing API rather than adding a new one.
- `authorization_source` names the existing service, policy, guard, or API that rechecks access at request time.
- Resource-entry requirements should not rely only on the containing feed, message, or page authorization when the target resource has its own access rule.

## Reverse Indexes

Use reverse indexes to find cross-requirement effects for shared business terms and boundary states.

```yaml
reverse_index:
  terms:
    - term: 离班学生
      affects:
        - requirement_id: REQ-CLASS-0003
          fields:
            - rules
        - requirement_id: REQ-PLAN-0002
          fields:
            - scenarios
```

Reverse index expectations:

- Generate reverse indexes from current specs when possible; do not treat them as authoritative truth.
- Terms should come from `domain_terms`, rules, preconditions, scenarios, acceptance criteria, and trace related requirements.
- Use reverse indexes during implementation audits to list adjacent requirements that might be affected by the same boundary.

## Code Entrypoint Annotation

Trace comments align implementation entrypoints with AIFR requirement ids. When aligning implementation with AIFR requirements, add concise comments at stable code entrypoints named or implied by `trace.expected_code`.

Good annotation targets include:

- Public service methods that enforce a requirement.
- Controllers, handlers, or routes that expose the behavior.
- Commands, jobs, policies, workflow orchestration functions, or adapters that own the requirement boundary.

Avoid annotating every private helper, data mapper, or incidental utility. Use the local language's normal documentation or line-comment style and include the stable requirement id:

```java
// AIFR: REQ-PAY-0012/RULE-001
public Money calculateRefundAmount(RefundRequest request) {
  ...
}
```

```typescript
/**
 * AIFR: REQ-PAY-0012
 */
export async function refundHandler(request: Request) {
  ...
}
```

Annotation rules:

- The requirement id in code must match an existing `aifr_spec.id`.
- Use `REQ-.../RULE-...` only when the entrypoint specifically enforces that rule.
- Keep the comment short; do not paste requirement prose into code.
- If several requirements share an entrypoint, list the ids in one comment.
- If the correct requirement id or entrypoint is ambiguous, report the ambiguity instead of guessing.

Completion checks:

- Every requested requirement id is resolved to one `aifr_spec.id` or reported as unresolved.
- Every modified entrypoint has one trace comment covering the relevant requirement ids.
- Comments are not duplicated across low-level helpers when one stable entrypoint owns the behavior.
- The final report names the requirement id, code entrypoint, and any mapping gap.

## Requirement Path Mapping

Use `identity.canonical_path` to make the current authoritative file discoverable:

```yaml
identity:
  primary_domain: PAY
  domain_path: pay
  frozen_slug: refund-amount-calculation
  canonical_path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
  naming_standard_version: "1.0.0"
```

Do not treat path as identity. If path and `aifr_spec.id` disagree, report the mismatch and trust `aifr_spec.id`.

## Risk Mapping

For `risk.level: high` or `risk.level: critical`, include traceability to auditability, security, compliance, or explicit review expectations. Financial calculation requirements should usually include:

- Rule version logging
- Input parameter logging
- Boundary test coverage
- Finance or reconciliation system touchpoints
