# AIFR Requirement Grilling

Use grilling when a user asks to complete, implement, or turn an idea into a requirement before the boundary is clear.

Grilling is a discussion discipline. Keep the conversation at the requirement level unless a technical or operational decision changes scope, acceptance, risk, rollout, data, or compatibility.

## Grill Modes

There are two grill modes:

- Interactive grill: interview the user one blocking question at a time.
- Self-grill: the agent interrogates its own requirement understanding, challenges assumptions, answers from source evidence where possible, and records unresolved gaps without asking the user each round.

If the user says to use grill but does not specify interactive grill or self-grill, ask which mode to use before continuing. First explain self-grill in plain language:

```text
Self-grill means I will interrogate the requirement myself: ask the hard boundary questions internally, answer from the facts we have, record assumptions and gaps, and stop if something cannot be safely decided.
```

If the user explicitly says self-grill, do not ask for mode confirmation. Start self-grill immediately.

## Interactive Grill Rules

Interactive grilling must not turn into private analysis followed by a finished spec.

- Ask one blocking question at a time.
- Wait for the user's answer before asking the next question.
- Include your recommended answer with each question.
- If the answer can be found by inspecting existing specs, code, README, issues, or source material, inspect that source instead of asking.
- If the user declines to answer, record the point as an explicit open question or deferral.
- Do not draft or implement while a blocking question is unanswered unless the user explicitly asks to proceed with assumptions.

## Self-Grill Rules

Self-grill is internal interrogation, not a user interview.

- Run up to 50 rounds maximum.
- Each round asks one hard boundary question and answers it from source evidence, current facts, or an explicit assumption.
- Prefer source evidence over assumptions.
- Record every assumption and unresolved gap.
- Stop early when no blocking branch remains.
- If round 50 is reached, stop and report remaining gaps instead of continuing.
- Do not manufacture certainty. If a blocking branch cannot be answered safely, mark it as an open question or deferred decision.

Self-grill round format:

```text
Round <n>
Question: <one hard boundary question>
Answer: <evidence-based answer or explicit assumption>
Result: <decision | assumption | open question | deferral>
```

## Boundary Cuts

Make these cuts before drafting or implementing:

- Intent: the user-visible outcome and business reason.
- In scope: behavior that must be delivered now.
- Out of scope: adjacent behavior that must not be silently included.
- Actors: users, roles, systems, jobs, or external services involved.
- Rules: deterministic business rules, calculations, permissions, state transitions, or limits.
- Scenarios: normal, boundary, failure, and permission examples.
- Acceptance: observable conditions that prove the requirement is done.
- Interfaces: APIs, events, commands, jobs, UI surfaces, files, or reports affected.
- Data: new, changed, read, written, migrated, retained, or audited data.
- Non-functional constraints: performance, reliability, auditability, security, compliance, localization, accessibility, and observability.
- Rollout: feature flags, migration, compatibility, backfill, release order, and fallback behavior.
- Risks: where wrong behavior causes financial, legal, security, operational, or user harm.

## Blocking Questions

Ask questions only when the answer changes the requirement. Prefer a small set of grouped questions over a long interrogation.

Question order:

1. Requirement boundary: what is included, excluded, and considered done?
2. Business rules: what decisions, calculations, permissions, or state transitions must be deterministic?
3. Acceptance: what examples or checks prove correctness?
4. Necessary implementation constraints: what data, interface, rollout, compatibility, or operational decisions affect the requirement?

Avoid asking about code structure, libraries, internal naming, or implementation style unless the choice changes externally visible behavior, traceability, risk, or delivery constraints.

Question format:

```text
Question: <one blocking decision>
Recommended answer: <the answer you would choose and why>
Why it matters: <scope, rule, acceptance, risk, rollout, data, or compatibility impact>
```

## Grilled Restatement

After discussion, restate:

- Intent and business value.
- Scope in and scope out.
- Actors and affected systems.
- Rules and scenarios.
- Acceptance criteria.
- Interfaces and trace targets when known.
- Risks and non-functional constraints.
- Open questions and deferred decisions.

Do not present assumptions as facts. If the user cannot answer a blocking question, record it as an open question and state what work can safely proceed without it.

## Completion Checks

- Grill mode is explicit: interactive grill or self-grill.
- Scope has both `in` and `out` boundaries.
- Acceptance criteria are observable and testable.
- Each rule is deterministic enough for implementation or is marked as an open question.
- Every blocking branch has been resolved by source evidence, user answer, or explicit deferral.
- Self-grill stops at or before 50 rounds and reports unresolved gaps.
- Necessary technical and operational constraints are captured without drifting into optional design discussion.
- Deferred items are explicit, not silently excluded.

## Failure Modes

- Ambiguous mode: user says "grill" and the agent starts without asking interactive vs self-grill.
- Batch interrogation: asking several questions at once makes the user do the skill's sorting work.
- Silent assumption: inventing answers to keep moving hides requirement risk.
- Premature spec: writing the AIFR YAML before blocking branches are resolved.
- Technical drift: asking about implementation style when the requirement boundary would not change.
- Infinite self-grill: continuing past 50 rounds instead of reporting the remaining gaps.
