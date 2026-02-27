---
name: javascript-clean-tests
description: Use when writing, fixing, editing, or refactoring JavaScript tests. Enforces Clean Code principles—fast tests, boundary coverage, one concept per test, Jest/Vitest best practices.
---

# Clean Tests (JavaScript)

## T1: Insufficient Tests

Test everything that could possibly break. Use coverage tools as a guide, not a goal.

```javascript
// Bad - only tests happy path
test('divides numbers', () => {
  expect(divide(10, 2)).toBe(5);
});

// Good - tests edge cases too
test('should return quotient when dividing valid numbers', () => {
  expect(divide(10, 2)).toBe(5);
});

test('should throw when dividing by zero', () => {
  expect(() => divide(10, 0)).toThrow('Division by zero');
});

test('should handle negative numbers', () => {
  expect(divide(-10, 2)).toBe(-5);
});
```

## T2: Use a Coverage Tool

Coverage tools report gaps in your testing strategy.

```bash
# Jest
npx jest --coverage

# Vitest
npx vitest --coverage

# Aim for meaningful coverage, not 100%
```

## T3: Don't Skip Trivial Tests

Trivial tests document behavior and catch regressions. They're worth more than their cost.

```javascript
// Worth having - documents expected behavior
test('should assign default role to new user', () => {
  const user = createUser({ name: 'Alice' });
  expect(user.role).toBe('member');
});
```

## T4: An Ignored Test Is a Question About an Ambiguity

Don't use `test.skip` to hide problems. Either fix the test or delete it.

```javascript
// Bad - hiding a problem
test.skip('handles async operation', () => { ... });

// Good - clear reason
test.skip('handles cache invalidation (requires Redis)', () => { ... });
```

## T5: Test Boundary Conditions

Bugs congregate at boundaries. Test them explicitly.

```javascript
describe('paginate', () => {
  const items = Array.from({ length: 100 }, (_, i) => i);

  test('should return first page', () => {
    expect(paginate(items, { page: 1, size: 10 })).toEqual(items.slice(0, 10));
  });

  test('should return last page', () => {
    expect(paginate(items, { page: 10, size: 10 })).toEqual(items.slice(90, 100));
  });

  test('should return empty array beyond last page', () => {
    expect(paginate(items, { page: 11, size: 10 })).toEqual([]);
  });

  test('should throw on page zero', () => {
    expect(() => paginate(items, { page: 0, size: 10 })).toThrow();
  });

  test('should handle empty array', () => {
    expect(paginate([], { page: 1, size: 10 })).toEqual([]);
  });
});
```

## T6: Exhaustively Test Near Bugs

When you find a bug, write tests for all similar cases. Bugs cluster.

```javascript
// Found bug: off-by-one in date calculation
// Now test ALL date boundaries
test.each([
  [2024, 1, 31],   // January
  [2024, 2, 29],   // Leap year February
  [2023, 2, 28],   // Non-leap February
  [2024, 4, 30],   // 30-day month
  [2024, 12, 31],  // December
])('lastDayOfMonth(%i, %i) should return %i', (year, month, expected) => {
  expect(lastDayOfMonth(year, month)).toBe(expected);
});
```

## T7: Patterns of Failure Are Revealing

When tests fail, look for patterns. They often point to deeper issues.

## T8: Test Coverage Patterns Can Be Revealing

Look at which code paths are untested. Often they reveal design problems.

## T9: Tests Should Be Fast

Slow tests don't get run. Keep unit tests under 100ms each.

```javascript
// Bad - hits real API
test('creates user', async () => {
  const response = await fetch('/api/users', { ... }); // Slow!
  expect(response.ok).toBe(true);
});

// Good - uses mock
test('creates user', async () => {
  jest.spyOn(api, 'createUser').mockResolvedValue({ id: '1', name: 'Alice' });

  const user = await service.createUser({ name: 'Alice' });
  expect(user.name).toBe('Alice');
});
```

## Test Organization

### F.I.R.S.T. Principles

- **Fast**: Tests should run quickly (< 100ms)
- **Independent**: Tests shouldn't depend on each other
- **Repeatable**: Same result every time, any environment
- **Self-Validating**: Pass or fail, no manual inspection
- **Timely**: Written before or with the code, not after

### One Concept Per Test

```javascript
// Bad - testing multiple things
test('creates a valid user', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.name).toBe('Alice');
  expect(user.email).toBe('alice@example.com');
  expect(user.isValid()).toBe(true);
  user.activate();
  expect(user.isActive).toBe(true);
});

// Good - one concept each
test('should store name', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.name).toBe('Alice');
});

test('should store email', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.email).toBe('alice@example.com');
});

test('should be valid when created with required fields', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.isValid()).toBe(true);
});

test('should be active after activation', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  user.activate();
  expect(user.isActive).toBe(true);
});
```

### Test Naming Convention

Use `test('should [expected behavior] when [state]')` or `describe`/`it` blocks.

```javascript
describe('UserService', () => {
  describe('when user exists', () => {
    it('should return the user', () => { ... });
    it('should increment access count', () => { ... });
  });

  describe('when user does not exist', () => {
    it('should return undefined', () => { ... });
    it('should not throw', () => { ... });
  });
});
```

## Modern JavaScript Test Idioms

```javascript
// Use async/await in tests
test('should fetch and return user', async () => {
  const user = await service.getUser('123');
  expect(user.name).toBe('Alice');
});

// Use test.each for data-driven tests
test.each([
  ['', false],
  ['a', false],
  ['valid@email.com', true],
  ['no-at-sign.com', false],
])('should validate email "%s" as %s', (email, expected) => {
  expect(isValidEmail(email)).toBe(expected);
});

// Use beforeEach for shared setup, not beforeAll (tests stay independent)
describe('OrderService', () => {
  let service;
  let mockRepo;

  beforeEach(() => {
    mockRepo = { findById: jest.fn(), save: jest.fn() };
    service = new OrderService(mockRepo);
  });

  test('should process order', () => { ... });
});
```

## Quick Reference

| Rule | Principle |
|------|-----------|
| T1 | Test everything that could break |
| T2 | Use coverage tools (Istanbul/c8) |
| T3 | Don't skip trivial tests |
| T4 | Ignored test = ambiguity question |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Look for patterns in failures |
| T8 | Check coverage when debugging |
| T9 | Tests must be fast (< 100ms) |

## AI Behavior

When reviewing tests, cite the rule number (e.g., "T5 violation: no boundary condition tests").
When writing tests, explain the coverage (e.g., "Added edge cases for null, undefined, and empty string (T5)").
