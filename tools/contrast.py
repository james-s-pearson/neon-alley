#!/usr/bin/env python3
"""Check WCAG contrast for every Neon Alley palette.

Reads the palette blocks in src/theme.src.css and checks each text
color against the note and sidebar backgrounds:

- body text: 7:1 or more
- colored text (headings, links, bold, italics, tags): 4.5:1
- faint text: 3:1

Usage: python3 tools/contrast.py src/theme.src.css
"""
import re
import sys

ROLES = ["text", "muted", "faint", "red", "orange", "gold", "green",
         "blue", "cyan", "bold", "italic", "bold-italic", "link", "accent",
         "h1", "h2", "h3", "h4", "h5", "h6"]
BLOCK = re.compile(r"\n(\.theme-(dark|light)(\.na-[a-z-]+)?) \{\n(.*?)\n\}",
                   re.S)


def luminance(hex_color):
    h = hex_color.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    channels = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
                for c in channels]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def ratio(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def main(path):
    source = open(path, encoding="utf-8").read()
    blocks = {}
    for m in BLOCK.finditer(source):
        selector = m.group(1)
        if selector not in blocks:
            values = dict(re.findall(r"--na-([a-z0-9-]+):\s*([^;]+);",
                                     m.group(4)))
            blocks[selector] = (m.group(2), values)

    failures = 0
    for selector, (mode, values) in blocks.items():
        merged = {**blocks[f".theme-{mode}"][1], **values}

        def resolve(value):
            value = value.strip()
            ref = re.fullmatch(r"var\(--na-([a-z0-9-]+)\)", value)
            return resolve(merged[ref.group(1)]) if ref else value

        problems = []
        for background in ("page", "side"):
            bg = resolve(merged[background])
            for role in ROLES:
                if role not in merged:
                    continue
                color = resolve(merged[role])
                if not color.startswith("#"):
                    continue
                need = 7 if role == "text" else 3 if role == "faint" else 4.5
                r = ratio(color, bg)
                if r < need:
                    problems.append(f"{role} on {background}: {r:.2f} "
                                    f"(need {need}) {color} on {bg}")
        print(selector, "OK" if not problems else "")
        for p in problems:
            print("   ", p)
        failures += len(problems)

    print("failures:", failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "src/theme.src.css"))
