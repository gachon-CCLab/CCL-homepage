import data from "../content/pages/gallery.json";
import type { PageContent } from "../content/types";
import { DocumentPage } from "../components/content/DocumentPage";

export const page = data as PageContent;
export default function GalleryPage() {
  return <DocumentPage page={page} />;
}
