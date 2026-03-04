---
name: typescript-clean-comments
description: Use when writing, fixing, editing, or reviewing TypeScript comments and TSDoc. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code.
---

# Clean Comments (TypeScript)

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history,
ticket numbers, and dates. Comments are for technical notes about code only.

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists or works differently,
delete it immediately. Stale comments become "floating islands of
irrelevance and misdirection."

## C3: No Redundant Comments

```typescript
// Bad - the code already says this
i++; // increment i
user.save(); // save the user

// Bad - types already document this
/** Name of the user */
name: string;

// Good - explains WHY, not WHAT
i++; // compensate for zero-indexing in display

// Good - adds context the type can't express
/** ISO 8601 date string in UTC. Used for API serialization. */
createdAt: string;
```

## C4: Write Comments Well

If a comment is worth writing, write it well:

- Choose words carefully
- Use correct grammar
- Don't ramble or state the obvious
- Be brief

## C5: Never Commit Commented-Out Code

```typescript
// DELETE THIS - it's an abomination
// function calculateTax(income: number): number {
//   return income * 0.15;
// }
```

Who knows how old it is? Who knows if it's meaningful? Delete it.
Git remembers everything.

## TSDoc Best Practices

```typescript
// Good - TSDoc for public API
/**
 * Transfers funds between two accounts.
 *
 * @remarks
 * The transfer is atomic: either both accounts are updated
 * or neither is. Insufficient funds result in a thrown error.
 *
 * @param from - Source account to debit
 * @param to - Destination account to credit
 * @param amount - Positive amount to transfer
 * @throws {@link InsufficientFundsError} if source balance is too low
 */
function transfer(from: Account, to: Account, amount: number): void { ... }

// Good - no comment needed, types are self-documenting
function filterActiveUsers(users: ReadonlyArray<User>): User[] {
  return users.filter(user => user.isActive);
}

// Good - use @ts-expect-error with explanation, not @ts-ignore
// @ts-expect-error - legacy API returns untyped data, migration tracked in PROJ-456
const data = legacyApi.getData();
```

## The Goal

The best comment is the code itself. TypeScript's type system is your
strongest documentation tool — leverage it.

```typescript
// Before - needs comment
// Status can be 'active', 'inactive', or 'pending'
let status: string;

// After - self-documenting with types
type Status = 'active' | 'inactive' | 'pending';
let status: Status;
```

## Modern TypeScript Comment Idioms

### `satisfies` Replaces Type-Assertion Comments

```typescript
// Bad — comment to explain type intent
// This config must match the Config type
const config = { port: 3000, host: 'localhost' } as Config;

// Good — satisfies validates at compile time without widening
const config = { port: 3000, host: 'localhost' } satisfies Config;
```

### `@deprecated` JSDoc Tag Triggers IDE Strikethrough

```typescript
// Bad — comment that tooling can't enforce
// Deprecated: use newApi() instead
function oldApi(): void { ... }

// Good — type checker and IDE both warn callers
/** @deprecated Use {@link newApi} instead. Will be removed in v3.0. */
function oldApi(): void { ... }
```

### Template Literal Types Are Self-Documenting

```typescript
// Bad — comment describing allowed formats
/** Must be a CSS color like '#ff0000' or 'rgb(255,0,0)' */
type Color = string;

// Good — type itself documents the format
type HexColor = `#${string}`;
type RgbColor = `rgb(${number},${number},${number})`;
type Color = HexColor | RgbColor;
```

### `import type` Signals Documentation-Only Imports

```typescript
// Bad — unclear if import is used at runtime
import { User } from './models';

// Good — explicit: this import is for type-checking only
import type { User } from './models';
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| C1 | No metadata in comments | Author, date, ticket → use Git |
| C2 | Delete obsolete comments | Stale comment → delete immediately |
| C3 | No redundant comments | Types already document → remove comment |
| C4 | Write comments well | Brief, precise, explains WHY not WHAT |
| C5 | No commented-out code | Dead code → delete, Git remembers |
| TS8 | `@ts-expect-error` over `@ts-ignore` | Always add explanation |

## AI Behavior

When reviewing comments, cite the rule number (e.g., "C3 violation: types already document this").
When cleaning comments, explain the action (e.g., "Replaced `@ts-ignore` with `@ts-expect-error` and added reason (TS8)").
