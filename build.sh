#!/bin/sh
# Builds theme.css from src/theme.src.css and embeds the fonts and
# the built-in wallpapers (made by tools/skyline.py and tools/scenes.py).
# Usage: ./build.sh            (writes theme.css next to this script)
set -eu
cd "$(dirname "$0")"

font_face() {
  # $1 = font file, $2 = weight
  printf '@font-face {\n  font-family: "Chakra Petch";\n  font-weight: %s;\n  font-style: normal;\n  font-display: swap;\n  src: url(data:font/woff2;base64,%s) format("woff2");\n}\n' \
    "$2" "$(base64 < "$1" | tr -d '\n')"
}

{
  cat src/theme.src.css
  font_face src/fonts/ChakraPetch-SemiBold.woff2 600
  font_face src/fonts/ChakraPetch-Bold.woff2 700
  for pair in skyline:neon-skyline alley:rain-alley sodium:sodium-street; do
    printf 'body {\n  --na-%s: url(data:image/svg+xml;base64,%s);\n}\n' \
      "${pair%%:*}" "$(base64 < "src/wallpapers/${pair#*:}.svg" | tr -d '\n')"
  done
} > theme.css

echo "Built theme.css ($(wc -c < theme.css | tr -d ' ') bytes)"
