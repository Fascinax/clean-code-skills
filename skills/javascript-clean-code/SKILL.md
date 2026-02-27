---
name: javascript-clean-code
description: Use when writing, fixing, editing, reviewing, or refactoring any JavaScript code. Enforces Robert Martin's complete Clean Code catalog—naming, functions, comments, DRY, and boundary conditions—adapted for JavaScript.
---

# Clean JavaScript: Complete Reference

Enforces all Clean Code principles from Robert C. Martin's Chapter 17, adapted for JavaScript.

## Comments (C1-C5)
- C1: No metadata in comments (use Git)
- C2: Delete obsolete comments immediately
- C3: No redundant comments
- C4: Write comments well if you must
- C5: Never commit commented-out code

## Environment (E1-E2)
- E1: One command to build (`npm run build`)
- E2: One command to test (`npm test`)

## Functions (F1-F4)
- F1: Maximum 2-3 arguments (use object destructuring for more)
- F2: No output arguments (return values)
- F3: No flag arguments (split functions)
- F4: Delete dead functions

## General (G1-G36)
- G1: One language per file
- G2: Implement expected behavior
- G3: Handle boundary conditions
- G4: Don't override safeties
- G5: DRY — no duplication
- G6: Consistent abstraction levels
- G7: Base classes don't know children
- G8: Minimize public interface
- G9: Delete dead code
- G10: Variables near usage
- G11: Be consistent
- G12: Remove clutter
- G13: No artificial coupling
- G14: No feature envy
- G15: No selector arguments
- G16: No obscured intent
- G17: Code where expected
- G18: Prefer instance methods
- G19: Use explanatory variables
- G20: Function names say what they do
- G21: Understand the algorithm
- G22: Make dependencies physical
- G23: Prefer polymorphism to if/else
- G24: Follow conventions (ESLint, Prettier)
- G25: Named constants, not magic numbers
- G26: Be precise
- G27: Structure over convention
- G28: Encapsulate conditionals
- G29: Avoid negative conditionals
- G30: Functions do one thing
- G31: Make temporal coupling explicit
- G32: Don't be arbitrary
- G33: Encapsulate boundary conditions
- G34: One abstraction level per function
- G35: Config at high levels
- G36: Law of Demeter (no train wrecks)

## JavaScript-Specific (JS1-JS7)
- JS1: Use `const` by default, `let` when needed — never `var`
- JS2: Use object destructuring for function arguments (F1 equivalent)
- JS3: Prefer async/await over Promises over callbacks
- JS4: Use ES6+ class syntax over prototype manipulation
- JS5: Favor functional patterns (map/filter/reduce over imperative loops)
- JS6: Use `===` strict equality — never `==`
- JS7: Use default parameters instead of short-circuiting

## Names (N1-N7)
- N1: Choose descriptive names
- N2: Right abstraction level
- N3: Use standard nomenclature (camelCase functions, PascalCase classes)
- N4: Unambiguous names
- N5: Name length matches scope
- N6: No encodings
- N7: Names describe side effects

## Tests (T1-T9)
- T1: Test everything that could break
- T2: Use coverage tools (Istanbul/c8)
- T3: Don't skip trivial tests
- T4: Ignored test = ambiguity question
- T5: Test boundary conditions
- T6: Exhaustively test near bugs
- T7: Look for patterns in failures
- T8: Check coverage when debugging
- T9: Tests must be fast (< 100ms each)

## Quick Reference Table

| Category | Rule | One-Liner |
|----------|------|-----------|
| **Comments** | C1 | No metadata (use Git) |
| | C3 | No redundant comments |
| | C5 | No commented-out code |
| **Functions** | F1 | Max 2-3 arguments (destructure) |
| | F3 | No flag arguments |
| | F4 | Delete dead functions |
| **General** | G5 | DRY — no duplication |
| | G9 | Delete dead code |
| | G16 | No obscured intent |
| | G23 | Polymorphism over if/else |
| | G25 | Named constants, not magic numbers |
| | G30 | Functions do one thing |
| | G36 | Law of Demeter (one dot) |
| **JavaScript** | JS1 | `const` by default, never `var` |
| | JS3 | async/await over Promises |
| | JS6 | `===` strict equality |
| **Names** | N1 | Descriptive names |
| | N5 | Name length matches scope |
| **Tests** | T5 | Test boundary conditions |
| | T9 | Tests must be fast |

## Anti-Patterns (Don't → Do)

| Don't | Do |
|----------|-------|
| Comment every line | Delete obvious comments |
| Use `var` | Use `const` / `let` |
| Use `==` | Use `===` |
| Callbacks | async/await |
| Magic number `86400` | `const SECONDS_PER_DAY = 86400` |
| `process(data, true)` | `processVerbose(data)` |
| Deep nesting | Guard clauses, early returns |
| `obj.a.b.c.value` | `obj.getValue()` |
| 100+ line function | Split by responsibility |
| `for` loop for transform | `.map()` / `.filter()` / `.reduce()` |
| Short-circuit defaults | Default parameters |

## Modern JavaScript Idioms

```javascript
// JS1: const by default
const users = await fetchUsers();
const activeUsers = users.filter(u => u.isActive);

// JS2: Object destructuring for args
// Bad
function createMenu(title, body, buttonText, cancellable) { ... }

// Good
function createMenu({ title, body, buttonText, cancellable = false }) { ... }

// JS3: async/await over Promises
// Bad
function getUser(id) {
  return fetch(`/api/users/${id}`)
    .then(res => res.json())
    .then(data => data)
    .catch(err => console.error(err));
}

// Good
async function getUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    return await response.json();
  } catch (error) {
    console.error(`Failed to fetch user ${id}:`, error);
    throw error;
  }
}

// JS5: Functional patterns
// Bad
const totalPrice = [];
for (let i = 0; i < items.length; i++) {
  totalPrice.push(items[i].price * items[i].quantity);
}

// Good
const totalPrices = items.map(item => item.price * item.quantity);

// JS7: Default parameters
// Bad
function createUser(name, role) {
  const userRole = role || 'member';
  ...
}

// Good
function createUser(name, role = 'member') { ... }
```

## AI Behavior

When reviewing code, identify violations by rule number (e.g., "G5 violation: duplicated logic").
When fixing or editing code, report what was fixed (e.g., "Fixed: replaced `var` with `const` (JS1)").
