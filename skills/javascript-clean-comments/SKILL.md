---
name: javascript-clean-comments
description: Use when writing, fixing, editing, or reviewing JavaScript comments and JSDoc. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code.
---

# Clean Comments (JavaScript)

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history,
ticket numbers, and dates. Comments are for technical notes about code only.

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists or works differently,
delete it immediately. Stale comments become "floating islands of
irrelevance and misdirection."

## C3: No Redundant Comments

```javascript
// Bad - the code already says this
i++; // increment i
user.save(); // save the user

// Good - explains WHY, not WHAT
i++; // compensate for zero-indexing in display

// Good - only comment complex business logic
// Applying compound interest formula: A = P(1 + r/n)^(nt)
const finalAmount = principal * Math.pow(1 + rate / periods, periods * years);
```

## C4: Write Comments Well

If a comment is worth writing, write it well:
- Choose words carefully
- Use correct grammar
- Don't ramble or state the obvious
- Be brief

## C5: Never Commit Commented-Out Code

```javascript
// DELETE THIS - it's an abomination
// function calculateTax(income) {
//   return income * 0.15;
// }
```

Who knows how old it is? Who knows if it's meaningful? Delete it.
Git remembers everything.

## JSDoc Best Practices

```javascript
// Good - JSDoc for public API (especially useful in plain JS without types)
/**
 * Transfers funds between two accounts.
 *
 * The transfer is atomic: either both accounts are updated
 * or neither is. Insufficient funds result in a thrown error.
 *
 * @param {Account} from - Source account to debit
 * @param {Account} to - Destination account to credit
 * @param {number} amount - Positive amount to transfer
 * @throws {InsufficientFundsError} If source balance is too low
 * @returns {void}
 */
function transfer(from, to, amount) { ... }

// Good - especially valuable in JS to document parameter shapes
/**
 * @param {Object} options
 * @param {string} options.title - Menu title
 * @param {string} options.body - Menu body text
 * @param {boolean} [options.cancellable=false] - Whether menu can be dismissed
 */
function createMenu({ title, body, cancellable = false }) { ... }

// Good - no comment needed for self-documenting code
function filterActiveUsers(users) {
  return users.filter(user => user.isActive);
}
```

## The Goal

The best comment is the code itself. If you need a comment to explain
what code does, refactor first, comment last.

```javascript
// Before - needs comment
// Check if user is eligible for discount
if (user.age >= 65 || user.memberSince < cutoffDate) { ... }

// After - self-documenting
if (user.isEligibleForDiscount()) { ... }
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| C1 | No metadata in comments | Author, date, ticket → use Git |
| C2 | Delete obsolete comments | Stale comment → delete immediately |
| C3 | No redundant comments | Code says it already → remove comment |
| C4 | Write comments well | Brief, precise, explains WHY not WHAT |
| C5 | No commented-out code | Dead code → delete, Git remembers |
| JSDoc | Document public APIs | `@param` types especially useful in plain JS |

## AI Behavior

When reviewing comments, cite the rule number (e.g., "C3 violation: comment restates the code").
When cleaning comments, explain the action (e.g., "Removed redundant comment, added JSDoc for public API (C3)").
