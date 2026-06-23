# Source Snapshot Protocol

Use this when a requirement or implementation treats external facts as truth, such as synced schedules, imported prices, official results, policy tables, public directories, or semi-structured webpages.

Leading word: `snapshot`.

## Workflow

1. Fetch the source and record provenance.
2. Extract raw records without silently normalizing them.
3. Normalize entities with stable keys.
4. Normalize time with explicit source and display time zones.
5. Validate counts and required fields.
6. Emit a local snapshot artifact.
7. Diff against the previous snapshot when one exists.
8. Block on unresolved mappings instead of guessing.

## Snapshot Shape

```yaml
snapshot:
  id: SNAP-PRED-2026-WORLD-CUP-RESULTS-20260623
  captured_at: "2026-06-23T12:00:00+08:00"
  source:
    name: 2026 FIFA World Cup - Wikipedia
    url: https://en.wikipedia.org/wiki/2026_FIFA_World_Cup
    retrieved_at: "2026-06-23"
    source_modified_at: "2026-06-23T04:02:57Z"
  timezone:
    source: source-local-per-record
    display: Asia/Shanghai
  records:
    - key: group:A:round:1:mexico-v-south-africa
      status: completed
      fields:
        group: A
        home: 墨西哥
        away: 南非
        home_score: 2
        away_score: 0
        played_at_beijing: "2026-06-12 03:00"
      provenance:
        source_section: Schedule by group
        source_row_label: Match 1
```

## Rules

- A display name is not a stable key by itself.
- Every normalized record needs provenance.
- Every time field needs a source timezone or an explicit note that the source is already in the display timezone.
- Unknown entity mappings are blocking gaps.
- A snapshot update should produce a deterministic diff: added records, modified records, removed records, and unresolved records.
- Implementation should consume the snapshot artifact or generated data derived from it, not facts pasted only into code.

## Completion Criterion

A snapshot is complete only when the agent can regenerate it, explain every changed record in a diff, and identify every source row behind every normalized record.
