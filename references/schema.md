# AIFR Schema

AIFR specifications are YAML documents that describe a requirement with enough business context, deterministic rules, executable scenarios, acceptance criteria, interfaces, traceability, risk, non-functional expectations, and semantic version metadata for implementation and review.

## V1 Use Cases

- Grill vague requirement requests into explicit scope, boundaries, rules, acceptance criteria, and open questions before drafting or implementation.
- Convert a natural language requirement description into a structured AIFR YAML spec.
- Check an existing AIFR YAML spec for structural quality, traceability, and review readiness.
- Generate, compare, and explain semantic requirement version changes.
- Describe a release or product baseline as a snapshot of requirement versions.
- Locate requirements through stable ids, manifests, indexes, and canonical paths.
- Annotate stable code entrypoints with AIFR requirement ids for implementation traceability.

## Top-Level Fields

A single requirement is wrapped in an `aifr_spec` object. This excerpt shows the wrapper and identity fields; use `references/output-format.md` for complete output examples.

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

Required fields:

- `schema_version`: Version of the AIFR Spec format itself, for example `1.0.0`.
- `id`: Stable requirement identifier. Use an uppercase domain prefix and fixed-width sequence, for example `REQ-PAY-0012`.
- `version`: Semantic version of this requirement, for example `1.2.0`.
- `title`: Human-readable requirement title.
- `type`: Requirement category. Common values: `functional`, `non_functional`, `constraint`, `interface`, `data`.
- `status`: Review state. Common values: `draft`, `review`, `approved`, `deprecated`, `superseded`.
- `priority`: Delivery or business priority. Common values: `low`, `medium`, `high`, `critical`.
- `identity`: Stable naming and canonical path identity metadata.
- `lifecycle`: Ownership and review lifecycle metadata.
- `versioning`: Current version change metadata.
- `revision_history`: Requirement semantic version history.
- `intent`: Requirement intent object.
- `scope`: Included and excluded scope.
- `actors`: Primary and secondary actors.
- `domain_terms`: Domain vocabulary used by the requirement.
- `preconditions`: Preconditions that must hold before the requirement applies.
- `rules`: Deterministic business rules.
- `scenarios`: Behavior examples in Given/When/Then form.
- `acceptance_criteria`: Reviewable criteria linked to rules or scenarios.
- `interfaces`: APIs, events, jobs, or other system boundaries affected by the requirement.
- `trace`: Expected implementation and test trace targets.
- `risk`: Risk level and reasons.
- `non_functional`: Performance, auditability, reliability, security, or compliance constraints.

## Field Details

### schema_version

Use `schema_version` for the AIFR Spec format version, not for product or requirement versioning. V1 documents should use:

```yaml
schema_version: "1.0.0"
```

### version

Use `version` for the semantic version of one requirement. A complete requirement reference combines id and version:

```text
REQ-PAY-0012@1.2.0
```

Version bump decision rules and update report fields live in `references/output-format.md`.

### identity

Use `identity` to connect the requirement id to its stable canonical path. Path data is location metadata; `aifr_spec.id` remains the final authority for requirement identity.

- `primary_domain`: Uppercase domain code from the requirement id, for example `PAY`.
- `domain_path`: Lowercase path code, for example `pay`.
- `frozen_slug`: Stable kebab-case slug from the requirement directory.
- `canonical_path`: Expected canonical path to the current authoritative `spec.aifr.yaml`.
- `naming_standard_version`: Version of the AIFR naming standard, for example `1.0.0`.
- `related_domains`: Optional related uppercase domain codes when the requirement affects other domains.

Rules:

- `canonical_path` should match the actual path.
- `domain_path` should match the path directory under `aifr/requirements/items/`.
- `frozen_slug` should match the slug in `<requirement-id>--<frozen-slug>`.
- `primary_domain` should match the `DOMAIN` segment in `REQ-<DOMAIN>-<NUMBER>` unless a migration reason is recorded.
- If file path and `aifr_spec.id` conflict, trust `aifr_spec.id` but report a high-severity warning.

### lifecycle

Use `lifecycle` for ownership and review metadata:

- `created_at`: Creation timestamp or `null` when unknown.
- `updated_at`: Last semantic update timestamp or `null` when unknown.
- `owner`: Owning person, role, team, or `null`.
- `reviewers`: Review roles or people.

### versioning

Use `versioning` for the current version's relationship to earlier or later requirement versions:

- `change_type`: `initial`, `patch`, `minor`, `major`, `deprecated`, or `needs_review`.
- `previous_version`: Previous requirement version or `null`.
- `supersedes`: Requirement version references this version replaces.
- `superseded_by`: Requirement version reference that replaces this version, or `null`.
- `breaking_change`: `true` when existing implementation, tests, or business behavior must change.
- `change_summary`: Concise semantic change summary.

### revision_history

Use `revision_history` to summarize semantic requirement versions, not Git commits. Each entry should include:

- `version`
- `change_type`
- `summary`

### intent

Use `intent` to explain why the requirement exists.

- `user_goal`: User-facing outcome.
- `business_value`: Business reason or operational value.

### scope

Use `scope` to prevent requirement creep.

- `in`: Explicitly included cases.
- `out`: Explicitly excluded cases.

### actors

Use `actors` to name systems or roles that participate in the behavior.

- `primary`: Main actor that triggers or receives the behavior.
- `secondary`: Supporting systems, services, or roles.

### domain_terms

Use a mapping from term to definition. Terms should match the names used in rules, formulas, scenarios, and acceptance criteria.

### rules

Each rule must include:

- `id`: Stable rule identifier, for example `RULE-001`.
- `description`: Business-readable rule.

Each rule should include at least one deterministic expression:

- `invariant`: A condition that must always hold.
- `formula`: A calculation or derivation rule.

### scenarios

Each scenario must include:

- `id`: Stable scenario identifier, for example `SCN-001`.
- `name`: Scenario name.
- `given`: Initial facts or state.
- `when`: Triggering action.
- `then`: Expected outcome.

Use concrete values in scenarios when calculation, state transition, permission, or integration behavior matters.

### acceptance_criteria

Each acceptance criterion must include:

- `id`: Stable criterion identifier, for example `AC-001`.
- `text`: Testable acceptance statement.
- `verifies`: One or more linked `rules.id` values.

### interfaces

Use `interfaces` to describe affected integration points. For APIs, include:

- `method`
- `path`
- `request_schema`
- `response_schema`

### trace

Use `trace` to guide implementation and testing.

- `expected_code`: Expected service, module, method, handler, or command targets.
- `expected_tests`: Expected automated test classes, files, or suites.

Code entrypoint comments are implementation traceability aids. They should use existing requirement ids from `aifr_spec.id` and should be placed at stable entrypoints identified by `trace.expected_code`, not modeled as a separate schema field in V1.

### risk

Use `risk` to highlight implementation and review sensitivity.

- `level`: `low`, `medium`, `high`, or `critical`.
- `reasons`: Concrete reasons for the risk level.

### non_functional

Use `non_functional` for constraints such as:

- `performance`
- `auditability`
- `security`
- `reliability`
- `compliance`

## Quality Rules

Use these rules for manual quality review. `scripts/validate_aifr_spec.py` covers only a smoke-check subset and must not be treated as full schema validation.

- `aifr_spec.schema_version` is present.
- `aifr_spec.id` is stable and follows the requirement id format.
- `aifr_spec.version` is present and follows semantic version format.
- `aifr_spec.identity` is present in canonical `spec.aifr.yaml` files.
- `aifr_spec.identity.canonical_path` matches the actual path.
- `aifr_spec.versioning.change_type` is present.
- `aifr_spec.revision_history` contains at least one entry.
- Required top-level fields are present.
- Identifiers follow their expected prefixes: `REQ-`, `RULE-`, `SCN-`, and `AC-`.
- `acceptance_criteria[].verifies` values reference existing `rules[].id` values.
- Scenario sections include non-empty `given`, `when`, and `then` lists.
- Domain terms referenced in formulas or invariants are defined in `domain_terms`.
- High or critical risk requirements include at least one `non_functional.auditability`, `security`, `compliance`, or explicit review note.

## Baseline Documents

A baseline is a product, release, or snapshot reference that lists requirement versions. It is not a database and does not replace Git file history.

Baseline id format:

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

Baseline rules:

- `baseline.id` should use `BL-<SCOPE>-<PERIOD_OR_RELEASE>`.
- `requirements` must include id and version; `id@version` is the semantic reference.
- `path` is a location hint only.
- Baselines must not reference only paths without versions.
- Unknown requirement versions must be marked explicitly instead of guessed.
- Baselines describe snapshots only; V1 does not implement baseline storage, Git integration, or external tracker sync.
- In strong-audit scenarios, baseline-referenced versions must exist in `versions/`.

## Repository Manifest And Indexes

The repository entrypoint is `aifr/manifest.aifr.yaml`:

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

Indexes are generated lookup aids under `aifr/indexes/`, not authoritative sources. Their data must be reconstructable from `spec.aifr.yaml`.

```yaml
requirements:
  - id: REQ-PAY-0012
    title: 退款金额计算规则
    domain: PAY
    version: "1.2.0"
    status: approved
    path: aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/spec.aifr.yaml
```

Detailed naming and lookup rules live in `references/naming.md`.
