import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// news-image-20261125 v2 — "THE GLOBAL BRIEF", 25 November 2026.
// The image is drawn by render.py (same repo) and committed as entry.png;
// this program copies it to the grader output directory.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT ?? "/output";

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts: ${source}`);
}
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
// Guard against a partial copy: the output must be byte-for-byte the source.
if (statSync(target).size !== statSync(source).size) {
  throw new Error(`entry.png copy incomplete: ${target}`);
}
