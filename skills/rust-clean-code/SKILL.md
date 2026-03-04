---
name: rust-clean-code
description: Use when writing, fixing, editing, reviewing, or refactoring any Rust code. Enforces Robert Martin's complete Clean Code catalog—naming, functions, comments, DRY, and boundary conditions—adapted for Rust.
---

# Clean Rust: Complete Reference

Enforces all Clean Code principles from Robert C. Martin's Chapter 17, adapted for Rust.

## Comments (C1-C5)

- C1: No metadata in comments (use Git)
- C2: Delete obsolete comments immediately
- C3: No redundant comments
- C4: Write comments well if you must
- C5: Never commit commented-out code

## Environment (E1-E2)

- E1: One command to build (`cargo build`)
- E2: One command to test (`cargo test`)

## Functions (F1-F4)

- F1: Maximum 3 arguments (use struct or builder for more)
- F2: No output arguments (return values, use `&mut` sparingly)
- F3: No flag arguments (split functions)
- F4: Delete dead functions

## General (G1-G36)

- G1: One language per file
- G2: Implement expected behavior
- G3: Handle boundary conditions
- G4: Don't override safeties (don't reach for `unsafe`)
- G5: DRY — no duplication
- G6: Consistent abstraction levels
- G7: Base traits don't know implementors
- G8: Minimize public interface (`pub` only when needed)
- G9: Delete dead code (`#[allow(dead_code)]` is a smell)
- G10: Variables near usage
- G11: Be consistent
- G12: Remove clutter
- G13: No artificial coupling
- G14: No feature envy
- G15: No selector arguments
- G16: No obscured intent
- G17: Code where expected
- G18: Prefer methods on types
- G19: Use explanatory variables
- G20: Function names say what they do
- G21: Understand the algorithm
- G22: Make dependencies physical (explicit in `Cargo.toml`)
- G23: Prefer polymorphism (traits) to match on type
- G24: Follow conventions (`cargo fmt`, `cargo clippy`, Rust API Guidelines)
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

## Rust-Specific (RS1-RS8)

- RS1: Prefer borrowing over cloning — `&T` and `&mut T` before `Clone`
- RS2: Use `Result`/`Option` — never `panic!` in library code
- RS3: Derive standard traits (`Debug`, `Clone`, `PartialEq`, `Default`) when applicable
- RS4: Use iterators over manual loops — `.map()`, `.filter()`, `.collect()`
- RS5: Run `cargo clippy` — treat warnings as errors
- RS6: Exhaustive pattern matching — no wildcard `_` on enums (catch breaking changes)
- RS7: Use `thiserror` for library errors, `anyhow` for application errors
- RS8: Minimize `unsafe` — document invariants when unavoidable
- RS9: Implement `Send` + `Sync` where safe — enables use across threads (Rust API Guidelines: C-SEND-SYNC)

## Names (N1-N7)

- N1: Choose descriptive names
- N2: Right abstraction level
- N3: Use standard nomenclature (`snake_case` functions, `PascalCase` types, `SCREAMING_SNAKE` constants)
- N4: Unambiguous names
- N5: Name length matches scope
- N6: No encodings (no Hungarian notation, no `I` prefix on traits)
- N7: Names describe side effects

## Tests (T1-T9)

- T1: Test everything that could break
- T2: Use coverage tools (`cargo tarpaulin` or `cargo llvm-cov`)
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
| **Functions** | F1 | Max 3 arguments (use struct/builder) |
| | F3 | No flag arguments |
| | F4 | Delete dead functions |
| **General** | G5 | DRY — no duplication |
| | G9 | Delete dead code |
| | G16 | No obscured intent |
| | G23 | Traits over match on type |
| | G25 | Named constants, not magic numbers |
| | G30 | Functions do one thing |
| | G36 | Law of Demeter (one dot) |
| **Rust** | RS1 | Borrow before clone |
| | RS2 | `Result`/`Option`, never panic |
| | RS4 | Iterators over manual loops |
| | RS5 | `cargo clippy` — zero warnings |
| | RS7 | `thiserror` / `anyhow` for errors |
| **Names** | N1 | Descriptive names |
| | N5 | Name length matches scope |
| **Tests** | T5 | Test boundary conditions |
| | T9 | Tests must be fast |

## Anti-Patterns (Don't → Do)

| Don't | Do |
|-------|-----|
| `.clone()` everywhere | Borrow with `&T` / `&mut T` |
| `panic!("unexpected")` in libs | Return `Result<T, E>` |
| `unwrap()` in production code | `?` operator or `unwrap_or_default()` |
| Manual `for` loop to build vec | `.iter().map().collect()` |
| Wildcard `_` on enums | Match all variants exhaustively |
| `#[allow(dead_code)]` | Delete unused code |
| Stringly-typed errors | `thiserror` derive or custom error enum |
| `unsafe` without invariant doc | Document safety, minimize scope |
| Magic number `86400` | `const SECONDS_PER_DAY: u64 = 86400` |
| `Box<dyn Error>` in libraries | Custom error enum with `thiserror` |
| Huge `impl` block | Split into logical trait impls |

## Modern Rust Idioms

```rust
// RS1: Borrowing over cloning
fn greet(name: &str) -> String {
    format!("Hello, {name}!")
}

// RS2: Result/Option with ? operator
fn read_config(path: &Path) -> Result<Config, AppError> {
    let content = fs::read_to_string(path)?;
    let config: Config = toml::from_str(&content)?;
    Ok(config)
}

// RS3: Derive standard traits
#[derive(Debug, Clone, PartialEq, Default)]
struct Order {
    id: String,
    items: Vec<Item>,
    total: f64,
}

// RS4: Iterators over manual loops
let active_emails: Vec<&str> = users
    .iter()
    .filter(|u| u.is_active())
    .map(|u| u.email.as_str())
    .collect();

// RS6: Exhaustive pattern matching
enum Shape {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
    Triangle { base: f64, height: f64 },
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle { radius } => std::f64::consts::PI * radius.powi(2),
        Shape::Rectangle { width, height } => width * height,
        Shape::Triangle { base, height } => 0.5 * base * height,
    }
}

// RS7: thiserror for library errors
#[derive(Debug, thiserror::Error)]
enum OrderError {
    #[error("order {id} not found")]
    NotFound { id: String },
    #[error("insufficient stock for item {item_id}")]
    InsufficientStock { item_id: String },
    #[error(transparent)]
    Database(#[from] sqlx::Error),
}

// Builder pattern for complex construction
struct ServerBuilder {
    port: u16,
    host: String,
    workers: usize,
}

impl ServerBuilder {
    fn new() -> Self {
        Self { port: 8080, host: "localhost".into(), workers: 4 }
    }
    fn port(mut self, port: u16) -> Self { self.port = port; self }
    fn host(mut self, host: impl Into<String>) -> Self { self.host = host.into(); self }
    fn build(self) -> Server { Server { /* ... */ } }
}

// Newtype pattern for type safety
struct UserId(String);
struct OrderId(String);
// Can't accidentally pass UserId where OrderId is expected
```

## AI Behavior

When reviewing code, identify violations by rule number (e.g., "RS2 violation: `unwrap()` in library code").
When fixing or editing code, report what was fixed (e.g., "Fixed: replaced `clone()` with borrow (RS1)").
Before applying Modern Rust idioms, check `Cargo.toml` for the Rust edition (2018, 2021, 2024) and dependency versions. Edition 2021: default. Edition 2024: new `use` rules. Default to Edition 2021 if no signal found.

