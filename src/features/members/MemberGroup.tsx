import type { Member } from "../../content/types";
import { MemberCard } from "./MemberCard";

export function MemberGroup({
  group,
  title,
  subtitle,
  members,
}: {
  group: string;
  title: string;
  subtitle: string;
  members: Member[];
}) {
  return (
    <section
      className="member-group"
      id={`${group}-members`}
      aria-labelledby={`${group}-members-title`}
    >
      <header className="member-group-heading">
        <div>
          <h2 id={`${group}-members-title`}>{title}</h2>
          <p>{subtitle}</p>
        </div>
        <span className="member-group-count">{members.length} members</span>
      </header>
      <div className="people-grid">
        {members.map((member) => (
          <MemberCard key={member.id} member={member} />
        ))}
      </div>
    </section>
  );
}
