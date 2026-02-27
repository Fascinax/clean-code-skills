# Contributing to Clean Code Skills

Thanks for your interest in contributing! This project teaches AI agents to write clean code, and contributions help make that better for everyone.

## How to Contribute

### Adding a New Language

1. Create 6 skill files following the existing pattern:
   - `skills/{lang}-clean-code/SKILL.md` — Master reference (all rules)
   - `skills/{lang}-clean-names/SKILL.md` — N1-N7 with language examples
   - `skills/{lang}-clean-functions/SKILL.md` — F1-F4 with language examples
   - `skills/{lang}-clean-comments/SKILL.md` — C1-C5 with language examples
   - `skills/{lang}-clean-general/SKILL.md` — G5, G16, G23, G25, G30, G36 with language examples
   - `skills/{lang}-clean-tests/SKILL.md` — T1-T9 with language examples

2. Each `SKILL.md` must include:
   - YAML frontmatter with `name` and `description`
   - Bad/Good code example pairs
   - A Quick Reference table
   - An AI Behavior section
   - Language-specific rules (e.g., `GO1-GO5` for Go)

3. Update the `boy-scout` skill orchestration table with the new language.

4. Update `README.md` with the new language in the overview table.

### Improving Existing Skills

- **Add Modern Idioms**: If a language has new features (e.g., Python 3.12+ features), add examples in a "Modern {Language} Idioms" section.
- **Fix bugs**: Code examples should be correct and runnable.
- **Add missing sections**: Use Java/TypeScript/JavaScript skills as the reference template for structural consistency.

### Skill File Structure

Every category skill should follow this structure:

```
---
name: {lang}-clean-{category}
description: Use when... (trigger conditions for the AI)
---

# Clean {Category} ({Language})

## Rule sections (e.g., F1, F2, F3, F4)
Each with Bad/Good code pairs

## Modern {Language} {Category} Idioms (optional)
Language-specific modern patterns

## Quick Reference
Summary table of rules

## AI Behavior
Instructions for how the AI should use this skill
```

### Quality Checklist

Before submitting a PR, verify:

- [ ] YAML frontmatter has `name` and `description`
- [ ] All code examples use the correct language
- [ ] Bad/Good pairs are clearly marked
- [ ] Quick Reference table is present
- [ ] AI Behavior section is present
- [ ] No commented-out code in examples (C5!)
- [ ] Rule numbers match the Clean Code catalog (C1-C5, F1-F4, G1-G36, N1-N7, T1-T9)

## Style Guide

- Use fenced code blocks with language identifiers (` ```python`, ` ```java`, etc.)
- Mark bad examples with `// Bad` or `# Bad` comments
- Mark good examples with `// Good` or `# Good` comments
- Keep SKILL.md files under 300 lines
- Use `❌` / `✅` in anti-pattern tables (master skills only)

## Reporting Issues

- **Wrong code example**: Open an issue with the file path and the specific error
- **Missing rule**: Open an issue describing which rule is missing and for which language
- **Structural inconsistency**: Open an issue describing the discrepancy between languages

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
