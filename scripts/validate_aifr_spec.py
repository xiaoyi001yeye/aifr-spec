#!/usr/bin/env python3
"""Smoke-check the AIFR spec repository and lightweight AIFR YAML quality."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/schema.md",
    "references/schema.zh-CN.md",
    "references/naming.md",
    "references/output-format.md",
    "references/examples.md",
    "references/quality-checklist.md",
    "references/traceability.md",
    "scripts/validate_aifr_spec.py",
    "README.md",
]

REQUIRED_TOP_LEVEL_FIELDS = [
    "schema_version",
    "id",
    "version",
    "title",
    "type",
    "status",
    "priority",
    "identity",
    "lifecycle",
    "versioning",
    "revision_history",
    "intent",
    "scope",
    "actors",
    "domain_terms",
    "preconditions",
    "rules",
    "scenarios",
    "acceptance_criteria",
    "interfaces",
    "trace",
    "risk",
    "non_functional",
]

ALLOWED_TYPES = {"functional", "non_functional", "constraint", "interface", "data"}
ALLOWED_STATUSES = {"draft", "review", "approved", "deprecated", "superseded"}
ALLOWED_PRIORITIES = {"low", "medium", "high", "critical"}
ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}
ALLOWED_CHANGE_TYPES = {"initial", "patch", "minor", "major", "deprecated", "needs_review"}


def validate_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        if not path.is_file():
            errors.append(f"missing required file: {relative_path}")
    return errors


def validate_skill_frontmatter(root: Path) -> list[str]:
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return []

    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ["SKILL.md must start with YAML frontmatter"]

    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        return ["SKILL.md frontmatter must be enclosed by --- delimiters"]

    errors: list[str] = []
    if "name:" not in frontmatter:
        errors.append("SKILL.md frontmatter must include name")
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter must include description")
    return errors


def top_level_fields(text: str) -> set[str]:
    fields: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", line)
        if match:
            fields.add(match.group(1))
    return fields


def unwrap_aifr_spec(text: str) -> str:
    """Return the requirement body, accepting either legacy top-level or aifr_spec-wrapped YAML."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == "aifr_spec:":
            body: list[str] = []
            for nested_line in lines[index + 1 :]:
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", nested_line):
                    break
                if nested_line.startswith("  "):
                    body.append(nested_line[2:])
                else:
                    body.append(nested_line)
            return "\n".join(body)
    return text


def scalar_top_level_value(text: str, field: str) -> str | None:
    match = re.search(rf"^{re.escape(field)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def collect_ids(text: str, section: str) -> list[str]:
    ids: list[str] = []
    in_section = False
    for line in text.splitlines():
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", line):
            in_section = line.startswith(f"{section}:")
            continue
        if not in_section:
            continue
        match = re.match(r"^\s*-\s+id:\s*([A-Za-z0-9_-]+)\s*$", line)
        if match:
            ids.append(match.group(1))
    return ids


def collect_verify_targets(text: str) -> list[str]:
    targets: list[str] = []
    in_acceptance = False
    for line in text.splitlines():
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", line):
            in_acceptance = line.startswith("acceptance_criteria:")
            continue
        if not in_acceptance:
            continue
        match = re.match(r"^\s*-\s+(RULE-[0-9]+)\s*$", line)
        if match:
            targets.append(match.group(1))
    return targets


def scenario_blocks(text: str) -> list[str]:
    match = re.search(
        r"^scenarios:\n(?P<body>.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return []
    body = match.group("body")
    return [block for block in re.split(r"(?=^\s*-\s+id:\s*SCN-)", body, flags=re.MULTILINE) if block.strip()]


def block_has_non_empty_list(block: str, field: str) -> bool:
    match = re.search(
        rf"^\s+{re.escape(field)}:\s*\n(?P<body>.*?)(?=^\s+[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        block,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return False
    return bool(re.search(r"^\s+-\s+\S", match.group("body"), re.MULTILINE))


def risk_level(text: str) -> str | None:
    match = re.search(
        r"^risk:\n(?P<body>.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    level = re.search(r"^\s+level:\s*(.+?)\s*$", match.group("body"), re.MULTILINE)
    if not level:
        return None
    return level.group(1).strip().strip("\"'")


def nested_scalar(text: str, section: str, field: str) -> str | None:
    match = re.search(
        rf"^{re.escape(section)}:\n(?P<body>.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    value = re.search(rf"^\s+{re.escape(field)}:\s*(.+?)\s*$", match.group("body"), re.MULTILINE)
    if not value:
        return None
    return value.group(1).strip().strip("\"'")


def validate_enum(
    text: str,
    field: str,
    allowed_values: set[str],
    errors: list[str],
) -> None:
    value = scalar_top_level_value(text, field)
    if value is not None and value not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        errors.append(f"{field} must be one of: {allowed}")


def validate_spec_file(spec_path: Path) -> tuple[list[str], list[str]]:
    text = unwrap_aifr_spec(spec_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    fields = top_level_fields(text)
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in fields:
            errors.append(f"missing required top-level field: {field}")

    spec_id = scalar_top_level_value(text, "id")
    if spec_id is not None and not re.match(r"^REQ-[A-Z0-9]+-[0-9]+$", spec_id):
        errors.append("id must match REQ-<DOMAIN>-<NUMBER>, for example REQ-PAY-0012")

    version = scalar_top_level_value(text, "version")
    if version is not None and not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", version):
        errors.append("version must match semantic version format, for example 1.2.0")

    validate_enum(text, "type", ALLOWED_TYPES, errors)
    validate_enum(text, "status", ALLOWED_STATUSES, errors)
    validate_enum(text, "priority", ALLOWED_PRIORITIES, errors)

    change_type = nested_scalar(text, "versioning", "change_type")
    if change_type is not None and change_type not in ALLOWED_CHANGE_TYPES:
        allowed = ", ".join(sorted(ALLOWED_CHANGE_TYPES))
        errors.append(f"versioning.change_type must be one of: {allowed}")

    if "revision_history" in fields and version is not None:
        revision_block = re.search(
            r"^revision_history:\n(?P<body>.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
        if revision_block and f'version: "{version}"' not in revision_block.group("body") and f"version: {version}" not in revision_block.group("body"):
            warnings.append("revision_history should include the current requirement version")

    level = risk_level(text)
    if level is not None and level not in ALLOWED_RISK_LEVELS:
        allowed = ", ".join(sorted(ALLOWED_RISK_LEVELS))
        errors.append(f"risk.level must be one of: {allowed}")

    rule_ids = collect_ids(text, "rules")
    scenario_ids = collect_ids(text, "scenarios")
    acceptance_ids = collect_ids(text, "acceptance_criteria")

    if not rule_ids:
        errors.append("rules must include at least one rule id")
    if not scenario_ids:
        errors.append("scenarios must include at least one scenario id")
    if not acceptance_ids:
        errors.append("acceptance_criteria must include at least one acceptance criterion id")

    for rule_id in rule_ids:
        if not re.match(r"^RULE-[0-9]+$", rule_id):
            errors.append(f"rule id must match RULE-<NUMBER>: {rule_id}")
    for scenario_id in scenario_ids:
        if not re.match(r"^SCN-[0-9]+$", scenario_id):
            errors.append(f"scenario id must match SCN-<NUMBER>: {scenario_id}")
    for acceptance_id in acceptance_ids:
        if not re.match(r"^AC-[0-9]+$", acceptance_id):
            errors.append(f"acceptance criterion id must match AC-<NUMBER>: {acceptance_id}")

    for target in collect_verify_targets(text):
        if target not in rule_ids:
            errors.append(f"acceptance criterion verifies missing rule: {target}")

    for index, block in enumerate(scenario_blocks(text), start=1):
        for field in ("given", "when", "then"):
            if not block_has_non_empty_list(block, field):
                errors.append(f"scenario #{index} missing non-empty {field}")

    if level in {"high", "critical"}:
        if not re.search(r"^non_functional:\n.*^\s+(auditability|security|compliance):", text, re.MULTILINE | re.DOTALL):
            warnings.append(
                "high or critical risk specs should include auditability, security, compliance, or an explicit review control"
            )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="This is a smoke check, not complete schema validation. Apply references/quality-checklist.md manually.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Path to the AIFR spec repository root.",
    )
    parser.add_argument(
        "--spec",
        help="Optional path to an AIFR YAML spec file to quality-check.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors = validate_required_files(root)
    errors.extend(validate_skill_frontmatter(root))
    warnings: list[str] = []

    if args.spec:
        spec_path = Path(args.spec)
        if not spec_path.is_absolute():
            spec_path = root / spec_path
        if not spec_path.is_file():
            errors.append(f"spec file does not exist: {spec_path}")
        else:
            spec_errors, spec_warnings = validate_spec_file(spec_path)
            errors.extend(f"{spec_path.name}: {error}" for error in spec_errors)
            warnings.extend(f"{spec_path.name}: {warning}" for warning in spec_warnings)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    print(f"OK: AIFR smoke check passed at {root}")
    print("NOTE: This is not complete schema validation; apply references/quality-checklist.md manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
