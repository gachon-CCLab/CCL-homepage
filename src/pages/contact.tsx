import data from "../content/pages/contact.json";
import type { PageContent } from "../content/types";
import { DocumentPage } from "../components/content/DocumentPage";

export const page = data as PageContent;
export default function ContactPage() {
  return <DocumentPage page={page} />;
}
