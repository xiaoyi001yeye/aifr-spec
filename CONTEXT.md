# AIFR Spec

AIFR Spec describes AI-friendly requirements and the vocabulary used to compare requirement versions without treating the repository as a database.

## Language

**Requirement Version**:
The semantic version of one requirement, written as `REQ-DOMAIN-0000@x.y.z` for new projects when referenced outside the requirement body.
_Avoid_: file version, Git version

**Schema Version**:
The version of the AIFR Spec document format itself.
_Avoid_: requirement version, product version

**Baseline**:
A named product, release, or snapshot that lists a set of requirement versions.
_Avoid_: database, registry

**Semantic Change**:
A requirement change that alters business behavior, rules, scenarios, acceptance criteria, code impact, or test impact.
_Avoid_: textual change, formatting change

**Textual Change**:
A wording, terminology, formatting, or explanation change that does not alter business behavior.
_Avoid_: semantic change

**Modified Rule**:
A rule listed in `change_set.modified_rules` because its business semantics changed.
_Avoid_: clarified rule, wording change

**Clarified Rule**:
A rule whose wording changed without changing its business semantics.
_Avoid_: modified rule

## Example Dialogue

Dev: "I changed `RULE-002` to say 'cash refund' instead of 'refund' so the term is less ambiguous. Is that a modified rule?"

Domain expert: "No. That is a textual change or clarified rule. Use `modified_rules` only when the business behavior of `RULE-002` changes."
