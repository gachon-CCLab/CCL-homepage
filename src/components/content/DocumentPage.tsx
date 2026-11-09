import type { PageContent } from "../../content/types";
import { RichContent } from "./RichContent";

export function PageHeading({ page }: { page: PageContent }) {
  return page.heading ? <RichContent nodes={[page.heading]} /> : null;
}

export function DocumentPage({ page }: { page: PageContent }) {
  return (
    <>
      <PageHeading page={page} />
      <div className="container page-body">
        <RichContent nodes={page.content} />
      </div>
    </>
  );
}
