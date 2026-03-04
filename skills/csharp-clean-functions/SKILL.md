---
name: csharp-clean-functions
description: Use when writing, fixing, editing, or refactoring C# methods. Enforces Clean Code principles—maximum 3 arguments, single responsibility, no flag parameters.
---

# Clean Functions (C#)

## F1: Maximum 3 Arguments

More than 3 arguments? Use a request object or record.

```csharp
// Bad — too many arguments
public User CreateUser(string name, string email, string role, int age, bool active)
{
    // ...
}

// Good — request record
public record CreateUserRequest(string Name, string Email, string Role, int Age, bool Active);

public User CreateUser(CreateUserRequest request)
{
    // ...
}
```

## F2: No Output Arguments

Return values instead of `out`/`ref` parameters.

```csharp
// Bad — output argument
public void PopulateDefaults(ref Config config)
{
    config.Timeout = TimeSpan.FromSeconds(30);
    config.Retries = 3;
}

// Good — return a new value
public Config WithDefaults(Config config) => config with
{
    Timeout = TimeSpan.FromSeconds(30),
    Retries = 3
};
```

## F3: No Flag Arguments

Split into separate methods.

```csharp
// Bad — flag argument
public string FormatOutput(byte[] data, bool pretty)
{
    return pretty ? FormatPretty(data) : FormatCompact(data);
}

// Good — separate methods
public string FormatPretty(byte[] data) { ... }
public string FormatCompact(byte[] data) { ... }
```

## F4: Delete Dead Methods

Private methods with no callers? Delete them. Git remembers.

## Modern C# Function Idioms

```csharp
// Expression-bodied methods for simple one-liners (C# 6+)
public decimal Total => Items.Sum(i => i.Price);
public bool IsEmpty => !Items.Any();
public override string ToString() => $"Order({Id}, {Total:C})";

// Record with-expressions for immutable updates (C# 9+)
public record Order(string Id, List<Item> Items, decimal Discount);

public Order ApplyDiscount(Order order, decimal rate)
    => order with { Discount = order.Items.Sum(i => i.Price) * rate };

// Guard clauses — handle errors early, keep happy path unindented
public async Task<Receipt> ProcessOrderAsync(Order order, CancellationToken ct)
{
    ArgumentNullException.ThrowIfNull(order);
    if (!order.Items.Any())
        throw new InvalidOperationException("Order has no items");

    // Happy path
    var receipt = await ChargeAsync(order, ct);
    await SendConfirmationAsync(receipt, ct);
    return receipt;
}

// Local functions for helper logic
public IEnumerable<int> Fibonacci()
{
    return Generate();

    static IEnumerable<int> Generate()
    {
        int a = 0, b = 1;
        while (true)
        {
            yield return a;
            (a, b) = (b, a + b);
        }
    }
}

// Extension methods for fluent APIs
public static class OrderExtensions
{
    public static decimal TotalWithTax(this Order order, decimal taxRate)
        => order.Total * (1 + taxRate);

    public static bool IsHighValue(this Order order)
        => order.Total > 1000m;
}

// CancellationToken as last parameter (async convention)
// In library code, use ConfigureAwait(false) to avoid
// capturing the synchronization context (prevents deadlocks).
public async Task<Order> GetOrderAsync(
    string orderId,
    bool includeItems = false,
    CancellationToken ct = default)
{
    var order = await _repository.FindByIdAsync(orderId, ct)
        .ConfigureAwait(false); // library code: always ConfigureAwait(false)
    // ...
}

// Tuple returns for multiple values (prefer record for public APIs)
private (bool IsValid, string? ErrorMessage) Validate(Order order)
{
    if (string.IsNullOrEmpty(order.Id))
        return (false, "Order ID is required");
    return (true, null);
}
```

## Quick Reference

| Rule | Principle | C# Idiom |
|------|-----------|----------|
| F1 | Max 3 arguments | Use record or request object |
| F2 | No output arguments | Return values, `with` expressions |
| F3 | No flag arguments | Split into separate methods |
| F4 | Delete dead methods | Remove private with no callers |

## AI Behavior

When reviewing methods, cite the rule number (e.g., "F1 violation: 5 arguments, use request record").
When refactoring, explain the improvement (e.g., "Extracted `ValidateOrder` from `ProcessOrder` (G30)").
Prefer expression-bodied members for single-expression methods. Use `record` for request/response DTOs.

