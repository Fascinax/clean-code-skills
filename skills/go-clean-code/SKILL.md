---
name: go-clean-code
description: Use when writing, fixing, editing, reviewing, or refactoring any Go code. Enforces Robert Martin's complete Clean Code catalog—naming, functions, comments, DRY, and boundary conditions—adapted for Go.
---

# Clean Go: Complete Reference

Enforces all Clean Code principles from Robert C. Martin's Chapter 17, adapted for Go.

## Comments (C1-C5)

- C1: No metadata in comments (use Git)
- C2: Delete obsolete comments immediately
- C3: No redundant comments
- C4: Write comments well if you must
- C5: Never commit commented-out code

## Environment (E1-E2)

- E1: One command to build (`go build ./...`)
- E2: One command to test (`go test ./...`)

## Functions (F1-F4)

- F1: Maximum 3 arguments (use struct for more)
- F2: No output arguments (return values instead)
- F3: No flag arguments (split functions)
- F4: Delete dead functions

## General (G1-G36)

- G1: One language per file
- G2: Implement expected behavior
- G3: Handle boundary conditions
- G4: Don't override safeties
- G5: DRY — no duplication
- G6: Consistent abstraction levels
- G7: Base types don't know implementations
- G8: Minimize public interface (unexported by default)
- G9: Delete dead code
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
- G22: Make dependencies physical
- G23: Prefer polymorphism (interfaces) to if/else
- G24: Follow conventions (`go fmt`, `go vet`, Effective Go)
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

## Go-Specific (GO1-GO8)

- GO1: Exported names are PascalCase, unexported are camelCase — no underscores
- GO2: Accept interfaces, return structs
- GO3: Always check errors — wrap with `fmt.Errorf("...: %w", err)`
- GO4: `go fmt` is non-negotiable — never argue about formatting
- GO5: Keep interfaces small (1-2 methods) — `io.Reader`, not `io.Everything`
- GO6: Use `defer` for cleanup — files, locks, connections
- GO7: Goroutine safety — use `context.Context` for cancellation, never leak goroutines
- GO8: Table-driven tests — the idiomatic Go test pattern

## Names (N1-N7)

- N1: Choose descriptive names
- N2: Right abstraction level
- N3: Use standard nomenclature (PascalCase exported, camelCase local, acronyms all-caps: `HTTPClient`)
- N4: Unambiguous names
- N5: Name length matches scope (short names for short scopes: `i`, `r`, `w`)
- N6: No encodings (no Hungarian, no `I` prefix on interfaces)
- N7: Names describe side effects

## Tests (T1-T9)

- T1: Test everything that could break
- T2: Use coverage tools (`go test -cover`)
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
| **Functions** | F1 | Max 3 arguments (use struct) |
| | F3 | No flag arguments |
| | F4 | Delete dead functions |
| **General** | G5 | DRY — no duplication |
| | G9 | Delete dead code |
| | G16 | No obscured intent |
| | G23 | Interfaces over if/else |
| | G25 | Named constants, not magic numbers |
| | G30 | Functions do one thing |
| | G36 | Law of Demeter (one dot) |
| **Go** | GO1 | PascalCase exported, camelCase local |
| | GO2 | Accept interfaces, return structs |
| | GO3 | Always check and wrap errors |
| | GO5 | Small interfaces (1-2 methods) |
| | GO7 | Goroutine safety with context |
| **Names** | N1 | Descriptive names |
| | N5 | Short names for short scopes |
| **Tests** | T5 | Test boundary conditions |
| | T9 | Tests must be fast |

## Anti-Patterns (Don't → Do)

| Don't | Do |
|-------|-----|
| Ignore returned errors | `if err != nil { return fmt.Errorf("...: %w", err) }` |
| `interface{ Method1(); Method2(); Method3() }` | Split into focused 1-method interfaces |
| `func Process(data []byte, verbose bool)` | `func Process(data []byte)` / `func ProcessVerbose(data []byte)` |
| `panic("unexpected")` in library code | Return `error` |
| `var ErrFoo = errors.New(...)` + string matching | `errors.Is` / `errors.As` |
| Magic number `86400` | `const secondsPerDay = 86400` |
| Goroutine without cancellation | Pass `context.Context`, select on `ctx.Done()` |
| Deep nesting | Guard clauses, early returns |
| `getters/setters` on structs | Direct field access (Go convention) |
| `IReader` interface prefix | `Reader` (no prefix) |
| `utils` package | Descriptive package names (`httputil`, `strconv`) |

## Modern Go Idioms

```go
// GO1: Naming — exported PascalCase, unexported camelCase
type OrderService struct {
    repo OrderRepository
}

// GO2: Accept interfaces, return structs
type OrderRepository interface {
    FindByID(ctx context.Context, id string) (*Order, error)
}

func NewOrderService(repo OrderRepository) *OrderService {
    return &OrderService{repo: repo}
}

// GO3: Error wrapping (Go 1.13+)
func (s *OrderService) GetOrder(ctx context.Context, id string) (*Order, error) {
    order, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("get order %s: %w", id, err)
    }
    return order, nil
}

// GO5: Small interfaces compose
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type ReadWriter interface { Reader; Writer }

// GO6: defer for cleanup
func ReadConfig(path string) (Config, error) {
    f, err := os.Open(path)
    if err != nil {
        return Config{}, fmt.Errorf("open config: %w", err)
    }
    defer f.Close()
    // ...
}

// GO7: Goroutine with context cancellation
func FetchAll(ctx context.Context, urls []string) ([]Result, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]Result, len(urls))
    for i, url := range urls {
        g.Go(func() error {
            res, err := fetch(ctx, url)
            if err != nil {
                return err
            }
            results[i] = res
            return nil
        })
    }
    if err := g.Wait(); err != nil {
        return nil, err
    }
    return results, nil
}

// GO8: Table-driven tests
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}

// Generics (Go 1.18+) — type-safe containers
func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

// Structured logging with slog (Go 1.21+)
slog.Info("order processed",
    slog.String("order_id", order.ID),
    slog.Int("items", len(order.Items)),
)
```

## AI Behavior

When reviewing code, identify violations by rule number (e.g., "GO3 violation: error not checked").
When fixing or editing code, report what was fixed (e.g., "Fixed: wrapped error with context (GO3)").
Before applying Modern Go idioms, check `go.mod` for the Go version. Go 1.13+: error wrapping `%w`. Go 1.18+: generics. Go 1.21+: `slog`, `slices`, `maps`. Go 1.22+: range-over-int. Default to Go 1.21 if no signal found.

