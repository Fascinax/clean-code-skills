---
name: csharp-clean-code
description: Use when writing, fixing, editing, reviewing, or refactoring any C# code. Enforces Robert Martin's complete Clean Code catalog—naming, functions, comments, DRY, and boundary conditions—adapted for C#.
---

# Clean C#: Complete Reference

Enforces all Clean Code principles from Robert C. Martin's Chapter 17, adapted for C#.

## Comments (C1-C5)

- C1: No metadata in comments (use Git)
- C2: Delete obsolete comments immediately
- C3: No redundant comments
- C4: Write comments well if you must
- C5: Never commit commented-out code

## Environment (E1-E2)

- E1: One command to build (`dotnet build`)
- E2: One command to test (`dotnet test`)

## Functions (F1-F4)

- F1: Maximum 3 arguments (use object/record for more)
- F2: No output arguments (no `out`/`ref` for results — return values)
- F3: No flag arguments (split methods)
- F4: Delete dead methods

## General (G1-G36)

- G1: One language per file
- G2: Implement expected behavior
- G3: Handle boundary conditions
- G4: Don't override safeties (don't suppress nullable warnings with `!`)
- G5: DRY — no duplication
- G6: Consistent abstraction levels
- G7: Base classes don't know children
- G8: Minimize public interface (`internal` by default)
- G9: Delete dead code
- G10: Variables near usage
- G11: Be consistent
- G12: Remove clutter
- G13: No artificial coupling
- G14: No feature envy
- G15: No selector arguments
- G16: No obscured intent
- G17: Code where expected
- G18: Prefer instance methods
- G19: Use explanatory variables
- G20: Method names say what they do
- G21: Understand the algorithm
- G22: Make dependencies physical (explicit via DI)
- G23: Prefer polymorphism to if/else
- G24: Follow conventions (.NET naming, `dotnet format`, editorconfig)
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

## C#-Specific (CS1-CS8)

- CS1: Use properties, not public fields
- CS2: Use LINQ for collection operations — no manual loops for filter/map/reduce
- CS3: async/await all the way — never block with `.Result` or `.Wait()`
- CS4: Use `record` for immutable data types (C# 9+)
- CS5: Enable nullable reference types — annotate with `?` where null is valid
- CS6: Use pattern matching in switch expressions (C# 8+)
- CS7: Use `using` declarations over `using` blocks (C# 8+)
- CS8: Use primary constructors for DI (C# 12+)

## Names (N1-N7)

- N1: Choose descriptive names
- N2: Right abstraction level
- N3: Use standard nomenclature (PascalCase methods/properties, camelCase locals/params, `I` prefix on interfaces)
- N4: Unambiguous names
- N5: Name length matches scope
- N6: No encodings (except `I` prefix for interfaces — C# convention)
- N7: Names describe side effects

## Tests (T1-T9)

- T1: Test everything that could break
- T2: Use coverage tools (Coverlet, dotCover)
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
| **Functions** | F1 | Max 3 arguments (use record/object) |
| | F3 | No flag arguments |
| | F4 | Delete dead methods |
| **General** | G5 | DRY — no duplication |
| | G9 | Delete dead code |
| | G16 | No obscured intent |
| | G23 | Polymorphism over if/else |
| | G25 | Named constants, not magic numbers |
| | G30 | Methods do one thing |
| | G36 | Law of Demeter (one dot) |
| **C#** | CS1 | Properties, not public fields |
| | CS2 | LINQ over manual loops |
| | CS3 | async/await, never `.Result` |
| | CS5 | Nullable reference types enabled |
| | CS6 | Pattern matching switch expressions |
| **Names** | N1 | Descriptive names |
| | N5 | Name length matches scope |
| **Tests** | T5 | Test boundary conditions |
| | T9 | Tests must be fast |

## Anti-Patterns (Don't → Do)

| Don't | Do |
|-------|-----|
| `public string name;` | `public string Name { get; init; }` |
| Manual loop to filter/map | LINQ `.Where().Select()` |
| `task.Result` or `task.Wait()` | `await task` |
| `class DataDto { ... }` mutable | `record Data(string Name, int Age)` |
| `string? name = null!;` suppress | Handle nullable properly |
| `if/else if/else if` chains | `switch` expression with patterns |
| `using (var s = ...) { }` block | `using var s = ...;` declaration |
| Magic number `86400` | `const int SecondsPerDay = 86400;` |
| `catch (Exception) { }` swallow | Log and rethrow or handle specifically |
| `ILogger logger` as field | Primary constructor parameter (C# 12) |
| `obj.A.B.C.Value` | `obj.GetValue()` |

## Modern C# Idioms

```csharp
// CS1: Properties with init-only setters (C# 9+)
public class User
{
    public string Name { get; init; } = string.Empty;
    public string Email { get; init; } = string.Empty;
    public Role Role { get; init; } = Role.Member;
}

// CS4: Records for immutable data (C# 9+)
public record OrderSummary(string OrderId, decimal Total, DateTime CreatedAt);

// CS2: LINQ over manual loops
var activeEmails = users
    .Where(u => u.IsActive)
    .Select(u => u.Email)
    .ToList();

// CS3: async/await all the way
public async Task<Order> GetOrderAsync(string id, CancellationToken ct)
{
    var order = await _repository.FindByIdAsync(id, ct);
    return order ?? throw new NotFoundException($"Order {id} not found");
}

// CS5: Nullable reference types
public string? FindDisplayName(int userId)
{
    var user = _repo.Find(userId);
    return user?.DisplayName;
}

// CS6: Pattern matching switch expression (C# 8+)
public decimal CalculateArea(Shape shape) => shape switch
{
    Circle c => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    Triangle t => 0.5m * t.Base * t.Height,
    _ => throw new ArgumentException($"Unknown shape: {shape}")
};

// CS7: using declaration (C# 8+)
public async Task<string> ReadConfigAsync(string path)
{
    using var reader = new StreamReader(path);
    return await reader.ReadToEndAsync();
}

// CS8: Primary constructor for DI (C# 12+)
public class OrderService(
    IOrderRepository repository,
    IPaymentGateway payment,
    ILogger<OrderService> logger)
{
    public async Task<Order> ProcessAsync(CreateOrderRequest request)
    {
        logger.LogInformation("Processing order for {Customer}", request.CustomerId);
        var order = Order.Create(request);
        await payment.ChargeAsync(order.Total);
        await repository.SaveAsync(order);
        return order;
    }
}

// Collection expressions (C# 12+)
List<int> numbers = [1, 2, 3, 4, 5];
int[] primes = [2, 3, 5, 7, 11];

// Raw string literals (C# 11+)
var json = """
    {
        "name": "Alice",
        "role": "admin"
    }
    """;
```

## AI Behavior

When reviewing code, identify violations by rule number (e.g., "CS3 violation: blocking on `.Result`").
When fixing or editing code, report what was fixed (e.g., "Fixed: replaced public field with property (CS1)").
Before applying Modern C# idioms, check the `<TargetFramework>` and `<LangVersion>` in `.csproj`. C# 8: nullable refs, switch expressions, using declarations. C# 9: records, init-only. C# 10: global usings, file-scoped namespaces. C# 11: raw string literals. C# 12: primary constructors, collection expressions. Default to C# 10 / .NET 6 if no signal found.

