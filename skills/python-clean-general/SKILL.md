---
name: python-clean-general
description: Use when writing, fixing, editing, or reviewing Python code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles

## Critical Rules

### G5: DRY (Don't Repeat Yourself)

Every piece of knowledge has one authoritative representation.

```python
# Bad - duplication
tax_rate = 0.0825
ca_total = subtotal * 1.0825
ny_total = subtotal * 1.07

# Good - single source of truth
TAX_RATES = {"CA": 0.0825, "NY": 0.07}
def calculate_total(subtotal: float, state: str) -> float:
    return subtotal * (1 + TAX_RATES[state])
```

### G16: No Obscured Intent

Don't be clever. Be clear.

```python
# Bad - what does this do?
return (x & 0x0F) << 4 | (y & 0x0F)

# Good - obvious intent
return pack_coordinates(x, y)
```

### G23: Prefer Polymorphism to If/Else

```python
# Bad - will grow forever
def calculate_pay(employee):
    if employee.type == "SALARIED":
        return employee.salary
    elif employee.type == "HOURLY":
        return employee.hours * employee.rate
    elif employee.type == "COMMISSIONED":
        return employee.base + employee.commission

# Good - open/closed principle
class SalariedEmployee:
    def calculate_pay(self): return self.salary

class HourlyEmployee:
    def calculate_pay(self): return self.hours * self.rate

class CommissionedEmployee:
    def calculate_pay(self): return self.base + self.commission
```

### G25: Replace Magic Numbers with Named Constants

```python
# Bad
if elapsed_time > 86400:
    ...

# Good
SECONDS_PER_DAY = 86400
if elapsed_time > SECONDS_PER_DAY:
    ...
```

### G30: Functions Should Do One Thing

If you can extract another function, your function does more than one thing.

### G36: Law of Demeter (Avoid Train Wrecks)

```python
# Bad - reaching through multiple objects
output_dir = context.options.scratch_dir.absolute_path

# Good - one dot
output_dir = context.get_scratch_dir()
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
- [ ] No wildcard imports (P1)
- [ ] Enums instead of magic constants (P2)
- [ ] Type hints on public interfaces (P3)

## Modern Python Idioms

```python
# Context managers for resource handling
from contextlib import contextmanager

@contextmanager
def managed_connection(url: str):
    conn = create_connection(url)
    try:
        yield conn
    finally:
        conn.close()

# Protocol for structural subtyping (Python 3.8+)
from typing import Protocol

class Repository(Protocol):
    def find_by_id(self, id: int) -> Model | None: ...
    def save(self, entity: Model) -> Model: ...

# Any class with these methods satisfies Repository — no inheritance needed
class InMemoryRepo:
    def find_by_id(self, id: int) -> Model | None: ...
    def save(self, entity: Model) -> Model: ...

# Frozen dataclass for immutability
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

# Comprehensions over imperative loops
# Bad — imperative accumulation
result = []
for item in items:
    if item.is_valid():
        result.append(item.value)

# Good — declarative intent
result = [item.value for item in items if item.is_valid()]

# Mutable default argument trap
# Bad — shared mutable default
def append_to(element, target=[]):  # noqa: B006
    target.append(element)
    return target  # Surprising: target persists across calls!

# Good — use None sentinel
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

# G28: Encapsulate conditionals with @property
class User:
    @property
    def is_eligible_for_discount(self) -> bool:
        return self.tenure_years >= 2 or self.total_spent > 1000

# G23: match/case for exhaustive pattern matching (Python 3.10+)
def area(shape: Shape) -> float:
    match shape:
        case Circle(radius=r):
            return math.pi * r ** 2
        case Rectangle(width=w, height=h):
            return w * h
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| G3 | Handle boundary conditions | Edge cases, nulls, empty collections |
| G5 | DRY — no duplication | Single source of truth |
| G9 | Delete dead code | Unused imports, unreachable branches |
| G16 | No obscured intent | Extract to well-named function |
| G23 | Polymorphism over if/else | Growing conditional chains |
| G25 | Named constants, no magic numbers | `SECONDS_PER_DAY = 86400` |
| G30 | Functions do one thing | Can you extract another function? |
| G36 | Law of Demeter | Max one dot per expression |

## AI Behavior

When reviewing code quality, cite the rule number (e.g., "G25 violation: magic number `86400`").
When refactoring, explain the improvement (e.g., "Extracted constant `SECONDS_PER_DAY = 86400` (G25)").
When applying Modern Python idioms, infer the Python version from project config first (3.8+: walrus `:=`; 3.10+: `match/case`; 3.12+: `type` aliases; default: 3.8).
