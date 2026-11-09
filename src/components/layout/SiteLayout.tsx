import type { PropsWithChildren } from "react";
import type { PageContent } from "../../content/types";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { PhotoProvider } from "../media/PhotoViewer";

export function SiteLayout({
  page,
  children,
}: PropsWithChildren<{ page: PageContent }>) {
  return (
    <PhotoProvider photos={page.photos}>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <Header filename={page.filename} />
      <main id="main">{children}</main>
      <Footer />
    </PhotoProvider>
  );
}
