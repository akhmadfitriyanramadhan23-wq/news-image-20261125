// news-image-20261125 — "THE WORLD TODAY" front page for Wednesday 25 November 2026.
// Node 22, standard library only. The entry image is the entry.png beside this
// file, drawn from scratch by tools/make-image.py (Pillow vector art, no network,
// deterministic); this program copies it to /output/entry.png.
// Content: 35 stories first reported on 25 Nov 2026 (3 leads + 10 secondary +
// 22 briefs), timeline, markets strip, numbered world map, DATE CHECK box.
// See NEWS.md for the sourced story list and the excluded 24-Nov stories.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) throw new Error('entry.png missing beside main.ts');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
