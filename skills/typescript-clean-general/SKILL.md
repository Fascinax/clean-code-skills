---
name: typescript-clean-general
description: Use when writing, fixing, editing, or reviewing TypeScript code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles (TypeScript)

## Critical Rules

**G5: DRY (Don't Repeat Yourself)**

Every piece of knowledge has one authoritative representation.

```typescript
// Bad - duplication
const caTotal = subtotal * 1.0825;
const nyTotal = subtotal * 1.07;

// Good - single source of truth
const TAX_RATES = {
  CA: 0.0825,
  NY: 0.07,
} as const satisfies Record<string, number>;

type State = keyof typeof TAX_RATES;

function calculateTotal(subtotal: number, state: State): number {
  return subtotal * (1 + TAX_RATES[state]);
}
```

**G16: No Obscured Intent**

Don't be clever. Be clear.

```typescript
// Bad - what does this do?
return (x & 0x0F) << 4 | (y & 0x0F);

// Good - obvious intent
return packCoordinates(x, y);
```

**G23: Prefer Polymorphism to If/Else**

```typescript
// Bad - will grow forever
function calculatePay(employee: Employee): number {
  if (employee.type === 'salaried') return employee.salary;
  if (employee.type === 'hourly') return employee.hours * employee.rate;
  if (employee.type === 'commissioned') return employee.base + employee.commission;
  throw new Error(`Unknown type: ${employee.type}`);
}

// Good - discriminated union with exhaustive switch (TS3)
type Employee =
  | { kind: 'salaried'; salary: number }
  | { kind: 'hourly'; hours: number; rate: number }
  | { kind: 'commissioned'; base: number; commission: number };

function calculatePay(employee: Employee): number {
  switch (employee.kind) {
    case 'salaried': return employee.salary;
    case 'hourly': return employee.hours * employee.rate;
    case 'commissioned': return employee.base + employee.commission;
  }
}
```

**G25: Replace Magic Numbers with Named Constants**

```typescript
// Bad
if (elapsedTime > 86400) { ... }

// Good
const SECONDS_PER_DAY = 86400;
if (elapsedTime > SECONDS_PER_DAY) { ... }
```

**G30: Functions Should Do One Thing**

If you can extract another function, your function does more than one thing.

**G36: Law of Demeter (Avoid Train Wrecks)**

```typescript
// Bad - reaching through multiple objects
const outputDir = context.options.scratchDir.absolutePath;

// Good - one dot
const outputDir = context.getScratchDir();
```

## Enforcement Checklist

When reviewing AI-generated code, verify:
- [ ] No duplication (G5)
- [ ] Clear intent, no magic numbers (G16, G25)
- [ ] Polymorphism/discriminated unions over conditionals (G23, TS3)
- [ ] Functions do one thing (G30)
- [ ] No Law of Demeter violations (G36)
- [ ] Boundary conditions handled (G3)
- [ ] Dead code removed (G9)
- [ ] No `any` — use `unknown` and narrow (TS1)
- [ ] `readonly` where mutation isn't needed (TS5)

## Modern TypeScript Idioms

```typescript
// G23 with discriminated unions and exhaustive checks
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function handleResult<T>(result: Result<T>): void {
  switch (result.success) {
    case true:
      console.log(result.data);
      break;
    case false:
      console.error(result.error);
      break;
  }
}

// G5 with utility types — no manual repetition
type UserUpdate = Partial<Pick<User, 'name' | 'email' | 'avatar'>>;

// G25 with as const satisfies
const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
} as const satisfies Record<string, number>;

// G28: Encapsulate conditionals — use type guards
function isAdmin(user: User): user is Admin {
  return user.role === 'admin' && user.permissions.includes('admin:all');
}

if (isAdmin(user)) {
  // TypeScript narrows to Admin type here
  user.adminPanel.open();
}
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| G3 | Handle boundary conditions | Edge cases, nulls, empty collections |
| G5 | DRY — no duplication | Use utility types (`Partial`, `Pick`) |
| G9 | Delete dead code | Unused imports, unreachable branches |
| G16 | No obscured intent | Extract to well-named function |
| G23 | Polymorphism over if/else | Discriminated unions + exhaustive switch |
| G25 | Named constants, no magic numbers | `as const satisfies` |
| G28 | Encapsulate conditionals | Type guards (`user is Admin`) |
| G30 | Functions do one thing | Can you extract another function? |
| G36 | Law of Demeter | Max one dot per expression |

## AI Behavior

When reviewing code quality, cite the rule number (e.g., "TS1 violation: `any` used instead of `unknown`").
When refactoring, explain the improvement (e.g., "Replaced `any` with `unknown` and added type guard (TS1, G28)").
When applying Modern TypeScript idioms, infer the TS version from project config first (4.5+: inline `import type`; 4.9+: `satisfies`; 5.0+: `const` type params; default: 4.5).
