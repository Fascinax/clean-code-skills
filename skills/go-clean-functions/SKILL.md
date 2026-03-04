---
name: go-clean-functions
description: Use when writing, fixing, editing, or refactoring Go functions. Enforces Clean Code principles—maximum 3 arguments, single responsibility, no flag parameters.
---

# Clean Functions (Go)

## F1: Maximum 3 Arguments

More than 3 arguments? Use an options struct.

```go
// Bad — too many arguments
func CreateUser(name, email, role string, age int, active bool) (*User, error) {
    // ...
}

// Good — options struct
type CreateUserParams struct {
    Name   string
    Email  string
    Role   string
    Age    int
    Active bool
}

func CreateUser(params CreateUserParams) (*User, error) {
    // ...
}
```

## F2: No Output Arguments

Return values instead of modifying parameters.

```go
// Bad — output argument
func PopulateDefaults(cfg *Config) {
    cfg.Timeout = 30 * time.Second
    cfg.Retries = 3
}

// Good — return a new value
func WithDefaults(cfg Config) Config {
    cfg.Timeout = 30 * time.Second
    cfg.Retries = 3
    return cfg
}
```

## F3: No Flag Arguments

Split into separate functions.

```go
// Bad — flag argument
func FormatOutput(data []byte, pretty bool) string {
    if pretty {
        return formatPretty(data)
    }
    return formatCompact(data)
}

// Good — separate functions
func FormatPretty(data []byte) string { ... }
func FormatCompact(data []byte) string { ... }
```

## F4: Delete Dead Functions

Unexported functions with no callers in the package? Delete them. Git remembers.

## Modern Go Function Idioms

```go
// Functional options pattern (idiomatic for constructors)
type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage — reads like English
srv := NewServer(
    WithPort(9090),
    WithTimeout(5 * time.Second),
)

// Error-returning functions: error always last
func ReadConfig(path string) (Config, error) { ... }

// Named return values for documentation (not naked returns)
func divide(a, b float64) (result float64, err error) {
    if b == 0 {
        return 0, ErrDivisionByZero
    }
    return a / b, nil
}

// Guard clauses — handle errors early, keep happy path unindented
func ProcessOrder(ctx context.Context, order Order) error {
    if err := order.Validate(); err != nil {
        return fmt.Errorf("invalid order: %w", err)
    }
    if order.Total() == 0 {
        return ErrEmptyOrder
    }

    // Happy path — not nested
    receipt, err := charge(ctx, order)
    if err != nil {
        return fmt.Errorf("charge failed: %w", err)
    }
    return sendConfirmation(ctx, receipt)
}

// Closure for deferred setup/teardown
func withTransaction(db *sql.DB, fn func(tx *sql.Tx) error) error {
    tx, err := db.Begin()
    if err != nil {
        return err
    }
    defer func() {
        if p := recover(); p != nil {
            _ = tx.Rollback()
            panic(p)
        }
    }()
    if err := fn(tx); err != nil {
        _ = tx.Rollback()
        return err
    }
    return tx.Commit()
}

// Methods with value receivers for read-only, pointer receivers for mutation
func (o Order) Total() float64       { ... }  // read-only
func (o *Order) AddItem(item Item)    { ... }  // mutates
```

## Quick Reference

| Rule | Principle | Go Idiom |
|------|-----------|----------|
| F1 | Max 3 arguments | Use options struct or functional options |
| F2 | No output arguments | Return new values |
| F3 | No flag arguments | Split into separate functions |
| F4 | Delete dead functions | Remove unexported with no callers |

## AI Behavior

When reviewing functions, cite the rule number (e.g., "F1 violation: 5 arguments, use options struct").
When refactoring, explain the improvement (e.g., "Extracted `validateOrder` from `ProcessOrder` (G30)").
Prefer functional options for constructors with many optional parameters.

