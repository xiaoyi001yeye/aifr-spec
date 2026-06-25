# AIFR Naming Standard

AIFR paths are a long-lived protocol. Treat them like API routes: stable, predictable, and boring. Requirement identity is carried by stable ids and file content; paths are for location and should not drift when titles, versions, status, ownership, or domain understanding changes.

## Core Principles

- Stable `id` determines requirement identity.
- File paths locate requirements; they do not define identity.
- Slugs improve readability only.
- Versions live in `aifr_spec.version` and optional `versions/` snapshots, not in the current canonical path.
- Status lives in YAML, not in directory moves.
- Title changes do not automatically rename directories.
- Business domain understanding changes do not automatically move directories.
- Deprecated or superseded requirements are not deleted or moved. Use `status: deprecated` or `status: superseded`.
- The current authoritative requirement is always `spec.aifr.yaml`.
- Historical version snapshots may live in `versions/`.
- Baselines semantically reference `id@version`; paths are location hints only.
- AI should locate requirements through `manifest`, `indexes`, `id`, and `canonical_path`, not fuzzy path guesses.

## Recommended Repository Structure

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

The canonical requirement path is:

```text
aifr/requirements/items/<domain-path>/<requirement-id>--<frozen-slug>/spec.aifr.yaml
```

Example:

```text
aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

This is the recommended canonical path. Early simple projects may temporarily keep only `spec.aifr.yaml`, but should migrate toward this structure when requirements need indexing, baselines, CI checks, or multi-agent work.

## Requirement ID

Format:

```text
REQ-<DOMAIN>-<NUMBER>
```

New projects should use 4-digit numbers:

```text
REQ-PAY-0012
REQ-ORDER-0007
REQ-AUTH-0003
REQ-INV-0041
```

Rules:

- `REQ` is fixed uppercase.
- `DOMAIN` is a 2-8 character uppercase business domain code.
- `NUMBER` uses fixed-width digits. New projects should use 4 digits.
- Existing projects that already use 3 digits may continue, but one domain must not mix 3-digit and 4-digit ids.
- An id never changes because title, status, version, ownership, or domain understanding changes.
- Deprecated ids are never reused.
- Merged, split, and replaced requirements keep their original ids.

## Domain Path

The path domain uses a lowercase short code:

```text
pay
order
auth
inv
notify
user-profile
```

Rules:

- `domain-path` comes from the `DOMAIN` part of `REQ-<DOMAIN>-<NUMBER>`.
- `REQ-PAY-0012` maps to `pay`; `REQ-ORDER-0007` maps to `order`.
- Do not use team names such as `backend-team` or `growth-team`.
- Do not use long names such as `payment-and-financial-reconciliation`.
- Domain details belong in `aifr/registries/domains.aifr.yaml`.
- When domain understanding changes, update `identity.related_domains`, `ownership`, or `trace`; do not move files automatically.

Domain registry example:

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

  - code: AUTH
    path: auth
    name: Authentication
    description: 登录、注册、鉴权、安全策略相关需求
    id_number_width: 4
```

## Requirement Directory

Directory format:

```text
<requirement-id>--<frozen-slug>
```

Examples:

```text
REQ-PAY-0012--refund-amount-calculation
REQ-ORDER-0007--auto-cancel-unpaid-order
REQ-AUTH-0003--login-rate-limit
```

Rules:

- Use double hyphen `--` between id and slug.
- Do not use a single hyphen between id and slug; scripts and AI cannot split it reliably.
- The left side is the stable id; the right side is the frozen slug.
- Directories are not renamed by default after creation.
- Do not include version, status, owner, date, or team name in the directory.

## Frozen Slug

A frozen slug is the short English-readable name created with the requirement.

Rules:

- Use lowercase English letters, numbers, and hyphens.
- Do not use spaces, Chinese, underscores, versions, or status names.
- Keep it under 60 characters.
- Prefer 3-6 English words.
- Do not automatically change it when the title changes.
- If a directory truly must be renamed, keep `aifr_spec.id` unchanged and record the reason in the change explanation.

Examples:

```text
refund-amount-calculation
coupon-refund-policy
auto-cancel-unpaid-order
login-rate-limit
inventory-reservation-release
```

Chinese titles belong in YAML `title`, not in paths.

## Current Spec File

Every current authoritative requirement file is named:

```text
spec.aifr.yaml
```

Example:

```text
aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

Do not use these current spec filenames:

```text
REQ-PAY-0012.aifr.yaml
refund-amount-calculation.aifr.yaml
latest.aifr.yaml
v1.2.0.aifr.yaml
approved.aifr.yaml
```

Reason:

- There is one current authoritative file.
- Version lives in `aifr_spec.version` and `versions/`.
- Status lives in `aifr_spec.status`.
- The current path must not drift because version or status changes.

## Manifest

`aifr/manifest.aifr.yaml` is the entrypoint for AI and tools:

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

Codex and other AI should read `manifest.aifr.yaml` first, then indexes or target spec files. They should not blindly guess paths across the repository.

## Spec Identity

Each `spec.aifr.yaml` should include:

```yaml
aifr_spec:
  schema_version: "1.0.0"

  id: REQ-PAY-0012
  version: "1.2.0"
  title: 退款金额计算规则
  status: approved
  priority: high

  identity:
    primary_domain: PAY
    domain_path: pay
    frozen_slug: refund-amount-calculation
    canonical_path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
    naming_standard_version: "1.0.0"
```

Rules:

- `aifr_spec.id` is the final authority for requirement identity.
- If path and `aifr_spec.id` conflict, trust `aifr_spec.id` but report a high-severity warning.
- `identity.canonical_path` should match the actual path.
- `identity.frozen_slug` should match the slug in the directory.
- `identity.domain_path` should match the domain path directory.
- `identity.primary_domain` should match the `DOMAIN` segment in the id unless a migration reason is explicitly recorded.

## Versions Directory

`versions/` stores explicit historical snapshots:

```text
versions/
  v1.0.0.aifr.yaml
  v1.1.0.aifr.yaml
  v2.0.0.aifr.yaml
```

Rules:

- Files under `versions/` are historical snapshots.
- Historical snapshots should not be edited after creation.
- The current authoritative version remains `spec.aifr.yaml`.
- Git history remains the final file history source.
- `versions/` is audit-friendly explicit snapshot storage, not a database.
- Ordinary projects may rely only on Git history.
- Compliance projects should write every approved version to `versions/`.
- In strong-audit projects, versions referenced by baselines must exist in `versions/`.

## Changelog

`changelog.md` is a human-readable change summary. It does not replace Git history or `revision_history`.

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

## Plans And Evidence

Optional derived directories:

```text
plans/
  test-plan.md
  implementation-plan.md
  review-checklist.md

evidence/
  product-decision-2026-06-22.md
  finance-confirmation.md
  edge-case-notes.md
```

Rules:

- `plans/` is for test plans, implementation plans, and review checklists.
- `evidence/` is for meeting notes, business confirmations, design notes, and edge-case evidence.
- These files are not authoritative requirement sources.
- Authoritative rules must be folded back into `spec.aifr.yaml`.
- These files must explicitly reference `requirement_id`.

## Baselines

Baseline id format:

```text
BL-<SCOPE>-<PERIOD_OR_RELEASE>
```

Examples:

```text
BL-PAY-2026-Q3
BL-ORDER-v3.4
BL-PLATFORM-2026-06-RELEASE
```

Baseline path:

```text
aifr/baselines/<scope-path>/<baseline-id>.aifr-baseline.yaml
```

Examples:

```text
aifr/baselines/pay/BL-PAY-2026-Q3.aifr-baseline.yaml
aifr/baselines/order/BL-ORDER-v3.4.aifr-baseline.yaml
```

Baseline content:

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

Rules:

- Baseline semantic references are `id@version`.
- Path is only a location hint.
- A baseline must not reference only `path` without `version`.
- In strong-audit scenarios, referenced versions must exist in `versions/`.

## Indexes

Indexes are generated files, not authoritative sources:

```text
aifr/indexes/
  requirements.aifr-index.yaml
  domains.aifr-index.yaml
  baselines.aifr-index.yaml
  reverse-terms.aifr-index.yaml
```

Example:

```yaml
requirements:
  - id: REQ-PAY-0012
    title: 退款金额计算规则
    domain: PAY
    version: "1.2.0"
    status: approved
    path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml

  - id: REQ-ORDER-0007
    title: 订单自动取消
    domain: ORDER
    version: "2.1.0"
    status: approved
    path: aifr/requirements/items/order/REQ-ORDER-0007--auto-cancel-unpaid-order/spec.aifr.yaml
```

Reverse index example:

```yaml
reverse_index:
  terms:
    - term: 离班学生
      affects:
        - requirement_id: REQ-CLASS-0003
          path: aifr/requirements/items/class/REQ-CLASS-0003--class-membership/spec.aifr.yaml
          fields:
            - rules
        - requirement_id: REQ-PLAN-0002
          path: aifr/requirements/items/plan/REQ-PLAN-0002--student-learning-plan/spec.aifr.yaml
          fields:
            - preconditions
            - scenarios
```

Rules:

- Indexes may be regenerated.
- Indexes are not authoritative requirement sources.
- Index information must be reconstructable from `spec.aifr.yaml`.
- AI may read indexes first to find candidates, then open `spec.aifr.yaml`.
- Reverse indexes help audit cross-requirement boundary terms; they must be regenerated from specs or treated as hints until confirmed against `spec.aifr.yaml`.

## Status Changes

Status changes do not move files. Status lives in YAML:

```yaml
status: draft
```

```yaml
status: approved
```

```yaml
status: deprecated
```

Do not use status directories:

```text
aifr/requirements/draft/...
aifr/requirements/approved/...
aifr/requirements/deprecated/...
```

Deprecated requirements stay in place:

```yaml
status: deprecated

versioning:
  superseded_by:
    - REQ-PAY-0041@1.0.0
  change_summary: 被新的统一退款规则替代
```

## Domain Changes

Do not move files or change ids when domain understanding changes. If `REQ-PAY-0012` later affects order behavior, do not rename it to `REQ-ORDER-0012` and do not move it to `order/`.

Use related domains and trace links:

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

## Title Changes

Title changes do not rename directories. If the directory is:

```text
REQ-PAY-0012--refund-amount-calculation/
```

and the title becomes:

```yaml
title: 退款金额与优惠券分摊计算规则
```

the directory remains unchanged. Record aliases in content when useful:

```yaml
aliases:
  titles:
    - 退款金额计算规则
    - 退款金额与优惠券分摊计算规则
  slugs:
    - refund-amount-calculation
    - refund-coupon-allocation
```

## Split, Merge, And Replacement

When splitting a requirement, keep the old requirement in place:

```yaml
status: superseded

versioning:
  superseded_by:
    - REQ-PAY-0041@1.0.0
    - REQ-PAY-0042@1.0.0
  change_summary: 原退款金额计算需求拆分为金额计算和优惠券分摊两个需求
```

Create new directories for new requirements:

```text
REQ-PAY-0041--refund-base-amount-calculation/
REQ-PAY-0042--coupon-allocation-for-refund/
```

When merging requirements, the new requirement records:

```yaml
versioning:
  supersedes:
    - REQ-PAY-0012@1.2.0
    - REQ-PAY-0018@1.0.0
```

Old requirements are marked:

```yaml
status: superseded
versioning:
  superseded_by:
    - REQ-PAY-0045@1.0.0
```

Do not delete old files. Do not merge old directories into one directory.

## AI And Codex Lookup

By id:

1. Extract domain code from the id, for example `PAY`.
2. Convert it to domain path through `registries/domains.aifr.yaml` or convention, for example `pay`.
3. Search `aifr/requirements/items/pay/REQ-PAY-0012--*/spec.aifr.yaml`.
4. Open the matched `spec.aifr.yaml`.
5. If multiple files match, report a conflict warning and do not guess.

By title or keyword:

1. Read `aifr/indexes/requirements.aifr-index.yaml`.
2. Search `title`, `aliases`, `slug`, `domain_terms`, and `code_search_hints`.
3. Identify candidate ids.
4. Open candidate `spec.aifr.yaml` files.

By baseline:

1. Prefer `aifr/indexes/baselines.aifr-index.yaml`.
2. Or locate `aifr/baselines/<scope-path>/<baseline-id>.aifr-baseline.yaml`.

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
- Chinese appears in the path.
- Version and status appear in the current path.
- Status changes cause moves.
- Team changes cause moves.
- `latest` is ambiguous.
