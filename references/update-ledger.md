# AIFR Update Ledger

Use an update ledger whenever a requirement's semantic version changes.

Leading word: `ledger`.

## Path

Write the ledger beside the authoritative spec:

```text
aifr/requirements/items/<domain-path>/<requirement-id>--<frozen-slug>/changes/v<to_version>.aifr-update.yaml
```

Example:

```text
aifr/requirements/items/pay/REQ-PAY-0012--refund-amount-calculation/changes/v1.2.0.aifr-update.yaml
```

## Required Sections

```yaml
version_update:
  requirement_id: REQ-PAY-0012
  from_version: "1.1.0"
  to_version: "1.2.0"
  recommended_bump: minor
  breaking_change: false
  reason: 新增边界场景和验收标准，不改变已有行为。

change_set:
  added_rules: []
  modified_rules: []
  removed_rules: []
  added_scenarios: []
  modified_scenarios: []
  removed_scenarios: []
  added_acceptance_criteria: []
  modified_acceptance_criteria: []
  removed_acceptance_criteria: []
  textual_changes: {}
  semantic_summary: []

impact_analysis:
  requirement_impact:
    related_requirements: []
  code_impact:
    level: medium
    reason: ""
    code_search_hints: []
  test_impact:
    level: medium
    reason: ""
    recommended_tests: []
  review_impact:
    recommended_reviewers: []
```

## Rules

- `version_update.requirement_id` must equal `aifr_spec.id`.
- `version_update.from_version` must equal `aifr_spec.versioning.previous_version`.
- `version_update.to_version` must equal `aifr_spec.version`.
- `version_update.recommended_bump` must equal `aifr_spec.versioning.change_type`, unless the ledger explicitly uses `needs_review`.
- Keep semantic changes in `added_*`, `modified_*`, and `removed_*`.
- Keep wording-only changes in `textual_changes`.
- List all impact sections even when their arrays are empty.

## Completion Criterion

The ledger is complete only when the strict AIFR gate passes and a reviewer can understand what changed, why the version bump is valid, what code/test review is needed, and what stayed unchanged.
