---
name: csharp-clean-tests
description: Use when writing, fixing, editing, or refactoring C# tests. Enforces Clean Code principles—fast tests, boundary coverage, one concept per test, xUnit/NUnit best practices.
---

# Clean Tests (C#)

## T1: Insufficient Tests

Test everything that could possibly break. Use coverage tools as a guide, not a goal.

```csharp
// Bad — only tests happy path
[Fact]
public void Divide_ReturnsQuotient()
{
    Assert.Equal(5, Calculator.Divide(10, 2));
}

// Good — tests edge cases too
[Fact]
public void Divide_Normal_ReturnsQuotient()
{
    Assert.Equal(5m, Calculator.Divide(10, 2));
}

[Fact]
public void Divide_ByZero_ThrowsDivideByZeroException()
{
    Assert.Throws<DivideByZeroException>(() => Calculator.Divide(10, 0));
}

[Fact]
public void Divide_Negative_ReturnsNegativeQuotient()
{
    Assert.Equal(-5m, Calculator.Divide(-10, 2));
}
```

## T2: Use a Coverage Tool

```bash
# Coverlet with dotnet test
dotnet test --collect:"XPlat Code Coverage"

# Generate HTML report
dotnet tool install -g dotnet-reportgenerator-globaltool
reportgenerator -reports:coverage.cobertura.xml -targetdir:coveragereport
```

## T3: Don't Skip Trivial Tests

Trivial tests document behavior and catch regressions.

```csharp
[Fact]
public void User_DefaultRole_IsMember()
{
    var user = new User("Alice");
    Assert.Equal(Role.Member, user.Role);
}
```

## T4: An Ignored Test Is a Question About an Ambiguity

Don't use `[Skip]` to hide problems. Either fix the test or delete it.

```csharp
// Bad — hiding a problem
[Fact(Skip = "Flaky, fix later")]
public void AsyncOperation_Should_Complete() { }

// Good — documents a real constraint
[Fact(Skip = "Requires Redis; run integration tests separately")]
public void CacheInvalidation_Should_PropagateAsync() { }
```

## T5: Test Boundary Conditions

Bugs congregate at boundaries. Test them explicitly.

```csharp
[Theory]
[InlineData(1, 10, 10)]   // first page
[InlineData(10, 10, 10)]  // last page
[InlineData(11, 10, 0)]   // beyond last page
public void Paginate_ReturnsCorrectCount(int page, int size, int expected)
{
    var items = Enumerable.Range(0, 100).ToList();
    var result = Paginator.Paginate(items, page, size);
    Assert.Equal(expected, result.Count);
}

[Fact]
public void Paginate_ZeroPage_ThrowsArgumentException()
{
    Assert.Throws<ArgumentException>(() => Paginator.Paginate(new List<int>(), 0, 10));
}

[Fact]
public void Paginate_EmptyList_ReturnsEmpty()
{
    var result = Paginator.Paginate(new List<int>(), 1, 10);
    Assert.Empty(result);
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

```csharp
// Bad — hits real database
[Fact]
public async Task CreateUser_PersistsToDatabase()
{
    var db = new SqlConnection(connectionString); // Slow!
    // ...
}

// Good — uses mock
[Fact]
public async Task CreateUser_CallsRepository()
{
    var repo = new Mock<IUserRepository>();
    var svc = new UserService(repo.Object);
    await svc.CreateAsync(new CreateUserRequest("Alice", "alice@test.com"));
    repo.Verify(r => r.SaveAsync(It.IsAny<User>(), default), Times.Once);
}
```

## Test Organization

### xUnit Conventions

```csharp
// One test class per production class
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _repo = new();
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _sut = new OrderService(_repo.Object);
    }

    [Fact]
    public async Task ProcessOrder_ValidOrder_ReturnsReceipt() { ... }

    [Fact]
    public async Task ProcessOrder_EmptyOrder_ThrowsException() { ... }
}
```

### Test Naming Convention

Use `Method_Scenario_Expected` for clarity.

```csharp
[Fact] public void FindByEmail_ExistingUser_ReturnsUser() { }
[Fact] public void FindByEmail_UnknownEmail_ReturnsNull() { }
[Fact] public void Transfer_InsufficientFunds_ThrowsException() { }
[Fact] public void Paginate_EmptyList_ReturnsEmpty() { }
```

### AAA Pattern

```csharp
[Fact]
public void ApplyDiscount_ValidCoupon_ReducesTotal()
{
    // Arrange
    var order = new Order(new[] { new Item(Price: 100m) }, Coupon: "SAVE10");

    // Act
    var discounted = DiscountService.Apply(order);

    // Assert
    Assert.Equal(90m, discounted.Total);
}
```

## Modern C# Test Idioms

```csharp
// [Theory] + [InlineData] for parameterized tests (xUnit)
[Theory]
[InlineData(2024, 1, 31)]
[InlineData(2024, 2, 29)]   // leap year
[InlineData(2023, 2, 28)]   // non-leap year
[InlineData(2024, 4, 30)]
[InlineData(2024, 12, 31)]
public void LastDayOfMonth_ReturnsCorrectDay(int year, int month, int expected)
{
    Assert.Equal(expected, DateHelper.LastDayOfMonth(year, month));
}

// FluentAssertions for readable assertions
using FluentAssertions;

[Fact]
public void Order_Total_SumsAllItems()
{
    var order = new Order(new[] { new Item(100m), new Item(200m) });
    order.Total.Should().Be(300m);
}

[Fact]
public async Task GetOrder_NotFound_ThrowsWithMessage()
{
    var act = () => _sut.GetOrderAsync("unknown");
    await act.Should().ThrowAsync<NotFoundException>()
        .WithMessage("*unknown*");
}

// NSubstitute for clean mocking
using NSubstitute;

[Fact]
public async Task ProcessOrder_SendsConfirmation()
{
    var emailService = Substitute.For<IEmailService>();
    var sut = new OrderService(emailService);

    await sut.ProcessAsync(sampleOrder);

    await emailService.Received(1).SendAsync(
        Arg.Is<Email>(e => e.To == sampleOrder.CustomerEmail));
}

// TestContainers for integration tests (C#)
[Fact]
public async Task Repository_SaveAndRetrieve()
{
    await using var container = new PostgreSqlBuilder().Build();
    await container.StartAsync();
    // ...
}

// AutoFixture for test data generation
[Theory, AutoData]
public void User_WithRandomData_IsValid(string name, string email)
{
    var user = new User(name, $"{email}@test.com");
    Assert.True(user.IsValid());
}
```

## Quick Reference

| Rule | Principle |
|------|-----------|
| T1 | Test everything that could break |
| T2 | Use coverage tools (Coverlet) |
| T3 | Don't skip trivial tests |
| T4 | Ignored test = ambiguity question |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Look for patterns in failures |
| T8 | Check coverage when debugging |
| T9 | Tests must be fast (<100ms) |

## AI Behavior

When reviewing tests, cite the rule number (e.g., "T5 violation: no boundary condition tests").
When writing tests, prefer `[Theory] + [InlineData]` for parameterized cases.
Use AAA pattern (Arrange/Act/Assert) and `Method_Scenario_Expected` naming.

