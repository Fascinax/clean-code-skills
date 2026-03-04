---
name: csharp-clean-general
description: Use when writing, fixing, editing, or reviewing C# code quality. Enforces Clean Code's core principles—DRY, single responsibility, clear intent, no magic numbers, proper abstractions.
---

# General Clean Code Principles (C#)

## Critical Rules

### G5: DRY (Don't Repeat Yourself)

Every piece of knowledge has one authoritative representation.

```csharp
// Bad — duplication
decimal CalculateCATax(decimal subtotal) => subtotal * 1.0825m;
decimal CalculateNYTax(decimal subtotal) => subtotal * 1.07m;

// Good — single source of truth
private static readonly Dictionary<string, decimal> TaxRates = new()
{
    ["CA"] = 0.0825m,
    ["NY"] = 0.07m,
};

public decimal CalculateTotal(decimal subtotal, string state)
    => subtotal * (1 + TaxRates[state]);
```

### G16: No Obscured Intent

Don't be clever. Be clear.

```csharp
// Bad — what does this do?
return (x & 0x0F) << 4 | (y & 0x0F);

// Good — obvious intent
return PackCoordinates(x, y);
```

### G23: Prefer Polymorphism to If/Else

```csharp
// Bad — will grow forever
public decimal CalculatePay(Employee emp) => emp.Type switch
{
    "salaried" => emp.Salary,
    "hourly" => emp.Hours * emp.Rate,
    "commissioned" => emp.Base + emp.Commission,
    _ => 0
};

// Good — open/closed principle via interfaces
public interface IPayCalculator
{
    decimal CalculatePay();
}

public record SalariedEmployee(decimal Salary) : IPayCalculator
{
    public decimal CalculatePay() => Salary;
}

public record HourlyEmployee(int Hours, decimal Rate) : IPayCalculator
{
    public decimal CalculatePay() => Hours * Rate;
}
```

### G25: Replace Magic Numbers with Named Constants

```csharp
// Bad
if (elapsedTime > 86400)
{
    // ...
}

// Good
const int SecondsPerDay = 86400;
if (elapsedTime > SecondsPerDay)
{
    // ...
}
```

### G30: Methods Should Do One Thing

If you can extract another method, your method does more than one thing.

### G36: Law of Demeter (Avoid Train Wrecks)

```csharp
// Bad — reaching through multiple objects
var path = context.Options.ScratchDir.AbsolutePath;

// Good — one level of access
var path = context.GetScratchDirPath();
```

## Enforcement Checklist

When reviewing AI-generated code, verify:

- [ ] No duplication (G5)
- [ ] Clear intent, no magic numbers (G16, G25)
- [ ] Polymorphism over conditionals (G23)
- [ ] Methods do one thing (G30)
- [ ] No Law of Demeter violations (G36)
- [ ] Boundary conditions handled (G3)
- [ ] Dead code removed (G9)
- [ ] Properties, not public fields (CS1)
- [ ] LINQ over manual loops (CS2)
- [ ] async/await, no blocking (CS3)
- [ ] Nullable reference types respected (CS5)

## Modern C# Idioms

```csharp
// Pattern matching for type checks (C# 8+)
public string Describe(object obj) => obj switch
{
    int i when i > 0 => $"Positive: {i}",
    string { Length: > 0 } s => $"Text: {s}",
    null => "Nothing",
    _ => obj.ToString() ?? "Unknown"
};

// Records for value semantics (C# 9+)
public record Money(decimal Amount, string Currency)
{
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException("Currency mismatch");
        return this with { Amount = Amount + other.Amount };
    }
}

// G28: Encapsulate conditionals with properties
public class Subscription
{
    public DateTime ExpiresAt { get; init; }
    public string Plan { get; init; } = "free";

    public bool IsActive => ExpiresAt > DateTime.UtcNow;
    public bool IsPremium => Plan == "premium" && IsActive;
}

// Collection expressions (C# 12+)
List<string> names = ["Alice", "Bob", "Charlie"];
ReadOnlySpan<int> primes = [2, 3, 5, 7, 11];

// Global using directives (C# 10+)
// GlobalUsings.cs
global using System.Collections.Generic;
global using System.Linq;

// File-scoped namespaces (C# 10+)
namespace MyApp.Services;

public class OrderService { }

// IAsyncEnumerable for streaming (C# 8+)
public async IAsyncEnumerable<Order> GetOrdersAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var order in _repository.StreamAllAsync(ct))
    {
        yield return order;
    }
}

// Span<T> for zero-allocation slicing
public static int CountDigits(ReadOnlySpan<char> text)
{
    var count = 0;
    foreach (var c in text)
    {
        if (char.IsDigit(c)) count++;
    }
    return count;
}
```

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| G3 | Handle boundary conditions | Edge cases, null, empty collections |
| G5 | DRY — no duplication | Single source of truth |
| G9 | Delete dead code | Unused usings, unreachable branches |
| G16 | No obscured intent | Extract to well-named method |
| G23 | Polymorphism over if/else | Growing conditional chains |
| G25 | Named constants, no magic numbers | `SecondsPerDay = 86400` |
| G30 | Methods do one thing | Can you extract another method? |
| G36 | Law of Demeter | Max one dot per expression |

## AI Behavior

When reviewing code quality, cite the rule number (e.g., "G25 violation: magic number `86400`").
When refactoring, explain the improvement (e.g., "Extracted constant `SecondsPerDay = 86400` (G25)").
When applying Modern C# idioms, check `.csproj` for `<LangVersion>` and `<TargetFramework>`. C# 8+: switch expressions, nullable refs. C# 9+: records. C# 10+: global usings, file-scoped namespaces. C# 12+: primary constructors, collection expressions. Default to C# 10 / .NET 6.

