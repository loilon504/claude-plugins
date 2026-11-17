# tech-explainer

A Claude Code skill, packaged as a plugin, that turns "how does this system work?" into one published artifact
page: monospace type (Maple Mono, JetBrains Mono), Nerd Font icons, one colour per component, hand-drawn SVG
diagrams, annotated config files, code proofs quoted with line numbers, and side-by-side file changes. Light and
dark, phone width.

Ask for it in words ("explain how X and Y work together, as a page") or by name. The workflow and rules are in
`SKILL.md`; the blocks in `references/`.

## Install

```
/plugin install tech-explainer --marketplace loilon504/claude-plugins
```

(`claude plugin install tech-explainer --marketplace loilon504/claude-plugins` from a shell.)

## Needs

- Python 3. `pip install fonttools` (and `brotli` for smaller files) lets the build cut the icon font to exactly
  the icons a page uses; without it, a built-in set of 158 common icons is embedded.
- Optional: Node with Playwright and Chromium, for `scripts/shoot.cjs` screenshots.

## Fonts

Maple Mono NF and JetBrains Mono Nerd Font, under the SIL Open Font License 1.1 (`fonts/*-license.txt`).
`fonts/glyphnames.json` is from Nerd Fonts 3.5.1.
