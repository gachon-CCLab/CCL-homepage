import data from "../content/pages/professor.json";
import type { PageContent } from "../content/types";
import { DocumentPage } from "../components/content/DocumentPage";

export const page = data as PageContent;
export default function ProfessorPage() {
  return <DocumentPage page={page} />;
}
