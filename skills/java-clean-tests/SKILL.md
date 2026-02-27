---
name: java-clean-tests
description: Use when writing, fixing, editing, or refactoring Java tests. Enforces Clean Code principles—fast tests, boundary coverage, one assert per test, JUnit 5 best practices.
---

# Clean Tests (Java)

## T1: Insufficient Tests

Test everything that could possibly break. Use coverage tools as a guide, not a goal.

```java
// Bad - only tests happy path
@Test
void testDivide() {
    assertEquals(5, calculator.divide(10, 2));
}

// Good - tests edge cases too
@Test
void divide_returnsQuotient() {
    assertEquals(5, calculator.divide(10, 2));
}

@Test
void divide_byZero_throwsException() {
    assertThrows(ArithmeticException.class,
        () -> calculator.divide(10, 0));
}

@Test
void divide_negativeNumbers_returnsNegativeQuotient() {
    assertEquals(-5, calculator.divide(-10, 2));
}
```

## T2: Use a Coverage Tool

Coverage tools report gaps in your testing strategy. Don't ignore them.

```xml
<!-- JaCoCo in Maven -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
</plugin>
```

```bash
# Run with coverage
mvn test jacoco:report
# Aim for meaningful coverage, not 100%
```

## T3: Don't Skip Trivial Tests

Trivial tests document behavior and catch regressions. They're worth more than their cost.

```java
// Worth having - documents expected behavior
@Test
void newUser_hasDefaultRole() {
    var user = new User("Alice");
    assertEquals(Role.MEMBER, user.getRole());
}
```

## T4: An Ignored Test Is a Question About an Ambiguity

Don't use `@Disabled` to hide problems. Either fix the test or delete it.

```java
// Bad - hiding a problem
@Disabled("Flaky, fix later")
@Test
void testAsyncOperation() { ... }

// Good - document why with a clear reason and a linked issue
@Disabled("Requires Redis — see CONTRIBUTING.md for local setup")
@Test
void testCacheInvalidation() { ... }
```

## T5: Test Boundary Conditions

Bugs congregate at boundaries. Test them explicitly.

```java
@Test
void pagination_firstPage() {
    var page = paginate(items, 1, 10);
    assertEquals(items.subList(0, 10), page);
}

@Test
void pagination_lastPage() {
    var page = paginate(items, 10, 10);
    assertEquals(items.subList(90, 100), page);
}

@Test
void pagination_beyondLastPage() {
    var page = paginate(items, 11, 10);
    assertTrue(page.isEmpty());
}

@Test
void pagination_pageZero_throwsException() {
    assertThrows(IllegalArgumentException.class,
        () -> paginate(items, 0, 10));
}

@Test
void pagination_emptyList() {
    var page = paginate(List.of(), 1, 10);
    assertTrue(page.isEmpty());
}
```

## T6: Exhaustively Test Near Bugs

When you find a bug, write tests for all similar cases. Bugs cluster.

```java
// Found bug: off-by-one in date calculation
// Now test ALL date boundaries
@ParameterizedTest
@CsvSource({
    "2024, 1, 31",   // January
    "2024, 2, 29",   // Leap year February
    "2023, 2, 28",   // Non-leap February
    "2024, 4, 30",   // 30-day month
    "2024, 12, 31"   // December
})
void lastDayOfMonth_returnsCorrectDay(int year, int month, int expected) {
    assertEquals(expected, DateUtils.lastDayOfMonth(year, month));
}
```

## T7: Patterns of Failure Are Revealing

When tests fail, look for patterns. They often point to deeper issues.

## T8: Test Coverage Patterns Can Be Revealing

Look at which code paths are untested. Often they reveal design problems.
If you can't easily test a method, it probably does too much.

## T9: Tests Should Be Fast

Slow tests don't get run. Keep unit tests under 100ms each.

```java
// Bad - hits real database
@Test
void testUserCreation() {
    var db = DatabaseConnection.connect();  // Slow!
    var user = db.createUser("Alice");
    assertEquals("Alice", user.getName());
}

// Good - uses mock or in-memory
@Test
void testUserCreation() {
    var repository = mock(UserRepository.class);
    when(repository.save(any())).thenAnswer(inv -> inv.getArgument(0));

    var service = new UserService(repository);
    var user = service.createUser("Alice");
    assertEquals("Alice", user.getName());
}
```

## Test Organization

### F.I.R.S.T. Principles

- **Fast**: Tests should run quickly (< 100ms)
- **Independent**: Tests shouldn't depend on each other
- **Repeatable**: Same result every time, any environment
- **Self-Validating**: Pass or fail, no manual inspection
- **Timely**: Written before or with the code, not after

### One Concept Per Test

```java
// Bad - testing multiple things
@Test
void testUser() {
    var user = new User("Alice", "alice@example.com");
    assertEquals("Alice", user.getName());
    assertEquals("alice@example.com", user.getEmail());
    assertTrue(user.isValid());
    user.activate();
    assertTrue(user.isActive());
}

// Good - one concept each
@Test
void newUser_storesName() {
    var user = new User("Alice", "alice@example.com");
    assertEquals("Alice", user.getName());
}

@Test
void newUser_storesEmail() {
    var user = new User("Alice", "alice@example.com");
    assertEquals("alice@example.com", user.getEmail());
}

@Test
void newUser_isValid() {
    var user = new User("Alice", "alice@example.com");
    assertTrue(user.isValid());
}

@Test
void user_canBeActivated() {
    var user = new User("Alice", "alice@example.com");
    user.activate();
    assertTrue(user.isActive());
}
```

### Test Naming Convention

Use `methodName_stateUnderTest_expectedBehavior` or `should_expectedBehavior_when_stateUnderTest`.

```java
@Test void findByEmail_existingUser_returnsUser() { ... }
@Test void findByEmail_unknownEmail_returnsEmpty() { ... }
@Test void transfer_insufficientFunds_throwsException() { ... }
```

## Modern Java Test Idioms

```java
// Use @ParameterizedTest for data-driven tests
@ParameterizedTest
@ValueSource(strings = {"", " ", "  "})
void validate_blankName_throwsException(String name) {
    assertThrows(ValidationException.class,
        () -> new User(name, "email@test.com"));
}

// Use assertAll for grouped assertions
@Test
void orderSummary_containsAllFields() {
    var summary = service.getSummary(orderId);
    assertAll(
        () -> assertNotNull(summary.total()),
        () -> assertTrue(summary.itemCount() > 0),
        () -> assertNotNull(summary.createdAt())
    );
}

// Use Testcontainers for integration tests (keep unit tests fast)
@Testcontainers
class UserRepositoryIT {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");
}
```

## Quick Reference

| Rule | Principle |
|------|-----------|
| T1 | Test everything that could break |
| T2 | Use coverage tools (JaCoCo) |
| T3 | Don't skip trivial tests |
| T4 | Ignored test = ambiguity question |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Look for patterns in failures |
| T8 | Check coverage when debugging |
| T9 | Tests must be fast (< 100ms) |

## AI Behavior

When reviewing tests, cite the rule number (e.g., "T5 violation: no boundary condition tests").
When writing tests, explain the coverage (e.g., "Added edge cases for null, empty Optional, and leap year (T5)").
