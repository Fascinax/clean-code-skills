---
name: boy-scout
description: Use when fixing, editing, changing, debugging, or working with any Python, Java, TypeScript, JavaScript, Go, Rust, C# code. Applies the Boy Scout Rule—always leave code cleaner than you found it. Orchestrates other clean code skills as needed.
---

# The Boy Scout Rule

> "Always leave the campground cleaner than you found it."
> — Robert Baden-Powell
>
> "Always check a module in cleaner than when you checked it out."
> — Robert C. Martin, *Clean Code*

## The Philosophy

You don't have to make every module perfect. You simply have to make it **a little bit better** than when you found it.

If we all followed this simple rule:

- Our systems would gradually get better as they evolved
- Teams would care for the system as a whole
- The relentless deterioration of software would end

## When Working on Code

Every time you touch code, look for **at least one small improvement**:

### Quick Wins (Do These Immediately)

- Rename a poorly named variable → triggers language-specific `clean-names`
- Delete a redundant comment → triggers language-specific `clean-comments`
- Remove dead code or unused imports
- Replace a magic number with a named constant
- Extract a deeply nested block into a well-named function

### Deeper Improvements (When Time Allows)

- Split a function that does multiple things → triggers language-specific `clean-functions`
- Remove duplication (DRY) → triggers language-specific `clean-general`
- Add missing boundary checks
- Improve test coverage → triggers language-specific `clean-tests`

## The Rule in Practice

```python
# You're asked to fix a bug in this function:
def proc(d, x, flag=False):
    # process data
    for i in d:
        if i > 0:
            if flag:
                x.append(i * 1.0825)  # tax
            else:
                x.append(i)
    return x

# Don't just fix the bug and leave.
# Leave it cleaner:
TAX_RATE = 0.0825

def process_positive_values(
    values: list[float],
    apply_tax: bool = False
) -> list[float]:
    """Filter positive values, optionally applying tax."""
    rate = 1 + TAX_RATE if apply_tax else 1
    return [v * rate for v in values if v > 0]
```

**What changed:**

- ✅ Descriptive function name (N1)
- ✅ Clear parameter names (N1)
- ✅ Type hints (P3)
- ✅ Named constant for magic number (G25)
- ✅ No output argument mutation (F2)
- ✅ Useful docstring (C4)

## Skill Orchestration

This skill coordinates with specialized skills based on what you're doing and the language:

### Python

| Task | Trigger Skill |
|------|---------------|
| Writing/reviewing any Python | `python-clean-code` (master) |
| Naming variables, functions, classes | `python-clean-names` |
| Writing or editing comments | `python-clean-comments` |
| Creating or refactoring functions | `python-clean-functions` |
| Reviewing code quality | `python-clean-general` |
| Writing or reviewing tests | `python-clean-tests` |

### Java

| Task | Trigger Skill |
|------|---------------|
| Writing/reviewing any Java | `java-clean-code` (master) |
| Naming variables, methods, classes | `java-clean-names` |
| Writing or editing comments/Javadoc | `java-clean-comments` |
| Creating or refactoring methods | `java-clean-functions` |
| Reviewing code quality | `java-clean-general` |
| Writing or reviewing tests | `java-clean-tests` |

### TypeScript

| Task | Trigger Skill |
|------|---------------|
| Writing/reviewing any TypeScript | `typescript-clean-code` (master) |
| Naming variables, functions, types | `typescript-clean-names` |
| Writing or editing comments/TSDoc | `typescript-clean-comments` |
| Creating or refactoring functions | `typescript-clean-functions` |
| Reviewing code quality | `typescript-clean-general` |
| Writing or reviewing tests | `typescript-clean-tests` |

### JavaScript

| Task | Trigger Skill |
|------|---------------|
| Writing/reviewing any JavaScript | `javascript-clean-code` (master) |
| Naming variables, functions, classes | `javascript-clean-names` |
| Writing or editing comments/JSDoc | `javascript-clean-comments` |
| Creating or refactoring functions | `javascript-clean-functions` |
| Reviewing code quality | `javascript-clean-general` |
| Writing or reviewing tests | `javascript-clean-tests` |

### Go

| Task | Trigger Skill |
|------|---------------|
| Writing/reviewing any Go | `go-clean-code` (master) |
| Naming variables, functions, types | `go-clean-names` |
| Writing or editing comments/godoc | `go-clean-comments` |
| Creating or refactoring functions | `go-clean-functions` |
| Reviewing code quality | `go-clean-general` |
| Writing or reviewing tests | `go-clean-tests` |

### Rust

| Task | Trigger Skill |
|------|---------------|
| Writing/reviewing any Rust | `rust-clean-code` (master) |
| Naming variables, functions, types | `rust-clean-names` |
| Writing or editing comments/rustdoc | `rust-clean-comments` |
| Creating or refactoring functions | `rust-clean-functions` |
| Reviewing code quality | `rust-clean-general` |
| Writing or reviewing tests | `rust-clean-tests` |

### C\#

| Task | Trigger Skill |
|------|---------------|
| Writing/reviewing any C# | `csharp-clean-code` (master) |
| Naming variables, methods, types | `csharp-clean-names` |
| Writing or editing comments/XML docs | `csharp-clean-comments` |
| Creating or refactoring methods | `csharp-clean-functions` |
| Reviewing code quality | `csharp-clean-general` |
| Writing or reviewing tests | `csharp-clean-tests` |

## The Mindset

**Don't:**

- Leave code worse than you found it
- Say "that's not my code"
- Wait for a dedicated refactoring sprint
- Make massive changes unrelated to your task

**Do:**

- Make one small improvement with every commit
- Fix what you see, even if you didn't break it
- Keep changes proportional to your task
- Leave a trail of quality improvements

## AI Behavior

> **CRITICAL**: Loading a master `{lang}-clean-code` skill is NOT sufficient on its own. The master skill provides a summary reference, but the sub-skills contain the detailed rules, examples, and anti-patterns that drive enforcement. You MUST load ALL sub-skills every time — no exceptions, no shortcuts.

When working on code:

1. Detect the language (Python, Java, TypeScript, JavaScript, Go, Rust, C#)
2. Complete the requested task first
3. MUST read and load the `{lang}-clean-code` master skill — it will instruct you to load all sub-skills
4. MUST ALSO read and load EVERY sub-skill for the detected language, regardless of what was touched:
   - `{lang}-clean-names` — apply N1-N7 to all names
   - `{lang}-clean-functions` — apply F1-F4 to all functions/methods
   - `{lang}-clean-comments` — apply C1-C5 to all comments/docs
   - `{lang}-clean-general` — apply G1-G36 for code quality
   - `{lang}-clean-tests` — apply T1-T9 to all tests
5. Apply every loaded skill's rules and flag each violation with its rule number
6. Note every improvement made (e.g., "Also cleaned up: renamed `x` to `results` — N1")

**Do not cherry-pick sub-skills.** Even if you only changed a function name, load all 5 sub-skills — a name change may reveal a comment violation, a function length issue, or a missing test.

When reviewing code:

1. MUST load and read `{language}-clean-code` master skill first
2. MUST load and read ALL 5 sub-skills: `{lang}-clean-names`, `{lang}-clean-functions`, `{lang}-clean-comments`, `{lang}-clean-general`, `{lang}-clean-tests`
3. Do NOT proceed with the review until all 6 skills (1 master + 5 sub-skills) are loaded
4. Flag each violation by rule number (e.g., "N1: variable `x` should be `results`")
5. Suggest incremental improvements, not complete rewrites

## The Boy Scout Promise

Every piece of code you touch gets a little better. Not perfect—just better.

Over time, better compounds into excellent.
