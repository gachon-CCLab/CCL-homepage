import type { Seminar } from "../../content/types";
import { PhotoLink } from "../../components/media/PhotoViewer";

export function SeminarCard({ seminar }: { seminar: Seminar }) {
  return (
    <section className="seminar" id={seminar.id}>
      <div className="seminar-when">
        <span className="micro-label">
          SEMINAR / {String(seminar.order).padStart(2, "0")}
        </span>
        <p>{seminar.date}</p>
      </div>
      <div>
        <header className="seminar-heading">
          <h2>{seminar.organization}</h2>
          {seminar.details.map((detail, index) => (
            <p key={index}>{detail}</p>
          ))}
          <div className="seminar-links">
            {seminar.links.map((link, index) => (
              <a key={index} className="seminar-material" href={link.href}>
                {link.label}
                <span aria-hidden="true"> ↗</span>
              </a>
            ))}
          </div>
        </header>
        <div className="seminar-photos">
          {seminar.images.map((src, index) => (
            <figure key={src + index}>
              <PhotoLink href={src} group={seminar.id} index={index}>
                <img
                  src={src}
                  alt={`${seminar.date} · ${seminar.organization} · Photo ${index + 1}`}
                  width="640"
                  height="480"
                  loading="lazy"
                />
              </PhotoLink>
              <figcaption>
                {String(index + 1).padStart(2, "0")} /{" "}
                {String(seminar.images.length).padStart(2, "0")}
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
