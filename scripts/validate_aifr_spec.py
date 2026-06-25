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
    "references/update-ledger.md",
    "references/source-snapshot.md",
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
    "implementation",
    "risk",
    "non_functional",
]

ALLOWED_TYPES = {"functional", "non_functional", "constraint", "interface", "data"}
ALLOWED_STATUSES = {"draft", "review", "approved", "deprecated", "superseded"}
ALLOWED_PRIORITIES = {"low", "medium", "high", "critical"}
ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}
ALLOWED_CHANGE_TYPES = {"initial", "patch", "minor", "major", "deprecated", "needs_review"}
ALLOWED_IMPLEMENTATION_STATUSES = {"not_started", "partial", "implemented", "verified"}


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
    body = section_body(text, section)
    if body is None:
        return None
    value = re.search(rf"^\s+{re.escape(field)}:\s*(.+?)\s*$", body, re.MULTILINE)
    if not value:
        return None
    return value.group(1).strip().strip("\"'")


def section_body(text: str, section: str) -> str | None:
    match = re.search(
        rf"^{re.escape(section)}:\n(?P<body>.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    return match.group("body")


def nested_block_body(text: str, section: str, field: str) -> str | None:
    parent_body = section_body(text, section)
    if parent_body is None:
        return None
    match = re.search(
        rf"^\s{{2}}{re.escape(field)}:\s*\n(?P<body>.*?)(?=^\s{{2}}[A-Za-z_][A-Za-z0-9_]*:|^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
        parent_body,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None
    return match.group("body")


def collect_nested_values(text: str, section: str, field: str) -> list[str]:
    body = section_body(text, section)
    if body is None:
        return []
    return [match.group(1) for match in re.finditer(rf"^\s+{re.escape(field)}:\s*([A-Za-z0-9_-]+)\s*$", body, re.MULTILINE)]


def validate_trace_tests_shape(text: str, warnings: list[str]) -> None:
    tests_body = nested_block_body(text, "trace", "expected_tests")
    if tests_body is None:
        return
    if re.search(r"^\s{4}-\s+\S", tests_body, re.MULTILINE):
        warnings.append("trace.expected_tests should separate planned and implemented tests instead of using a flat list")
        return
    if not re.search(r"^\s+planned:\s*(?:\[\])?\s*(?:\n|$)", tests_body, re.MULTILINE):
        warnings.append("trace.expected_tests should include planned")
    if not re.search(r"^\s+implemented:\s*(?:\[\])?\s*(?:\n|$)", tests_body, re.MULTILINE):
        warnings.append("trace.expected_tests should include implemented")


def validate_reused_endpoint_authorization(text: str, warnings: list[str]) -> None:
    interface_body = section_body(text, "interfaces")
    if interface_body is None or "reuse_existing_endpoint: true" not in interface_body:
        return
    for block in re.split(r"(?=^\s*-\s+)", interface_body, flags=re.MULTILINE):
        if "reuse_existing_endpoint: true" in block and "authorization_source:" not in block:
            warnings.append("interfaces.apis entries with reuse_existing_endpoint: true should identify authorization_source")


def validate_implementation_coverage(text: str, rule_ids: list[str], acceptance_ids: list[str], errors: list[str], warnings: list[str]) -> None:
    implementation_body = section_body(text, "implementation")
    if implementation_body is None:
        return

    status = nested_scalar(text, "implementation", "status")
    if status is None:
        errors.append("implementation.status is required")
    elif status not in ALLOWED_IMPLEMENTATION_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_IMPLEMENTATION_STATUSES))
        errors.append(f"implementation.status must be one of: {allowed}")

    for rule_id in collect_nested_values(text, "implementation", "rule_id"):
        if rule_id not in rule_ids:
            errors.append(f"implementation.rule_coverage references missing rule: {rule_id}")
    for acceptance_id in collect_nested_values(text, "implementation", "acceptance_criterion_id"):
        if acceptance_id not in acceptance_ids:
            errors.append(f"implementation.acceptance_coverage references missing acceptance criterion: {acceptance_id}")

    if status == "verified" and not re.search(r"verification|verified_by|commands:", implementation_body):
        warnings.append("implementation.status verified should include verification evidence such as commands or verified_by")


def relative_posix(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def discover_spec_files(root: Path) -> list[Path]:
    direct_root = root / "aifr" / "requirements" / "items"
    if direct_root.is_dir():
        return sorted(direct_root.glob("**/spec.aifr.yaml"))
    return sorted(root.glob("**/aifr/requirements/items/**/spec.aifr.yaml"))


def project_root_for_spec(spec_path: Path) -> Path:
    parts = spec_path.resolve().parts
    for index in range(len(parts) - 1, -1, -1):
        if parts[index] == "aifr":
            return Path(*parts[:index])
    return spec_path.parent


def collect_list_ids_unique(ids: list[str], label: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item_id in ids:
        if item_id in seen:
            errors.append(f"duplicate {label} id: {item_id}")
        seen.add(item_id)
    return errors


def parse_index_entries(index_path: Path) -> list[dict[str, str]]:
    if not index_path.is_file():
        return []
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in index_path.read_text(encoding="utf-8").splitlines():
        start = re.match(r"^\s*-\s+id:\s*(.+?)\s*$", line)
        if start:
            if current:
                entries.append(current)
            current = {"id": start.group(1).strip().strip("\"'")}
            continue
        if current is None:
            continue
        field = re.match(r"^\s+([A-Za-z_][A-Za-z0-9_]*):\s*(.+?)\s*$", line)
        if field:
            current[field.group(1)] = field.group(2).strip().strip("\"'")
    if current:
        entries.append(current)
    return entries


def validate_update_ledger(project_root: Path, spec_path: Path, body: str) -> list[str]:
    errors: list[str] = []
    previous_version = nested_scalar(body, "versioning", "previous_version")
    current_version = scalar_top_level_value(body, "version")
    spec_id = scalar_top_level_value(body, "id")
    change_type = nested_scalar(body, "versioning", "change_type")
    if not previous_version or previous_version in {"null", "None"} or not current_version:
        return errors

    ledger_path = spec_path.parent / "changes" / f"v{current_version}.aifr-update.yaml"
    if not ledger_path.is_file():
        errors.append(f"{relative_posix(project_root, spec_path)}: missing update ledger: {relative_posix(project_root, ledger_path)}")
        return errors

    ledger = ledger_path.read_text(encoding="utf-8")
    ledger_id = nested_scalar(ledger, "version_update", "requirement_id")
    from_version = nested_scalar(ledger, "version_update", "from_version")
    to_version = nested_scalar(ledger, "version_update", "to_version")
    recommended_bump = nested_scalar(ledger, "version_update", "recommended_bump")
    for section in ("version_update", "change_set", "impact_analysis"):
        if not re.search(rf"^{section}:\s*$", ledger, re.MULTILINE):
            errors.append(f"{relative_posix(project_root, ledger_path)}: missing required ledger section: {section}")
    if ledger_id != spec_id:
        errors.append(f"{relative_posix(project_root, ledger_path)}: version_update.requirement_id must equal spec id {spec_id}")
    if from_version != previous_version:
        errors.append(f"{relative_posix(project_root, ledger_path)}: version_update.from_version must equal spec previous_version {previous_version}")
    if to_version != current_version:
        errors.append(f"{relative_posix(project_root, ledger_path)}: version_update.to_version must equal spec version {current_version}")
    if recommended_bump and change_type and recommended_bump != change_type and recommended_bump != "needs_review":
        errors.append(
            f"{relative_posix(project_root, ledger_path)}: recommended_bump must equal versioning.change_type {change_type} or needs_review"
        )
    return errors


def validate_strict_project(project_root: Path, spec_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    records: dict[str, dict[str, str]] = {}

    for spec_path in spec_paths:
        if spec_path is None or not spec_path.is_file():
            continue
        body = unwrap_aifr_spec(spec_path.read_text(encoding="utf-8"))
        spec_id = scalar_top_level_value(body, "id")
        version = scalar_top_level_value(body, "version")
        title = scalar_top_level_value(body, "title")
        status = scalar_top_level_value(body, "status")
        primary_domain = nested_scalar(body, "identity", "primary_domain")
        domain_path = nested_scalar(body, "identity", "domain_path")
        frozen_slug = nested_scalar(body, "identity", "frozen_slug")
        canonical_path = nested_scalar(body, "identity", "canonical_path")
        relative_path = relative_posix(project_root, spec_path)

        if spec_id in records:
            errors.append(f"duplicate requirement id {spec_id}: {records[spec_id]['path']} and {relative_path}")
        if spec_id:
            records[spec_id] = {
                "id": spec_id,
                "version": version or "",
                "title": title or "",
                "status": status or "",
                "domain": primary_domain or "",
                "domain_path": domain_path or "",
                "path": relative_path,
            }

        parent_name = spec_path.parent.name
        if spec_id and not parent_name.startswith(f"{spec_id}--"):
            errors.append(f"{relative_path}: directory id must match aifr_spec.id {spec_id}")
        if frozen_slug and spec_id and parent_name != f"{spec_id}--{frozen_slug}":
            errors.append(f"{relative_path}: directory slug must match identity.frozen_slug")
        actual_domain_path = spec_path.parent.parent.name
        if domain_path and domain_path != actual_domain_path:
            errors.append(f"{relative_path}: identity.domain_path must match path domain {actual_domain_path}")
        if canonical_path and canonical_path != relative_path:
            errors.append(f"{relative_path}: identity.canonical_path must match actual path")
        if primary_domain and spec_id:
            id_domain = spec_id.split("-")[1]
            if primary_domain != id_domain:
                errors.append(f"{relative_path}: identity.primary_domain must match id domain {id_domain}")

        revision_block = re.search(
            r"^revision_history:\n(?P<body>.*?)(?=^[A-Za-z_][A-Za-z0-9_]*:|\Z)",
            body,
            re.MULTILINE | re.DOTALL,
        )
        if version and (not revision_block or (f'version: "{version}"' not in revision_block.group("body") and f"version: {version}" not in revision_block.group("body"))):
            errors.append(f"{relative_path}: revision_history must include current version {version}")

        errors.extend(f"{relative_path}: {error}" for error in collect_list_ids_unique(collect_ids(body, "rules"), "rule"))
        errors.extend(f"{relative_path}: {error}" for error in collect_list_ids_unique(collect_ids(body, "scenarios"), "scenario"))
        errors.extend(
            f"{relative_path}: {error}" for error in collect_list_ids_unique(collect_ids(body, "acceptance_criteria"), "acceptance criterion")
        )
        errors.extend(validate_update_ledger(project_root, spec_path, body))

    index_path = project_root / "aifr" / "indexes" / "requirements.aifr-index.yaml"
    index_entries = parse_index_entries(index_path)
    for entry in index_entries:
        spec = records.get(entry.get("id", ""))
        entry_label = f"{relative_posix(project_root, index_path)} entry {entry.get('id', '<missing id>')}"
        if not spec:
            errors.append(f"{entry_label}: id has no matching spec")
            continue
        comparisons = {
            "title": spec["title"],
            "version": spec["version"],
            "status": spec["status"],
            "domain": spec["domain"],
            "path": spec["path"],
        }
        for field, expected in comparisons.items():
            if entry.get(field, "") != expected:
                errors.append(f"{entry_label}: {field} must be {expected!r}, got {entry.get(field, '')!r}")
    return errors


def validate_strict_repository(root: Path, target_spec: Path | None = None) -> list[str]:
    if target_spec:
        return validate_strict_project(project_root_for_spec(target_spec), [target_spec])

    grouped: dict[Path, list[Path]] = {}
    for spec_path in discover_spec_files(root):
        grouped.setdefault(project_root_for_spec(spec_path), []).append(spec_path)

    errors: list[str] = []
    for project_root, spec_paths in sorted(grouped.items(), key=lambda item: item[0].as_posix()):
        errors.extend(validate_strict_project(project_root, spec_paths))
    return errors


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
    validate_trace_tests_shape(text, warnings)
    validate_reused_endpoint_authorization(text, warnings)
    validate_implementation_coverage(text, rule_ids, acceptance_ids, errors, warnings)

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
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Run cross-file consistency checks for specs, indexes, ids, paths, and update ledgers.",
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
    else:
        spec_path = None

    if args.strict:
        errors.extend(validate_strict_repository(root, spec_path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    check_name = "strict consistency check" if args.strict else "smoke check"
    print(f"OK: AIFR {check_name} passed at {root}")
    if not args.strict:
        print("NOTE: This is not complete schema validation; apply references/quality-checklist.md manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
