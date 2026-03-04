---
name: csharp-clean-comments
description: Use when writing, fixing, editing, or reviewing C# comments and XML documentation. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code.
---

# Clean Comments (C#)

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history, and dates.

```csharp
// Bad — metadata belongs in Git
// Author: John Doe
// Created: 2024-01-15
// Ticket: JIRA-1234
public class OrderService { }

// Good — only technical documentation
/// <summary>
/// Processes orders by validating inventory, calculating totals,
/// and dispatching to the fulfillment system.
/// </summary>
public class OrderService { }
```

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists, delete it immediately.

## C3: No Redundant Comments

```csharp
// Bad — the code already says this
i++; // increment i
user.Save(); // save the user

// Good — explains WHY, not WHAT
i++; // compensate for zero-indexing in display
```

## C4: Write Comments Well

If a comment is worth writing, write it well:

- Use single-line comments (`//`) — avoid multi-line `/* */` (Microsoft coding conventions)
- Begin comment text with an uppercase letter
- End comment text with a period
- Insert one space between `//` and the comment text
- Be brief, precise, and explain WHY not WHAT

## C5: Never Commit Commented-Out Code

```csharp
// DELETE THIS — Git remembers everything
// public decimal OldCalculateTax(decimal income)
// {
//     return income * 0.15m;
// }
```

## XML Documentation Best Practices

C# uses `///` XML doc comments for API documentation. They power IntelliSense and generate documentation.

### Type Documentation

```csharp
/// <summary>
/// Manages the order lifecycle from creation through fulfillment.
/// </summary>
/// <remarks>
/// Thread-safe. All public methods accept <see cref="CancellationToken"/>
/// for cooperative cancellation.
/// </remarks>
public class OrderService { }
```

### Method Documentation

```csharp
/// <summary>
/// Transfers funds between two accounts atomically.
/// </summary>
/// <param name="from">Source account to debit.</param>
/// <param name="to">Destination account to credit.</param>
/// <param name="amount">Positive amount to transfer.</param>
/// <returns>The transfer result with updated balances.</returns>
/// <exception cref="InsufficientFundsException">
/// Thrown when the source balance is too low.
/// </exception>
public async Task<TransferResult> TransferAsync(
    Account from, Account to, decimal amount, CancellationToken ct)
{
    // ...
}
```

### When Documentation Is Unnecessary

```csharp
// Types are clear — doc adds no value. Skip it.
public bool IsActive => Status == UserStatus.Active;

// Complex business logic — doc explains the rule.
/// <summary>
/// Checks discount eligibility: 2+ years membership OR $1000+ spent in 90 days.
/// </summary>
public bool IsEligibleForDiscount { get; }
```

## The Goal

The best comment is clear code itself. Refactor first, comment last.

```csharp
// Bad — comment needed to explain intent
// Check if user is eligible for premium discount
if (user.Years >= 2 && user.TotalSpent > 1000)
    ApplyDiscount(user);

// Good — self-documenting code
if (user.IsEligibleForPremiumDiscount)
    ApplyDiscount(user);
```

## Modern C# Comment Idioms

### `[Obsolete]` Replaces "Deprecated" Comments

```csharp
// Bad — comment that tooling can't enforce
/// <summary>Deprecated: use NewApi() instead.</summary>
public void OldApi() { }

// Good — compiler warns on usage
[Obsolete("Use NewApi() instead", error: false)]
public void OldApi() { }
```

### `#pragma warning` with Reason

```csharp
// Bad — suppressing with no explanation
#pragma warning disable CS8618
public string Name { get; set; }
#pragma warning restore CS8618

// Good — reason documented
#pragma warning disable CS8618 // Initialized by EF Core
public string Name { get; set; }
#pragma warning restore CS8618
```

### `<inheritdoc/>` Reduces Redundant Docs

```csharp
public interface IOrderRepository
{
    /// <summary>
    /// Finds an order by its unique identifier.
    /// </summary>
    Task<Order?> FindByIdAsync(string id, CancellationToken ct);
}

public class SqlOrderRepository : IOrderRepository
{
    /// <inheritdoc/>
    public async Task<Order?> FindByIdAsync(string id, CancellationToken ct)
    {
        // ...
    }
}
```

### `<see cref=""/>` for Cross-References

```csharp
/// <summary>
/// Validates the order using <see cref="OrderValidator"/>.
/// Throws <see cref="ValidationException"/> on failure.
/// </summary>
public void Validate(Order order) { }
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| C1 | No metadata in comments | Author, date, ticket → use Git |
| C2 | Delete obsolete comments | Stale comment → delete immediately |
| C3 | No redundant comments | Code says it already → remove comment |
| C4 | Write comments well | Brief, precise, explains WHY not WHAT |
| C5 | No commented-out code | Dead code → delete, Git remembers |
| CS1 | Properties are self-documenting | Types + names reduce comment need |

## AI Behavior

When reviewing comments, cite the rule number (e.g., "C3 violation: redundant comment restates the code").
When cleaning comments, explain the action (e.g., "Removed metadata comment, use Git for author tracking (C1)").
For XML docs, use `<summary>`, `<param>`, `<returns>`, `<exception>` tags. Use `<inheritdoc/>` to avoid duplication.
