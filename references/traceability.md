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

Use `trace.expected_tests` to name expected automated tests:

```yaml
trace:
  expected_tests:
    - RefundServiceTest
    - RefundControllerTest
```

Test mapping expectations:

- Calculation rules should have unit tests.
- API behavior should have controller, handler, or integration tests.
- Risky financial or audit behavior should include boundary and regression tests.
- Each `acceptance_criteria[].verifies` target should be covered by at least one expected test.

## Code Mapping

Use `trace.expected_code` to name likely implementation targets:

```yaml
trace:
  expected_code:
    - service: RefundService
    - method_hint: calculateRefundAmount
```

Code mapping should be specific enough for an implementer to find the change area without forcing an exact file path too early.

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
