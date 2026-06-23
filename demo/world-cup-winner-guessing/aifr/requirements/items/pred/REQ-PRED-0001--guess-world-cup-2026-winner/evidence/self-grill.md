# Self-Grill Evidence

Requirement id: REQ-PRED-0001

Mode: self-grill

Round limit: 50

Rounds used: 40

## Rounds

### Round 1

Question: Is the feature a serious prediction product or an entertainment guessing product?

Answer: Treat it as entertainment. The user asked to create a guessing project, not a statistical forecasting product.

Result: Decision.

### Round 2

Question: Should the product depend on live 2026 World Cup data?

Answer: No runtime dependency on live data. Current tournament state is time-sensitive, and a demo requirement should avoid fragile external data unless explicitly requested.

Result: Decision.

### Round 3

Question: How can the product stay relevant to the 2026 World Cup without live data?

Answer: Use a local configurable candidate country pool. Maintainers can update the pool manually as tournament context changes.

Result: Decision.

### Round 4

Question: Should the candidate pool include all FIFA countries or only configured contenders?

Answer: Use a configured pool, not all FIFA countries. The feature guesses a possible 2026 champion, so the pool should contain countries the product owner wants to consider.

Result: Decision.

### Round 5

Question: Should guesses be uniform random or weighted?

Answer: Support optional configured weights. If weights are absent, fall back to equal probability. This keeps the MVP simple while allowing plausibility.

Result: Decision.

### Round 6

Question: Should the same click always return the same country?

Answer: No. Random guesses may vary between clicks because the feature is entertainment-oriented.

Result: Decision.

### Round 7

Question: What is the user interaction surface?

Answer: Use a simple web page with one primary action to guess the champion.

Result: Assumption, based on prior demo pattern and the user's request for a project rather than an API.

### Round 8

Question: Does the user need to input anything?

Answer: No required input. The page can show a "guess champion" action because the tournament is fixed to the 2026 World Cup.

Result: Decision.

### Round 9

Question: Should the page expose the candidate pool?

Answer: Show the guessed country and a short statement that the guess comes from a local entertainment pool. Do not require exposing the full pool in the MVP.

Result: Decision.

### Round 10

Question: What happens if the candidate pool is empty?

Answer: The system must not guess. It should show a configuration error.

Result: Decision.

### Round 11

Question: What makes the candidate pool valid?

Answer: It must contain at least one country, each country must have a non-empty display name, country names must be unique after normalization, and weights must be positive when present.

Result: Decision.

### Round 12

Question: Should the result mention accuracy?

Answer: It must include a disclaimer that the result is for entertainment only, does not guarantee accuracy, and is not betting advice.

Result: Decision.

### Round 13

Question: Should the project explain why the selected country can win?

Answer: Not in V1. Explaining reasons would imply analysis quality or require data. Keep V1 to the country guess plus disclaimer.

Result: Decision.

### Round 14

Question: Should the app use official FIFA branding or logos?

Answer: No. Avoid official branding unless licensed. Use plain text naming only.

Result: Decision.

### Round 15

Question: Should the feature allow repeated guesses?

Answer: Yes. The user can click again and receive another random country.

Result: Decision.

### Round 16

Question: What is the main risk?

Answer: Misrepresentation: users might read it as real prediction or betting advice. Mitigate with clear entertainment and no-betting disclaimer.

Result: Decision.

### Round 17

Question: What should tests cover?

Answer: Candidate pool validation, random selection from the pool, weighted selection configuration, repeated guessing, empty-pool failure, and disclaimer display.

Result: Decision.

### Round 18

Question: Are any blocking branches unresolved?

Answer: No blocking branch remains for drafting. Remaining items can be open questions: exact default candidate pool, exact weights, and whether to show the full pool.

Result: Done.

### Round 19

Question: The user now asks to write the 2026 World Cup participating teams into the requirement. Should the candidate pool remain arbitrary?

Answer: No. The candidate pool should become the documented 48 participating teams.

Result: Decision.

### Round 20

Question: Should guesses ever use countries outside the documented participant teams?

Answer: No. Every guess must be selected from the documented 48 teams only.

Result: Decision.

### Round 21

Question: Should optional weights remain in V1 after the user asks to guess from the participating teams?

Answer: No. Remove weights from V1 to keep the requirement focused on the user's request: choose from the listed teams.

Result: Decision.

### Round 22

Question: How should the team list be sourced?

Answer: Use the current 2026 FIFA World Cup teams list and record the retrieval date. Because tournament pages can change, the requirement should treat the embedded 48-team list as the V1 source of truth for runtime selection.

Result: Decision.

### Round 23

Question: The user now asks to show group-stage match order and guess each score until a champion is produced. Is the previous "single champion guess" enough?

Answer: No. The feature must become a tournament simulation.

Result: Decision.

### Round 24

Question: Should the page show every group-stage match score?

Answer: Yes. The user specifically asks for each group-stage matchup to be guessed separately.

Result: Decision.

### Round 25

Question: How should group-stage match order be represented?

Answer: Use the four-team group order 1v2, 3v4, 1v3, 4v2, 4v1, 2v3 for every group.

Result: Decision.

### Round 26

Question: How should teams qualify for the knockout stage?

Answer: Use the 2026 48-team format: top two from each group plus eight best third-placed teams.

Result: Decision.

### Round 27

Question: Should V1 exactly implement official Annex C third-place matchup combinations?

Answer: No. That mapping is complex and depends on 495 combinations. V1 should document an entertainment bracket seeded from simulated performance and leave exact Annex C as an open question.

Result: Decision.

### Round 28

Question: What must the page show to make the process feel more real?

Answer: Show group-stage scores, group standings, knockout rounds, and final champion.

Result: Decision.

### Round 29

Question: Are blocking branches unresolved for this enhancement?

Answer: No blocking branch remains for a V1 entertainment simulator. Exact venue/time display and official Annex C pairing remain open questions.

Result: Done.

### Round 30

Question: Does the new sync request change the previous "no real data" boundary?

Answer: Yes, but only narrowly. The feature should not perform runtime live-data fetching in the single-file demo; it can use an embedded completed-results snapshot as the synced source.

Result: Decision.

### Round 31

Question: Where should the sync action appear?

Answer: Place a "同步赛况" action immediately to the left of "重新模拟", matching the user's requested position and preserving the existing primary simulation action.

Result: Decision.

### Round 32

Question: What does synchronization do to a completed match already displayed as a prediction?

Answer: It replaces the corresponding fixture's predicted score with the synced real final score, keeping the fixture in the same group-stage slot.

Result: Decision.

### Round 33

Question: How should users tell real results apart from predictions?

Answer: Each match card should display a source label: "同步真实赛果" for completed synced matches and "模拟预测" for remaining simulated matches. Real scores should also use distinct styling.

Result: Decision.

### Round 34

Question: What key data must a synced match show?

Answer: At minimum: both teams, final score, result source label, and match time converted to Beijing time.

Result: Decision.

### Round 35

Question: Should synced real results affect only display, or also future simulation?

Answer: They must affect computation. Synced scores should feed the group standings, which determine qualifiers, knockout slot filling, and the final simulated champion.

Result: Decision.

### Round 36

Question: What happens to future or unsynced fixtures after synchronization?

Answer: They remain simulated predictions and are explicitly labeled as such. Re-simulating after sync keeps the real results fixed and re-randomizes future predictions.

Result: Decision.

### Round 37

Question: How should knockout placement work after synced group results change standings?

Answer: Use the public round-of-32 seed slots from the schedule: group winners, runners-up, and best third-place candidates fill the bracket, then winners advance by official match numbers. Exact Annex C third-place combination selection remains deferred.

Result: Decision with deferral.

### Round 38

Question: Should the sync button fetch Wikipedia at runtime?

Answer: No. The local demo should remain a deterministic single-file app; the sync button applies an embedded snapshot retrieved on 2026-06-23.

Result: Decision.

### Round 39

Question: Is there a data freshness risk?

Answer: Yes. The snapshot can lag the current tournament. The requirement should show retrieval date/source and leave live authorized API integration as a future open question.

Result: Assumption and open question.

### Round 40

Question: Are blocking branches unresolved for this sync enhancement?

Answer: No blocking branch remains for a local snapshot-based sync implementation. Live official data integration, full Annex C mapping, and richer match metadata are deferred.

Result: Done.

## Summary

Resolved decisions:

- Entertainment-only champion guess.
- Simple web page.
- No required user input.
- The requirement embeds the 48 participating teams for the 2026 FIFA World Cup.
- The page simulates group-stage scores, standings, qualifiers, knockout rounds, and champion from the embedded 48-team field.
- The page can synchronize a local completed-results snapshot and keep those real results fixed while simulating future fixtures.
- Synced matches show Beijing time, final score, and a "同步真实赛果" label; predicted matches show a "模拟预测" label.
- Synced real results affect standings, qualifiers, knockout slots, and the eventual simulated champion.
- Random result may vary between clicks.
- Required entertainment and no-betting disclaimer.
- Missing, incomplete, or duplicated participant pool blocks guessing.
- The sync snapshot is embedded in the demo and is not fetched from the network at runtime.

Assumptions:

- The project should follow the existing demo style and focus on AIFR requirement documentation rather than implementation code.
- A simple page is the right surface for the demo.
- Wikipedia is acceptable as the user-provided source for the local snapshot, but it may lag the live tournament state.

Open questions:

- Should a future version display the full candidate pool to users?
- Should future versions update the embedded team list automatically from an official source?
- Should future versions implement official Annex C third-place pairing combinations exactly?
- Should future versions connect to an authorized live data source instead of an embedded snapshot?
- Should future versions show real cities, stadiums, referees, attendance, and scorer details for each synced match?
