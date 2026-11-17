# Diagrams

Inline SVG, drawn by hand on a fixed grid, styled only by classes from `base.css` so both themes work.
Draw a diagram only when it shows something prose cannot: who talks to whom, in what order, where a name
or a file goes. One idea per diagram.

## Frame

```html
<svg class="dg" viewBox="0 0 1160 H" role="img" aria-label="The whole story of the diagram in one sentence.">
  <defs>
    <marker id="d1t" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path class="ah-teal" d="M0,0 L8,4 L0,8 z"/></marker>
  </defs>
  …
</svg>
```

- Width is always 1160 (the page column). `.dg` keeps a 900px minimum and its `.scroll` wrapper scrolls on
  phones. Set the height H to the content plus 16px.
- One marker per arrow colour, ids unique on the page: `d<diagram number><slot letter>`, e.g. `d3b`.
  Arrowhead classes: `ah-n` (grey) or `ah-SLOT`, `ah-good`, `ah-bad`.
- Keep 16px from the viewBox edges.

## Boxes

| Class | Use |
|---|---|
| `b` | a plain box (a folder, a user) |
| `b-SLOT` | a component, in its slot colour |
| `b-good`, `b-bad` | a good or broken state |
| `b-off` | dashed grey: a step that runs but does nothing, or something optional |
| `b-new` | dashed teal: something the page proposes to add |
| `zonebox` | dashed grey area: a container or host holding other boxes |
| `panel` | filled area: one side of a two-column comparison |
| `band` | a full-width strip naming a phase of a sequence diagram |
| `note` | a small grey box for a side remark |

Boxes use `rx="10"` (areas `rx="14"` or `16`). Usual sizes: a component 180–220 × 56–64, a sequence head
152 × 48.

## Text

| Class | Size | Use |
|---|---|---|
| (none) | 13px | ordinary label |
| `ttl` | 14px bold | a box's name |
| `sub` | 11.5px muted | the line under a name, a label on an arrow |
| `mono` | 11.5px JetBrains | a path, a command, a config line |
| `eb` | 11px caps | the name of an area or a phase ("1 · LIBRARY STEP") |
| `big` | 16px | rare emphasis |
| `t-SLOT`, `t-good`, `t-bad` | | colour, added to the above |
| `halo` | | outlines a label in the surface colour so it reads over lines (`halo-z` on a zone) |

A box's name sits 27px below the box top and its sub-line 48px below, both centred:
`<text class="ttl t-teal" x="CENTRE" y="TOP+27" text-anchor="middle"><tspan class="ic">&#xF171A;</tspan> worker</text>`.
The icon goes in a `<tspan class="ic">` before the name, the same icon as the legend chip.

## Lines

`<line class="ln ln-SLOT" x1 y1 x2 y2 marker-end="url(#d1t)"/>`. Add `dash` for a reply or anything
indirect. Stop the line 4px short of the box it points at, so the arrowhead touches the edge. Bends are
`<path class="ln …" d="M… L… L…" fill="none"/>` with right angles only.

## Sequence diagrams

Heads in a row at the top, `life` lifelines down from each centre, then numbered `band` strips for the
phases. Calls run left to right, replies dashed back; a label sits 7px above its arrow with `halo`, starting
14px from the caller (`text-anchor="end"` for replies). Rows every 30px.

## Before publishing

`python3 scripts/svgfit.py page.html` predicts every label's width and lists labels that leave their box
or the viewBox; expect `labels over: 0`. Long names (paths, component names) are what overflow: widen the
box or shorten the label, never shrink the font.
