---
name: typescript-clean-names
description: Use when naming, renaming, or fixing names of variables, functions, types, or modules in TypeScript. Enforces Clean Code principles—descriptive names, appropriate length, no encodings.
---

# Clean Names (TypeScript)

## N1: Choose Descriptive Names

Names should reveal intent. If a name requires a comment, it doesn't reveal its intent.

```typescript
// Bad - what is d?
const d = 86400;

// Good - obvious meaning
const SECONDS_PER_DAY = 86400;

// Bad - what does this function do?
function proc(lst: number[]): number[] {
  return lst.filter(x => x > 0);
}

// Good - intent is clear
function filterPositiveNumbers(numbers: number[]): number[] {
  return numbers.filter(n => n > 0);
}
```

## N2: Choose Names at the Appropriate Level of Abstraction

Don't pick names that communicate implementation; choose names that reflect the level of abstraction.

```typescript
// Bad - too implementation-specific
function getMapOfUserIdsToNames(): Map<number, string> { ... }

// Good - abstracts the data structure
function getUserDirectory(): Map<number, string> { ... }
```

## N3: Use Standard Nomenclature Where Possible

Use terms from the domain, design patterns, or TypeScript conventions.

```typescript
// Good - uses pattern name
class UserFactory {
  create(dto: CreateUserDto): User { ... }
}

// Good - TypeScript conventions
// Types/Interfaces: PascalCase
type UserResponse = { ... };
// Functions/variables: camelCase
const activeUsers = getActiveUsers();
// Constants: UPPER_SNAKE_CASE
const MAX_RETRY_ATTEMPTS = 5;
```

## N4: Unambiguous Names

Choose names that make the workings of a function or variable unambiguous.

```typescript
// Bad - ambiguous
function rename(old: string, newName: string): void { ... }

// Good - clear what's being renamed
function renameFile(oldPath: string, newPath: string): void { ... }

// Bad - ambiguous return
function getStatus(): string;

// Good - specific
function isActive(): boolean;
function getOrderStatus(): OrderStatus;
```

## N5: Use Longer Names for Longer Scopes

Short names are fine for tiny scopes. Longer scopes need more descriptive names.

```typescript
// Good - short name for tiny scope
const total = numbers.reduce((sum, x) => sum + x, 0);

// Good - longer name for module-level constant
const MAX_RETRY_ATTEMPTS_BEFORE_FAILURE = 5;

// Bad - short name at module level
const MAX = 5;
```

## N6: Avoid Encodings

Don't encode type or scope information into names.

```typescript
// Bad - Hungarian notation
const strName = 'Alice';
const arrUsers: User[] = [];
const numCount = 0;

// Good - clean names
const name = 'Alice';
const users: User[] = [];
const count = 0;

// Bad - interface prefix
interface IUserRepository { ... }

// Good - no prefix, use type
type UserRepository = { ... };
```

## N7: Names Should Describe Side Effects

If a function does something beyond what its name suggests, the name is misleading.

```typescript
// Bad - name doesn't mention file creation
function getConfig(): Config {
  if (!fs.existsSync(configPath)) {
    fs.writeFileSync(configPath, '{}');  // Hidden side effect!
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

// Good - name reveals behavior
function getOrCreateConfig(): Config {
  if (!fs.existsSync(configPath)) {
    fs.writeFileSync(configPath, '{}');
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}
```

## Modern TypeScript Naming Idioms

```typescript
// Descriptive generic names (TS7)
// Bad
function fetch<T>(url: string): Promise<T> { ... }

// Good
function fetchData<TResponse>(url: string): Promise<TResponse> { ... }
function transformArray<TInput, TOutput>(
  items: ReadonlyArray<TInput>,
  mapper: (item: TInput) => TOutput
): TOutput[] { ... }

// Discriminated union type names — use the concept they model
type PaymentMethod =
  | { kind: 'credit-card'; cardNumber: string }
  | { kind: 'bank-transfer'; iban: string }
  | { kind: 'wallet'; walletId: string };

// Const assertions — use UPPER_SNAKE_CASE for config objects
const API_ROUTES = {
  users: '/api/users',
  orders: '/api/orders',
} as const satisfies Record<string, string>;

// Boolean names — use is/has/should/can prefixes
type UserState = {
  isActive: boolean;
  hasVerifiedEmail: boolean;
  canAccessAdmin: boolean;
};
```

## Quick Reference

| Rule | Principle | Example |
|------|-----------|---------|
| N1 | Descriptive names | `SECONDS_PER_DAY` not `d` |
| N2 | Right abstraction level | `getUserDirectory()` not `getMapOf...` |
| N3 | Standard nomenclature | PascalCase types, camelCase functions |
| N4 | Unambiguous | `renameFile(oldPath, newPath)` |
| N5 | Length matches scope | Short for callbacks, long for exports |
| N6 | No encodings | `users` not `arrUsers`, no `I` prefix |
| N7 | Describe side effects | `getOrCreateConfig()` |

## AI Behavior

When reviewing naming, cite the rule number (e.g., "N1 violation: `d` is not descriptive").
When renaming, explain the improvement (e.g., "Renamed generic `T` to `TResponse` for clarity (TS7, N1)").
When applying Modern TypeScript idioms, infer the TS version from project config first (4.5+: inline `import type`; 4.9+: `satisfies`; 5.0+: `const` type params; default: 4.5).
