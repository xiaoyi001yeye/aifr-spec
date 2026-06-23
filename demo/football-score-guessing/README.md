# Football Score Guessing Demo

This demo project contains an AIFR requirement for an entertainment football score guessing page.

## Grilled Requirement

User request:

> 用户给出两个足球队，给我猜最终的比分。

Resolved through requirement grilling:

- The score guess is entertainment-only and does not use external football data.
- The same teams may return different random scores on different requests.
- Scores should look plausible for football: common low scores, occasional larger scores, never absurd scores.
- Teams are displayed in the input order only; no home/away modeling.
- Empty team names, missing team names, and identical team names are rejected.
- The result must include a disclaimer that the guess is for entertainment and does not guarantee accuracy.
- The interaction surface is a simple web page.

Canonical requirement:

```text
aifr/requirements/items/pred/REQ-PRED-0001--guess-football-final-score/spec.aifr.yaml
```

