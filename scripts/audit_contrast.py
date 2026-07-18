#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Pair:
    name: str
    foreground: str
    background: str
    minimum: float

PAIRS = [
    Pair("body text", "#17201c", "#f3eee2", 4.5),
    Pair("muted text", "#58615b", "#f3eee2", 4.5),
    Pair("link", "#164f75", "#f3eee2", 4.5),
    Pair("white on wood", "#ffffff", "#24533d", 4.5),
    Pair("white on fire", "#ffffff", "#8a332c", 4.5),
    Pair("white on earth", "#ffffff", "#765d25", 4.5),
    Pair("white on metal", "#ffffff", "#424a52", 4.5),
    Pair("white on water", "#ffffff", "#204d68", 4.5),
]

def channel(value: int) -> float:
    c = value / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hex_color: str) -> float:
    value = hex_color.lstrip("#")
    r, g, b = (int(value[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast(a: str, b: str) -> float:
    l1, l2 = sorted((luminance(a), luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

def main() -> int:
    failed = False
    for pair in PAIRS:
        ratio = contrast(pair.foreground, pair.background)
        status = "PASS" if ratio >= pair.minimum else "FAIL"
        print(f"{status}: {pair.name}: {ratio:.2f}:1")
        failed = failed or status == "FAIL"
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
