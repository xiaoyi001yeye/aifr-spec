# P0 Skill Capability Analysis

Requirement id: REQ-PRED-0001

Captured at: 2026-06-23

## P0 Test

A skill gap is P0 when it can silently corrupt requirement truth, implementation truth, or source-data truth while still letting the agent finish with a confident-looking answer.

P0 requires all of these:

- The failure can pass ordinary smoke checks.
- The failure affects the semantic meaning of a requirement, the data grounding of an implementation, or the traceability of a change.
- The failure is likely to recur across requirements, not only this demo.
- The fix can be made into a reusable skill workflow, validator, or artifact protocol.

## Writing-Great-Skills Pass

The P0 abilities below are shaped with the `writing-great-skills` vocabulary. The goal is predictability: the agent should take the same process every time a requirement update, external fact sync, or skill conflict appears.

Design rules:

- Give each P0 ability one leading word so the agent can think with it cheaply.
- Put deterministic checks in scripts when possible; do not make prose carry what code can verify.
- Keep the always-loaded skill body small; push schemas and examples behind context pointers.
- Define completion criteria that are both checkable and exhaustive.
- Avoid no-op guidance such as "be careful"; name the exact artifact, command, or failure that must exist.
- Keep single source of truth: a rule should live in either the skill body, a reference file, or a script, not all three.

## P0 Ability Summary

| Ability | Leading word | Primary form | Completion criterion |
| --- | --- | --- | --- |
| AIFR Consistency Gate | `gate` | Script plus AIFR validation instruction | Strict validation fails on stale index, bad path, duplicate id, or missing current revision. |
| Requirement Update Ledger | `ledger` | Artifact protocol plus template | Every semantic version bump has a matching immutable update artifact whose fields agree with the spec. |
| Source-to-Snapshot Protocol | `snapshot` | Skill branch plus extraction/diff scripts | External facts are traceable to source, normalized, diffable, and blocked on unresolved mappings. |
| Skill Arbitration Contract | `precedence` | Short shared rule in domain skills | Explicit domain workflow wins over generic workflow, and ambiguous mode still asks the user. |

## Gap Triage

| Gap | Severity | Reason |
| --- | --- | --- |
| AIFR validator only does smoke checks and misses index/version drift | P0 | It lets stale requirement metadata survive validation, so agents and humans can locate or cite the wrong version. |
| AIFR update report has no standard landing place | P0 | The spec can be overwritten while the required semantic delta, bump reason, and impact analysis vanish from the repo. |
| No source-to-snapshot workflow for semi-structured external facts | P0 | "Real" synchronized results can be hand-copied incorrectly, lose provenance, or use inconsistent time zones and match keys. |
| Generic grilling and AIFR self-grill routing is blurry | P1/P0-adjacent | It can interrupt or distort requirement discovery, but the domain AIFR skill already contains the correct self-grill rule. Make it P0 only as part of a broader skill-arbitration contract. |
| Browser skill does not mention localhost fallback for static HTML | P1 | It wastes validation time and can cause under-testing, but it does not directly corrupt requirement semantics or source data. |

## P0 Capability 1: AIFR Consistency Gate

Capability:

Run a strict cross-file consistency check after any AIFR spec update.

Leading word:

`gate`. The agent should not call an AIFR update done until it has passed the gate or reported every gate failure.

Invocation:

- Trigger from the existing AIFR skill whenever creating, updating, locating, validating, or versioning a spec.
- Do not create a separate model-invoked skill at first; this belongs inside the AIFR skill because it is a mandatory post-update step, not an optional branch.

Information hierarchy:

- In-skill step: "run the gate before finalizing."
- Script: actual cross-file checks.
- Reference: strict check list and error meanings.

Required checks:

- `aifr_spec.id` matches canonical directory id.
- `identity.canonical_path` matches the actual spec path.
- `identity.primary_domain`, `identity.domain_path`, and registry domain mapping agree.
- `aifr_spec.version` appears in `revision_history`.
- `versioning.previous_version` is coherent with the prior revision entry.
- `aifr/indexes/requirements.aifr-index.yaml` entries match each referenced spec id, title, version, status, domain, and path.
- Duplicate requirement ids are rejected across the repo.
- Acceptance criteria reference existing rule ids.
- Scenario/rule/acceptance ids are unique within a spec.
- Deprecated/superseded specs include replacement or explicit no-replacement reason.

Why P0:

The existing smoke validator can pass while an index points to an obsolete version. That makes downstream lookup, review, baselines, and implementation traceability unreliable.

Preferred form:

- Add `scripts/validate_aifr_spec.py --strict` or `scripts/check_aifr_consistency.py`.
- Update the AIFR skill's validation completion criterion: "Done only when smoke check and strict consistency gate both pass, or any strict failure is reported."

Anti-failure:

- Prevents premature completion after the smoke check.
- Prevents sediment in indexes and manifests.
- Prevents duplication between spec metadata and index metadata from drifting silently.

Done when:

- A stale index version fails validation.
- A mismatched canonical path fails validation.
- A missing current `revision_history` entry fails validation.
- A duplicate requirement id fails validation.
- A stale title/status/domain/path in `requirements.aifr-index.yaml` fails validation.

## P0 Capability 2: Requirement Update Ledger

Capability:

Every semantic requirement update must write an immutable update artifact beside the spec.

Leading word:

`ledger`. If requirement meaning changes, the ledger records what changed, why the bump is valid, and what review/test impact follows.

Invocation:

- Trigger from the AIFR skill's "Update Requirement Versions" workflow.
- Keep it as an AIFR branch, not a separate user-invoked skill, because an agent must not rely on the user to remember it.

Information hierarchy:

- In-skill step: compare old and new semantics, then write the ledger.
- Reference: ledger schema and examples.
- Template asset: empty update artifact.
- Script/gate: verify the ledger agrees with the spec.

Proposed path:

```text
aifr/requirements/items/<domain>/<REQ-ID>--<slug>/changes/v<to_version>.aifr-update.yaml
```

Minimum artifact:

```yaml
version_update:
  requirement_id: REQ-PRED-0001
  from_version: "1.1.0"
  to_version: "1.2.0"
  recommended_bump: minor
  breaking_change: false
  reason: 新增同步真实赛果展示和后续赛程影响，不移除既有模拟行为。

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

Why P0:

`references/output-format.md` requires `version_update`, `change_set`, and `impact_analysis`, but without a repository location those objects are easy to omit. That silently erases semantic history.

Preferred form:

- Add a template under `references/` or `assets/`.
- Add strict validation that any spec with `versioning.previous_version != null` has a matching `changes/v<version>.aifr-update.yaml`.
- Add skill instruction: update the spec and ledger in the same change.

Anti-failure:

- Prevents semantic history from being overwritten by a clean-looking current spec.
- Prevents no-op version updates that bump `version` without a change-set.
- Prevents impact analysis from living only in the chat transcript.

Done when:

- A requirement version bump without a ledger fails strict validation.
- The ledger's `to_version` must equal `aifr_spec.version`.
- The ledger's `recommended_bump` must agree with `versioning.change_type` unless marked `needs_review`.
- The ledger lists added/modified/removed rules, scenarios, and acceptance criteria, even when the list is empty.
- The ledger includes code, test, requirement, and review impact sections.

## P0 Capability 3: Source-to-Snapshot Protocol

Capability:

Convert external, semi-structured source material into a local, auditable snapshot before implementation uses it as truth.

This should not be sports-specific. Sports fixtures are one branch; the general capability is external-fact snapshotting.

Leading word:

`snapshot`. The agent should treat external current facts as untrusted until they have been turned into a local, dated, provenance-bearing snapshot.

Invocation:

- Create a model-invoked skill only if multiple repos need external fact ingestion.
- For this repo, first add it as an AIFR reference branch: use when a requirement or implementation claims to sync, mirror, import, or display external facts as truth.

Information hierarchy:

- In-skill step: decide whether external facts are requirement truth; if yes, require a snapshot.
- Reference: source reliability, provenance, timezone, entity key, and diff rules.
- Scripts: fetch/extract/normalize/diff.
- Assets: snapshot template.

Required workflow:

1. Fetch source and record URL, retrieval timestamp, source revision or page modified date when available.
2. Extract raw facts into a temporary raw snapshot.
3. Normalize entities with stable keys, not display names alone.
4. Normalize date/time with explicit source timezone and target timezone.
5. Validate record counts against a source-visible count when available.
6. Emit a snapshot artifact with provenance per record.
7. Emit a diff report when updating an existing snapshot.
8. Mark unresolved mappings instead of guessing.

For this World Cup demo, record shape should include:

```yaml
source:
  name: 2026 FIFA World Cup - Wikipedia
  url: https://en.wikipedia.org/wiki/2026_FIFA_World_Cup
  retrieved_at: "2026-06-23"
  source_modified_at: "2026-06-23T04:02:57Z"
timezone:
  source: America/New_York or source-local-per-match
  display: Asia/Shanghai
matches:
  - match_key: group:A:round:1:mexico-v-south-africa
    group: A
    home: 墨西哥
    away: 南非
    home_score: 2
    away_score: 0
    played_at_beijing: "2026-06-12 03:00"
    status: completed
    provenance:
      source_section: Schedule by group
```

Why P0:

The feature distinguishes "真实比赛结果" from predictions. If the snapshot is wrong, the app becomes confidently false. Manual extraction is fragile across names, ordering, time zones, and changed pages.

Preferred form:

- Create a new `source-snapshot` skill or an AIFR reference branch.
- Provide scripts for HTML table extraction, record normalization, and diffing.
- Require snapshot provenance in specs that use external current facts.

Anti-failure:

- Prevents display names from becoming unstable record identity.
- Prevents source timezone and display timezone from collapsing into one ambiguous date.
- Prevents "real result" UI from being backed by hand-copied, non-regenerable facts.
- Prevents source changes from being absorbed without a diff.

Done when:

- A snapshot can be regenerated with a deterministic diff.
- Unknown match/team mappings are reported as blocking gaps.
- Timezone conversion is visible in output and testable.
- Each normalized record has source URL, retrieval timestamp, source section/table, and stable key.
- The implementation consumes the snapshot artifact, not loose facts pasted only into application code.

## P0 Capability 4: Skill Arbitration Contract

Capability:

When multiple skills apply, the domain skill must declare precedence for mode selection and handoff.

Leading word:

`precedence`. The agent should know which skill owns the workflow when generic and domain skills both apply.

Invocation:

- Add this rule to model-invoked domain skills that overlap with generic skills.
- Do not create a standalone model-invoked arbitration skill yet; that would add context load without solving the local ambiguity.

Information hierarchy:

- In-skill reference: a short precedence rule near "When to Use" or "Core Workflows."
- External reference only if several skills adopt the same contract.

Minimal contract:

- If a domain skill has an explicit workflow for a requested mode, it owns that mode.
- Generic skills may provide vocabulary or checks, but must not override the domain workflow.
- If two skills impose incompatible blocking behavior, the agent records the conflict and chooses the narrower domain workflow unless the user explicitly asked otherwise.

Why P0-adjacent:

The generic grilling skill says to ask one question at a time. The AIFR skill says explicit self-grill should run internally and report decisions. Without precedence, an agent can either stop when it should continue, or continue privately when it should ask. That affects requirement discovery.

Preferred form:

- Add a short "Skill Precedence" section to AIFR skill docs.
- Add a generic router note to the grilling skill: "If a domain skill defines self-grill, follow that domain workflow."

Anti-failure:

- Prevents interactive-grill rules from overriding explicit self-grill requests.
- Prevents domain-specific completion criteria from being weakened by generic guidance.
- Prevents sprawl from creating a new always-loaded router before there are enough conflicts to justify it.

Done when:

- An explicit self-grill request never triggers an interactive question because the generic grilling skill was also relevant.
- An ambiguous "grill this" request still asks for interactive vs self-grill mode.
- A final self-grill artifact records assumptions, decisions, deferred items, and remaining open questions.

## Not P0: Static HTML Browser Fallback

Capability:

When Browser blocks `file://`, serve the directory over localhost and test the same artifact through HTTP.

Why not P0:

It is a validation ergonomics issue. It can delay or weaken QA, but it does not by itself change requirement semantics, source truth, or traceability.

Recommended severity:

P1. Add one line to the frontend/browser validation skill:

```text
For static local HTML files, if `file://` navigation is blocked, run a local static server and navigate to localhost.
```

## Recommended P0 Build Order

1. Build the AIFR strict consistency gate.
2. Add the requirement update ledger protocol and validate it from the gate.
3. Add the source-to-snapshot protocol for external facts.
4. Add the skill arbitration contract.

This order protects the repository's core truth first, then protects external truth, then improves skill routing reliability.

## Concrete Next Changes

1. Patch the AIFR skill validation section to require the `gate`.
2. Add `references/update-ledger.md` with the ledger schema and one example.
3. Add `scripts/check_aifr_consistency.py` or extend `scripts/validate_aifr_spec.py --strict`.
4. Add a fixture that intentionally desynchronizes `requirements.aifr-index.yaml` from a spec; strict validation must fail.
5. Add `references/source-snapshot.md` with the snapshot protocol and timezone/provenance rules.
6. Add a small `source-snapshot` script for HTML table extraction only after the protocol is stable.
7. Add an AIFR skill precedence paragraph; leave the generic grilling skill untouched unless the conflict recurs outside AIFR.
