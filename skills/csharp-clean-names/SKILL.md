---
name: csharp-clean-names
description: Use when naming, renaming, or fixing names of variables, methods, types, or namespaces in C#. Enforces Clean Code principles—descriptive names, appropriate length, no encodings.
---

# Clean Names (C#)

## N1: Choose Descriptive Names

Names should reveal intent.

```csharp
// Bad — meaningless names
public int P(List<int> d, bool f)
{
    var r = 0;
    foreach (var x in d) { if (f) r += x; }
    return r;
}

// Good — descriptive
public int SumPositiveValues(List<int> values)
{
    return values.Where(v => v > 0).Sum();
}
```

## N2: Names at Appropriate Abstraction Level

```csharp
// Bad — implementation detail in the name
public User ReadFromSqlServer(string id)

// Good — abstracts the storage mechanism
public User FindById(string id)
```

## N3: Use Standard Nomenclature

.NET conventions: PascalCase methods/properties/types/constants, camelCase locals/params, `I` prefix interfaces.

```csharp
// Bad — violates .NET naming conventions
public class order_service { }       // should be PascalCase
public void processOrder() { }       // should be PascalCase
private string Name;                 // field should be _camelCase
const int max_retries = 3;           // constants are PascalCase

// Good — idiomatic C#
public class OrderService { }
public void ProcessOrder() { }
private readonly string _name;
public string Name { get; }
const int MaxRetries = 3;            // PascalCase for all constants
```

## N4: Unambiguous Names

```csharp
// Bad — what does "handle" mean?
public void Handle(HttpRequest request)

// Good — specific action
public void ValidateAndRoute(HttpRequest request)
```

## N5: Name Length Matches Scope

Short names for short scopes, descriptive names for wide scopes.

```csharp
// Good — short names in tight scopes (LINQ, lambdas)
users.Where(u => u.IsActive).Select(u => u.Email);
for (var i = 0; i < items.Count; i++) { ... }

// Good — descriptive names in wider scopes
public class TransactionProcessingService
{
    private readonly ITransactionRepository _transactionRepository;
    private readonly IEventPublisher _eventPublisher;
}
```

## N6: No Encodings

C# convention allows `I` prefix on interfaces — this is the one exception to "no encodings."

```csharp
// Bad — Hungarian notation
string strName;
int nCount;
List<User> lstUsers;

// Good — no type encodings
string name;
int count;
List<User> users;

// C# exception: I prefix for interfaces is OK
public interface IOrderRepository { }
```

## N7: Names Describe Side Effects

```csharp
// Bad — hides side effect
public DbConnection GetConnection()
{
    // opens a new connection!
}

// Good — reveals behavior
public DbConnection OpenConnection()
{
    // ...
}
```

## Modern C# Naming Idioms

```csharp
// Async methods: Async suffix (C# convention)
public Task<Order> GetOrderAsync(string id, CancellationToken ct) { ... }
public Task SaveAsync(Order order, CancellationToken ct) { ... }

// Private fields: _camelCase with underscore prefix
// Static private fields: s_ prefix (.NET Runtime convention)
// Thread-static fields: t_ prefix
public class OrderService
{
    private readonly IOrderRepository _repository;
    private readonly ILogger<OrderService> _logger;
    private static readonly HttpClient s_httpClient = new();
    [ThreadStatic] private static TimeSpan t_timeout;
}

// Methods are verbs/verb phrases, properties are nouns/adjectives
// (Framework Design Guidelines)
public class Order
{
    public decimal Total { get; }            // noun — property
    public bool IsValid { get; }             // adjective — property
    public void Submit() { }                 // verb — method
    public decimal CalculateTotal() { }      // verb phrase — method
}

// Boolean properties/methods: Is, Has, Can prefix
public bool IsActive { get; }
public bool HasPermission(Permission perm) { ... }
public bool CanEdit(Resource resource) { ... }

// Event handlers: On prefix, EventArgs suffix
public event EventHandler<OrderCreatedEventArgs>? OrderCreated;
protected virtual void OnOrderCreated(OrderCreatedEventArgs e) { ... }

// Extension methods: descriptive verb
public static class StringExtensions
{
    public static bool IsNullOrWhiteSpace(this string? value) { ... }
    public static string TruncateTo(this string value, int maxLength) { ... }
}

// Generic type parameters: T prefix with description
public interface IRepository<TEntity> where TEntity : class { }
public Task<TResponse> SendAsync<TRequest, TResponse>(TRequest request) { ... }

// Records: noun, no suffix
public record OrderSummary(string OrderId, decimal Total);
public record Address(string Street, string City, string PostalCode);
```

## Quick Reference

| Rule | Principle | C# Idiom |
|------|-----------|----------|
| N1 | Descriptive names | Reveal intent clearly |
| N2 | Right abstraction level | No impl details in names |
| N3 | Standard nomenclature | PascalCase types/methods, camelCase locals, `I` for interfaces |
| N4 | Unambiguous names | Specific verbs over generic "Handle/Process" |
| N5 | Length matches scope | `u` in lambdas, `TransactionProcessor` for types |
| N6 | No encodings | No Hungarian; `I` prefix for interfaces is OK |
| N7 | Describe side effects | `OpenConnection`, not `GetConnection` |

## AI Behavior

When reviewing names, cite the rule number (e.g., "N3 violation: method should be PascalCase").
When renaming, explain the change (e.g., "Renamed `proc` → `ProcessOrder` for clarity (N1)").
Follow .NET conventions: `Async` suffix, `_camelCase` fields, `I` prefix interfaces, PascalCase everything else.

