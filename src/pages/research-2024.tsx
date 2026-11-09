import data from "../content/pages/research-2024.json";
import type { PageContent } from "../content/types";
import { DocumentPage } from "../components/content/DocumentPage";

export const page = data as PageContent;
export default function Research2024Page() {
  return <DocumentPage page={page} />;
}
