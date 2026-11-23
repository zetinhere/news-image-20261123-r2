// news-image-20261123-r2 entrypoint (Node 22, standard library only).
// The image is drawn offline by draw.py and committed as entry.png;
// this program just copies it to the grader's output directory, so both
// runs write the same bytes. MAKEFUN_OUTPUT_DIR stands in for /output
// outside the grader:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
