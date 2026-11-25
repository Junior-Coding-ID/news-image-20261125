import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// news-image-20261125 v3 — "THE GLOBAL BRIEF", Wednesday 25 November 2026.
// The image is drawn by render.py (same directory) and committed as entry.png;
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
const sha256 = (path) =>
  createHash("sha256").update(readFileSync(path)).digest("hex");
if (statSync(target).size !== statSync(source).size) {
  throw new Error(`entry.png copy incomplete: ${target}`);
}
if (sha256(target) !== sha256(source)) {
  throw new Error(`entry.png copy not byte-identical: ${target}`);
}
console.log(`wrote ${target} (${statSync(target).size} bytes)`);
