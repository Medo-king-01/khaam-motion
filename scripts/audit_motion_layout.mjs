#!/usr/bin/env node
// Optional local DOM-geometry probe for Khaam's own HyperFrames blocks.
// Requires an already-installed Playwright/Playwright Core and an available Chrome;
// it never installs a browser, contacts a service, or treats a first measurement as approval.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const DEFAULT_PROJECT = resolve(HERE, '..', 'templates', 'hyperframes');
const DEFAULT_CATALOG = join(DEFAULT_PROJECT, 'motion-catalog.json');

function options(argv) {
  const out = { projectRoot: DEFAULT_PROJECT, catalog: DEFAULT_CATALOG, at: [], tolerance: 0.02, strict: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') { out.help = true; continue; }
    if (arg === '--strict') { out.strict = true; continue; }
    if (arg === '--template') out.template = argv[++i];
    else if (arg === '--project-root') out.projectRoot = resolve(argv[++i]);
    else if (arg === '--catalog') out.catalog = resolve(argv[++i]);
    else if (arg === '--timing-js') out.timingJs = resolve(argv[++i]);
    else if (arg === '--baseline') out.baseline = resolve(argv[++i]);
    else if (arg === '--out') out.output = resolve(argv[++i]);
    else if (arg === '--at') out.at.push(Number(argv[++i]));
    else if (arg === '--tolerance') out.tolerance = Number(argv[++i]);
    else if (!arg.startsWith('-')) out.template ??= arg;
    else throw new Error(`Unknown option: ${arg}`);
  }
  if (out.at.some((x) => !Number.isFinite(x) || x < 0)) throw new Error('--at must be a finite non-negative time in seconds.');
  if (!Number.isFinite(out.tolerance) || out.tolerance < 0 || out.tolerance > 1) throw new Error('--tolerance must be from 0 to 1.');
  if (out.strict && !out.baseline) throw new Error('--strict requires a previously reviewed --baseline JSON file.');
  return out;
}

function help() {
  console.log(`Usage: node scripts/audit_motion_layout.mjs --template <id> [options]

Options:
  --project-root <dir>  copied templates/hyperframes project (default: skill starter)
  --catalog <path>      motion-catalog.json (default: skill catalog)
  --at <seconds>        sample a specific time; repeatable (default: catalog samples)
  --timing-js <path>    project's local timing.js for real cue resolution
  --out <path>          save new measurement JSON; refuses overwrite
  --baseline <path>     compare against a measurement saved after visual review
  --tolerance <0..1>    allowed absolute fraction change (default: 0.02)
  --strict              fail on missing selectors or baseline drift; requires --baseline

This runs trusted local composition HTML in a headless browser. It measures selector
bounds, not Arabic readability, visual quality, correctness, or final-render behavior.
No browser/package is installed automatically.`);
}

function playwrightModule() {
  for (const name of ['playwright-core', 'playwright']) {
    try { return require(name); } catch (error) {
      if (error.code !== 'MODULE_NOT_FOUND') throw error;
    }
  }
  throw new Error('Playwright is not available in this project. The probe is optional; do not install it without the user’s permission.');
}

function inside(parent, child) {
  const rel = relative(parent, child);
  return rel === '' || (!rel.startsWith(`..${sep}`) && rel !== '..' && !isAbsolute(rel));
}

function geometry(rects, width, height) {
  if (!rects.length) return { visibleElements: 0, bounds: null, occupancy: 0, span: { width: 0, height: 0 } };
  const x0 = Math.min(...rects.map((r) => r.x)), y0 = Math.min(...rects.map((r) => r.y));
  const x1 = Math.max(...rects.map((r) => r.x + r.width)), y1 = Math.max(...rects.map((r) => r.y + r.height));
  const w = x1 - x0, h = y1 - y0;
  return { visibleElements: rects.length, bounds: { x: +x0.toFixed(2), y: +y0.toFixed(2), width: +w.toFixed(2), height: +h.toFixed(2) },
    occupancy: +((w * h) / (width * height)).toFixed(5), span: { width: +(w / width).toFixed(5), height: +(h / height).toFixed(5) } };
}

async function main() {
  const opt = options(process.argv.slice(2));
  if (opt.help) { help(); return 0; }
  if (!opt.template) throw new Error('Choose --template <id>.');
  const catalog = JSON.parse(readFileSync(opt.catalog, 'utf8'));
  const entry = catalog.templates.find((item) => item.id === opt.template);
  if (!entry) throw new Error(`Unknown template id: ${opt.template}`);
  const audit = entry.layoutAudit;
  if (!audit?.subjectSelectors?.length || !audit?.frameSelectors?.length) throw new Error(`${entry.id} has no layout audit selectors.`);
  const root = resolve(opt.projectRoot);
  const sourcePath = resolve(root, entry.source);
  if (!inside(root, sourcePath) || !existsSync(sourcePath)) throw new Error(`Composition source is missing or outside the project root: ${sourcePath}`);
  const samples = opt.at.length ? opt.at : audit.sampleSeconds;
  if (!samples.length) throw new Error('No sample times are declared; pass --at <seconds>.');
  const { chromium } = playwrightModule();
  const executablePath = process.env.KHAAM_CHROMIUM || process.env.CHROME_PATH || process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  const launch = { headless: true };
  if (executablePath) launch.executablePath = executablePath;
  let browser;
  try { browser = await chromium.launch(launch); }
  catch (error) { throw new Error(`Could not launch the already-available Chrome/Chromium. Set KHAAM_CHROMIUM or CHROME_PATH; nothing was installed. ${error.message}`); }
  try {
    const parser = await browser.newPage({ viewport: { width: catalog.canvas.width, height: catalog.canvas.height } });
    await parser.setContent(readFileSync(sourcePath, 'utf8'));
    const parts = await parser.evaluate(() => {
      const tpl = document.querySelector('template');
      if (!tpl) throw new Error('Composition source has no HyperFrames <template> root.');
      const content = tpl.content;
      const roots = [...content.querySelectorAll('[data-composition-id]')];
      if (!roots.length) throw new Error('No data-composition-id element found inside the template.');
      const scripts = [...content.querySelectorAll('script')].map((s) => ({ src: s.getAttribute('src'), code: s.textContent || '' }));
      const styles = [...content.querySelectorAll('style')].map((s) => s.textContent || '');
      return { markup: roots[0].outerHTML, scripts, styles, compositionId: roots[0].getAttribute('data-composition-id') };
    });
    await parser.close();
    const page = await browser.newPage({ viewport: { width: catalog.canvas.width, height: catalog.canvas.height }, deviceScaleFactor: 1 });
    const baseHref = pathToFileURL(root + sep).href;
    await page.setContent(`<!doctype html><html><head><base href="${baseHref}"><link rel="stylesheet" href="motion-tokens.css"><style>html,body{margin:0;width:${catalog.canvas.width}px;height:${catalog.canvas.height}px;overflow:hidden}*{box-sizing:border-box}</style>${parts.styles.map((s) => `<style>${s.replace(/<\/style/gi, '<\\/style')}</style>`).join('')}</head><body>${parts.markup}</body></html>`);
    const gsap = join(root, 'vendor', 'gsap.min.js');
    if (!existsSync(gsap)) throw new Error(`Local GSAP is missing: ${gsap}`);
    await page.addScriptTag({ path: gsap });
    const cueIsUsed = parts.scripts.some((script) => /(?:window\.)?cue\s*\(/.test(script.code));
    if (cueIsUsed && !opt.timingJs) throw new Error('This composition resolves spoken cues. Pass --timing-js from the actual video project; cue names are never guessed or replaced with zero.');
    await page.evaluate(() => { window.__timelines = window.__timelines || {}; });
    if (opt.timingJs) {
      const timingPath = resolve(opt.timingJs);
      if (!inside(root, timingPath) || !existsSync(timingPath)) throw new Error('--timing-js must be a local file inside --project-root.');
      await page.addScriptTag({ path: timingPath });
      const hasCueResolver = await page.evaluate(() => typeof window.cue === 'function');
      if (cueIsUsed && !hasCueResolver) throw new Error('The supplied --timing-js did not define window.cue.');
    }
    for (const script of parts.scripts) {
      if (script.src) {
        const localScript = resolve(root, script.src);
        if (!inside(root, localScript) || !existsSync(localScript)) throw new Error(`External/non-local composition script is not allowed by this probe: ${script.src}`);
        await page.addScriptTag({ path: localScript });
      } else if (script.code.trim()) await page.addScriptTag({ content: script.code });
    }
    await page.evaluate(() => document.fonts?.ready);
    const rows = [];
    for (const at of samples) {
      const seek = await page.evaluate(({ id, time }) => {
        const timeline = window.__timelines?.[id];
        if (!timeline || typeof timeline.seek !== 'function') return { ok: false, error: `No registered paused timeline for ${id}.` };
        timeline.pause().seek(time, false);
        return { ok: true };
      }, { id: parts.compositionId, time: at });
      if (!seek.ok) throw new Error(seek.error);
      const measured = await page.evaluate(({ subjectSelectors, frameSelectors }) => {
        const collect = (selectors) => {
          const rects = [];
          for (const selector of selectors) {
            let nodes;
            try { nodes = document.querySelectorAll(selector); }
            catch { return { selectorError: selector, rects: [] }; }
            for (const node of nodes) {
              const style = getComputedStyle(node), r = node.getBoundingClientRect();
              if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) <= 0.05 || r.width <= 1 || r.height <= 1) continue;
              rects.push({ x: r.x, y: r.y, width: r.width, height: r.height });
            }
          }
          return { rects };
        };
        return { subject: collect(subjectSelectors), frame: collect(frameSelectors) };
      }, { subjectSelectors: audit.subjectSelectors, frameSelectors: audit.frameSelectors });
      rows.push({ time_s: at,
        subject: geometry(measured.subject.rects, catalog.canvas.width, catalog.canvas.height),
        frame: geometry(measured.frame.rects, catalog.canvas.width, catalog.canvas.height),
        selectorErrors: [measured.subject.selectorError, measured.frame.selectorError].filter(Boolean) });
    }
    await page.close();
    const result = { version: 1, templateId: entry.id, source: relative(root, sourcePath), viewport: [catalog.canvas.width, catalog.canvas.height],
      samples: rows, note: 'DOM bounds only. Not Arabic legibility, visual quality, source truth, or final encoded output. A baseline must be saved only after a human has inspected the corresponding render.' };
    let drift = [];
    if (opt.baseline) {
      const baseline = JSON.parse(readFileSync(opt.baseline, 'utf8'));
      if (baseline.templateId !== result.templateId || JSON.stringify(baseline.viewport) !== JSON.stringify(result.viewport)) throw new Error('Baseline templateId or viewport does not match.');
      for (const row of rows) {
        const prior = baseline.samples?.find((sample) => sample.time_s === row.time_s);
        if (!prior) { drift.push(`No baseline sample at ${row.time_s}s.`); continue; }
        for (const key of ['occupancy', 'span.width', 'span.height']) {
          const get = (object) => key.split('.').reduce((value, part) => value?.[part], object);
          if (Math.abs(get(row.subject) - get(prior.subject)) > opt.tolerance) drift.push(`${row.time_s}s ${key} drift exceeds ${opt.tolerance}.`);
        }
      }
      result.baseline = { path: opt.baseline, tolerance: opt.tolerance, drift };
    }
    if (opt.output) {
      if (existsSync(opt.output)) throw new Error(`Refusing to overwrite existing measurement file: ${opt.output}`);
      writeFileSync(opt.output, JSON.stringify(result, null, 2) + '\n', { flag: 'wx' });
      console.log(`Layout measurements: ${opt.output}`);
    } else console.log(JSON.stringify(result, null, 2));
    if (result.samples.some((sample) => sample.subject.visibleElements === 0 || sample.frame.visibleElements === 0 || sample.selectorErrors.length)) {
      console.warn('WARNING: one or more selectors returned no visible geometry. This is a diagnostic, not a visual pass.');
      if (opt.strict) return 1;
    }
    if (drift.length) {
      for (const message of drift) console.warn(`DRIFT: ${message}`);
      if (opt.strict) return 1;
    }
    return 0;
  } finally {
    await browser.close();
  }
}

main().then((code) => { process.exitCode = code; }).catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exitCode = 2;
});
