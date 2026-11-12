# Changelog

## 1.0.1 (12 November 2026)

- Mission-status task markers (`[/]`, `[!]`, `[?]`, `[>]`, `[-]`) work
  again in Obsidian 1.15, which moved the task status from the checkbox
  to its line; both are now matched.
- Cancelled tasks (`[-]`) are faded and struck through again.
- New screenshots, taken in a demo vault: a full-window view with
  wallpaper, and Retro, light and Cold Forge views.

## 1.0.0 (12 November 2026)

First public release.

- Inline-code styling no longer spreads into code blocks (no raised
  boxes behind code lines; uncoloured code keeps the code colour).
- Custom wallpaper help text no longer shows a web address.
- Release workflow: GitHub release made from a version tag, with a check
  that theme.css is built from the source.

## 0.3.0

- Code colours and code-block background now match LazyVim's default
  Tokyo Night (moon and day), checked against Neovim's own
  highlighting.
- H2 now has a fine underline like H1, in its own colour.
- The theme now paints the space behind the panes itself, so it stays
  the palette's frame colour with Obsidian's translucent window on and
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
- Graph view and Canvas colours for every palette.
- Calendar and Kanban plugin styling.
- Severity and status colours now also apply to tags in Properties.
- Every text colour meets WCAG contrast targets in all eight palette
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
