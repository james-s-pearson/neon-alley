# Changelog

## 1.1.0 (November 13, 2026)

- New Colors settings (Style Settings or Style Manager): the accent (or
  Obsidian's own accent color), the six neon colors, bold, italic and
  bold italic, each heading level, links, the default and severity
  tags, code colors, each callout type, the Retro frames, and text and
  background shades. Each has a dark and a light value; an empty color
  keeps the palette's own.
- New Look settings: use the body font for headings, normal-case
  headings, and sharp or rounded corners.
- Glow strength slider (0 to 2) for headings and links on hover. It
  replaces "Turn off heading glow": if you had turned the glow off, set
  Glow strength to 0.
- Three more built-in wallpapers in other colors: Rail line (green),
  Harbor (ice blue) and Tunnel (red).
- Mermaid diagrams follow the theme: accent outlines with a soft glow,
  cyan lines and neon chart colors.
- Tasks plugin: overdue due dates in red, due today in amber.
- File Explorer Note Count plugin: folder counts as small HUD-style tags.
- Smaller theme file for the same look: the embedded font keeps only the
  characters headings use (Thai and precomposed Vietnamese letters are
  dropped), and the wallpapers are embedded as text instead of base64.
- The editor's italic keywords no longer use a :has() selector, which
  Obsidian's theme review flagged; they look the same.
- American English spelling in the theme's comments and settings.

## 1.0.1 (November 12, 2026)

- Mission-status task markers (`[/]`, `[!]`, `[?]`, `[>]`, `[-]`) work
  again in Obsidian 1.15, which moved the task status from the checkbox
  to its line; both are now matched.
- Canceled tasks (`[-]`) are faded and struck through again.
- New screenshots, taken in a demo vault: a full-window view with
  wallpaper, and Retro, light and Cold Forge views.

## 1.0.0 (November 12, 2026)

First public release.

- Inline-code styling no longer spreads into code blocks (no raised
  boxes behind code lines; uncolored code keeps the code color).
- Custom wallpaper help text no longer shows a web address.
- Release workflow: GitHub release made from a version tag, with a check
  that theme.css is built from the source.

## 0.3.0

- Code colors and code-block background now match LazyVim's default
  Tokyo Night (moon and day), checked against Neovim's own
  highlighting.
- H2 now has a fine underline like H1, in its own color.
- The theme now paints the space behind the panes itself, so it stays
  the palette's frame color with Obsidian's translucent window on and
  whatever macOS appearance is set.
- Built-in wallpapers: "Neon skyline", "Rain alley" and "Sodium street"
  (SVG drawn by `tools/skyline.py` and `tools/scenes.py`), with dimming,
  a custom image option or none.
- See-through, blurred panes in Glass and Retro whenever Obsidian's
  Translucent window setting is on; opacity and blur are adjustable.
- Retro: optional glass sheen on the framed panes.
- Neon Alley palette: links are now amber, italics wet teal and bold
  italics neon fuchsia. Default tags stay cyan.
- Retro: header frames are now orange and content frames cyan (Sodium
  Rain: content frames wet teal).
- Light mode for all four palettes.
- Mission-status tasks: `[/]`, `[!]`, `[?]`, `[>]` and `[-]`.
- Shape markers on severity tags (◆ ▲ ■ ▼ ●), with an option to turn
  them off.
- HUD-style status bar, link glow on hover and optional CRT scanlines.
- Graph view and Canvas colors for every palette.
- Calendar and Kanban plugin styling.
- Severity and status colors now also apply to tags in Properties.
- Every text color meets WCAG contrast targets in all eight palette
  and mode combinations.
- Fonts embedded as WOFF2; the theme is now about 108 KB, down from
  about 247 KB.
- Retro structure: sidebars framed as one block, and room left for the
  status bar.

## 0.2.0

- One theme with four palettes (Neon Alley, Sodium Rain, Cold Forge,
  Polar Ember), two structures (Glass, Retro) and two callout styles
  (HUD, Glass).
- Retro structure written from scratch.

## 0.1.0

- First version: Neon Alley palette, glass panes, HUD callouts, security
  and project callouts, severity tags.
