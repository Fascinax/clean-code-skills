---
name: javascript-clean-general
description: Use when writing, fixing, editing, or reviewing JavaScript code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles (JavaScript)

## Critical Rules

### G5: DRY (Don't Repeat Yourself)

Every piece of knowledge has one authoritative representation.

```javascript
// Bad - duplication
const caTotal = subtotal * 1.0825;
const nyTotal = subtotal * 1.07;

// Good - single source of truth
const TAX_RATES = Object.freeze({
  CA: 0.0825,
  NY: 0.07,
});

function calculateTotal(subtotal, state) {
  return subtotal * (1 + TAX_RATES[state]);
}
```

### G16: No Obscured Intent

Don't be clever. Be clear.

```javascript
// Bad - what does this do?
return (x & 0x0F) << 4 | (y & 0x0F);

// Good - obvious intent
return packCoordinates(x, y);
```

### G23: Prefer Polymorphism to If/Else

```javascript
// Bad - will grow forever
function calculatePay(employee) {
  if (employee.type === 'salaried') return employee.salary;
  if (employee.type === 'hourly') return employee.hours * employee.rate;
  if (employee.type === 'commissioned') return employee.base + employee.commission;
  throw new Error(`Unknown type: ${employee.type}`);
}

// Good - strategy pattern with classes
class SalariedEmployee {
  constructor(salary) { this.salary = salary; }
  calculatePay() { return this.salary; }
}

class HourlyEmployee {
  constructor(hours, rate) { this.hours = hours; this.rate = rate; }
  calculatePay() { return this.hours * this.rate; }
}

class CommissionedEmployee {
  constructor(base, commission) { this.base = base; this.commission = commission; }
  calculatePay() { return this.base + this.commission; }
}

// Alternative - lookup table (good for simple cases)
const payCalculators = {
  salaried: (emp) => emp.salary,
  hourly: (emp) => emp.hours * emp.rate,
  commissioned: (emp) => emp.base + emp.commission,
};

function calculatePay(employee) {
  const calculator = payCalculators[employee.type];
  if (!calculator) throw new Error(`Unknown type: ${employee.type}`);
  return calculator(employee);
}
```

### G25: Replace Magic Numbers with Named Constants

```javascript
// Bad
if (elapsedTime > 86400) { ... }

// Good
const SECONDS_PER_DAY = 86400;
if (elapsedTime > SECONDS_PER_DAY) { ... }
```

### G30: Functions Should Do One Thing

If you can extract another function, your function does more than one thing.

### G36: Law of Demeter (Avoid Train Wrecks)

```javascript
// Bad - reaching through multiple objects
const outputDir = context.options.scratchDir.absolutePath;

// Good - one dot
const outputDir = context.getScratchDir();
```

## Enforcement Checklist

When reviewing AI-generated code, verify:

- [ ] No duplication (G5)
- [ ] Clear intent, no magic numbers (G16, G25)
- [ ] Polymorphism over conditionals (G23)
- [ ] Functions do one thing (G30)
- [ ] No Law of Demeter violations (G36)
- [ ] Boundary conditions handled (G3)
- [ ] Dead code removed (G9)
- [ ] `const` / `let` only, no `var` (JS1)
- [ ] `===` strict equality (JS6)

## Modern JavaScript Idioms

```javascript
// G5 with spread/destructuring — avoid manual copies
const defaults = { theme: 'light', lang: 'en', notifications: true };
const userPrefs = { ...defaults, ...savedPrefs };

// G23 with Map for dynamic dispatch
const handlers = new Map([
  ['click', handleClick],
  ['submit', handleSubmit],
  ['keydown', handleKeydown],
]);

function handleEvent(event) {
  const handler = handlers.get(event.type);
  if (handler) handler(event);
}

// G25 with Object.freeze for immutable config
const CONFIG = Object.freeze({
  MAX_RETRIES: 3,
  TIMEOUT_MS: 5000,
  API_BASE_URL: '/api/v1',
});

// G28: Encapsulate conditionals
// Bad
if (user.age >= 18 && user.emailVerified && !user.banned) { ... }

// Good
function isEligibleForPurchase(user) {
  return user.age >= 18 && user.emailVerified && !user.banned;
}

if (isEligibleForPurchase(user)) { ... }

// G30 with async/await — compose small async functions
async function processOrder(orderId) {
  const order = await fetchOrder(orderId);
  const validated = await validateOrder(order);
  const processed = await applyDiscounts(validated);
  return await saveOrder(processed);
}
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| G3 | Handle boundary conditions | Edge cases, nulls, empty collections |
| G5 | DRY — no duplication | Spread/destructuring, single source |
| G9 | Delete dead code | Unused imports, unreachable branches |
| G16 | No obscured intent | Extract to well-named function |
| G23 | Polymorphism over if/else | Map dispatch or strategy classes |
| G25 | Named constants, no magic numbers | `Object.freeze({...})` |
| G28 | Encapsulate conditionals | Extract to boolean function |
| G30 | Functions do one thing | Compose small async functions |
| G36 | Law of Demeter | Max one dot per expression |

## AI Behavior

When reviewing code quality, cite the rule number (e.g., "JS1 violation: `var` used instead of `const`").
When refactoring, explain the improvement (e.g., "Replaced `var` with `const`, added `Object.freeze` for config (JS1, G25)").
When applying Modern JavaScript idioms, infer the Node/ES version from project config first (ES2020+: `?.`, `??`; ES2022+: class fields `#`, top-level `await`; default: ES2020).
