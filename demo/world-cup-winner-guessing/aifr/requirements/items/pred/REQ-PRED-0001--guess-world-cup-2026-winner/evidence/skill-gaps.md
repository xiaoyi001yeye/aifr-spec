# Skill Gap Notes

Requirement id: REQ-PRED-0001

Captured at: 2026-06-23

## Observed Gaps

- Generic grilling guidance says to ask one question at a time, while the repository AIFR skill adds a separate self-grill mode. The routing is workable, but the generic skill alone does not explain how to produce a non-interactive self-grill artifact for implementation tasks.
- The frontend browser validation skill requires Browser first, but the Browser runtime blocks `file://` URLs. The skill would be clearer if it explicitly recommended serving static HTML over localhost when validating local single-file pages.
- The AIFR validator is intentionally a smoke check and does not catch semantic consistency issues such as a stale requirements index version. A dedicated index/spec consistency check would reduce manual drift.
- There is no repository-local skill for extracting, normalizing, and snapshotting sports schedules/results from a semi-structured web source. Time-zone conversion, source dating, and match-key normalization had to be handled manually.
- The current AIFR update workflow describes semantic change reports, but the demo repository has no standard location or template for storing the per-update `version_update`, `change_set`, and `impact_analysis` alongside the authoritative spec.
