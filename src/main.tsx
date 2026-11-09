import { createRoot, hydrateRoot } from "react-dom/client";
import { SiteLayout } from "./components/layout/SiteLayout";
import { pageModules, resolvePage } from "./app/routes";
import "./styles/index.css";

async function start() {
  const root = document.getElementById("root");
  if (!root) throw new Error("CCL root element is missing.");
  const { page, default: Page } =
    await pageModules[resolvePage(window.location.pathname)]();
  document.documentElement.classList.add("js");
  document.body.className = `page-${page.id}`;
  document.title = `${page.title} | Cognitive Computing Lab`;
  const app = (
    <SiteLayout page={page}>
      <Page />
    </SiteLayout>
  );
  if (root.hasChildNodes()) hydrateRoot(root, app);
  else createRoot(root).render(app);
}

void start();
