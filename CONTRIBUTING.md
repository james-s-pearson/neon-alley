# Contributing to Neon Alley

Thank you for your interest. Bug reports, fixes for other plugins and
small, focused pull requests are welcome.

Neon Alley was designed and directed by James Pearson; its CSS and tools
were generated with AI assistance (Claude). Contributions made with AI
tools are welcome too; please say so in the pull request.

## Reporting a problem

Open an issue with your Obsidian version, your operating system, the
palette and structure you use, light or dark mode, any other theme or
CSS snippet that is turned on, and a screenshot if you can. Use notes
without private content in the screenshot.

## Making a change

- Edit `src/theme.src.css`, never `theme.css`: the build writes
  `theme.css` from the source, and a release is refused if the two do not
  match.
- Build and check contrast before opening a pull request:

  ```sh
  ./build.sh
  python3 tools/contrast.py src/theme.src.css
  ```

  The contrast check must report 0 failures in every palette and mode.
- Test in a fresh vault with no other plugins, in dark and light mode,
  and check Obsidian's developer console for errors.
- The theme loads nothing from the internet: fonts and wallpapers are
  embedded. Keep it that way.
- Keep each pull request to one change, and explain why it is needed.

## Licence

By contributing, you agree that your contribution is licensed under the
MIT licence in [LICENSE](LICENSE). The Chakra Petch font keeps its own
licence ([OFL.txt](OFL.txt)).
