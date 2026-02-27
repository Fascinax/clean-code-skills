---
name: typescript-clean-code
description: Use when writing, fixing, editing, reviewing, or refactoring any TypeScript code. Enforces Robert Martin's complete Clean Code catalog—naming, functions, comments, DRY, and boundary conditions—adapted for TypeScript.
---

# Clean TypeScript: Complete Reference

Enforces all Clean Code principles from Robert C. Martin's Chapter 17, adapted for TypeScript.

## Comments (C1-C5)
- C1: No metadata in comments (use Git)
- C2: Delete obsolete comments immediately
- C3: No redundant comments
- C4: Write comments well if you must
- C5: Never commit commented-out code

## Environment (E1-E2)
- E1: One command to build (`npm run build` or `tsc`)
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
- G24: Follow conventions (strict TS config, linting)
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

## TypeScript-Specific (TS1-TS8)
- TS1: Use `unknown` over `any` — always narrow types
- TS2: Prefer `type` over `interface` (except for extension/declaration merging)
- TS3: Use discriminated unions for exhaustive pattern matching
- TS4: Prefer `as const satisfies` for const assertions
- TS5: Use `readonly` and `ReadonlyArray` for immutability
- TS6: Use `import type` for type-only imports
- TS7: Name generics descriptively (`TRequest`, `TResponse`, not `T`, `U`)
- TS8: Use `@ts-expect-error` over `@ts-ignore`

## Names (N1-N7)
- N1: Choose descriptive names
- N2: Right abstraction level
- N3: Use standard nomenclature (camelCase functions, PascalCase types)
- N4: Unambiguous names
- N5: Name length matches scope
- N6: No encodings (no `I` prefix on interfaces, no Hungarian notation)
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
| **TypeScript** | TS1 | `unknown` over `any` |
| | TS3 | Discriminated unions |
| | TS5 | `readonly` for immutability |
| **Names** | N1 | Descriptive names |
| | N5 | Name length matches scope |
| **Tests** | T5 | Test boundary conditions |
| | T9 | Tests must be fast |

## Anti-Patterns (Don't → Do)

| Don't | Do |
|----------|-------|
| Comment every line | Delete obvious comments |
| Use `any` | Use `unknown` and narrow |
| `interface IUser` | `type User` (no `I` prefix) |
| Magic number `86400` | `const SECONDS_PER_DAY = 86400` |
| `process(data, true)` | `processVerbose(data)` |
| Deep nesting | Guard clauses, early returns |
| `obj.a.b.c.value` | `obj.getValue()` |
| 100+ line function | Split by responsibility |
| `enum Status { ... }` | `type Status = 'active' \| 'inactive'` |
| `@ts-ignore` | `@ts-expect-error` |
| `T`, `U` generics | `TRequest`, `TResponse` |

## Modern TypeScript Idioms

```typescript
// TS1: unknown over any — always narrow
function processInput(input: unknown): string {
  if (typeof input === 'string') return input.toUpperCase();
  if (typeof input === 'number') return input.toFixed(2);
  throw new Error(`Unexpected input type: ${typeof input}`);
}

// TS3: Discriminated unions
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rectangle'; width: number; height: number }
  | { kind: 'triangle'; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle': return Math.PI * shape.radius ** 2;
    case 'rectangle': return shape.width * shape.height;
    case 'triangle': return 0.5 * shape.base * shape.height;
  }
}

// TS4: as const satisfies
const ROUTES = {
  home: '/',
  about: '/about',
  users: '/users',
} as const satisfies Record<string, string>;

// TS5: Readonly for immutability
function processItems(items: ReadonlyArray<string>): string[] {
  return items.map(item => item.toUpperCase());
}

// TS6: import type
import type { User } from './types';
import { createUser } from './services';

// TS7: Descriptive generics
function fetchData<TResponse>(url: string): Promise<TResponse> { ... }
```

## AI Behavior

When reviewing code, identify violations by rule number (e.g., "G5 violation: duplicated logic").
When fixing or editing code, report what was fixed (e.g., "Fixed: replaced `any` with `unknown` (TS1)").
