#!/usr/bin/env python3
import json
import sys
from datetime import datetime


def bar(pct, width=10):
    filled = round(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def color(pct):
    if pct >= 80:
        return "\033[31m"
    if pct >= 50:
        return "\033[33m"
    return "\033[32m"


def window(label, data, time_format):
    if not data or data.get("used_percentage") is None:
        return None
    pct = float(data["used_percentage"])
    text = f"{label} {color(pct)}{bar(pct)} {pct:.0f}%\033[0m"
    resets_at = data.get("resets_at")
    if resets_at:
        text += f" ↻{datetime.fromtimestamp(resets_at).strftime(time_format)}"
    return text


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    parts = [(payload.get("model") or {}).get("display_name", "")]
    limits = payload.get("rate_limits") or {}
    for part in (
        window("5h", limits.get("five_hour"), "%H:%M"),
        window("7j", limits.get("seven_day"), "%a %H:%M"),
    ):
        if part:
            parts.append(part)
    context = (payload.get("context_window") or {}).get("used_percentage")
    if context is not None:
        parts.append(f"ctx {float(context):.0f}%")
    print(" │ ".join(p for p in parts if p))


main()
