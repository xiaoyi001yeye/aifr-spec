---
name: aifr-spec
description: Use when creating, updating, locating, comparing, reviewing, validating, or versioning AIFR requirements, baselines, naming paths, schema fields, output formats, traceability, or repository-local AIFR specs.
---

# AIFR Spec

Use this skill for AIFR requirement specifications: turning source material into specs, revising existing specs, comparing semantic versions, describing baselines, locating requirement files, and checking spec quality.

## When to Use

- User mentions AIFR, requirement specs, baselines, canonical paths, schema fields, traceability, quality checks, or `validate_aifr_spec.py`.
- User provides raw requirements, product notes, meeting notes, issues, or feature descriptions and wants structured AIFR output.
- User asks whether a requirement change is patch/minor/major, what changed, or what code/test impact follows.
- User asks to find a requirement by id, title, keyword, baseline, or canonical path.

Do not use this skill to connect directly to Jira, CodeGraph, coverage, or other external systems in V1. Provide downstream hints instead.

## Load References by Task

Read only the relevant references before acting:

| Task | Required references |
| --- | --- |
| Draft or revise specs | `references/schema.md`, `references/naming.md`, `references/output-format.md`, `references/examples.md` |
| Change schema fields | `references/schema.md`, `references/schema.zh-CN.md` |
| Create, move, or find files | `references/naming.md` |
| Generate version updates, change sets, impact analysis, or baselines | `references/output-format.md` |
| Review spec quality | `references/schema.md`, `references/quality-checklist.md`, `references/naming.md`, `references/output-format.md`, `references/traceability.md` |
| Add source, decision, test, or implementation mappings | `references/traceability.md` |

When `references/schema.md` changes, update `references/schema.zh-CN.md` in the same change.

## Core Workflows

### Draft Requirement Specs

Extract intent, scope, actors, domain terms, preconditions, rules, scenarios, acceptance criteria, interfaces, trace targets, risk, and non-functional constraints. Preserve known facts. Mark important missing information as concise open questions instead of inventing details. Output YAML with required schema/version fields and use the canonical path pattern from `references/naming.md`.

Done only when the YAML includes every required field from `references/schema.md`, every important unknown is either resolved or listed as an open question, and the canonical output path follows `references/naming.md`.

### Update Requirement Versions

Read the old requirement and requested change. Do not overwrite history as if it never existed. Generate the updated requirement plus `version_update`, `change_set`, and `impact_analysis`.

Use `references/output-format.md` as the single source of truth for bump rules and change report structure. Use `from_version: unknown` when old version input is unavailable. Keep wording changes in `change_set.textual_changes`; use `change_set.modified_*` only for business semantic changes.

Done only when the old and new semantics have been compared field-by-field, the recommended bump is justified by `references/output-format.md`, textual changes are separated from semantic changes, and code/test/review impact is explicit.

### Compare Versions

Separate file history from requirement semantics. Use Git history only when the user provides it or asks for it. Compare ids, versions, rules, scenarios, acceptance criteria, interfaces, trace targets, risk, and non-functional constraints. Output version update, change set, impact analysis, and migration guidance when possible.

Done only when unchanged, textual-only, added, modified, removed, and uncertain semantics are each accounted for.

### Describe Baselines

Output a `baseline` object with `BL-<SCOPE>-<PERIOD_OR_RELEASE>`, product version or release label, and requirement entries with id, version, and optional path. Treat a baseline as a provided snapshot, not a database or registry. Mark unknown requirement versions explicitly.

Done only when every baseline entry has an id and an explicit version or `unknown`, and every path is treated as a location hint rather than identity.

### Locate Requirement Files

Read `aifr/manifest.aifr.yaml` first when it exists. For id lookup, extract the domain code, resolve the domain path through `aifr/registries/domains.aifr.yaml` or convention, then search `aifr/requirements/items/<domain-path>/<id>--*/spec.aifr.yaml`. For title, keyword, or baseline lookup, use available indexes before opening candidate spec files. If multiple canonical matches exist for one id, report a conflict and do not guess.

Done only when each returned candidate is tied back to `aifr_spec.id`; if no unique match exists, report the ambiguity instead of selecting a best guess.

### Quality Check Specs

Check structure, naming, business semantics, rules, scenarios, acceptance criteria, interfaces, traceability, risk, non-functional requirements, and version management fields. Report findings in priority order with concrete field names and suggested fixes. Run the validator when the spec exists as a file.

Done only when the manual checklist in `references/quality-checklist.md` has been applied in addition to the validator smoke check, with validator warnings reported separately from reviewer findings.

## Version Concepts

- `schema_version`: version of the AIFR format, for example `1.0.0`
- Requirement `version`: semantic version of one requirement, for example `REQ-PAY-0012@1.2.0`
- `baseline`: named product version, release, or snapshot containing requirement versions

AIFR is not a database or persistence system. Git may record file history; AIFR records semantic requirement state.

## Naming Guardrails

Use `aifr/requirements/items/<domain-path>/<requirement-id>--<frozen-slug>/spec.aifr.yaml` as the canonical requirement path. Keep the authoritative requirement in `spec.aifr.yaml`. Store version, status, title, domain relationships, and ownership inside YAML, not path segments.

Never rename directories because a title changed, move files because status/domain understanding changed, put version/status/owner/date/team/Chinese text/`latest` in the current spec path, or delete deprecated/superseded requirement files.

## Validation

Run before considering spec updates complete:

```bash
python3 scripts/validate_aifr_spec.py .
python3 scripts/validate_aifr_spec.py . --spec path/to/spec.yaml
```

The validator is a smoke check for repository structure and lightweight AIFR YAML issues. It does not replace the required references, manual quality checklist, semantic comparison, or review judgment.
