---
name: javascript-clean-names
description: Use when naming, renaming, or fixing names of variables, functions, classes, or modules in JavaScript. Enforces Clean Code principles—descriptive names, appropriate length, no encodings.
---

# Clean Names (JavaScript)

## N1: Choose Descriptive Names

Names should reveal intent. If a name requires a comment, it doesn't reveal its intent.

```javascript
// Bad - what is d?
const d = 86400;

// Good - obvious meaning
const SECONDS_PER_DAY = 86400;

// Bad - what does this function do?
function proc(lst) {
  return lst.filter(x => x > 0);
}

// Good - intent is clear
function filterPositiveNumbers(numbers) {
  return numbers.filter(n => n > 0);
}
```

## N2: Choose Names at the Appropriate Level of Abstraction

Don't pick names that communicate implementation; choose names that reflect the level of abstraction.

```javascript
// Bad - too implementation-specific
function getArrayOfUserIdsToNames() { ... }

// Good - abstracts the data structure
function getUserDirectory() { ... }
```

## N3: Use Standard Nomenclature Where Possible

Use terms from the domain, design patterns, or JavaScript conventions.

```javascript
// Good - uses pattern name
class UserFactory {
  create(data) { ... }
}

// Good - JavaScript conventions
// Functions/variables: camelCase
const activeUsers = getActiveUsers();
// Classes: PascalCase
class UserService { ... }
// Constants: UPPER_SNAKE_CASE
const MAX_RETRY_ATTEMPTS = 5;
// Private (convention): #prefix
class Cache {
  #data = new Map();
}
```

## N4: Unambiguous Names

Choose names that make the workings of a function or variable unambiguous.

```javascript
// Bad - ambiguous
function rename(old, newName) { ... }

// Good - clear what's being renamed
function renameFile(oldPath, newPath) { ... }
```

## N5: Use Longer Names for Longer Scopes

Short names are fine for tiny scopes. Longer scopes need more descriptive names.

```javascript
// Good - short name for tiny scope
const total = numbers.reduce((sum, x) => sum + x, 0);

// Good - longer name for module-level constant
const MAX_RETRY_ATTEMPTS_BEFORE_FAILURE = 5;

// Bad - short name at module level
const MAX = 5;
```

## N6: Avoid Encodings

Don't encode type or scope information into names.

```javascript
// Bad - Hungarian notation
const strName = 'Alice';
const arrUsers = [];
const numCount = 0;

// Good - clean names
const name = 'Alice';
const users = [];
const count = 0;
```

## N7: Names Should Describe Side Effects

If a function does something beyond what its name suggests, the name is misleading.

```javascript
// Bad - name doesn't mention file creation
function getConfig() {
  if (!fs.existsSync(configPath)) {
    fs.writeFileSync(configPath, '{}');  // Hidden side effect!
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

// Good - name reveals behavior
function getOrCreateConfig() {
  if (!fs.existsSync(configPath)) {
    fs.writeFileSync(configPath, '{}');
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}
```

## Modern JavaScript Naming Idioms

```javascript
// Private class fields — use # prefix
class UserService {
  #repository;
  #cache;

  constructor(repository, cache) {
    this.#repository = repository;
    this.#cache = cache;
  }
}

// Boolean variables — use is/has/should/can prefixes
const isActive = user.status === 'active';
const hasPermission = user.roles.includes('admin');
const canEdit = isActive && hasPermission;

// Event handlers — prefix with handle or on
function handleClick(event) { ... }
function onSubmit(formData) { ... }

// Async functions — name should reflect the async nature
async function fetchUserProfile(userId) { ... }
async function loadDashboardData() { ... }
```

## Quick Reference

| Rule | Principle | Example |
|------|-----------|---------|
| N1 | Descriptive names | `SECONDS_PER_DAY` not `d` |
| N2 | Right abstraction level | `getUserDirectory()` not `getArrayOf...` |
| N3 | Standard nomenclature | camelCase functions, PascalCase classes |
| N4 | Unambiguous | `renameFile(oldPath, newPath)` |
| N5 | Length matches scope | Short for callbacks, long for exports |
| N6 | No encodings | `users` not `arrUsers` |
| N7 | Describe side effects | `getOrCreateConfig()` |

## AI Behavior

When reviewing naming, cite the rule number (e.g., "N1 violation: `d` is not descriptive").
When renaming, explain the improvement (e.g., "Renamed `proc` to `processTransactions` (N1)").
When applying Modern JavaScript idioms, infer the Node/ES version from project config first (ES2020+: `?.`, `??`; ES2022+: class fields `#`, top-level `await`; default: ES2020).
