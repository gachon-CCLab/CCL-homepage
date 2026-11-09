export const pageModules = {
  main: () => import("../pages/main"),
  professor: () => import("../pages/professor"),
  "cloud-seminar": () => import("../pages/cloud-seminar"),
  members: () => import("../pages/members"),
  research: () => import("../pages/research"),
  "research-2025": () => import("../pages/research-2025"),
  "research-2024": () => import("../pages/research-2024"),
  project: () => import("../pages/project"),
  publication: () => import("../pages/publication"),
  gallery: () => import("../pages/gallery"),
  contact: () => import("../pages/contact"),
};
export type PageId = keyof typeof pageModules;

export function resolvePage(pathname: string): PageId {
  const filename = pathname.split("/").filter(Boolean).at(-1) ?? "index.html";
  const id =
    filename === "index.html" ? "main" : filename.replace(/\.html$/, "");
  return Object.hasOwn(pageModules, id) ? (id as PageId) : "main";
}
