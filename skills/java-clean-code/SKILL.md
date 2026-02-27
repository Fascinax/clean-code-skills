---
name: java-clean-code
description: Use when writing, fixing, editing, reviewing, or refactoring any Java code. Enforces Robert Martin's complete Clean Code catalog—naming, functions, comments, DRY, and boundary conditions—adapted for Java.
---

# Clean Java: Complete Reference

Enforces all Clean Code principles from Robert C. Martin's Chapter 17, adapted for Java.

## Comments (C1-C5)
- C1: No metadata in comments (use Git)
- C2: Delete obsolete comments immediately
- C3: No redundant comments
- C4: Write comments well if you must
- C5: Never commit commented-out code

## Environment (E1-E2)
- E1: One command to build (`mvn clean install` or `gradle build`)
- E2: One command to test (`mvn test` or `gradle test`)

## Functions (F1-F4)
- F1: Maximum 3 arguments (use Builder or parameter objects for more)
- F2: No output arguments (return values)
- F3: No flag arguments (split methods)
- F4: Delete dead methods

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
- G24: Follow conventions (Google Java Style Guide)
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

## Java-Specific (J1-J10)
- J1: Use `record` for immutable data classes (Java 16+)
- J2: Use sealed classes/interfaces for restricted hierarchies (Java 17+)
- J3: Use pattern matching in `switch` (Java 21+)
- J4: Use `Optional` return types — never return null
- J5: Use text blocks for multi-line strings (Java 15+)
- J6: Use virtual threads for I/O-bound concurrency (Java 21+)
- J7: Follow Google Java Style (no wildcard imports, K&R braces, +2 indent)
- J8: Always use `@Override`
- J9: Use enums, not integer constants
- J10: Javadoc for all public APIs

## Names (N1-N7)
- N1: Choose descriptive names
- N2: Right abstraction level
- N3: Use standard nomenclature
- N4: Unambiguous names
- N5: Name length matches scope
- N6: No encodings (no Hungarian notation, no `I` prefix on interfaces)
- N7: Names describe side effects

## Tests (T1-T9)
- T1: Test everything that could break
- T2: Use coverage tools (JaCoCo)
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
| **Functions** | F1 | Max 3 arguments |
| | F3 | No flag arguments |
| | F4 | Delete dead methods |
| **General** | G5 | DRY — no duplication |
| | G9 | Delete dead code |
| | G16 | No obscured intent |
| | G23 | Polymorphism over if/else |
| | G25 | Named constants, not magic numbers |
| | G30 | Functions do one thing |
| | G36 | Law of Demeter (one dot) |
| **Java** | J1 | Records for data classes |
| | J4 | Optional, never null |
| | J8 | Always `@Override` |
| **Names** | N1 | Descriptive names |
| | N5 | Name length matches scope |
| **Tests** | T5 | Test boundary conditions |
| | T9 | Tests must be fast |

## Anti-Patterns (Don't → Do)

| Don't | Do |
|----------|-------|
| Comment every line | Delete obvious comments |
| Return null | Return `Optional<T>` |
| POJO with boilerplate getters/setters | `record` |
| `import java.util.*` | Explicit imports |
| Magic number `86400` | `static final int SECONDS_PER_DAY = 86400` |
| `process(data, true)` | `processVerbose(data)` |
| Deep nesting | Guard clauses, early returns |
| `obj.getA().getB().getC()` | `obj.getValue()` |
| 100+ line method | Split by responsibility |
| Integer constants `int STATUS_ACTIVE = 1` | `enum Status { ACTIVE, INACTIVE }` |
| `catch (Exception e) {}` | Log, rethrow, or handle meaningfully |

## Modern Java Idioms

```java
// J1: Records for immutable data
public record UserDto(String name, String email, Instant createdAt) {}

// J2: Sealed interfaces for restricted hierarchies
public sealed interface Shape permits Circle, Rectangle, Triangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}

// J3: Pattern matching in switch
public double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> 0.5 * t.base() * t.height();
    };
}

// J4: Optional instead of null
public Optional<User> findByEmail(String email) {
    return Optional.ofNullable(repository.findByEmail(email));
}

// J5: Text blocks
String query = """
        SELECT u.name, u.email
        FROM users u
        WHERE u.active = true
        ORDER BY u.name
        """;

// J6: Virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    var futures = tasks.stream()
        .map(executor::submit)
        .toList();
}
```

## AI Behavior

When reviewing code, identify violations by rule number (e.g., "G5 violation: duplicated logic").
When fixing or editing code, report what was fixed (e.g., "Fixed: replaced POJO with record (J1)").
