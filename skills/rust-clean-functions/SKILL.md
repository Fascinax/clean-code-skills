---
name: rust-clean-functions
description: Use when writing, fixing, editing, or refactoring Rust functions. Enforces Clean Code principles—maximum 3 arguments, single responsibility, no flag parameters.
---

# Clean Functions (Rust)

## F1: Maximum 3 Arguments

More than 3 arguments? Use a config struct or builder pattern.

```rust
// Bad — too many arguments
fn create_user(
    name: &str, email: &str, role: Role, age: u32, active: bool,
) -> Result<User, CreateError> {
    // ...
}

// Good — config struct
struct CreateUserRequest {
    name: String,
    email: String,
    role: Role,
    age: u32,
    active: bool,
}

fn create_user(req: CreateUserRequest) -> Result<User, CreateError> {
    // ...
}
```

## F2: No Output Arguments

Return values instead of taking `&mut` for output.

```rust
// Bad — output argument
fn populate_defaults(cfg: &mut Config) {
    cfg.timeout = Duration::from_secs(30);
    cfg.retries = 3;
}

// Good — return a new value
fn with_defaults(cfg: Config) -> Config {
    Config {
        timeout: Duration::from_secs(30),
        retries: 3,
        ..cfg
    }
}
```

## F3: No Flag Arguments

Split into separate functions.

```rust
// Bad — flag argument
fn format_output(data: &[u8], pretty: bool) -> String {
    if pretty { format_pretty(data) } else { format_compact(data) }
}

// Good — separate functions
fn format_pretty(data: &[u8]) -> String { ... }
fn format_compact(data: &[u8]) -> String { ... }
```

## F4: Delete Dead Functions

Functions with no callers? Delete them. `cargo clippy` warns about unused code. `#[allow(dead_code)]` is a smell.

## Modern Rust Function Idioms

```rust
// Builder pattern for complex construction (F1 alternative)
struct ServerConfig {
    port: u16,
    host: String,
    workers: usize,
    tls: bool,
}

impl ServerConfig {
    fn builder() -> ServerConfigBuilder {
        ServerConfigBuilder::default()
    }
}

#[derive(Default)]
struct ServerConfigBuilder {
    port: Option<u16>,
    host: Option<String>,
    workers: Option<usize>,
    tls: Option<bool>,
}

impl ServerConfigBuilder {
    fn port(mut self, port: u16) -> Self { self.port = Some(port); self }
    fn host(mut self, host: impl Into<String>) -> Self { self.host = Some(host.into()); self }
    fn build(self) -> ServerConfig {
        ServerConfig {
            port: self.port.unwrap_or(8080),
            host: self.host.unwrap_or_else(|| "localhost".into()),
            workers: self.workers.unwrap_or(4),
            tls: self.tls.unwrap_or(false),
        }
    }
}

// Usage
let config = ServerConfig::builder()
    .port(9090)
    .host("0.0.0.0")
    .build();

// Guard clauses — handle errors early, keep happy path unindented
fn process_order(order: &Order) -> Result<Receipt, OrderError> {
    if !order.is_valid() {
        return Err(OrderError::Invalid);
    }
    if order.total() == 0.0 {
        return Err(OrderError::Empty);
    }

    // Happy path
    let receipt = charge(order)?;
    send_confirmation(&receipt)?;
    Ok(receipt)
}

// impl Trait in argument position — accept any type implementing a trait
fn log_message(writer: &mut impl Write, msg: &str) -> io::Result<()> {
    writeln!(writer, "[LOG] {msg}")
}

// Closures for higher-order functions
fn apply_discount(items: &[Item], rate: f64) -> Vec<Item> {
    items.iter()
        .map(|item| Item {
            price: item.price * (1.0 - rate),
            ..item.clone()
        })
        .collect()
}

// Struct update syntax for partial modifications
fn with_premium(user: User) -> User {
    User {
        plan: Plan::Premium,
        upgraded_at: Some(Utc::now()),
        ..user
    }
}

// From/Into for type conversions instead of ad-hoc functions
impl From<CreateUserRequest> for User {
    fn from(req: CreateUserRequest) -> Self {
        Self {
            name: req.name,
            email: req.email,
            role: req.role,
            ..Default::default()
        }
    }
}
```

## Quick Reference

| Rule | Principle | Rust Idiom |
|------|-----------|------------|
| F1 | Max 3 arguments | Config struct or builder pattern |
| F2 | No output arguments | Return values, struct update syntax |
| F3 | No flag arguments | Split into separate functions |
| F4 | Delete dead functions | `cargo clippy` catches unused code |

## AI Behavior

When reviewing functions, cite the rule number (e.g., "F1 violation: 5 arguments, use config struct").
When refactoring, explain the improvement (e.g., "Extracted `validate_order` from `process_order` (G30)").
Prefer builder pattern for constructors with 4+ optional fields.
