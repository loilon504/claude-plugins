#!/usr/bin/env node
// The one look before publishing: screenshots of a built page, as the artifact viewer wraps it.
//
//   node shoot.cjs out.html shots/ [selector ...]
//
// Without selectors: the top of the page at desktop (1280) light and dark, and phone (390) light.
// With selectors: each one scrolled into view at desktop light; the last also dark and phone.
// Also prints each font face's status and the page width at both sizes (it should equal the viewport:
// anything wider is horizontal scroll).
//
// Needs Playwright with Chromium. Found through require() from the current folder, or from the
// folder named in PLAYWRIGHT_PATH. Install once: npm i -D playwright && npx playwright install chromium
const fs = require('fs');
const path = require('path');

function loadPlaywright() {
  const tries = [process.env.PLAYWRIGHT_PATH, process.cwd()].filter(Boolean);
  for (const base of tries) {
    try { return require(require.resolve('playwright', { paths: [base] })); } catch (e) { /* next */ }
  }
  try { return require('playwright'); } catch (e) { /* none */ }
  console.error('Playwright not found. Run in a folder that has it, or set PLAYWRIGHT_PATH to one.\n' +
    'Install: npm i -D playwright && npx playwright install chromium');
  process.exit(2);
}

const [page_, out, ...sels] = process.argv.slice(2);
if (!page_ || !out) { console.error('usage: node shoot.cjs out.html shots/ [selector ...]'); process.exit(1); }
fs.mkdirSync(out, { recursive: true });
const skel = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">' +
  '<style>:root{color-scheme:light;box-sizing:border-box}body{margin:0;font:14px sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>\n' +
  fs.readFileSync(page_, 'utf8') + '</body></html>';
const file = path.resolve(out, 'wrapped.html');
fs.writeFileSync(file, skel);

(async () => {
  const { chromium } = loadPlaywright();
  const b = await chromium.launch();
  const open = async (w, h, scheme) => {
    const p = await b.newPage({ viewport: { width: w, height: h }, colorScheme: scheme });
    await p.goto('file://' + file); await p.evaluate(() => document.fonts.ready); return p;
  };
  const to = async (p, s) => { if (s) await p.evaluate((s) => { const el = document.querySelector(s); if (!el) throw new Error('no element: ' + s); el.scrollIntoView(); }, s); };
  let p = await open(1280, 1200, 'light');
  console.log('fonts:', (await p.evaluate(() => [...document.fonts].map((f) => `${f.family} ${f.weight}${f.style === 'italic' ? 'i' : ''} ${f.status}`))).join(', '));
  console.log('desktop width', await p.evaluate(() => document.documentElement.scrollWidth), '(viewport 1280)');
  const shots = [];
  if (sels.length) {
    for (const [i, s] of sels.entries()) { await to(p, s); const f = `${out}/light-${i}.png`; await p.screenshot({ path: f }); shots.push(f); }
  } else { const f = `${out}/light.png`; await p.screenshot({ path: f }); shots.push(f); }
  const last = sels[sels.length - 1];
  p = await open(1280, 1200, 'dark'); await to(p, last); await p.screenshot({ path: `${out}/dark.png` }); shots.push(`${out}/dark.png`);
  p = await open(390, 844, 'light');
  console.log('phone width', await p.evaluate(() => document.documentElement.scrollWidth), '(viewport 390)');
  await to(p, last); await p.screenshot({ path: `${out}/phone.png` }); shots.push(`${out}/phone.png`);
  await b.close();
  console.log('shots:\n  ' + shots.map((s) => path.resolve(s)).join('\n  '));
})().catch((e) => { console.error(e.message); process.exit(1); });
