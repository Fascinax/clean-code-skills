"""Validate SKILL.md files against project conventions.

Checks:
- YAML frontmatter with required fields (name, description)
- Required sections (Quick Reference, AI Behavior)
- Code blocks have language identifiers
- H1 title includes language name in parentheses
- File stays under 300 lines (per CONTRIBUTING.md)
- Structural consistency across languages for same category
"""

import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"

REQUIRED_FRONTMATTER_FIELDS = {"name", "description"}

REQUIRED_SECTIONS = {
    "Quick Reference",
    "AI Behavior",
}

LANGUAGES = {"python", "java", "typescript", "javascript"}

CATEGORIES = {"names", "functions", "comments", "general", "tests"}

LANGUAGE_LABELS = {
    "python": "Python",
    "java": "Java",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
}

MAX_LINES = 300

errors: list[str] = []
warnings: list[str] = []


def report_error(path: str, message: str) -> None:
    errors.append(f"ERROR  {path}: {message}")


def report_warning(path: str, message: str) -> None:
    warnings.append(f"WARN   {path}: {message}")


def parse_frontmatter(content: str) -> dict[str, str] | None:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    frontmatter = {}
    for line in match.group(1).strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def check_frontmatter(path: Path, content: str) -> None:
    rel = path.relative_to(SKILLS_DIR.parent)
    frontmatter = parse_frontmatter(content)
    if frontmatter is None:
        report_error(str(rel), "Missing YAML frontmatter (---)")
        return
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter or not frontmatter[field]:
            report_error(str(rel), f"Missing frontmatter field: {field}")


ORCHESTRATOR_SKILLS = {"boy-scout"}


def check_required_sections(path: Path, content: str) -> None:
    rel = path.relative_to(SKILLS_DIR.parent)
    folder_name = path.parent.name
    if folder_name in ORCHESTRATOR_SKILLS:
        return
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in content:
            report_error(str(rel), f"Missing required section: ## {section}")


def check_code_blocks(path: Path, content: str) -> None:
    rel = path.relative_to(SKILLS_DIR.parent)
    code_block_pattern = re.compile(r"^```(\w*)", re.MULTILINE)
    for match in code_block_pattern.finditer(content):
        if not match.group(1):
            line_num = content[:match.start()].count("\n") + 1
            report_warning(
                str(rel), f"Code block at line {line_num} has no language identifier"
            )


def check_h1_title(path: Path, content: str) -> None:
    rel = path.relative_to(SKILLS_DIR.parent)
    folder_name = path.parent.name

    for lang_key, lang_label in LANGUAGE_LABELS.items():
        if folder_name.startswith(f"{lang_key}-clean-"):
            h1_match = re.search(r"^# (.+)$", content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1)
                if f"({lang_label})" not in title and lang_label not in title:
                    report_error(
                        str(rel),
                        f"H1 title should include ({lang_label}), got: # {title}",
                    )
            break


def check_line_count(path: Path, content: str) -> None:
    rel = path.relative_to(SKILLS_DIR.parent)
    line_count = content.count("\n") + 1
    if line_count > MAX_LINES:
        report_warning(
            str(rel),
            f"File has {line_count} lines (max recommended: {MAX_LINES})",
        )


def validate_skill_file(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    check_frontmatter(path, content)
    check_required_sections(path, content)
    check_code_blocks(path, content)
    check_h1_title(path, content)
    check_line_count(path, content)


def check_cross_language_consistency() -> None:
    for category in CATEGORIES:
        lang_sections: dict[str, set[str]] = {}
        for lang in LANGUAGES:
            skill_path = SKILLS_DIR / f"{lang}-clean-{category}" / "SKILL.md"
            if not skill_path.exists():
                report_error(
                    str(skill_path.relative_to(SKILLS_DIR.parent)),
                    f"Missing skill file for {lang}-clean-{category}",
                )
                continue
            content = skill_path.read_text(encoding="utf-8")
            sections = set(re.findall(r"^## (.+)$", content, re.MULTILINE))
            lang_sections[lang] = sections

        if len(lang_sections) < 2:
            continue

        all_sections = set()
        for sections in lang_sections.values():
            all_sections.update(sections)

        for section in sorted(all_sections):
            present_in = [l for l, s in lang_sections.items() if section in s]
            missing_from = [l for l, s in lang_sections.items() if section not in s]
            if missing_from and present_in:
                report_warning(
                    f"*-clean-{category}",
                    f"Section '## {section}' present in {present_in} "
                    f"but missing from {missing_from}",
                )


def main() -> int:
    skill_files = list(SKILLS_DIR.rglob("SKILL.md"))

    if not skill_files:
        print("No SKILL.md files found!")
        return 1

    print(f"Validating {len(skill_files)} skill files...\n")

    for skill_file in sorted(skill_files):
        validate_skill_file(skill_file)

    check_cross_language_consistency()

    for warning in sorted(warnings):
        print(warning)

    for error in sorted(errors):
        print(error)

    print(f"\n{'='*60}")
    print(f"Files scanned: {len(skill_files)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"{'='*60}")

    if errors:
        print("\nValidation FAILED")
        return 1

    print("\nValidation PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
