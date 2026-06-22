# AIFR Quality Checklist

Use this checklist before treating an AIFR spec as review-ready.

## V1 Quality Check Output

When reviewing a spec, report:

- Blocking issues: missing required fields, broken rule references, invalid identifiers, or untestable acceptance criteria.
- Warnings: unclear scope, weak scenarios, missing interface details, missing trace targets, unclear version bump, or insufficient high-risk controls.
- Suggested fixes: concrete YAML field or text changes.

## Structure

- Required top-level fields from `references/schema.md` are present.
- `references/schema.md` and `references/schema.zh-CN.md` are updated together when schema rules change.
- `references/output-format.md` is updated when version output, change-set output, impact analysis, or baseline output changes.
- `references/naming.md` is updated when path, filename, manifest, index, or baseline naming rules change.
- `id`, `rules[].id`, `scenarios[].id`, and `acceptance_criteria[].id` use stable prefixes.
- `type`, `status`, `priority`, and `risk.level` use documented values.
- Field names and nesting match the schema.

## Naming And Paths

- `spec.aifr.yaml` files are located at `aifr/requirements/items/<domain-path>/<id>--<slug>/spec.aifr.yaml` when using canonical structure.
- `identity.canonical_path` matches the actual path.
- The directory id matches `aifr_spec.id`.
- The directory slug matches `identity.frozen_slug`.
- `identity.domain_path` matches the path domain directory.
- `identity.primary_domain` matches the domain segment in `aifr_spec.id`, unless a migration reason is recorded.
- The current authoritative file is named `spec.aifr.yaml`.
- Current paths do not contain version numbers, status names, owner names, dates, team names, Chinese text, spaces, underscores, or `latest`.
- Frozen slug uses lowercase kebab-case, contains only English letters, numbers, and hyphens, and is no longer than 60 characters.
- Paths do not conflict by case only.

## ID Registry

- Requirement ids follow `REQ-<DOMAIN>-<NUMBER>`.
- New project ids use fixed 4-digit numbers such as `REQ-PAY-0012`.
- Existing domains do not mix 3-digit and 4-digit requirement numbers.
- `DOMAIN` exists in `aifr/registries/domains.aifr.yaml` when the registry exists.
- `NUMBER` width matches the domain registry `id_number_width`.
- There are no duplicate requirement ids.
- Deprecated or superseded ids are not reused.

## Version Management

- `schema_version` is present and refers to the AIFR Spec format version.
- `id` is stable across requirement revisions.
- `version` is present and uses semantic version format.
- `identity` is present for canonical `spec.aifr.yaml` files.
- `versioning.change_type` is present.
- `versioning.previous_version`, `versioning.supersedes`, and `versioning.superseded_by` do not conflict with the stated current version.
- `versioning.breaking_change` is explicitly true or false.
- `revision_history` is present and includes the current requirement version.
- Requirement updates include a `version_update` object.
- Requirement updates include a `change_set` instead of silently replacing old content.
- `recommended_bump` matches the bump decision rules in `references/output-format.md`.
- `change_set.modified_rules`, `change_set.modified_scenarios`, and `change_set.modified_acceptance_criteria` contain business semantic changes only.
- Wording, terminology, formatting, or explanation-only changes are listed under `change_set.textual_changes`.
- Missing old versions use `from_version: unknown`; the spec does not pretend to know old state.
- `versions/` snapshots align with `revision_history` when explicit snapshots are used.
- Baselines include id and version for every requirement.
- Baseline semantic references are `id@version`; paths are location hints only.
- Strong-audit baselines reference versions that exist in `versions/`.

## Status And Lifecycle

- `status` is one of the documented values.
- Status changes do not move files.
- `deprecated` and `superseded` requirements include `versioning.superseded_by` or an explicit reason when no replacement exists.
- `approved` requirements include reviewers or approval evidence.
- `draft` requirements are not locked into approved baselines.

## Business Semantics

- `intent.user_goal` describes the user-visible outcome.
- `intent.business_value` explains why the requirement matters.
- `scope.in` and `scope.out` make boundaries explicit.
- `domain_terms` defines calculation terms, status names, and business vocabulary used by rules.
- Preconditions are concrete enough to decide whether the requirement applies.

## Rules And Scenarios

- Each rule has a stable id and a business-readable description.
- Each calculation rule includes a formula or invariant.
- Scenarios use Given/When/Then lists.
- Scenarios include concrete values when they verify calculations, permissions, or state transitions.
- Scenario outcomes are consistent with the rules.

## Acceptance

- Each acceptance criterion is testable.
- Each acceptance criterion verifies at least one existing rule.
- High-risk requirements include criteria that cover boundary cases and failure cases.

## Interfaces

- APIs include method, path, request schema, and response schema.
- External systems are listed under `actors.secondary` or the relevant interface section.
- Interface names match the implementation vocabulary used in `trace.expected_code`.

## Traceability

- Expected code targets identify the likely service, module, method, handler, or command.
- Expected tests identify test files, classes, or suites.
- Acceptance criteria link back to rules.
- High-risk requirements identify auditability, security, compliance, or explicit review needs.

## Impact Analysis

- Requirement updates include `impact_analysis`.
- `requirement_impact.related_requirements` lists known adjacent requirements or is explicitly empty.
- `code_impact.level` is present and justified.
- `code_impact.code_search_hints` provides useful service, class, method, policy, event, or job names.
- `test_impact.level` is present and justified.
- `test_impact.recommended_tests` names expected new or changed tests.
- `review_impact.recommended_reviewers` lists relevant review roles for risky changes.
- Breaking changes include migration or implementation adjustment guidance.

## Validation

- Examples remain consistent with the current schema.
- Ambiguous requirements are clarified or marked as open questions.
- The smoke check passes with `scripts/validate_aifr_spec.py`.
- Passing the smoke check is not enough by itself; every relevant checklist section above has been reviewed manually.
