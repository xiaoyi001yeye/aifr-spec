# World Cup Winner Guessing Demo

This demo project contains an AIFR requirement for an entertainment page that guesses which country may win the 2026 FIFA World Cup.

## Self-Grilled Requirement

User request:

> 创建一个猜2026届世界杯哪个国家能夺冠的项目。

Resolved through self-grill:

- The project is entertainment-only and must not claim predictive accuracy.
- The interaction surface is a simple web page.
- The user triggers a full entertainment tournament simulation.
- The requirement document lists the 48 participating teams for the 2026 FIFA World Cup.
- The page guesses scores for each group-stage match in group fixture order.
- The page calculates simulated standings, chooses 32 qualifiers, simulates knockouts, and reveals one champion.
- Every simulated match and champion must use teams from the documented 48-team field only.
- The runtime does not call live fixtures, odds, rankings, news, or historical match databases.
- The page must include a disclaimer that the result is for entertainment only and is not betting advice.
- If the documented participant pool is missing, incomplete, or duplicated, the page must show a clear configuration error instead of guessing.

Canonical requirement:

```text
aifr/requirements/items/pred/REQ-PRED-0001--guess-world-cup-2026-winner/spec.aifr.yaml
```

Runnable single-file app:

```text
index.html
```
