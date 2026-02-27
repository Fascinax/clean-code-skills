---
name: typescript-clean-tests
description: Use when writing, fixing, editing, or refactoring TypeScript tests. Enforces Clean Code principles—fast tests, boundary coverage, one concept per test, Jest/Vitest best practices.
---

# Clean Tests (TypeScript)

## T1: Insufficient Tests

Test everything that could possibly break. Use coverage tools as a guide, not a goal.

```typescript
// Bad - only tests happy path
it('divides numbers', () => {
  expect(divide(10, 2)).toBe(5);
});

// Good - tests edge cases too
it('should return quotient when dividing valid numbers', () => {
  expect(divide(10, 2)).toBe(5);
});

it('should throw when dividing by zero', () => {
  expect(() => divide(10, 0)).toThrow('Division by zero');
});

it('should handle negative numbers', () => {
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

```typescript
// Worth having - documents expected behavior
it('should assign default role to new user', () => {
  const user = createUser({ name: 'Alice' });
  expect(user.role).toBe('member');
});
```

## T4: An Ignored Test Is a Question About an Ambiguity

Don't use `it.skip` to hide problems. Either fix the test or delete it.

```typescript
// Bad - hiding a problem
it.skip('handles async operation', () => { ... });

// Good - clear reason and linked issue
it.skip('handles cache invalidation (requires Redis — see CONTRIBUTING.md)', () => { ... });
```

## T5: Test Boundary Conditions

Bugs congregate at boundaries. Test them explicitly.

```typescript
describe('paginate', () => {
  const items = Array.from({ length: 100 }, (_, i) => i);

  it('should return first page', () => {
    expect(paginate(items, { page: 1, size: 10 })).toEqual(items.slice(0, 10));
  });

  it('should return last page', () => {
    expect(paginate(items, { page: 10, size: 10 })).toEqual(items.slice(90, 100));
  });

  it('should return empty array beyond last page', () => {
    expect(paginate(items, { page: 11, size: 10 })).toEqual([]);
  });

  it('should throw on page zero', () => {
    expect(() => paginate(items, { page: 0, size: 10 })).toThrow();
  });

  it('should handle empty array', () => {
    expect(paginate([], { page: 1, size: 10 })).toEqual([]);
  });
});
```

## T6: Exhaustively Test Near Bugs

When you find a bug, write tests for all similar cases. Bugs cluster.

```typescript
// Found bug: off-by-one in date calculation
// Now test ALL date boundaries
it.each([
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

```typescript
// Bad - hits real API
it('creates user', async () => {
  const response = await fetch('/api/users', { ... }); // Slow!
  expect(response.ok).toBe(true);
});

// Good - uses mock
it('creates user', async () => {
  vi.spyOn(api, 'createUser').mockResolvedValue({ id: '1', name: 'Alice' });

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

```typescript
// Bad - testing multiple things
it('creates a valid user', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.name).toBe('Alice');
  expect(user.email).toBe('alice@example.com');
  expect(user.isValid()).toBe(true);
  user.activate();
  expect(user.isActive).toBe(true);
});

// Good - one concept each
it('should store name', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.name).toBe('Alice');
});

it('should store email', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.email).toBe('alice@example.com');
});

it('should be valid when created with required fields', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  expect(user.isValid()).toBe(true);
});

it('should be active after activation', () => {
  const user = createUser({ name: 'Alice', email: 'alice@example.com' });
  user.activate();
  expect(user.isActive).toBe(true);
});
```

### Test Naming Convention (AAA Pattern)

Use `it('should [expected behavior] when [state under test]')`.

```typescript
it('should return user when email exists', () => { ... });
it('should return undefined when email is unknown', () => { ... });
it('should throw when funds are insufficient', () => { ... });
```

## Modern TypeScript Test Idioms

```typescript
// Use type-safe mocks
const mockRepository: jest.Mocked<UserRepository> = {
  findById: jest.fn(),
  save: jest.fn(),
};

// Use satisfies for test fixtures
const testUser = {
  id: '1',
  name: 'Alice',
  email: 'alice@test.com',
  isActive: true,
} satisfies User;

// Use describe blocks for grouping by behavior
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
When writing tests, explain the coverage (e.g., "Added edge cases for undefined, empty array, and type narrowing (T5)").
