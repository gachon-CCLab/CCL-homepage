import data from "../content/pages/publication.json";
import type { PageContent } from "../content/types";
import { DocumentPage } from "../components/content/DocumentPage";

export const page = data as PageContent;
export default function PublicationPage() {
  return <DocumentPage page={page} />;
}
