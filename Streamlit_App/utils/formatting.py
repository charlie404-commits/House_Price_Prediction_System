"""
utils/formatting.py
--------------------
Presentation-only helpers: Indian currency formatting, timestamps,
and small text helpers. No ML logic lives here.
"""

from __future__ import annotations

from datetime import datetime


def format_inr(amount: float, *, with_symbol: bool = True) -> str:
    """
    Format a number using the Indian numbering system (lakh/crore commas),
    e.g. 12345678 -> "1,23,45,678".
    """
    amount = round(float(amount))
    negative = amount < 0
    amount = abs(amount)

    s = str(amount)
    if len(s) <= 3:
        grouped = s
    else:
        last_three = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last_three

    result = f"{'-' if negative else ''}{grouped}"
    return f"₹ {result}" if with_symbol else result


def format_inr_short(amount: float) -> str:
    """Compact form for cards/stats, e.g. 1.24 Cr, 8.5 L."""
    amount = float(amount)
    abs_amount = abs(amount)
    sign = "-" if amount < 0 else ""

    if abs_amount >= 1_00_00_000:
        return f"{sign}₹{abs_amount / 1_00_00_000:.2f} Cr"
    if abs_amount >= 1_00_000:
        return f"{sign}₹{abs_amount / 1_00_000:.2f} L"
    if abs_amount >= 1_000:
        return f"{sign}₹{abs_amount / 1_000:.1f} K"
    return f"{sign}₹{abs_amount:.0f}"


def now_timestamp() -> str:
    """ISO-ish, human-friendly timestamp for history/report records."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def humanize_timestamp(ts: str) -> str:
    """Convert a stored timestamp into a friendlier display string."""
    try:
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        return ts
