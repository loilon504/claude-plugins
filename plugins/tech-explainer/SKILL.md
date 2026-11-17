---
name: tech-explainer
description: Explains how a technical system works as a published artifact page in one house style - Maple Mono and JetBrains Mono, Nerd Font icons, one colour per component, hand-drawn SVG diagrams, annotated config files, exact code proofs with line numbers, side-by-side file changes, light and dark themes. Use when the user asks to explain or document how services, pipelines, configs or code paths work together, to answer how/why questions about code or infrastructure with proof, to lay out a plan of file changes, or names tech-explainer, an explainer page, or "an artifact like the last one".
---

# tech-explainer

Makes one self-contained HTML page that explains a technical system to someone who has to act on it:
what the parts are, how they talk, where each name and file goes, what to change, and the proof for each
claim. The look is fixed so every page reads the same; the work is in the facts.

`$SKILL` below is this skill's base directory (shown when the skill loads).

## Workflow

1. **Facts first.** Read the real sources: code, configs, templates, logs, the running system. Note every
   file:line, commit, image tag and log date as you go; the page cites them. When behaviour can be shown
   cheaply (a throwaway container, a config check such as `haproxy -c`, a dry run), run it and show the
   output. Never invent a name, port or path: mark it as assumed and list it under "not checked".
2. **Plan the page.** One thesis (the `h1` and lead), three key cards, then sections in the order the reader
   needs them, ending with the answers to the user's questions. Give each component of the system one colour
   slot and one icon (`scripts/icons.py`), and keep that pair on every mention.
3. **Start from the template.** Copy `$SKILL/assets/template.html` to the working folder (the scratchpad
   unless the user names one) as `src.html`. Keep its `/*@FONTS@*/` and `/*@BASE@*/` markers.
4. **Write it** from `$SKILL/references/components.md` (every block, as HTML) and
   `$SKILL/references/diagrams.md` (how to draw). For file changes, write the new files beside copies of the
   old ones and use the side-by-side placeholder.
5. **Build:** `python3 $SKILL/scripts/build.py src.html <name>.html [--root <folder of old/ and new/>]`.
   It fills the side-by-side tables, inlines `base.css`, embeds the fonts and cuts the icon font to the icons
   used. Read its notes: an icon it says will not show must be replaced.
6. **Check:** `python3 $SKILL/scripts/svgfit.py src.html` (expect `labels over: 0`). Then take one look,
   as the Artifact tool allows: its preview, or `node $SKILL/scripts/shoot.cjs <name>.html shots/ [selectors]`
   (light, dark, phone; page width must equal the viewport). Fix what the look shows in one pass.
7. **Publish** the built file with the Artifact tool, loading `artifact-design` first as that tool requires.
   This skill is the page's existing design system, so its rules come first. The title is the `h1`: a name of
   two to four words. To update, edit `src.html`, rebuild and publish the same file path.
8. **Reply** with the link and a short account of what the page says, in the user's language.

## Writing rules

- **Ignore nitpicks and edge cases.** Mention one in a single line at most, and never go deep into it. The
  page is for the main path; detail that does not change what the reader does makes it harder to read.
- Conclusion first, then the evidence. Each section opens by saying what it shows.
- Plain words. Explain a term the first time it appears, or leave it out.
- Every claim about code cites `file:line`; quote the lines exactly (components.md, "Code proof"). Every
  figure from a log says which log and which dates.
- Say what was checked and what was not. An assumption is labelled as one, never stated as fact.
- When the user corrects the goal, rewrite the page around the new goal and delete what no longer applies.
  Do not keep a stale section with a note on it.
- Write the page in the language the user writes in (the fonts cover Vietnamese). Code, paths and config
  stay as they are.
- Structure carries meaning: numbers only for real sequences, a callout only for what must not be missed
  (one or two a section), a table when the reader compares rows.

## Design rules

- Fonts: Maple Mono NF for text, JetBrains Mono NF for code, embedded by `build.py`; Nerd Font icons from
  the Material Design set (`md-…`, outline style first).
- Colour: only the tokens in `base.css`: slots `blue teal plum amber olive slate`, plus `good` and `bad`.
  Never a literal colour; every token has light and dark values.
- Layout: `.wrap` holds the page (max 1160px). Running text in `.prose` (about 72 characters); figures,
  tables, code and diff tables run full width and scroll sideways on a phone, never the page.
- Add page-only CSS only when no component fits, in the template's `<style>`, through the tokens.

## Files

| Path | What |
|---|---|
| `assets/template.html` | the starting page: header, legend, contents, key cards, a section with a diagram, questions, footer |
| `assets/base.css` | every style; `build.py` inlines it |
| `references/components.md` | each block as HTML: tables, annotated configs, code proofs, side-by-side changes, callouts, options, answers |
| `references/diagrams.md` | SVG grid, box and text classes, arrows, sequence diagrams |
| `scripts/build.py` | builds the page (Python 3; `pip install fonttools` cuts the icon font exactly, else a 158-icon common set is used) |
| `scripts/icons.py` | `icons.py rocket launch` finds icons by name; `--code f14df` names one |
| `scripts/svgfit.py` | lists diagram labels that leave their box |
| `scripts/shoot.cjs` | screenshots at light, dark and phone width (needs Playwright) |
| `fonts/` | the fonts (SIL Open Font License, see the license files), Nerd Font glyph names |
