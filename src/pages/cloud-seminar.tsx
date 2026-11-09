import data from "../content/pages/cloud-seminar.json";
import seminars from "../content/seminars.json";
import type { PageContent } from "../content/types";
import { PageHeading } from "../components/content/DocumentPage";
import { RichContent } from "../components/content/RichContent";
import { SeminarCard } from "../features/seminars/SeminarCard";

export const page = data as PageContent;

export default function SeminarsPage() {
  return (
    <>
      <PageHeading page={page} />
      <div className="container page-body">
        <RichContent nodes={page.anchors} />
        <nav className="section-index" aria-label="Seminar index">
          {seminars.map((seminar) => (
            <a key={seminar.id} href={`#${seminar.id}`}>
              {seminar.organization}
            </a>
          ))}
        </nav>
        {seminars.map((seminar) => (
          <SeminarCard key={seminar.id} seminar={seminar} />
        ))}
      </div>
    </>
  );
}
