---
name: rust-clean-names
description: Use when naming, renaming, or fixing names of variables, functions, types, or modules in Rust. Enforces Clean Code principles—descriptive names, appropriate length, no encodings.
---

# Clean Names (Rust)

## N1: Choose Descriptive Names

Names should reveal intent.

```rust
// Bad — meaningless names
fn p(d: &[u8]) -> Result<(), E> {
    for b in d {
        if *b > t { return Err(e); }
    }
    Ok(())
}

// Good — descriptive
fn validate_payload(data: &[u8]) -> Result<(), ValidationError> {
    for &byte in data {
        if byte > MAX_BYTE_VALUE {
            return Err(ValidationError::InvalidByte(byte));
        }
    }
    Ok(())
}
```

## N2: Names at Appropriate Abstraction Level

```rust
// Bad — implementation detail in the name
fn read_from_postgresql(id: &str) -> Result<User, DbError>

// Good — abstracts the storage mechanism
fn find_user(id: &str) -> Result<User, RepoError>
```

## N3: Use Standard Nomenclature

Rust conventions: `snake_case` functions/variables, `PascalCase` types/traits, `SCREAMING_SNAKE` constants.

```rust
// Bad — violates Rust naming conventions
struct order_service;       // should be PascalCase
fn ProcessOrder() {}        // should be snake_case
const max_retries: u32 = 3; // should be SCREAMING_SNAKE

// Good — idiomatic Rust
struct OrderService;
fn process_order() {}
const MAX_RETRIES: u32 = 3;
```

## N4: Unambiguous Names

```rust
// Bad — what does "handle" mean here?
fn handle(req: &Request) -> Response

// Good — specific action
fn validate_and_route(req: &Request) -> Response
```

## N5: Name Length Matches Scope

Short names for short scopes, descriptive names for wide scopes.

```rust
// Good — short names in tight scopes
items.iter().filter(|x| x.is_active())
for (i, v) in values.iter().enumerate() { ... }

// Good — descriptive names in wider scopes
struct TransactionProcessor {
    repository: Box<dyn TransactionRepository>,
    event_publisher: Box<dyn EventPublisher>,
}
```

## N6: No Encodings

```rust
// Bad — type encodings and prefixes
trait IOrderRepository {}
let str_name: String = ...;
let n_count: usize = ...;

// Good — no prefixes, no type encodings
trait OrderRepository {}
let name: String = ...;
let count: usize = ...;
```

## N7: Names Describe Side Effects

```rust
// Bad — hides side effect
fn get_connection() -> Connection {
    // connects to database!
}

// Good — name reveals behavior
fn open_connection() -> Result<Connection, DbError> {
    // ...
}
```

## Modern Rust Naming Idioms

```rust
// Conversion methods follow C-CONV (Rust API Guidelines):
// as_  — free, borrowed→borrowed (&self → &T)
// to_  — expensive, borrowed→owned (&self → T)
// into_— owned→owned (self → T), consumes the value
impl Temperature {
    fn as_celsius(&self) -> f64 { ... }       // cheap borrow→borrow
    fn to_string(&self) -> String { ... }     // expensive borrow→owned
    fn into_inner(self) -> f64 { ... }        // consumes self
}

// C-WORD-ORDER: types named verb-object-error (Rust API Guidelines)
// Good: ParseIntError, ReadDirError
// Bad: IntParseError, DirReadError

// Constructor: new (returns Self)
impl OrderService {
    fn new(repo: Box<dyn OrderRepository>) -> Self {
        Self { repo }
    }
}

// Fallible constructor: try_new or new returning Result
impl Config {
    fn try_new(path: &Path) -> Result<Self, ConfigError> { ... }
}

// Boolean methods: is_, has_, can_
impl User {
    fn is_active(&self) -> bool { ... }
    fn has_permission(&self, perm: Permission) -> bool { ... }
    fn can_edit(&self, resource: &Resource) -> bool { ... }
}

// Getter: field name without get_ prefix (Rust convention)
impl User {
    fn name(&self) -> &str { &self.name }        // not get_name()
    fn set_name(&mut self, name: String) { self.name = name; }
}

// Iterator methods: iter, iter_mut, into_iter
impl OrderBook {
    fn iter(&self) -> impl Iterator<Item = &Order> { ... }
    fn iter_mut(&mut self) -> impl Iterator<Item = &mut Order> { ... }
}

// Error types: Error suffix
#[derive(Debug, thiserror::Error)]
enum ParseError {
    #[error("invalid token at position {pos}")]
    InvalidToken { pos: usize },
}

// Module names: snake_case, descriptive
mod order_processing;  // not: mod utils, mod helpers
mod payment_gateway;
```

## Quick Reference

| Rule | Principle | Rust Idiom |
|------|-----------|------------|
| N1 | Descriptive names | Reveal intent, short in closures |
| N2 | Right abstraction level | No impl details in names |
| N3 | Standard nomenclature | `snake_case` fns, `PascalCase` types, `SCREAMING_SNAKE` consts |
| N4 | Unambiguous names | Specific verbs over generic "handle/process" |
| N5 | Length matches scope | `x` in closures, `TransactionProcessor` for structs |
| N6 | No encodings | No `I` prefix on traits |
| N7 | Describe side effects | `open_connection`, not `get_connection` |

## AI Behavior

When reviewing names, cite the rule number (e.g., "N3 violation: use `PascalCase` for types").
When renaming, explain the change (e.g., "Renamed `proc` → `process_order` for clarity (N1)").
Follow Rust conventions: `as_`/`to_`/`into_` conversions, no `get_` prefix on getters, `is_`/`has_` for booleans.

