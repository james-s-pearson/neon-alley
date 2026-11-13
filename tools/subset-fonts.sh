#!/bin/sh
# Makes the embedded Chakra Petch fonts smaller by keeping only the
# characters headings realistically use: Latin (with accents and phonetic
# letters), accent marks, Greek, punctuation, super- and subscripts,
# currency, fractions, common symbols and ligatures. Dropped: Thai, the
# precomposed Vietnamese letters and private-use symbols. The full fonts
# stay in src/fonts/full/. Chakra Petch is under the SIL Open Font License
# 1.1, which declares no Reserved Font Name, so the subset keeps its name.
# Needs fonttools and brotli: pip install fonttools brotli
# Usage: ./tools/subset-fonts.sh   (from the folder above tools/)
set -eu
cd "$(dirname "$0")/.."
for f in ChakraPetch-SemiBold ChakraPetch-Bold; do
  pyftsubset "src/fonts/full/$f.woff2" \
    --unicodes="U+0000-036F,U+0370-03FF,U+2000-209F,U+20A0-20CF,U+2100-218F,U+2190-21FF,U+2200-22FF,U+25A0-25FF,U+FB00-FB06" \
    --layout-features='*' --flavor=woff2 \
    --output-file="src/fonts/$f.woff2"
done
echo "Subset fonts written to src/fonts/"
