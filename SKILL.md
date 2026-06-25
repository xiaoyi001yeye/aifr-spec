---
name: aifr-spec
description: Use when grilling, creating, updating, locating, comparing, reviewing, validating, versioning, implementation-auditing, or adding trace comments for AIFR requirements, baselines, schema fields, output formats, or repository-local specs.
---

# AIFR Spec

Use this skill for AIFR requirement specifications: grilling vague requests, turning source material into specs, revising existing specs, comparing semantic versions, describing baselines, locating requirement files, auditing implementation coverage, and checking spec quality.

## When to Use

- User mentions AIFR, requirement specs, baselines, canonical paths, schema fields, traceability, implementation status, implemented tests, trace comments, requirement id comments in code, quality checks, or `validate_aifr_spec.py`.
- User asks to help complete or implement a requirement, but the business intent, acceptance boundary, or implementation constraints are still fuzzy.
- User provides raw requirements, product notes, meeting notes, issues, or feature descriptions and wants structured AIFR output.
- User asks whether a requirement change is patch/minor/major, what changed, or what code/test impact follows.
- User asks to find a requirement by id, title, keyword, baseline, or canonical path.

Do not use this skill to connect directly to Jira, CodeGraph, coverage, or other external systems in V1. Provide downstream hints instead.

## Load References by Task

Read only the relevant references before acting:

| Task | Required references |
| --- | --- |
| Grill vague requirements before implementation or spec drafting | `references/requirement-grilling.md`, `references/schema.md` |
| Draft or revise specs | `references/schema.md`, `references/naming.md`, `references/output-format.md`, `references/examples.md` |
| Change schema fields | `references/schema.md`, `references/schema.zh-CN.md` |
| Create, move, or find files | `references/naming.md` |
| Generate version updates, change sets, impact analysis, or baselines | `references/output-format.md` |
| Review spec quality | `references/schema.md`, `references/quality-checklist.md`, `references/naming.md`, `references/output-format.md`, `references/traceability.md` |
| Add source, decision, test, or implementation mappings | `references/traceability.md` |
| Audit implementation coverage or update implementation status | `references/schema.md`, `references/traceability.md`, `references/quality-checklist.md` |
| Add code entry comments aligned to requirement ids | `references/traceability.md`, `references/naming.md` |
| Update a requirement semantic version | `references/output-format.md`, `references/update-ledger.md` |
| Use external facts as requirement or implementation truth | `references/source-snapshot.md` |

When `references/schema.md` changes, update `references/schema.zh-CN.md` in the same change.

## Skill Precedence

When this AIFR skill and a generic skill both apply, use the narrower AIFR workflow for requirement work.

- If the user explicitly asks for self-grill, run AIFR self-grill even if a generic grilling skill says to ask one question at a time.
- If the user ambiguously says "grill" without self-grill or interactive mode, ask for the mode.
- Use generic skills as reference vocabulary only when they do not override AIFR completion criteria.

## Core Workflows

### Grill Requirement Boundaries

Use this before drafting or implementing when the user says to complete a requirement but the requirement boundary is still unclear. Keep the discussion mostly at the requirement level; only ask about technical, data, migration, rollout, or operational details when they are necessary to define the requirement boundary.

First choose the grill mode:

- If the user explicitly asks for self-grill, use self-grill immediately.
- If the user explicitly asks to be interviewed, questioned, or grilled interactively, use interactive grill.
- If the user mentions grill but does not specify interactive grill or self-grill, stop and ask which mode to use. Explain that self-grill means the agent interrogates its own requirement understanding, challenges assumptions, and records unresolved gaps without asking the user each round.

Interactive grill:

1. Extract the current requirement candidate: user goal, business value, included scope, excluded scope, actors, rules, scenarios, acceptance criteria, interfaces, risks, and non-functional constraints.
2. Explore before asking. If a boundary answer can be found in existing specs, code, README, issues, or source material the user provided, inspect that source instead of asking.
3. Identify the next blocking branch. Use `references/requirement-grilling.md` to separate in-scope behavior, out-of-scope behavior, unknowns, assumptions, and implementation constraints that must be decided now.
4. Ask exactly one blocking question, include your recommended answer, and wait for the user's reply before asking the next question or drafting the spec. Do not batch questions.
5. Repeat until every blocking branch is resolved by evidence, user answer, or explicit deferral.
6. Restate the grilled requirement. Summarize the agreed intent, scope in/out, rules, acceptance criteria, open questions, and anything deliberately deferred.

Self-grill:

1. Extract the current requirement candidate.
2. Run an internal interviewer/respondent loop using `references/requirement-grilling.md`: ask the next strongest boundary question, answer it from source evidence or stated assumptions, then record the decision, assumption, or gap.
3. Stop when every blocking branch is resolved or deferred, or after 50 rounds at most.
4. Report the self-grill summary: resolved decisions, assumptions, open questions, deferred items, and whether the requirement is safe to draft or implement.

Done only when the grill mode is explicit, the requirement has explicit in-scope and out-of-scope boundaries, acceptance criteria are testable, every blocking branch has been answered or explicitly deferred, and the user can choose to draft an AIFR spec or implement from the grilled requirement without silent scope expansion. If interactive grill has a blocking question, stop after asking that one question. If self-grill reaches 50 rounds, stop and report remaining gaps instead of continuing.

### Draft Requirement Specs

Extract intent, scope, actors, domain terms, preconditions, rules, scenarios, acceptance criteria, interfaces, trace targets, risk, and non-functional constraints. Preserve known facts. Mark important missing information as concise open questions instead of inventing details. Output YAML with required schema/version fields and use the canonical path pattern from `references/naming.md`.

Done only when the YAML includes every required field from `references/schema.md`, every important unknown is either resolved or listed as an open question, and the canonical output path follows `references/naming.md`.

### Update Requirement Versions

Read the old requirement and requested change. Do not overwrite history as if it never existed. Generate the updated requirement plus `version_update`, `change_set`, and `impact_analysis`.

Use `references/output-format.md` as the single source of truth for bump rules and change report structure. Use `references/update-ledger.md` for the required ledger artifact. Use `from_version: unknown` when old version input is unavailable. Keep wording changes in `change_set.textual_changes`; use `change_set.modified_*` only for business semantic changes.

Done only when the old and new semantics have been compared field-by-field, the recommended bump is justified by `references/output-format.md`, textual changes are separated from semantic changes, code/test/review impact is explicit, a matching `changes/v<version>.aifr-update.yaml` ledger exists for semantic updates, and the strict gate passes or every strict failure is reported.

### Snapshot External Facts

Use this when a requirement or implementation treats external facts as truth, such as synced schedules, imported results, prices, policies, public registries, or semi-structured webpage data.

Read `references/source-snapshot.md`. Fetch or inspect the source, record provenance, normalize records with stable keys, normalize time zones explicitly, emit or update a local snapshot artifact, and report unresolved mappings as blocking gaps instead of guessing.

Done only when the snapshot can be regenerated, every normalized record has provenance, timezone handling is explicit, a deterministic diff exists for updates, and implementation consumes the snapshot artifact or generated data derived from it.

### Compare Versions

Separate file history from requirement semantics. Use Git history only when the user provides it or asks for it. Compare ids, versions, rules, scenarios, acceptance criteria, interfaces, trace targets, risk, and non-functional constraints. Output version update, change set, impact analysis, and migration guidance when possible.

Done only when unchanged, textual-only, added, modified, removed, and uncertain semantics are each accounted for.

### Describe Baselines

Output a `baseline` object with `BL-<SCOPE>-<PERIOD_OR_RELEASE>`, product version or release label, and requirement entries with id, version, and optional path. Treat a baseline as a provided snapshot, not a database or registry. Mark unknown requirement versions explicitly.

Done only when every baseline entry has an id and an explicit version or `unknown`, and every path is treated as a location hint rather than identity.

### Locate Requirement Files

Read `aifr/manifest.aifr.yaml` first when it exists. For id lookup, extract the domain code, resolve the domain path through `aifr/registries/domains.aifr.yaml` or convention, then search `aifr/requirements/items/<domain-path>/<id>--*/spec.aifr.yaml`. For title, keyword, or baseline lookup, use available indexes before opening candidate spec files. If multiple canonical matches exist for one id, report a conflict and do not guess.

Done only when each returned candidate is tied back to `aifr_spec.id`; if no unique match exists, report the ambiguity instead of selecting a best guess.

### Annotate Code Entrypoints

Add or update concise trace comments at implementation entrypoints so code can be traced back to AIFR requirement ids.

1. Resolve the requirement id. Use ids provided by the user or locate the requirement file. Confirm each id against `aifr_spec.id`; if a match is missing or ambiguous, report it and do not annotate that id.
2. Select stable entrypoints. Start from `trace.expected_code`, then inspect nearby code to choose public handlers, service methods, commands, jobs, policies, adapters, or workflow orchestration functions. Avoid private helpers unless they are the only stable boundary.
3. Add minimal comments. Use the local language's normal documentation or line-comment style and the format rules in `references/traceability.md`. Keep comments factual; do not paste requirement prose into code.
4. Report coverage. List each requirement id, annotated entrypoint, and any unresolved requirement or code mapping gap.

Done only when every requested requirement id is resolved or explicitly reported as unresolved, every annotated code entrypoint maps to an existing `aifr_spec.id`, comments are placed at stable entrypoints rather than low-level helpers, and every ambiguous mapping is listed as an open question.

### Audit Implementation Coverage

Use this after or during implementation when the user wants to know whether a requirement is actually covered by code and tests. Treat `trace.expected_code` and `trace.expected_tests.planned` as search hints, not proof.

1. Resolve the requirement file and inspect its rules, acceptance criteria, interfaces, `implementation`, `trace`, related requirements, and recommended vertical slices.
2. Inspect the repository for matching code and tests. Distinguish planned tests from tests that exist and exercise the rule or acceptance criterion.
3. Update machine-readable implementation state when asked: `implementation.status`, per-rule coverage, `trace.expected_tests.implemented`, and any related requirement index hints. Do not mark `verified` without running the relevant tests.
4. Report gaps by requirement id, rule id or acceptance criterion id, code target, and missing planned or implemented test.

Done only when every rule and acceptance criterion is marked covered, missing, or not applicable; planned tests and implemented tests are separated; reused endpoints identify the authorization source that rechecks access; related requirements affected by the same business term are named or explicitly unknown; and verification commands have passed or are reported as not run.

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
python3 scripts/validate_aifr_spec.py . --strict
```

The default validator is a smoke check for repository structure and lightweight AIFR YAML issues. The `--strict` gate checks cross-file consistency for ids, paths, indexes, revision history, duplicate local ids, and update ledgers. Neither mode replaces the required references, manual quality checklist, semantic comparison, or review judgment.
