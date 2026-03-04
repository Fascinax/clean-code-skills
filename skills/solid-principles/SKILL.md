---
name: solid-principles
description: Use when writing, fixing, editing, or reviewing class design in Python, Java, TypeScript, or JavaScript. Enforces SOLID principles—single responsibility, open-closed, Liskov substitution, interface segregation, and dependency inversion.
---

# SOLID Principles

These five design principles help keep class hierarchies maintainable and extensible. Each violation makes future change harder; each application makes it safer.

## S — Single Responsibility Principle

A class should have one, and only one, reason to change.

```python
# Bad — UserSettings does settings AND auth
class UserSettings:
    def __init__(self, user):
        self.user = user

    def change_setting(self, setting, value):
        if self.verify_credentials():
            ...

    def verify_credentials(self):
        ...

# Good — split into focused classes
class UserAuth:
    def __init__(self, user):
        self.user = user

    def verify_credentials(self):
        ...

class UserSettings:
    def __init__(self, user, auth: UserAuth):
        self.user = user
        self.auth = auth

    def change_setting(self, setting, value):
        if self.auth.verify_credentials():
            ...
```

```typescript
// Bad — class manages both settings and authentication
class UserSettings {
  constructor(private user: User) {}
  changeSetting(setting: string, value: string): void {
    if (this.verifyCredentials()) { /* ... */ }
  }
  verifyCredentials(): boolean { /* ... */ }
}

// Good — separate responsibilities
class UserAuth {
  constructor(private user: User) {}
  verifyCredentials(): boolean { /* ... */ }
}

class UserSettings {
  constructor(private user: User, private auth: UserAuth) {}
  changeSetting(setting: string, value: string): void {
    if (this.auth.verifyCredentials()) { /* ... */ }
  }
}
```

## O — Open/Closed Principle

Classes should be open for extension, closed for modification.

```java
// Bad — modifying existing code for every new adapter
public class HttpRequester {
    public void fetch(String url, Object adapter) {
        if (adapter instanceof AjaxAdapter) {
            ((AjaxAdapter) adapter).makeRequest(url);
        } else if (adapter instanceof FetchAdapter) {
            ((FetchAdapter) adapter).makeRequest(url);
        }
    }
}

// Good — extend via abstraction
public interface HttpAdapter {
    void makeRequest(String url);
}

public class HttpRequester {
    private final HttpAdapter adapter;

    public HttpRequester(HttpAdapter adapter) {
        this.adapter = adapter;
    }

    public void fetch(String url) {
        adapter.makeRequest(url);
    }
}
```

```javascript
// Bad — if/else checks for every adapter type
class HttpRequester {
  constructor(adapter) { this.adapter = adapter; }
  fetch(url) {
    if (this.adapter.name === 'ajaxAdapter') {
      return makeAjaxCall(url);
    } else if (this.adapter.name === 'fetchAdapter') {
      return makeFetchCall(url);
    }
  }
}

// Good — polymorphic adapter, no modification needed
class HttpRequester {
  constructor(adapter) { this.adapter = adapter; }
  fetch(url) {
    return this.adapter.request(url);
  }
}
```

## L — Liskov Substitution Principle

Subtypes must be substitutable for their base types without breaking the program.

```python
# Bad — Square breaks Rectangle's expected behavior
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    def area(self):
        return self._width * self._height

class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = value
        self._height = value  # surprise: setting width changes height

# Good — separate hierarchy from a shared abstraction
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

class Square(Shape):
    def __init__(self, size: float):
        self.size = size

    def area(self) -> float:
        return self.size ** 2
```

## I — Interface Segregation Principle

Clients should not be forced to depend on methods they do not use.

```java
// Bad — one fat interface forces every implementer to stub unused methods
public interface SmartDevice {
    void print(Document doc);
    void fax(Document doc);
    void scan(Document doc);
}

public class SimplePrinter implements SmartDevice {
    public void print(Document doc) { /* ok */ }
    public void fax(Document doc) { throw new UnsupportedOperationException(); }
    public void scan(Document doc) { throw new UnsupportedOperationException(); }
}

// Good — segregated interfaces
public interface Printer { void print(Document doc); }
public interface Fax    { void fax(Document doc); }
public interface Scanner { void scan(Document doc); }

public class SimplePrinter implements Printer {
    public void print(Document doc) { /* ok */ }
}

public class MultiFunctionDevice implements Printer, Fax, Scanner {
    public void print(Document doc) { /* ... */ }
    public void fax(Document doc)   { /* ... */ }
    public void scan(Document doc)  { /* ... */ }
}
```

## D — Dependency Inversion Principle

High-level modules should not depend on low-level modules. Both should depend on abstractions.

```typescript
// Bad — high-level module creates its own low-level dependency
class XmlFormatter {
  format(data: ReportData): string { /* ... */ }
}

class ReportReader {
  private formatter = new XmlFormatter();   // hard-wired
  read(): string { return this.formatter.format(this.data); }
}

// Good — depend on an abstraction, inject it
interface Formatter {
  format(data: ReportData): string;
}

class XmlFormatter implements Formatter {
  format(data: ReportData): string { /* ... */ }
}

class JsonFormatter implements Formatter {
  format(data: ReportData): string { /* ... */ }
}

class ReportReader {
  constructor(private formatter: Formatter) {}
  read(): string { return this.formatter.format(this.data); }
}
```

## Quick Reference

| Principle | Rule of Thumb | Code Smell |
|-----------|---------------|------------|
| **S**ingle Responsibility | One class = one reason to change | Class has `AND` in its description |
| **O**pen/Closed | Add behavior by extending, not modifying | `if/else` or `instanceof` chains for types |
| **L**iskov Substitution | Subtype must honor supertype's contract | Override that throws or silently breaks |
| **I**nterface Segregation | Many small interfaces > one fat interface | `NotImplementedError` / `UnsupportedOperationException` |
| **D**ependency Inversion | Depend on abstractions, inject them | `new` inside a constructor for a collaborator |

## AI Behavior

When reviewing class design, cite the principle (e.g., "SRP violation: this class manages both auth and settings").
When refactoring, explain the fix (e.g., "Extracted XmlFormatter behind a Formatter interface to satisfy DIP").
Apply the most relevant principle—don't force all five onto every review.
