---
name: java-clean-comments
description: Use when writing, fixing, editing, or reviewing Java comments and Javadoc. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code, proper Javadoc.
---

# Clean Comments (Java)

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history,
ticket numbers, and dates. Comments are for technical notes about code only.

```java
// Bad - metadata belongs in Git
/**
 * @author John Doe
 * @since 2024-01-15
 * @ticket JIRA-1234
 * Changed on 2024-03-01 by Jane
 */
public class OrderService { ... }

// Good - only technical documentation
/**
 * Processes orders by validating inventory, calculating totals,
 * and dispatching to the fulfillment system.
 */
public class OrderService { ... }
```

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists or works differently,
delete it immediately. Stale comments become "floating islands of
irrelevance and misdirection."

## C3: No Redundant Comments

```java
// Bad - the code already says this
i++; // increment i
user.save(); // save the user

// Bad - Javadoc restating the obvious
/** Returns the name. */
public String getName() { return name; }

// Good - explains WHY, not WHAT
i++; // compensate for zero-indexing in display

// Good - Javadoc that adds value
/**
 * Returns the user's display name, falling back to email prefix
 * if no explicit name was set.
 */
public String getDisplayName() { ... }
```

## C4: Write Comments Well

If a comment is worth writing, write it well:

- Choose words carefully
- Use correct grammar
- Don't ramble or state the obvious
- Be brief

## C5: Never Commit Commented-Out Code

```java
// DELETE THIS - it's an abomination
// public BigDecimal calculateTax(BigDecimal income) {
//     return income.multiply(new BigDecimal("0.15"));
// }
```

Who knows how old it is? Who knows if it's meaningful? Delete it.
Git remembers everything.

## Javadoc Best Practices (Google Java Style)

```java
// Good - proper Javadoc format
/**
 * Transfers funds between two accounts.
 *
 * <p>The transfer is atomic: either both accounts are updated
 * or neither is. Insufficient funds result in a thrown exception
 * rather than a partial transfer.
 *
 * @param from source account to debit
 * @param to destination account to credit
 * @param amount positive amount to transfer
 * @throws InsufficientFundsException if source balance is too low
 * @throws IllegalArgumentException if amount is not positive
 */
public void transfer(Account from, Account to, BigDecimal amount) { ... }

// Good - self-explanatory needs no Javadoc
public record UserDto(String name, String email) {}

// Good - summary fragment is a noun/verb phrase, not a sentence
/** Returns the canonical name of this type. */
public String getCanonicalName() { ... }

// Bad - starts with "This method..."
/** This method returns the canonical name. */
```

## The Goal

The best comment is the code itself. If you need a comment to explain
what code does, refactor first, comment last.

```java
// Before - needs comment
// Check if user is eligible for discount
if (user.getAge() >= 65 || user.getMemberSince().isBefore(cutoffDate)) { ... }

// After - self-documenting with pattern matching
if (user.isEligibleForDiscount()) { ... }
```

## Modern Java Comment Idioms

### `@snippet` Replaces Hand-Written Code in Javadoc (JDK 18+)

```java
// Bad — manually maintained code example that drifts from reality
/**
 * Example:
 * <pre>{@code
 *   var list = List.of("a", "b");
 * }</pre>
 */

// Good — snippet references verified source code
/**
 * Example:
 * {@snippet file="ListExample.java" region="creation"}
 */
```

### Records Need Minimal Javadoc

```java
// Bad — boilerplate Javadoc on a self-documenting record
/**
 * Represents a user with a name and email.
 * @param name the user's name
 * @param email the user's email
 */
public record UserDto(String name, String email) {}

// Good — record fields are self-documenting; add Javadoc only for non-obvious constraints
/** DTO for user display. Email is always lower-cased on creation. */
public record UserDto(String name, String email) {
    public UserDto {
        email = email.toLowerCase();
    }
}
```

### `{@return}` Shorthand (JDK 16+)

```java
// Bad — verbose @return that repeats the summary
/**
 * Returns the canonical name.
 * @return the canonical name
 */
public String getCanonicalName() { ... }

// Good — inline return tag generates both summary and @return
/** {@return the canonical name of this type} */
public String getCanonicalName() { ... }
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| C1 | No metadata in comments | Author, date, ticket → use Git |
| C2 | Delete obsolete comments | Stale comment → delete immediately |
| C3 | No redundant comments | Code says it already → remove comment |
| C4 | Write comments well | Brief, precise, explains WHY not WHAT |
| C5 | No commented-out code | Dead code → delete, Git remembers |
| J10 | Javadoc for public APIs | Summary fragment, `@param`, `@throws` |

## AI Behavior

When reviewing comments, cite the rule number (e.g., "C3 violation: Javadoc restates the method name").
When cleaning comments, explain the action (e.g., "Removed `@author` tag, use Git for author tracking (C1)").
