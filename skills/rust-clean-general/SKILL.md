---
name: rust-clean-general
description: Use when writing, fixing, editing, or reviewing Rust code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles (Rust)

## Critical Rules

### G5: DRY (Don't Repeat Yourself)

Every piece of knowledge has one authoritative representation.

```rust
// Bad — duplication
fn calc_ca_tax(subtotal: f64) -> f64 { subtotal * 1.0825 }
fn calc_ny_tax(subtotal: f64) -> f64 { subtotal * 1.07 }

// Good — single source of truth
use std::collections::HashMap;

fn tax_rates() -> HashMap<&'static str, f64> {
    [("CA", 0.0825), ("NY", 0.07)].into()
}

fn calculate_total(subtotal: f64, state: &str) -> f64 {
    let rates = tax_rates();
    subtotal * (1.0 + rates.get(state).copied().unwrap_or(0.0))
}
```

### G16: No Obscured Intent

Don't be clever. Be clear.

```rust
// Bad — what does this do?
(x & 0x0F) << 4 | (y & 0x0F)

// Good — obvious intent
pack_coordinates(x, y)
```

### G23: Prefer Polymorphism (Traits) to Match on Type

```rust
// Bad — will grow forever
fn calculate_pay(emp: &Employee) -> f64 {
    match emp.kind {
        EmployeeKind::Salaried => emp.salary,
        EmployeeKind::Hourly => emp.hours as f64 * emp.rate,
        EmployeeKind::Commissioned => emp.base + emp.commission,
    }
}

// Good — open/closed principle via traits
trait PayCalculator {
    fn calculate_pay(&self) -> f64;
}

struct SalariedEmployee { salary: f64 }
impl PayCalculator for SalariedEmployee {
    fn calculate_pay(&self) -> f64 { self.salary }
}

struct HourlyEmployee { hours: u32, rate: f64 }
impl PayCalculator for HourlyEmployee {
    fn calculate_pay(&self) -> f64 { self.hours as f64 * self.rate }
}
```

### G25: Replace Magic Numbers with Named Constants

```rust
// Bad
if elapsed_time > 86400 {
    // ...
}

// Good
const SECONDS_PER_DAY: u64 = 86400;
if elapsed_time > SECONDS_PER_DAY {
    // ...
}
```

### G30: Functions Should Do One Thing

If you can extract another function, your function does more than one thing.

### G36: Law of Demeter (Avoid Train Wrecks)

```rust
// Bad — reaching through multiple objects
let path = context.options.scratch_dir.absolute_path();

// Good — one level of access
let path = context.scratch_dir_path();
```

## Enforcement Checklist

When reviewing AI-generated code, verify:

- [ ] No duplication (G5)
- [ ] Clear intent, no magic numbers (G16, G25)
- [ ] Traits over match on type (G23)
- [ ] Functions do one thing (G30)
- [ ] No Law of Demeter violations (G36)
- [ ] Boundary conditions handled (G3)
- [ ] Dead code removed (G9)
- [ ] Borrowing over cloning (RS1)
- [ ] `Result`/`Option` instead of panic (RS2)
- [ ] `cargo clippy` clean (RS5)

## Modern Rust Idioms

```rust
// Enum variants for exhaustive state machines
#[derive(Debug)]
enum OrderState {
    Pending,
    Confirmed { confirmed_at: DateTime<Utc> },
    Shipped { tracking: String },
    Delivered { delivered_at: DateTime<Utc> },
    Cancelled { reason: String },
}

impl OrderState {
    fn can_cancel(&self) -> bool {
        matches!(self, OrderState::Pending | OrderState::Confirmed { .. })
    }
}

// Type-state pattern for compile-time correctness
struct Unlocked;
struct Locked;

struct Door<State> {
    _state: std::marker::PhantomData<State>,
}

impl Door<Locked> {
    fn unlock(self) -> Door<Unlocked> { Door { _state: PhantomData } }
}

impl Door<Unlocked> {
    fn lock(self) -> Door<Locked> { Door { _state: PhantomData } }
    fn open(&self) { println!("Door opened"); }
}

// G28: Encapsulate conditionals
impl Subscription {
    fn is_active(&self) -> bool {
        self.expires_at > Utc::now()
    }

    fn is_premium(&self) -> bool {
        self.plan == Plan::Premium && self.is_active()
    }
}

// Newtype pattern to prevent mixing IDs
struct UserId(Uuid);
struct OrderId(Uuid);
// fn find_order(id: OrderId) — can't accidentally pass UserId

// Error propagation with context (anyhow)
use anyhow::Context;

fn load_config(path: &Path) -> anyhow::Result<Config> {
    let content = fs::read_to_string(path)
        .with_context(|| format!("failed to read config from {}", path.display()))?;
    let config: Config = toml::from_str(&content)
        .context("failed to parse config")?;
    Ok(config)
}
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| G3 | Handle boundary conditions | Edge cases, `None`, empty `Vec` |
| G5 | DRY — no duplication | Single source of truth |
| G9 | Delete dead code | Unused imports, unreachable branches |
| G16 | No obscured intent | Extract to well-named function |
| G23 | Traits over match on type | Growing match arms |
| G25 | Named constants, no magic numbers | `SECONDS_PER_DAY = 86400` |
| G30 | Functions do one thing | Can you extract another function? |
| G36 | Law of Demeter | Max one dot per expression |

## AI Behavior

When reviewing code quality, cite the rule number (e.g., "G25 violation: magic number `86400`").
When refactoring, explain the improvement (e.g., "Extracted constant `SECONDS_PER_DAY = 86400` (G25)").
When applying Modern Rust idioms, check `Cargo.toml` for edition (2018/2021/2024) and dependencies. Default to Edition 2021.

