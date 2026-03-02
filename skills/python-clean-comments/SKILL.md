---
name: python-clean-comments
description: Use when writing, fixing, editing, or reviewing Python comments and docstrings. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code.
---

# Clean Comments

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history,
ticket numbers, and dates. Comments are for technical notes about code only.

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists or works differently,
delete it immediately. Stale comments become "floating islands of
irrelevance and misdirection."

## C3: No Redundant Comments

```python
# Bad - the code already says this
i += 1  # increment i
user.save()  # save the user

# Good - explains WHY, not WHAT
i += 1  # compensate for zero-indexing in display
```

## C4: Write Comments Well

If a comment is worth writing, write it well:

- Choose words carefully
- Use correct grammar
- Don't ramble or state the obvious
- Be brief

## C5: Never Commit Commented-Out Code

```python
# DELETE THIS - it's an abomination
# def old_calculate_tax(income):
#     return income * 0.15
```

Who knows how old it is? Who knows if it's meaningful? Delete it.
Git remembers everything.

## Docstring Best Practices

Python has three major docstring conventions. Pick one per project and be consistent.

### Google Style (recommended for new projects)

```python
def transfer_funds(
    from_account: Account,
    to_account: Account,
    amount: Decimal,
) -> TransferResult:
    """Transfer funds between two accounts atomically.

    Either both accounts are updated or neither is. Insufficient
    funds result in a raised exception, not a partial transfer.

    Args:
        from_account: Source account to debit.
        to_account: Destination account to credit.
        amount: Positive amount to transfer.

    Returns:
        A TransferResult with the new balances of both accounts.

    Raises:
        InsufficientFundsError: If source balance is too low.
        ValueError: If amount is not positive.
    """
```

### NumPy Style (common in scientific/data projects)

```python
def calculate_moving_average(data, window_size):
    """Calculate the simple moving average of a dataset.

    Parameters
    ----------
    data : array_like
        Input data array.
    window_size : int
        Number of points to average over.

    Returns
    -------
    numpy.ndarray
        Array of moving averages, length ``len(data) - window_size + 1``.
    """
```

### When Type Hints Make Docstrings Redundant

```python
# Types are clear — docstring adds no value. Skip it.
def is_active(user: User) -> bool:
    return user.status == Status.ACTIVE

# Types aren't enough — docstring explains business logic.
def eligible_for_discount(user: User) -> bool:
    """Check discount eligibility based on tenure and spending.

    Users qualify if they have been members for 2+ years
    OR have spent more than $1000 in the last 90 days.
    """
```

## The Goal

The best comment is the code itself. If you need a comment to explain
what code does, refactor first, comment last.

## Quick Reference

| Rule | Principle | Key Signal |
|------|-----------|------------|
| C1 | No metadata in comments | Author, date, ticket → use Git |
| C2 | Delete obsolete comments | Stale comment → delete immediately |
| C3 | No redundant comments | Code says it already → remove comment |
| C4 | Write comments well | Brief, precise, explains WHY not WHAT |
| C5 | No commented-out code | Dead code → delete, Git remembers |

## AI Behavior

When reviewing comments, cite the rule number (e.g., "C3 violation: redundant comment restates the code").
When cleaning comments, explain the action (e.g., "Removed metadata comment, use Git for author tracking (C1)").
