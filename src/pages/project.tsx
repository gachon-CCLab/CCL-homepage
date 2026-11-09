import data from "../content/pages/project.json";
import type { PageContent } from "../content/types";
import { DocumentPage } from "../components/content/DocumentPage";

export const page = data as PageContent;
export default function ProjectPage() {
  return <DocumentPage page={page} />;
}
