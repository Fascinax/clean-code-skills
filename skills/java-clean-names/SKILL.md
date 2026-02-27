---
name: java-clean-names
description: Use when naming, renaming, or fixing names of variables, methods, classes, or packages in Java. Enforces Clean Code principles—descriptive names, appropriate length, no encodings.
---

# Clean Names (Java)

## N1: Choose Descriptive Names

Names should reveal intent. If a name requires a comment, it doesn't reveal its intent.

```java
// Bad - what is d?
int d; // elapsed time in days

// Good - obvious meaning
int elapsedTimeInDays;

// Bad - what does this method do?
List<int[]> getThem(List<int[]> theList) {
    List<int[]> list1 = new ArrayList<>();
    for (int[] x : theList)
        if (x[0] == 4) list1.add(x);
    return list1;
}

// Good - intent is clear
List<Cell> getFlaggedCells(List<Cell> gameBoard) {
    return gameBoard.stream()
        .filter(Cell::isFlagged)
        .toList();
}
```

## N2: Choose Names at the Appropriate Level of Abstraction

Don't pick names that communicate implementation; choose names that reflect the level of abstraction.

```java
// Bad - too implementation-specific
Map<Integer, String> getHashMapOfUserIdsToNames() { ... }

// Good - abstracts the data structure
Map<Integer, String> getUserDirectory() { ... }
```

## N3: Use Standard Nomenclature Where Possible

Use terms from the domain, design patterns, or well-known conventions.

```java
// Good - uses pattern name
public class UserFactory {
    public User create(UserDto dto) { ... }
}

// Good - uses domain term
public BigDecimal calculateAmortization(BigDecimal principal, double rate, int term) { ... }

// Good - Google Java Style conventions
// Classes: UpperCamelCase (nouns)
// Methods: lowerCamelCase (verbs)
// Constants: UPPER_SNAKE_CASE
// Packages: all lowercase, no underscores
```

## N4: Unambiguous Names

Choose names that make the workings of a method or variable unambiguous.

```java
// Bad - ambiguous
void rename(String old, String newName) { ... }

// Good - clear what's being renamed
void renameFile(Path oldPath, Path newPath) { ... }

// Bad - ambiguous return
String getStatus();

// Good - specific
boolean isActive();
OrderStatus getOrderStatus();
```

## N5: Use Longer Names for Longer Scopes

Short names are fine for tiny scopes. Longer scopes need more descriptive names.

```java
// Good - short name for lambda/stream
users.stream().filter(u -> u.isActive()).toList();

// Good - longer name for class field
private final int maxRetryAttemptsBeforeFailure = 5;

// Bad - short name at class level
private int max = 5;
```

## N6: Avoid Encodings

Don't encode type or scope information into names. No Hungarian notation, no `I` prefix.

```java
// Bad - Hungarian notation
String strName = "Alice";
List<User> lstUsers = new ArrayList<>();
int iCount = 0;

// Good - clean names
String name = "Alice";
List<User> users = new ArrayList<>();
int count = 0;

// Bad - interface prefix (C# convention, not Java)
interface IUserRepository { ... }

// Good - name the interface cleanly, prefix the implementation
interface UserRepository { ... }
class JpaUserRepository implements UserRepository { ... }
```

## N7: Names Should Describe Side Effects

If a method does something beyond what its name suggests, the name is misleading.

```java
// Bad - name doesn't mention creation
public Config getConfig() {
    if (!Files.exists(configPath)) {
        Files.writeString(configPath, "{}");  // Hidden side effect!
    }
    return objectMapper.readValue(configPath.toFile(), Config.class);
}

// Good - name reveals behavior
public Config getOrCreateConfig() {
    if (!Files.exists(configPath)) {
        Files.writeString(configPath, "{}");
    }
    return objectMapper.readValue(configPath.toFile(), Config.class);
}
```

## Modern Java Naming Idioms

```java
// Records: use concise noun names matching their purpose
public record UserDto(String name, String email) {}
public record OrderSummary(BigDecimal total, int itemCount) {}

// Sealed interfaces: use the concept they model
public sealed interface PaymentMethod permits CreditCard, BankTransfer, Wallet {}

// Optional-returning methods: prefix with "find" not "get"
Optional<User> findByEmail(String email);   // Good - may not exist
User getById(Long id);                       // Good - guaranteed to exist or throw

// Builder: method names match field names
User.builder()
    .name("Alice")
    .email("alice@example.com")
    .build();
```

## Quick Reference

| Rule | Principle | Example |
|------|-----------|---------|
| N1 | Descriptive names | `elapsedTimeInDays` not `d` |
| N2 | Right abstraction level | `getUserDirectory()` not `getHashMapOf...` |
| N3 | Standard nomenclature | `UserFactory`, `UpperCamelCase` |
| N4 | Unambiguous | `renameFile(oldPath, newPath)` |
| N5 | Length matches scope | Short for lambdas, long for fields |
| N6 | No encodings | `users` not `lstUsers`, no `I` prefix |
| N7 | Describe side effects | `getOrCreateConfig()` |

## AI Behavior

When reviewing naming, cite the rule number (e.g., "N1 violation: `d` is not descriptive").
When renaming, explain the improvement (e.g., "Renamed `proc` to `processTransactions` (N1)").
