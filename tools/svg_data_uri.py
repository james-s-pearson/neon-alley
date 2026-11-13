#!/usr/bin/env python3
"""Print an SVG file as a compact CSS data URI.

SVG is text, so it is embedded URL-encoded instead of base64 (base64 makes
it about a third bigger). Whitespace between tags is collapsed, double
quotes become single quotes, and the characters that are unsafe in a CSS
url() are percent-encoded. Usage: svg_data_uri.py FILE.svg
"""
import re
import sys

svg = open(sys.argv[1], encoding="utf-8").read().strip()
svg = re.sub(r">\s+<", "><", svg)
svg = re.sub(r"\s+", " ", svg)
svg = svg.replace('"', "'")
for ch, code in (("%", "%25"), ("#", "%23"), ("<", "%3C"), (">", "%3E"),
                 ("{", "%7B"), ("}", "%7D"), ("\\", "%5C")):
    svg = svg.replace(ch, code)
print(f'url("data:image/svg+xml,{svg}")', end="")
