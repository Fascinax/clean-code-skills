---
name: go-clean-tests
description: Use when writing, fixing, editing, or refactoring Go tests. Enforces Clean Code principles—fast tests, boundary coverage, one concept per test, table-driven test best practices.
---

# Clean Tests (Go)

## T1: Insufficient Tests

Test everything that could possibly break. Use coverage tools as a guide, not a goal.

```go
// Bad — only tests happy path
func TestDivide(t *testing.T) {
    got := Divide(10, 2)
    if got != 5 {
        t.Errorf("Divide(10, 2) = %f, want 5", got)
    }
}

// Good — tests edge cases too
func TestDivide(t *testing.T) {
    t.Run("normal", func(t *testing.T) {
        got, err := Divide(10, 2)
        require.NoError(t, err)
        assert.Equal(t, 5.0, got)
    })
    t.Run("by zero", func(t *testing.T) {
        _, err := Divide(10, 0)
        assert.ErrorIs(t, err, ErrDivisionByZero)
    })
    t.Run("negative", func(t *testing.T) {
        got, err := Divide(-10, 2)
        require.NoError(t, err)
        assert.Equal(t, -5.0, got)
    })
}
```

## T2: Use a Coverage Tool

```bash
# Run with coverage
go test -cover ./...

# Generate HTML coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## T3: Don't Skip Trivial Tests

Trivial tests document behavior and catch regressions.

```go
func TestUserDefaultRole(t *testing.T) {
    user := NewUser("Alice")
    assert.Equal(t, RoleMember, user.Role)
}
```

## T4: An Ignored Test Is a Question About an Ambiguity

Don't use `t.Skip()` to hide problems. Either fix the test or delete it.

```go
// Bad — hiding a problem
func TestAsyncOperation(t *testing.T) {
    t.Skip("flaky, fix later")
}

// Good — documents a real constraint
func TestCacheInvalidation(t *testing.T) {
    if testing.Short() {
        t.Skip("requires Redis; run with -short=false")
    }
    // ...
}
```

## T5: Test Boundary Conditions

Bugs congregate at boundaries. Test them explicitly.

```go
func TestPaginate(t *testing.T) {
    items := makeItems(100)

    tests := []struct {
        name     string
        page     int
        size     int
        wantLen  int
        wantErr  bool
    }{
        {"first page", 1, 10, 10, false},
        {"last page", 10, 10, 10, false},
        {"beyond last", 11, 10, 0, false},
        {"zero page", 0, 10, 0, true},
        {"empty list", 1, 10, 0, false},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Paginate(items, tt.page, tt.size)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                require.NoError(t, err)
                assert.Len(t, result, tt.wantLen)
            }
        })
    }
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

```go
// Bad — hits real database
func TestUserCreation(t *testing.T) {
    db := connectToDatabase()  // Slow!
    // ...
}

// Good — uses interface mock
func TestUserCreation(t *testing.T) {
    repo := &mockUserRepo{users: make(map[string]*User)}
    svc := NewUserService(repo)
    // ...
}
```

## Test Organization

### Table-Driven Tests (GO8)

The idiomatic Go test pattern. Every test with multiple cases should use this.

```go
func TestParseSize(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    int64
        wantErr bool
    }{
        {"bytes", "100B", 100, false},
        {"kilobytes", "1KB", 1024, false},
        {"megabytes", "5MB", 5 * 1024 * 1024, false},
        {"invalid", "abc", 0, true},
        {"empty", "", 0, true},
        {"negative", "-1KB", 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseSize(tt.input)
            if tt.wantErr {
                assert.Error(t, err)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

### Test Helpers

Never call `t.Fatal` or `t.FailNow` from a goroutine other than the test goroutine — it causes undefined behavior (Go testing docs). Use `t.Error` and check in the main goroutine instead.

```go
// testutil package or helpers in _test.go
func newTestServer(t *testing.T) *httptest.Server {
    t.Helper()
    mux := http.NewServeMux()
    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })
    srv := httptest.NewServer(mux)
    t.Cleanup(srv.Close)
    return srv
}
```

### Test Naming Convention

Use `Test<Function>_<scenario>` or table-driven `name` field.

```go
func TestFindByEmail_existingUser_returnsUser(t *testing.T) { ... }
func TestFindByEmail_unknownEmail_returnsNotFound(t *testing.T) { ... }
func TestTransfer_insufficientFunds_returnsError(t *testing.T) { ... }
```

## Modern Go Test Idioms

```go
// testify for assertions (widely adopted)
import (
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestOrderTotal(t *testing.T) {
    order := NewOrder(Item{Price: 100}, Item{Price: 200})
    assert.Equal(t, 300.0, order.Total())
}

// t.Cleanup for deferred teardown
func TestWithDatabase(t *testing.T) {
    db := setupTestDB(t)
    t.Cleanup(func() { db.Close() })
    // ...
}

// t.Parallel for concurrent tests
func TestIndependentOps(t *testing.T) {
    t.Parallel()
    // ...
}

// testing/fstest for filesystem tests (Go 1.16+)
func TestReadConfig(t *testing.T) {
    fs := fstest.MapFS{
        "config.yaml": &fstest.MapFile{Data: []byte("key: value")},
    }
    cfg, err := ReadConfigFS(fs, "config.yaml")
    require.NoError(t, err)
    assert.Equal(t, "value", cfg.Key)
}
```

## Quick Reference

| Rule | Principle |
|------|-----------|
| T1 | Test everything that could break |
| T2 | Use coverage tools (`go test -cover`) |
| T3 | Don't skip trivial tests |
| T4 | Ignored test = ambiguity question |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Look for patterns in failures |
| T8 | Check coverage when debugging |
| T9 | Tests must be fast (<100ms) |
| GO8 | Table-driven tests for multiple cases |

## AI Behavior

When reviewing tests, cite the rule number (e.g., "T5 violation: no boundary condition tests").
When writing tests, prefer table-driven tests (GO8) for any function with 2+ test cases.
When applying test helpers, use `t.Helper()` and `t.Cleanup()` for clean setup/teardown.

