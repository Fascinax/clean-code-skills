---
name: go-clean-comments
description: Use when writing, fixing, editing, or reviewing Go comments and godoc. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code.
---

# Clean Comments (Go)

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history, and dates.

```go
// Bad — metadata belongs in Git
// Author: John Doe
// Created: 2024-01-15
// Ticket: JIRA-1234
type OrderService struct{}

// Good — only technical documentation
// OrderService processes orders by validating inventory,
// calculating totals, and dispatching to fulfillment.
type OrderService struct{}
```

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists or works differently, delete it immediately.

## C3: No Redundant Comments

```go
// Bad — the code already says this
i++ // increment i
user.Save() // save the user

// Good — explains WHY, not WHAT
i++ // compensate for zero-indexing in display
```

## C4: Write Comments Well

If a comment is worth writing, write it well:
- Choose words carefully
- Use correct grammar
- Don't ramble or state the obvious
- Be brief

## C5: Never Commit Commented-Out Code

```go
// DELETE THIS — it's an abomination
// func oldCalculateTax(income float64) float64 {
//     return income * 0.15
// }
```

Git remembers everything. Delete it.

## Godoc Best Practices

Go has a strong convention: doc comments start with the name of the thing they describe.

### Package Comments

```go
// Package httputil provides HTTP utility functions for request
// parsing, response writing, and middleware composition.
package httputil
```

### Exported Type Comments

```go
// OrderService manages the order lifecycle from creation
// through fulfillment. It coordinates inventory checks,
// payment processing, and shipping dispatch.
type OrderService struct {
    repo    OrderRepository
    payment PaymentGateway
}
```

### Exported Function Comments

```go
// FindByID returns the order with the given ID.
// It returns ErrNotFound if no order exists with that ID.
func (s *OrderService) FindByID(ctx context.Context, id string) (*Order, error) {
    // ...
}
```

### When Comments Are Unnecessary

```go
// Types are clear — comment adds no value. Skip it.
func (u *User) IsActive() bool {
    return u.status == StatusActive
}

// Complex business logic — comment explains the rule.
// eligible returns true if the user has been a member for 2+ years
// OR has spent more than $1000 in the last 90 days.
func (u *User) eligible() bool {
    // ...
}
```

## The Goal

The best comment is clear code itself. If you need a comment to explain what code does, refactor first, comment last.

```go
// Bad — comment needed to explain intent
// Check if eligible for premium discount
if user.Years >= 2 && user.TotalSpent > 1000 {
    applyDiscount(user)
}

// Good — self-documenting code
if user.IsEligibleForPremiumDiscount() {
    applyDiscount(user)
}
```

## Modern Go Comment Idioms

### `//go:generate` for Code Generation

```go
// Use go:generate directives instead of manual doc about generated code
//go:generate stringer -type=Status
type Status int

const (
    StatusPending Status = iota
    StatusActive
    StatusClosed
)
```

### `//nolint` Directives Document Exceptions

```go
// Bad — comment explaining why lint is ignored
// We need to ignore this error because the API is fire-and-forget
_ = sendNotification(ctx, event)

// Good — nolint directive with reason
_ = sendNotification(ctx, event) //nolint:errcheck // fire-and-forget notification
```

### Deprecated Functions

```go
// Deprecated: Use NewHTTPClient instead.
func NewClient() *Client {
    return NewHTTPClient(DefaultConfig())
}
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| C1 | No metadata in comments | Author, date, ticket → use Git |
| C2 | Delete obsolete comments | Stale comment → delete immediately |
| C3 | No redundant comments | Code says it already → remove comment |
| C4 | Write comments well | Brief, precise, explains WHY not WHAT |
| C5 | No commented-out code | Dead code → delete, Git remembers |
| GO4 | `go fmt` handles formatting | Never comment about style choices |

## AI Behavior

When reviewing comments, cite the rule number (e.g., "C3 violation: redundant comment restates the code").
When cleaning comments, explain the action (e.g., "Removed metadata comment, use Git for author tracking (C1)").
For godoc, ensure comments start with the declared name (e.g., "// FindByID returns...").

