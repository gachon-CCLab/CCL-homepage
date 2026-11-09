import { readFile, writeFile, mkdir } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const documentsDirectory = resolve(root, ".generated/documents");

export async function buildDocuments() {
  await mkdir(documentsDirectory, { recursive: true });
  async function uri(filename: string, mime: string) {
    return `data:${mime};base64,${(await readFile(resolve(root, "public", filename))).toString("base64")}`;
  }
  const values: Record<string, string> = {
    "@@FONT@@": await uri(
      "assets/fonts/PretendardVariable.woff2",
      "font/woff2",
    ),
    "@@PROFESSOR@@": await uri("assets/professor.jpg", "image/jpeg"),
    "@@FEDOPS@@": await uri("assets/fedops-icon.png", "image/png"),
    "@@MAP@@": await uri("assets/research-map.svg", "image/svg+xml"),
    "@@HERO_IMAGE@@": await uri("assets/ccl-hero-selected.png", "image/png"),
    "@@HERO_ALT@@":
      "Federated learning across mobile, manufacturing and robotics, with local data and model exchange",
    "@@HERO_WIDTH@@": "1374",
    "@@HERO_HEIGHT@@": "1145",
    "@@FAVICON@@": await uri("assets/favicon.svg", "image/svg+xml"),
    "@@DEPARTMENT_IMAGE@@": await uri(
      "assets/department-source-0.jpg",
      "image/jpeg",
    ),
  };
  const license = await readFile(
    resolve(root, "public/assets/fonts/OFL.txt"),
    "utf8",
  );
  for (const filename of ["ccl-introduction.html", "department.html"]) {
    let html = await readFile(resolve(root, "templates", filename), "utf8");
    for (const [key, value] of Object.entries(values))
      html = html.replaceAll(key, value);
    html = html.replace(
      "</body>",
      `<script type="text/plain" id="font-license">${license}</script></body>`,
    );
    await writeFile(resolve(documentsDirectory, filename), html);
  }
}

if (
  process.argv[1] &&
  resolve(process.argv[1]) === fileURLToPath(import.meta.url)
)
  await buildDocuments();
