#!/usr/bin/env python3
"""Write themes/kanagawa-<variant> from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
# The 16 ANSI colors, normal then bright.
COLORS = [f"term.{c}" for c in ANSI] + [f"term.bright_{c}" for c in ANSI]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}

NAMES = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]


def rgb(h):
    return ",".join(str(int(h[i : i + 2], 16)) for i in (1, 3, 5))


def theme(variant, appearance, c):
    out = [
        f"ForegroundColour={rgb(c['ui.fg'])}",
        f"BackgroundColour={rgb(c['ui.bg'])}",
        f"CursorColour={rgb(c['ui.fg_dim'])}",
        f"HighlightBackgroundColour={rgb(c['ui.bg_visual'])}",
        f"HighlightForegroundColour={rgb(c['ui.fg'])}",
    ]
    for n, r, b in zip(NAMES, COLORS[:8], COLORS[8:]):
        out += [f"{n}={rgb(c[r])}", f"Bold{n}={rgb(c[b])}"]
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(theme(v, variants[v]["appearance"], roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
