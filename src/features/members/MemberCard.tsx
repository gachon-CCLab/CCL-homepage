import type { Member } from "../../content/types";
import { PhotoLink } from "../../components/media/PhotoViewer";

export function MemberCard({ member }: { member: Member }) {
  return (
    <article className="person" aria-labelledby={member.id}>
      <div className="person-top">
        <PhotoLink
          className="person-photo"
          href={member.photo}
          group="members"
          index={member.order - 1}
          aria-label={`View photo of ${member.name}`}
        >
          <img
            src={member.photo}
            alt={member.name}
            width="160"
            height="200"
            loading="lazy"
          />
        </PhotoLink>
        <span className="person-index">
          {String(member.order).padStart(2, "0")}
        </span>
      </div>
      <div className="person-body">
        <h3 className="person-name" id={member.id}>
          {member.name}
        </h3>
        <p className="person-status">{member.status}</p>
        <p className="person-department">{member.department}</p>
        {member.notes.map((note) => (
          <p className="person-note" key={note}>
            {note}
          </p>
        ))}
        {member.email ? (
          <>
            <span className="person-email-label">[E-mail]</span>
            <a className="person-email" href={`mailto:${member.email}`}>
              {member.email}
            </a>
          </>
        ) : null}
        {member.links.map((link) => (
          <a key={link.href} className="person-email" href={link.href}>
            {link.label}
          </a>
        ))}
      </div>
    </article>
  );
}
