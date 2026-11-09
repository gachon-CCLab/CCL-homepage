import { readFile, writeFile, copyFile } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { build } from "vite";
import { renderToString } from "react-dom/server";
import { SiteLayout } from "../src/components/layout/SiteLayout";
import { pageModules } from "../src/app/routes";
import { buildDocuments, documentsDirectory } from "./documents";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const outDir = resolve(root, "dist");
if (dirname(outDir) !== root)
  throw new Error("Build output must remain inside ccl-website.");

await buildDocuments();
await build({ root, build: { outDir } });
const manifest = JSON.parse(
  await readFile(resolve(outDir, ".vite/manifest.json"), "utf8"),
) as Record<string, { file: string; css?: string[]; isEntry?: boolean }>;
const entry =
  manifest["src/main.tsx"] ??
  Object.values(manifest).find((item) => item.isEntry);
if (!entry) throw new Error("Vite client entry is missing.");

for (const load of Object.values(pageModules)) {
  const { page, default: Page } = await load();
  const body = renderToString(
    <SiteLayout page={page}>
      <Page />
    </SiteLayout>,
  );
  const escape = (value: string) =>
    value
      .replaceAll("&", "&amp;")
      .replaceAll('"', "&quot;")
      .replaceAll("<", "&lt;");
  const css = (entry.css ?? [])
    .map((file) => `<link rel="stylesheet" href="./${file}" />`)
    .join("\n");
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" />
<meta name="description" content="${escape(page.description)}" /><meta name="theme-color" content="#ffffff" />
<meta name="referrer" content="strict-origin-when-cross-origin" /><title>${escape(page.title)} | Cognitive Computing Lab</title>
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />${css}</head>
<body class="page-${page.id}"><div id="root">${body}</div><script type="module" src="./${entry.file}"></script></body></html>`;
  await writeFile(resolve(outDir, page.filename), html);
}
for (const filename of ["ccl-introduction.html", "department.html"]) {
  await copyFile(
    resolve(documentsDirectory, filename),
    resolve(outDir, filename),
  );
}
console.log(
  "Built 11 prerendered React pages + 2 self-contained HTML documents.",
);
