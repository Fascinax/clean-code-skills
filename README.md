# Clean Code Skills for AI Agents

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-blue)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Languages](https://img.shields.io/badge/Languages-Python%20%7C%20Java%20%7C%20TypeScript%20%7C%20JavaScript-orange)](#whats-included)

**Teach your AI to write code that doesn't suck — in any language.**

This repository contains [Agent Skills](https://agentskills.io) that enforce Robert C. Martin's *Clean Code* principles for **Python, Java, TypeScript, and JavaScript**. They work with Google Antigravity, Anthropic's Claude Code, and any agent that supports the Agent Skills standard.

Each language gets its own set of 6 skills (1 master + 5 category skills), all sharing the same universal Clean Code rules (C1-C5, F1-F4, G1-G36, N1-N7, T1-T9) while adding language-specific idioms and modern features.

## Why?

AI generates code fast, but research shows it also generates technical debt fast:

- **GitClear**: 4x increase in code duplication with AI adoption
- **Carnegie Mellon**: +30% static analysis warnings, +41% code complexity after Cursor adoption
- **Google DORA**: Negative relationship between AI adoption and software delivery stability

These skills encode battle-tested solutions to exactly these problems—directly into your AI workflow.

## What's Included

### Overview

| Language | Master Skill | Category Skills | Language-Specific Rules |
|----------|-------------|-----------------|------------------------|
| **Python** | `python-clean-code` | `python-clean-names`, `python-clean-functions`, `python-clean-comments`, `python-clean-general`, `python-clean-tests` | P1-P3 |
| **Java** | `java-clean-code` | `java-clean-names`, `java-clean-functions`, `java-clean-comments`, `java-clean-general`, `java-clean-tests` | J1-J10 |
| **TypeScript** | `typescript-clean-code` | `typescript-clean-names`, `typescript-clean-functions`, `typescript-clean-comments`, `typescript-clean-general`, `typescript-clean-tests` | TS1-TS8 |
| **JavaScript** | `javascript-clean-code` | `javascript-clean-names`, `javascript-clean-functions`, `javascript-clean-comments`, `javascript-clean-general`, `javascript-clean-tests` | JS1-JS7 |

Plus the language-agnostic **`boy-scout`** orchestrator that coordinates all skills.

### Skills by Category

| Skill Category | Description | Rules |
|----------------|-------------|-------|
| `{lang}-clean-code` | **Master skill** with all rules for the language | C1-C5, E1-E2, F1-F4, G1-G36, N1-N7, T1-T9 + language-specific |
| `{lang}-clean-names` | Descriptive, unambiguous naming | N1-N7 |
| `{lang}-clean-functions` | Small, focused, obvious functions | F1-F4 |
| `{lang}-clean-comments` | Minimal, accurate commenting | C1-C5 |
| `{lang}-clean-general` | Core principles (DRY, single responsibility) | G5, G16, G23, G25, G30, G36 |
| `{lang}-clean-tests` | Fast, thorough, boundary-aware tests | T1-T9 |
| `boy-scout` | **Orchestrator** — always leave code cleaner | Coordinates all skills |

### Language-Specific Rules

Each language extends the universal Clean Code catalog with idiomatic rules:

#### Python (P1-P3)

- P1: No wildcard imports — P2: Use Enums — P3: Type hints on public interfaces

#### Java (J1-J10)

- J1: Records for data classes — J2: Sealed classes — J3: Pattern matching in switch — J4: Optional, never null — J5: Text blocks — J6: Virtual threads — J7: Google Java Style — J8: Always `@Override` — J9: Enums not integer constants — J10: Javadoc for public APIs

#### TypeScript (TS1-TS8)

- TS1: `unknown` over `any` — TS2: `type` over `interface` — TS3: Discriminated unions — TS4: `as const satisfies` — TS5: `readonly` for immutability — TS6: `import type` — TS7: Descriptive generics — TS8: `@ts-expect-error` over `@ts-ignore`

#### JavaScript (JS1-JS7)

- JS1: `const` by default, never `var` — JS2: Object destructuring — JS3: async/await — JS4: ES6+ classes — JS5: Functional patterns — JS6: `===` strict equality — JS7: Default parameters

Use the master skill for comprehensive coverage, or individual skills for targeted enforcement.

### The Boy Scout Rule

The `boy-scout` skill embodies Clean Code's core philosophy:

> "Always check a module in cleaner than when you checked it out."

You don't have to make code perfect—just **a little bit better** with every touch. The `boy-scout` skill orchestrates the others, ensuring every code interaction leaves a trail of small improvements.

---

## Installation

### Google Antigravity

**Project-specific** (applies to one project):

```bash
# From your project root
mkdir -p .agent/skills
cp -r skills/* .agent/skills/
```

**Global** (applies to all projects):

```bash
mkdir -p ~/.gemini/antigravity/skills
cp -r skills/* ~/.gemini/antigravity/skills/
```

**Quick install** (global, one command):

```bash
git clone https://github.com/ertugrul-dmr/clean-code-skills.git /tmp/clean-code-skills && \
mkdir -p ~/.gemini/antigravity/skills && \
cp -r /tmp/clean-code-skills/skills/* ~/.gemini/antigravity/skills/ && \
rm -rf /tmp/clean-code-skills
```

### Anthropic Claude Code

**Project-specific**:

```bash
# From your project root
mkdir -p .claude/skills
cp -r skills/* .claude/skills/
```

**Global**:

```bash
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

**Quick install** (global, one command):

```bash
git clone https://github.com/ertugrul-dmr/clean-code-skills.git /tmp/clean-code-skills && \
mkdir -p ~/.claude/skills && \
cp -r /tmp/clean-code-skills/skills/* ~/.claude/skills/ && \
rm -rf /tmp/clean-code-skills
```

### Other Agent Skills-Compatible Tools

The skills follow the [Agent Skills](https://agentskills.io) open standard. Check your tool's documentation for the skills directory location, then copy the `skills/` folder contents there.

---

## Usage

Once installed, skills activate automatically based on context. Ask your agent to:

- **Write code**: "Create a user authentication module" → Skills enforce clean patterns
- **Review code**: "Review this function for issues" → Agent identifies violations by rule number
- **Refactor**: "Refactor this to be cleaner" → Agent applies all relevant rules

### Example

**Before** (10 violations):

```python
from utils import *  # P1

# Author: John, Modified: 2024-01-15  # C1
def proc(d, t, flag=False):  # N1, F1, F3
    # Process the data  # C3
    x = []  # N1
    for i in d:
        if flag:  # F3
            if i['type'] == 'A':  # G23
                x.append(i['val'] * 1.0825)  # G25
            elif i['type'] == 'B':
                x.append(i['val'] * 1.05)  # G25
        else:
            x.append(i['val'])
    return x
```

**After** (with skills active):

```python
import json
from dataclasses import dataclass
from typing import Literal

TAX_RATE_CA = 0.0825
TAX_RATE_NY = 0.05
TransactionType = Literal['CA', 'NY']

@dataclass
class Transaction:
    value: float
    type: TransactionType

def apply_tax(transaction: Transaction) -> float:
    """Apply state-specific tax to transaction value."""
    tax_rates = {'CA': TAX_RATE_CA, 'NY': TAX_RATE_NY}
    return transaction.value * (1 + tax_rates[transaction.type])

def process_transactions_with_tax(transactions: list[Transaction]) -> list[float]:
    """Calculate taxed values for all transactions."""
    return [apply_tax(t) for t in transactions]

def process_transactions_without_tax(transactions: list[Transaction]) -> list[float]:
    """Extract raw values from all transactions."""
    return [t.value for t in transactions]
```

---

## Rule Reference

### Comments (C1-C5)

| Rule | Principle |
|------|-----------|
| C1 | No metadata in comments (use Git) |
| C2 | Delete obsolete comments immediately |
| C3 | No redundant comments |
| C4 | Write comments well if you must |
| C5 | Never commit commented-out code |

### Functions (F1-F4)

| Rule | Principle |
|------|-----------|
| F1 | Maximum 3 arguments |
| F2 | No output arguments |
| F3 | No flag arguments |
| F4 | Delete dead functions |

### General (G1-G36)

| Rule | Principle |
|------|-----------|
| G1 | One language per file |
| G2 | Implement expected behavior |
| G3 | Handle boundary conditions |
| G4 | Don't override safeties |
| G5 | DRY—no duplication |
| G6 | Consistent abstraction levels |
| G7 | Base classes don't know children |
| G8 | Minimize public interface |
| G9 | Delete dead code |
| G10 | Variables near usage |
| G11 | Be consistent |
| G12 | Remove clutter |
| G13 | No artificial coupling |
| G14 | No feature envy |
| G15 | No selector arguments |
| G16 | No obscured intent |
| G17 | Code where expected |
| G18 | Prefer instance methods |
| G19 | Use explanatory variables |
| G20 | Function names say what they do |
| G21 | Understand the algorithm |
| G22 | Make dependencies physical |
| G23 | Polymorphism over if/else |
| G24 | Follow conventions (PEP 8 / Google Java Style / ESLint) |
| G25 | Named constants, not magic numbers |
| G26 | Be precise |
| G27 | Structure over convention |
| G28 | Encapsulate conditionals |
| G29 | Avoid negative conditionals |
| G30 | Functions do one thing |
| G31 | Make temporal coupling explicit |
| G32 | Don't be arbitrary |
| G33 | Encapsulate boundary conditions |
| G34 | One abstraction level per function |
| G35 | Config at high levels |
| G36 | Law of Demeter (one dot) |

### Names (N1-N7)

| Rule | Principle |
|------|-----------|
| N1 | Choose descriptive names |
| N2 | Names at appropriate abstraction level |
| N3 | Use standard nomenclature |
| N4 | Unambiguous names |
| N5 | Name length matches scope |
| N6 | No encodings (no Hungarian notation) |
| N7 | Names describe side effects |

### Python-Specific (P1-P3)

| Rule | Principle |
|------|-----------|
| P1 | No wildcard imports |
| P2 | Use Enums, not magic constants |
| P3 | Type hints on public interfaces |

### Java-Specific (J1-J10)

| Rule | Principle |
|------|----------|
| J1 | Use `record` for immutable data classes |
| J2 | Use sealed classes/interfaces for restricted hierarchies |
| J3 | Use pattern matching in `switch` |
| J4 | Use `Optional` return types — never return null |
| J5 | Use text blocks for multi-line strings |
| J6 | Use virtual threads for I/O-bound concurrency |
| J7 | Follow Google Java Style |
| J8 | Always use `@Override` |
| J9 | Use enums, not integer constants |
| J10 | Javadoc for all public APIs |

### TypeScript-Specific (TS1-TS8)

| Rule | Principle |
|------|----------|
| TS1 | Use `unknown` over `any` — always narrow types |
| TS2 | Prefer `type` over `interface` |
| TS3 | Use discriminated unions for exhaustive pattern matching |
| TS4 | Prefer `as const satisfies` for const assertions |
| TS5 | Use `readonly` and `ReadonlyArray` for immutability |
| TS6 | Use `import type` for type-only imports |
| TS7 | Name generics descriptively (`TRequest`, not `T`) |
| TS8 | Use `@ts-expect-error` over `@ts-ignore` |

### JavaScript-Specific (JS1-JS7)

| Rule | Principle |
|------|----------|
| JS1 | Use `const` by default, `let` when needed — never `var` |
| JS2 | Use object destructuring for function arguments |
| JS3 | Prefer async/await over Promises over callbacks |
| JS4 | Use ES6+ class syntax over prototype manipulation |
| JS5 | Favor functional patterns (map/filter/reduce) |
| JS6 | Use `===` strict equality — never `==` |
| JS7 | Use default parameters instead of short-circuiting |

### Tests (T1-T9)

| Rule | Principle |
|------|-----------|
| T1 | Test everything that could break |
| T2 | Use coverage tools |
| T3 | Don't skip trivial tests |
| T4 | Ignored test = ambiguity question |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Look for patterns in failures |
| T8 | Check coverage when debugging |
| T9 | Tests must be fast (<100ms) |

---

## Customization

### Using Individual Skills

Don't need all 66 rules? Copy only the skills you want:

```bash
# Just Java skills
cp -r skills/java-clean-* ~/.gemini/antigravity/skills/

# Just TypeScript function rules
cp -r skills/typescript-clean-functions ~/.claude/skills/

# Just the orchestrator + one language
cp -r skills/boy-scout skills/python-clean-* ~/.claude/skills/
```

### Extending Skills

Add your own rules by editing the `SKILL.md` files or creating new skill folders:

```text
skills/
├── boy-scout/                      # Orchestrator (all languages)
│   └── SKILL.md
├── python-clean-code/              # Python master
│   └── SKILL.md
├── python-clean-names/
│   └── SKILL.md
├── java-clean-code/                # Java master
│   └── SKILL.md
├── java-clean-names/
│   └── SKILL.md
├── typescript-clean-code/          # TypeScript master
│   └── SKILL.md
├── javascript-clean-code/          # JavaScript master
│   └── SKILL.md
│   ... (5 category skills per language)
└── my-team-standards/              # Your custom skill
    └── SKILL.md
```

### Adding Enforcement Scripts

For stricter enforcement, add a `scripts/` folder with linters the agent can run:

```text
skills/python-clean-code/
├── SKILL.md
└── scripts/
    └── lint.py
```

---

## How Skills Work

Skills use **Progressive Disclosure**:

1. **Discovery**: Agent sees only skill names and descriptions
2. **Activation**: When your request matches a description, full instructions load
3. **Execution**: Scripts and templates load only when needed

This keeps the agent fast—it's not thinking about database migrations when you're writing a React component.

---

## Contributing

PRs welcome! Some ideas:

- [x] ~~Additional language support~~ — Java, TypeScript, JavaScript added!
- [ ] Additional language support (Go, Rust, C#)
- [ ] SOLID principles as dedicated skills
- [ ] Framework-specific skills (React, Angular, Spring Boot)
- [ ] Integration tests
- [ ] Pre-commit hooks
- [ ] IDE extensions

---

## Resources

### Books

- [*Clean Code*](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) by Robert C. Martin
- [*Effective Java* (3rd Edition)](https://www.amazon.com/Effective-Java-Joshua-Bloch/dp/0134685997) by Joshua Bloch

### Clean Code Repos (sources for language skills)

- [clean-code-python](https://github.com/zedr/clean-code-python) — Python clean code guide adapted from Robert C. Martin's book (4.8k+ stars)
- [clean-code-javascript](https://github.com/ryanmcdermott/clean-code-javascript) — JavaScript clean code guide by Ryan McDermott
- [clean-code-typescript](https://github.com/labs42io/clean-code-typescript) — TypeScript adaptation by labs42io
- [TypeScript Style Guide](https://github.com/mkosir/typescript-style-guide) — Modern opinionated TS conventions by Marko Kosir
- [clean-code-java](https://github.com/leonardolemie/clean-code-java) — Java adaptation by Leonardo Lemie
- [python-patterns](https://github.com/faif/python-patterns) — A collection of design patterns and idioms in Python (42.8k+ stars)

### Style Guides & Standards

- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) — Formatting, naming, Javadoc conventions
- [Java Clean Code: Modern Practices for 2025](https://atruedev.com/blog/java-clean-code) — Records, sealed classes, virtual threads
- [The Hitchhiker's Guide to Python — Code Style](https://docs.python-guide.org/writing/style/) — PEP 8, idioms, and conventions
- [quantifiedcode/python-anti-patterns](https://github.com/quantifiedcode/python-anti-patterns) — Categorized Python anti-patterns book

### Tools & Platforms

- [Agent Skills Standard](https://agentskills.io)
- [Antigravity Documentation](https://developers.google.com/antigravity)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

*The future of programming is human intent translated by AI. Make sure the translation preserves quality, not just speed.*
