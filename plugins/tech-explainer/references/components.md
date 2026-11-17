# Components

Every block the house style has, as HTML to copy. All classes live in `assets/base.css`. Colour slots are
`blue teal plum amber olive slate`, plus `good` and `bad`; replace `SLOT` below with one.
Icons are Nerd Font codepoints written as entities (`&#xF0982;`); find them with `scripts/icons.py`.

## Page frame

The header (eyebrow, h1, lead, legend, table of contents) and the key cards are in `assets/template.html`.
Each `<section>` gets an `id` the table of contents links to, and a heading with an icon badge:

```html
<section id="startup">
  <h2><span class="ib SLOT"><i class="nf">&#xF0425;</i></span>When the container starts</h2>
  <div class="prose"><p>Running text stays in .prose, about 72 characters wide.</p></div>
</section>
```

`.ib` alone is a plain badge; `.ib SLOT` tints it. An `h3` takes the same badge. `.muted` greys text,
`.c-SLOT` colours an icon or a word, `.mono` sets JetBrains Mono.

## Figure

```html
<figure class="fig">
  <div class="scroll"><svg class="dg" viewBox="0 0 1160 H" role="img" aria-label="What it shows, in a sentence.">…</svg></div>
  <figcaption>How to read it, in a sentence or two.</figcaption>
</figure>
```

Drawing rules: `references/diagrams.md`.

## Table

```html
<div class="tblwrap">
  <table>
    <thead><tr><th>Program</th><th>Command</th><th>Started by</th></tr></thead>
    <tbody>
      <tr><td class="k">haproxy</td><td><code>/usr/local/sbin/haproxy -f …</code></td><td>supervisord</td></tr>
      <tr class="hl"><td class="k">upload</td><td>…</td><td>the row that is wrong, tinted red</td></tr>
    </tbody>
  </table>
</div>
```

`td.k` is the bold first column. `.tblwrap` scrolls sideways on a phone instead of the page.

## Annotated config file

A real file, cut down, with notes in the margin. The italic amber notes (`.an`) are the page's, never part of
the file; say so once in the section's intro.

```html
<div class="cfg">
  <div class="cfg-head"><b>/etc/supervisor/supervisord.conf.tpl</b><span>→ rendered to /srv/app/…/supervisord.conf</span></div>
<pre><span class="sec">[program:worker]</span>
<span class="kw">command</span>=<span class="mark">/srv/app/bin/report_worker</span>   <span class="an">← the name the installer writes</span>
<span class="kw">autostart</span>=false
<span class="gap">…  redis, mosquitto, cron</span></pre>
</div>
```

`.sec` a section header, `.sech` an amber one (haproxy), `.kw` a key, `.mark` a highlighted value,
`.cm` a comment in the file, `.gap` lines left out. Short inline diffs: `<span class="del">-…</span>` and
`<span class="add">+…</span>` in the `pre`. For whole files, use the side-by-side table below.

## Code proof

When a claim rests on code, show the exact lines: copied, never paraphrased, with their line numbers and
the file's path above them. Skip lines with a gap in the numbers, not with invented `...`.

```html
<pre><span class="cm">scheduler/pkg/jobs/queue_helper.go</span>
<span class="ln">352</span>  		for _, queueId := range queueList {
<span class="ln">353</span>  			<span class="mark">if queueId != config.DEFAULT_QUEUE_ID {</span>
<span class="ln">354</span>  				jobs.DrainQueue(queueId)    <span class="an">← drain step</span></pre>
```

Keep the source's tabs. Code fonts render `!=` and `==` as written (ligatures are off).
A log is proof too: count what it shows (a small table: app, step, count) rather than pasting pages of it.

## Side-by-side file changes

Old on the left, new on the right, line for line, unchanged stretches folded. `build.py` fills it from
two files on disk:

```html
<div class="files">
  <div class="diff">
    <div class="diff-head"><span class="badge mod"><i class="nf">&#xF11E8;</i>changed</span><b>Dockerfile</b><p>What changed and why, in a sentence or two.</p></div>
    <!--@SBS old="old/Dockerfile" new="new/Dockerfile"@-->
  </div>
  <div class="diff">
    <div class="diff-head"><span class="badge new"><i class="nf">&#xF0EED;</i>new</span><b>app.conf</b><span class="muted">→ /etc/supervisor/conf.d/app.conf</span><p>…</p></div>
    <!--@SBS old="" new="new/app.conf"@-->
  </div>
  <div class="diff">
    <div class="diff-head"><span class="badge del"><i class="nf">&#xF1037;</i>removed</span><b>stub.conf</b><p>…</p></div>
    <!--@SBS old="old/stub.conf" new=""@-->
  </div>
</div>
```

Paths are relative to `build.py --root` (default: the page's folder). Keep the old copies as they were and
write the new ones beside them, so the table shows exactly what will change. `context="5"` shows more
unchanged lines around each change (default 3). Labels follow the page language (Vietnamese or English).

## Callouts

```html
<div class="callout"><i class="nf">&#xF02FD;</i><p>A side fact the reader should not miss (amber).</p></div>
<div class="callout good"><i class="nf">&#xF06E9;</i><p>The recommendation.</p></div>
<div class="callout bad"><i class="nf">&#xF15D1;</i><div class="stack"><p><b>A blocker, in one bold line.</b></p><p>Why, and the ways around it.</p></div></div>
```

One or two callouts a section at most; a page of callouts has none.

## Options side by side

```html
<div class="opts">
  <div class="opt">
    <h3><span class="ib teal"><i class="nf">&#xF171A;</i></span>Option A: … <span class="tag">recommended</span></h3>
    <ol><li>Step</li><li>Step</li></ol>
  </div>
  <div class="opt">…</div>
</div>
```

Follow with a `.tblwrap` table comparing them row by row (one row per question a reader would ask).
The same `.opts` pair makes the "Checked / Not checked" block that closes a plan:
`<h3><i class="nf c-good">&#xF05E1;</i>Checked</h3>` and `<h3><i class="nf c-bad">&#xF002A;</i>Not checked</h3>`.

## Questions and answers

```html
<div class="answers">
  <div class="answer"><span class="n">1</span><b>The answer in one sentence.</b><p>Why, and the file:line that shows it.</p></div>
  <div class="answer wide" id="q-2"><span class="n">2</span><div class="body">
    <b>An answer that needs its proof shown.</b>
    <p>…</p>
    <pre>…exact code lines…</pre>
    <p>What that means for the reader.</p>
  </div></div>
</div>
```

`.answer.wide` is for answers carrying code or a table; it runs wider than the plain ones. Give it an `id` so
other sections can link to it ("why: see <a href="#q-2">question 2</a>").

## Footer

```html
<footer>
  <p><i class="nf">&#xF062C;</i> Read on 2026-11-17 from: repo at commit 0e5e0121f; image app-server:2.4.1 (templates); the installer's log of 2026-11-16.</p>
</footer>
```

Every source the page rests on, with its commit, tag or date, so a reader can tell when it goes stale.
