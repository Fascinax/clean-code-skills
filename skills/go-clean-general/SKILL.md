---
name: go-clean-general
description: Use when writing, fixing, editing, or reviewing Go code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles (Go)

## Critical Rules

### G5: DRY (Don't Repeat Yourself)

Every piece of knowledge has one authoritative representation.

```go
// Bad — duplication
func calcCATax(subtotal float64) float64 { return subtotal * 1.0825 }
func calcNYTax(subtotal float64) float64 { return subtotal * 1.07 }

// Good — single source of truth
var taxRates = map[string]float64{"CA": 0.0825, "NY": 0.07}

func calculateTotal(subtotal float64, state string) float64 {
    return subtotal * (1 + taxRates[state])
}
```

### G16: No Obscured Intent

Don't be clever. Be clear.

```go
// Bad — what does this do?
return (x & 0x0F) << 4 | (y & 0x0F)

// Good — obvious intent
return packCoordinates(x, y)
```

### G23: Prefer Polymorphism (Interfaces) to If/Else

```go
// Bad — will grow forever
func calculatePay(emp Employee) float64 {
    switch emp.Type {
    case "salaried":
        return emp.Salary
    case "hourly":
        return float64(emp.Hours) * emp.Rate
    case "commissioned":
        return emp.Base + emp.Commission
    default:
        return 0
    }
}

// Good — open/closed principle via interfaces
type PayCalculator interface {
    CalculatePay() float64
}

type SalariedEmployee struct{ Salary float64 }
func (e SalariedEmployee) CalculatePay() float64 { return e.Salary }

type HourlyEmployee struct{ Hours int; Rate float64 }
func (e HourlyEmployee) CalculatePay() float64 { return float64(e.Hours) * e.Rate }
```

### G25: Replace Magic Numbers with Named Constants

```go
// Bad
if elapsedTime > 86400 {
    // ...
}

// Good
const secondsPerDay = 86400
if elapsedTime > secondsPerDay {
    // ...
}
```

### G30: Functions Should Do One Thing

If you can extract another function, your function does more than one thing.

### G36: Law of Demeter (Avoid Train Wrecks)

```go
// Bad — reaching through multiple objects
outputDir := ctx.Options.ScratchDir.AbsolutePath

// Good — one level of access
outputDir := ctx.ScratchDirPath()
```

## Enforcement Checklist

When reviewing AI-generated code, verify:

- [ ] No duplication (G5)
- [ ] Clear intent, no magic numbers (G16, G25)
- [ ] Interfaces over switch on type (G23)
- [ ] Functions do one thing (G30)
- [ ] No Law of Demeter violations (G36)
- [ ] Boundary conditions handled (G3)
- [ ] Dead code removed (G9)
- [ ] Errors always checked (GO3)
- [ ] `go fmt` applied (GO4)
- [ ] Interfaces are small (GO5)

## Modern Go Idioms

```go
// Context for cancellation and deadlines
func FetchData(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return nil, fmt.Errorf("create request: %w", err)
    }
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("fetch %s: %w", url, err)
    }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}

// Generics for type-safe utilities (Go 1.18+)
func Filter[T any](s []T, predicate func(T) bool) []T {
    var result []T
    for _, v := range s {
        if predicate(v) {
            result = append(result, v)
        }
    }
    return result
}

// Sentinel errors with errors.Is (Go 1.13+)
var ErrNotFound = errors.New("not found")

func FindUser(ctx context.Context, id string) (*User, error) {
    user, err := repo.Get(ctx, id)
    if errors.Is(err, sql.ErrNoRows) {
        return nil, ErrNotFound
    }
    return user, err
}

// G28: Encapsulate conditionals with methods
type Subscription struct {
    Plan      string
    ExpiresAt time.Time
}

func (s Subscription) IsActive() bool {
    return s.ExpiresAt.After(time.Now())
}

func (s Subscription) IsPremium() bool {
    return s.Plan == "premium" && s.IsActive()
}

// G23: Embed interfaces for composition
type Logger interface {
    Info(msg string, args ...any)
    Error(msg string, args ...any)
}

type MetricsCollector interface {
    RecordDuration(name string, d time.Duration)
}

type Service struct {
    Logger
    MetricsCollector
    repo Repository
}
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| G3 | Handle boundary conditions | Edge cases, nil, empty slices |
| G5 | DRY — no duplication | Single source of truth |
| G9 | Delete dead code | Unused imports, unreachable branches |
| G16 | No obscured intent | Extract to well-named function |
| G23 | Interfaces over if/else | Growing switch/case chains |
| G25 | Named constants, no magic numbers | `secondsPerDay = 86400` |
| G30 | Functions do one thing | Can you extract another function? |
| G36 | Law of Demeter | Max one dot per expression |

## AI Behavior

When reviewing code quality, cite the rule number (e.g., "G25 violation: magic number `86400`").
When refactoring, explain the improvement (e.g., "Extracted constant `secondsPerDay = 86400` (G25)").
When applying Modern Go idioms, check `go.mod` for Go version. Go 1.13+: error wrapping. Go 1.18+: generics. Go 1.21+: `slog`, `slices`, `maps`. Default to Go 1.21 if no signal found.

