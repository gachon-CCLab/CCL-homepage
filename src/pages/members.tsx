import data from "../content/pages/members.json";
import records from "../content/members.json";
import type { Member, PageContent } from "../content/types";
import { PageHeading } from "../components/content/DocumentPage";
import { RichContent } from "../components/content/RichContent";
import { MemberGroup } from "../features/members/MemberGroup";

export const page = data as PageContent;
const members = records as Member[];
const current = members.filter((member) => member.membership === "current");
const former = members.filter((member) => member.membership === "former");

export default function MembersPage() {
  return (
    <>
      <PageHeading page={page} />
      <div className="container page-body">
        <RichContent nodes={page.anchors} />
        <nav className="member-index" aria-label="Members index">
          <a href="#current-members">
            <span>Current Members</span>
            <b>{current.length}</b>
          </a>
          <a href="#former-members">
            <span>Former Members</span>
            <b>{former.length}</b>
          </a>
        </nav>
        <MemberGroup
          group="current"
          title="Current Members"
          subtitle="Our current research team"
          members={current}
        />
        <hr className="member-divider" />
        <MemberGroup
          group="former"
          title="Former Members"
          subtitle="Past members of CCL"
          members={former}
        />
      </div>
    </>
  );
}
