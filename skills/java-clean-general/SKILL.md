---
name: java-clean-general
description: Use when writing, fixing, editing, or reviewing Java code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles (Java)

## Critical Rules

### G5: DRY (Don't Repeat Yourself)

Every piece of knowledge has one authoritative representation.

```java
// Bad - duplication
BigDecimal caTotal = subtotal.multiply(new BigDecimal("1.0825"));
BigDecimal nyTotal = subtotal.multiply(new BigDecimal("1.07"));

// Good - single source of truth
public enum State {
    CA(new BigDecimal("0.0825")),
    NY(new BigDecimal("0.07"));

    private final BigDecimal taxRate;
    State(BigDecimal taxRate) { this.taxRate = taxRate; }

    public BigDecimal calculateTotal(BigDecimal subtotal) {
        return subtotal.multiply(BigDecimal.ONE.add(taxRate));
    }
}
```

### G16: No Obscured Intent

Don't be clever. Be clear.

```java
// Bad - what does this do?
return (x & 0x0F) << 4 | (y & 0x0F);

// Good - obvious intent
return packCoordinates(x, y);
```

### G23: Prefer Polymorphism to If/Else

```java
// Bad - will grow forever
public BigDecimal calculatePay(Employee employee) {
    return switch (employee.getType()) {
        case "SALARIED" -> employee.getSalary();
        case "HOURLY" -> employee.getHours().multiply(employee.getRate());
        case "COMMISSIONED" -> employee.getBase().add(employee.getCommission());
        default -> throw new IllegalStateException("Unknown type: " + employee.getType());
    };
}

// Good - open/closed principle with sealed interfaces
public sealed interface Employee permits Salaried, Hourly, Commissioned {
    BigDecimal calculatePay();
}

public record Salaried(BigDecimal salary) implements Employee {
    public BigDecimal calculatePay() { return salary; }
}

public record Hourly(BigDecimal hours, BigDecimal rate) implements Employee {
    public BigDecimal calculatePay() { return hours.multiply(rate); }
}

public record Commissioned(BigDecimal base, BigDecimal commission) implements Employee {
    public BigDecimal calculatePay() { return base.add(commission); }
}
```

### G25: Replace Magic Numbers with Named Constants

```java
// Bad
if (elapsedTime > 86400) { ... }

// Good
private static final int SECONDS_PER_DAY = 86400;
if (elapsedTime > SECONDS_PER_DAY) { ... }

// Even better with modern Java
if (elapsed.compareTo(Duration.ofDays(1)) > 0) { ... }
```

### G30: Functions Should Do One Thing

If you can extract another method, your method does more than one thing.

### G36: Law of Demeter (Avoid Train Wrecks)

```java
// Bad - reaching through multiple objects
String outputDir = context.getOptions().getScratchDir().getAbsolutePath();

// Good - one dot
String outputDir = context.getScratchDir();
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
- [ ] No wildcard imports (J7)
- [ ] `@Override` used everywhere applicable (J8)

## Modern Java Idioms

```java
// G23 with pattern matching (Java 21+) — exhaustive switch
public double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> 0.5 * t.base() * t.height();
    };
}

// G25 with configuration records
@ConfigurationProperties(prefix = "app.retry")
public record RetryConfig(int maxAttempts, Duration backoff) {}

// G5 with Stream API — no manual loops
List<String> activeUserEmails = users.stream()
    .filter(User::isActive)
    .map(User::email)
    .toList();

// G28: Encapsulate conditionals into methods
// Bad
if (user.getAge() >= 18 && user.isEmailVerified() && !user.isBanned()) { ... }

// Good
if (user.isEligibleForPurchase()) { ... }
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| G3 | Handle boundary conditions | Edge cases, nulls, empty collections |
| G5 | DRY — no duplication | Single source of truth |
| G9 | Delete dead code | Unused imports, unreachable branches |
| G16 | No obscured intent | Extract to well-named method |
| G23 | Polymorphism over if/else | Use sealed interfaces + pattern matching |
| G25 | Named constants, no magic numbers | `static final` or `Duration.ofDays(1)` |
| G28 | Encapsulate conditionals | Extract to boolean method |
| G30 | Functions do one thing | Can you extract another method? |
| G36 | Law of Demeter | Max one dot per expression |

## AI Behavior

When reviewing code quality, cite the rule number (e.g., "G25 violation: magic number `86400`").
When refactoring, explain the improvement (e.g., "Replaced POJO with record (J1), extracted constant (G25)").
When applying Modern Java idioms, infer the Java version from project config first (17+: records/sealed; 21+: pattern matching/virtual threads; default: 17).
