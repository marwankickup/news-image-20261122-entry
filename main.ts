// The World on Sunday — entry for make.fun's news-image-20261122 bounty,
// "Sum up 22 November's world news in one image".
//
// The entry itself is the poster in entry.png beside this file: a
// front-page summary of Sunday 22 November 2026 — the COP31 climate
// talks ending with no deal, a Russian drone strike near Kyiv, sea
// drones sinking a Russian warship off Libya, the search for 36 workers
// missing after an Indonesian factory fire, the Democrats' biggest US
// House majority since 1992, and Marc Márquez's eighth MotoGP crown —
// drawn programmatically by draw_image.py (kept in this repository as
// the record of how the image was made). This program's whole job is to
// place that image where the grader looks for it, /output/entry.png;
// outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const poster = new URL("entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// Validate the poster before copying: it must exist, be a real PNG, and be
// exactly 1024x1024, the size the bounty requires. Fail loudly instead of
// handing the grader a broken or wrong-sized file.
if (!existsSync(poster)) {
  throw new Error(`poster not found: ${poster}`);
}
const head = readFileSync(poster).subarray(0, 33);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.subarray(0, 8).equals(PNG_MAGIC) || head.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png is not a valid PNG file");
}
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png must be 1024x1024, got ${width}x${height}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(poster, join(outDir, "entry.png"));
const bytes = statSync(poster).size;
console.log(`entry.png: ${bytes} bytes, ${width}x${height}, copied to ${join(outDir, "entry.png")}`);
