---
name: rust-clean-comments
description: Use when writing, fixing, editing, or reviewing Rust comments and rustdoc. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code.
---

# Clean Comments (Rust)

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history, and dates.

```rust
// Bad — metadata belongs in Git
// Author: John Doe
// Created: 2024-01-15
// Ticket: JIRA-1234
struct OrderService { ... }

// Good — only technical documentation
/// Processes orders by validating inventory, calculating totals,
/// and dispatching to the fulfillment system.
struct OrderService { ... }
```

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists, delete it immediately.

## C3: No Redundant Comments

```rust
// Bad — the code already says this
let count = items.len(); // get the length of items

// Good — explains WHY, not WHAT
let count = items.len(); // cached to avoid repeated traversal
```

## C4: Write Comments Well

If a comment is worth writing, write it well: be brief, precise, and explain WHY not WHAT.

## C5: Never Commit Commented-Out Code

```rust
// DELETE THIS — Git remembers everything
// fn old_calculate_tax(income: f64) -> f64 {
//     income * 0.15
// }
```

## Rustdoc Best Practices

Rust uses `///` for item documentation and `//!` for module-level docs. Rustdoc supports Markdown and auto-generates from code examples.

### Module Documentation

```rust
//! # Order Processing
//!
//! This module handles the order lifecycle from creation
//! through fulfillment, coordinating inventory and payment.

mod order_processing;
```

### Struct and Enum Documentation

```rust
/// A customer order containing one or more items.
///
/// Orders progress through states: `Pending` → `Confirmed` → `Shipped`.
/// Use [`OrderService::submit`] to begin processing.
#[derive(Debug, Clone)]
struct Order {
    /// Unique identifier assigned at creation.
    id: OrderId,
    /// Line items in this order.
    items: Vec<Item>,
}
```

### Function Documentation with Examples

```rust
/// Transfer funds between two accounts atomically.
///
/// Either both accounts are updated or neither is.
///
/// # Errors
///
/// Returns [`TransferError::InsufficientFunds`] if the source
/// balance is too low.
///
/// # Examples
///
/// ```
/// let result = transfer_funds(&from, &to, 100.0)?;
/// assert_eq!(result.new_balance, 900.0);
/// ```
fn transfer_funds(
    from: &Account,
    to: &Account,
    amount: f64,
) -> Result<TransferResult, TransferError> {
    // ...
}
```

### When Documentation Is Unnecessary

```rust
// Types are clear — doc adds no value. Skip it.
fn is_active(&self) -> bool {
    self.status == Status::Active
}

// Complex business logic — doc explains the rule.
/// Returns true if the user has been a member for 2+ years
/// OR has spent more than $1000 in the last 90 days.
fn is_eligible_for_discount(&self) -> bool {
    // ...
}
```

## The Goal

The best comment is clear code itself. Refactor first, comment last.

```rust
// Bad — comment needed to explain intent
// Check if eligible for premium discount
if user.years >= 2 && user.total_spent > 1000.0 {
    apply_discount(&user);
}

// Good — self-documenting code
if user.is_eligible_for_premium_discount() {
    apply_discount(&user);
}
```

## Modern Rust Comment Idioms

### `#[deprecated]` Replaces "Deprecated" Comments

```rust
// Bad — comment that tooling can't enforce
/// Deprecated: use `new_api()` instead.
fn old_api() { ... }

// Good — compiler warns on usage
#[deprecated(since = "2.0.0", note = "Use new_api() instead")]
fn old_api() { ... }
```

### `#[must_use]` Documents Ignored Return Values

```rust
// Bad — comment about checking return value
/// Important: check the returned Result!
fn process() -> Result<(), Error> { ... }

// Good — compiler enforces it
#[must_use = "this Result must be handled"]
fn process() -> Result<(), Error> { ... }
```

### Safety Comments for `unsafe`

```rust
// SAFETY comments are REQUIRED for unsafe blocks
unsafe {
    // SAFETY: `ptr` is valid because it was just allocated by `alloc`
    // and has not been freed. The alignment is guaranteed by `Layout`.
    ptr::write(ptr, value);
}
```

### Doc-Test Examples as Living Documentation

Use `?` instead of `unwrap()` in doc examples — it teaches proper error handling and readers copy-paste examples (Rust API Guidelines: C-EXAMPLE).

```rust
/// Parses a size string into bytes.
///
/// ```
/// # use mylib::parse_size;
/// assert_eq!(parse_size("1KB")?, 1024);
/// assert_eq!(parse_size("5MB")?, 5 * 1024 * 1024);
/// assert!(parse_size("invalid").is_err());
/// # Ok::<(), mylib::ParseError>(())
/// ```
fn parse_size(input: &str) -> Result<u64, ParseError> { ... }
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| C1 | No metadata in comments | Author, date, ticket → use Git |
| C2 | Delete obsolete comments | Stale comment → delete immediately |
| C3 | No redundant comments | Code says it already → remove comment |
| C4 | Write comments well | Brief, precise, explains WHY not WHAT |
| C5 | No commented-out code | Dead code → delete, Git remembers |
| RS8 | Document `unsafe` invariants | `// SAFETY:` comments are mandatory |

## AI Behavior

When reviewing comments, cite the rule number (e.g., "C3 violation: redundant comment restates the code").
When cleaning comments, explain the action (e.g., "Removed metadata comment, use Git for author tracking (C1)").
For rustdoc, ensure `///` starts with a brief summary sentence. Include `# Errors`, `# Panics`, `# Examples` sections where appropriate.
