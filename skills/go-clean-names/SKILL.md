---
name: go-clean-names
description: Use when naming, renaming, or fixing names of variables, functions, types, or packages in Go. Enforces Clean Code principles—descriptive names, appropriate length, no encodings.
---

# Clean Names (Go)

## N1: Choose Descriptive Names

Names should reveal intent. In Go, short names are fine in short scopes.

```go
// Bad — meaningless names
func p(d []byte) error {
    for _, b := range d {
        if b > t {
            return e
        }
    }
    return nil
}

// Good — descriptive
func validate(payload []byte) error {
    for _, b := range payload {
        if b > maxByteValue {
            return ErrInvalidByte
        }
    }
    return nil
}
```

## N2: Names at Appropriate Abstraction Level

```go
// Bad — implementation detail in the name
func readFromPostgreSQL(ctx context.Context, id string) (*User, error)

// Good — abstracts the storage mechanism
func FindUser(ctx context.Context, id string) (*User, error)
```

## N3: Use Standard Nomenclature

Go conventions: PascalCase exported, camelCase unexported, ALL_CAPS for acronyms in names.

```go
// Bad — violates Go naming conventions
type Http_client struct{}    // underscores
type HttpClient struct{}     // wrong acronym case
var MAX_RETRIES = 3          // screaming snake_case

// Good — idiomatic Go
type HTTPClient struct{}     // acronym all-caps
var maxRetries = 3           // camelCase unexported
type OrderService struct{}   // PascalCase exported
```

## N4: Unambiguous Names

```go
// Bad — what does "handle" mean here?
func handle(r *http.Request) error

// Good — specific action
func validateRequest(r *http.Request) error
```

## N5: Name Length Matches Scope

Go embraces short names in small scopes. The wider the scope, the longer the name.

```go
// Good — short names in tight scopes
for i, v := range items { ... }
if err != nil { return err }

// Good — descriptive names in wider scopes
type TransactionProcessor struct {
    repository     TransactionRepository
    eventPublisher EventPublisher
}
```

## N6: No Encodings

```go
// Bad — Hungarian notation, interface prefix
type IOrderRepository interface{}
var strName string
var nCount int

// Good — Go convention: no prefixes, no type encodings
type OrderRepository interface{}
var name string
var count int
```

## N7: Names Describe Side Effects

```go
// Bad — hides side effect
func GetConnection() *sql.DB {
    // creates a new connection pool!
}

// Good — name reveals behavior
func OpenConnectionPool() *sql.DB {
    // ...
}
```

## Modern Go Naming Idioms

```go
// Package names: short, lowercase, singular
package user    // not: package users, package userService
package http    // not: package httpUtils

// Don't repeat the package name in exported names (Effective Go)
// Bad: http.HTTPServer, user.UserService
// Good: http.Server, user.Service

// Receiver names: short, consistent, never "this" or "self"
func (s *OrderService) Process(ctx context.Context, o Order) error { ... }
func (s *OrderService) Cancel(ctx context.Context, id string) error { ... }

// Error variables: Err prefix, lowercase messages, no punctuation
var (
    ErrNotFound     = errors.New("not found")      // not "Not found."
    ErrUnauthorized = errors.New("unauthorized")    // not "Unauthorized!"
)

// Error types: Error suffix
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string { ... }

// Interface naming: -er suffix for single-method interfaces
type Reader interface { Read(p []byte) (int, error) }
type Stringer interface { String() string }
type Handler interface { ServeHTTP(ResponseWriter, *Request) }

// Interfaces belong in the consumer package, not the producer
// (Go Code Review Comments: define interfaces where they are used)
// package storage — defines concrete StorageClient
// package billing — defines interface: type Storage interface { Get(key string) ([]byte, error) }

// Constructor: New prefix
func NewOrderService(repo OrderRepository) *OrderService { ... }

// Getter: no Get prefix (Go convention)
func (u *User) Name() string { return u.name }   // not GetName()
func (u *User) SetName(n string) { u.name = n }  // setter keeps Set prefix

// Context always first parameter, named ctx
func FetchOrder(ctx context.Context, id string) (*Order, error) { ... }

// Acronyms: all-caps when exported (ID not Id, URL not Url, HTTP not Http)
type HTTPClient struct{}
type JSONParser struct{}
var userID string  // not userId
var xmlAPI string  // not xmlApi
```

## Quick Reference

| Rule | Principle | Go Idiom |
|------|-----------|----------|
| N1 | Descriptive names | Reveal intent, short in tight scopes |
| N2 | Right abstraction level | No implementation details in names |
| N3 | Standard nomenclature | PascalCase exported, camelCase local, ALL-CAPS acronyms |
| N4 | Unambiguous names | Specific verbs over generic "handle/process" |
| N5 | Length matches scope | `i` in loops, `TransactionProcessor` for types |
| N6 | No encodings | No `I` prefix, no Hungarian notation |
| N7 | Describe side effects | `OpenConnectionPool`, not `GetConnection` |

## AI Behavior

When reviewing names, cite the rule number (e.g., "N3 violation: use `HTTPClient` not `HttpClient`").
When renaming, explain the change (e.g., "Renamed `proc` → `processOrder` for clarity (N1)").
Follow Go conventions: no getters with `Get` prefix, `-er` interfaces, `Err` prefix for sentinel errors.

