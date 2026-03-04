---
name: rust-clean-tests
description: Use when writing, fixing, editing, or refactoring Rust tests. Enforces Clean Code principles—fast tests, boundary coverage, one concept per test, idiomatic Rust test patterns.
---

# Clean Tests (Rust)

## T1: Insufficient Tests

Test everything that could possibly break. Use coverage tools as a guide, not a goal.

```rust
// Bad — only tests happy path
#[test]
fn test_divide() {
    assert_eq!(divide(10.0, 2.0).unwrap(), 5.0);
}

// Good — tests edge cases too
#[test]
fn divide_normal() {
    assert_eq!(divide(10.0, 2.0).unwrap(), 5.0);
}

#[test]
fn divide_by_zero_returns_error() {
    assert!(matches!(divide(10.0, 0.0), Err(MathError::DivisionByZero)));
}

#[test]
fn divide_negative() {
    assert_eq!(divide(-10.0, 2.0).unwrap(), -5.0);
}
```

## T2: Use a Coverage Tool

```bash
# cargo-tarpaulin
cargo tarpaulin --out Html

# cargo-llvm-cov
cargo llvm-cov --html
```

## T3: Don't Skip Trivial Tests

Trivial tests document behavior and catch regressions.

```rust
#[test]
fn user_default_role_is_member() {
    let user = User::new("Alice");
    assert_eq!(user.role(), Role::Member);
}
```

## T4: An Ignored Test Is a Question About an Ambiguity

Don't use `#[ignore]` to hide problems. Either fix the test or delete it.

```rust
// Bad — hiding a problem
#[test]
#[ignore = "flaky, fix later"]
fn test_async_operation() { ... }

// Good — documents a real constraint
#[test]
#[ignore = "requires Redis; run with --include-ignored"]
fn test_cache_invalidation() { ... }
```

## T5: Test Boundary Conditions

Bugs congregate at boundaries. Test them explicitly.

```rust
#[test]
fn paginate_boundaries() {
    let items: Vec<i32> = (0..100).collect();

    assert_eq!(paginate(&items, 1, 10).unwrap().len(), 10);   // first page
    assert_eq!(paginate(&items, 10, 10).unwrap().len(), 10);  // last page
    assert!(paginate(&items, 11, 10).unwrap().is_empty());    // beyond last
    assert!(paginate(&items, 0, 10).is_err());                // invalid page
    assert!(paginate(&[], 1, 10).unwrap().is_empty());        // empty input
}
```

## T6: Exhaustively Test Near Bugs

When you find a bug, write tests for all similar cases. Bugs cluster.

## T7: Patterns of Failure Are Revealing

When tests fail, look for patterns. They often point to deeper issues.

## T8: Test Coverage Patterns Can Be Revealing

Untested code paths often reveal design problems.

## T9: Tests Should Be Fast

Slow tests don't get run. Keep unit tests under 100ms each.

```rust
// Bad — hits real database
#[test]
fn test_user_creation() {
    let db = connect_to_database(); // Slow!
    // ...
}

// Good — uses trait mock
#[test]
fn test_user_creation() {
    let repo = MockUserRepo::new();
    let svc = UserService::new(Box::new(repo));
    // ...
}
```

## Test Organization

### Module Tests

```rust
// In src/order.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn order_total_sums_items() {
        let order = Order::new(vec![
            Item { price: 100.0 },
            Item { price: 200.0 },
        ]);
        assert_eq!(order.total(), 300.0);
    }
}
```

### Test Naming Convention

Use `<function>_<scenario>_<expected>` pattern.

```rust
#[test]
fn find_by_email_existing_user_returns_user() { ... }

#[test]
fn find_by_email_unknown_returns_none() { ... }

#[test]
fn transfer_insufficient_funds_returns_error() { ... }
```

### Test Helpers

```rust
// In tests/common/mod.rs or as helper functions
fn sample_order() -> Order {
    Order::new(vec![
        Item { name: "Widget".into(), price: 10.0 },
        Item { name: "Gadget".into(), price: 20.0 },
    ])
}

fn assert_approx_eq(a: f64, b: f64) {
    assert!((a - b).abs() < f64::EPSILON, "{a} ≠ {b}");
}
```

## Modern Rust Test Idioms

```rust
// Parameterized tests with macro
macro_rules! test_parse_size {
    ($name:ident, $input:expr, $expected:expr) => {
        #[test]
        fn $name() {
            assert_eq!(parse_size($input).unwrap(), $expected);
        }
    };
}

test_parse_size!(parse_bytes, "100B", 100);
test_parse_size!(parse_kilobytes, "1KB", 1024);
test_parse_size!(parse_megabytes, "5MB", 5 * 1024 * 1024);

// rstest for data-driven tests (popular crate)
use rstest::rstest;

#[rstest]
#[case("100B", 100)]
#[case("1KB", 1024)]
#[case("5MB", 5 * 1024 * 1024)]
fn test_parse_size(#[case] input: &str, #[case] expected: u64) {
    assert_eq!(parse_size(input).unwrap(), expected);
}

// rstest fixtures for shared setup
#[rstest]
fn test_order_discount(#[fixture] sample_order: Order) {
    let discounted = apply_discount(&sample_order, 0.1);
    assert_eq!(discounted.total(), 27.0);
}

// assert_matches! for pattern matching (nightly or assert_matches crate)
use assert_matches::assert_matches;

#[test]
fn parse_invalid_returns_error() {
    assert_matches!(parse("invalid"), Err(ParseError::InvalidFormat { .. }));
}

// proptest for property-based testing
use proptest::prelude::*;

proptest! {
    #[test]
    fn addition_is_commutative(a in 0i64..1000, b in 0i64..1000) {
        assert_eq!(add(a, b), add(b, a));
    }
}

// Doc-tests as living examples (run with cargo test)
/// ```
/// # use mylib::add;
/// assert_eq!(add(2, 3), 5);
/// ```
fn add(a: i64, b: i64) -> i64 { a + b }

// tokio::test for async tests
#[tokio::test]
async fn fetch_order_returns_data() {
    let client = TestClient::new().await;
    let order = client.fetch_order("123").await.unwrap();
    assert_eq!(order.id, "123");
}
```

## Quick Reference

| Rule | Principle |
|------|-----------|
| T1 | Test everything that could break |
| T2 | Use coverage tools (`cargo tarpaulin` / `cargo llvm-cov`) |
| T3 | Don't skip trivial tests |
| T4 | Ignored test = ambiguity question |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Look for patterns in failures |
| T8 | Check coverage when debugging |
| T9 | Tests must be fast (<100ms) |

## AI Behavior

When reviewing tests, cite the rule number (e.g., "T5 violation: no boundary condition tests").
When writing tests, prefer `rstest` or macro-based parameterized tests for multiple cases.
Use `#[cfg(test)]` module pattern for unit tests, `tests/` directory for integration tests.

