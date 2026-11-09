import footer from "../../content/footer.json";

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-content">
        <div>
          <a className="footer-name" href="index.html">
            Cognitive Computing Lab<span>.</span>
          </a>
          <p>
            Gachon University · Global Campus
            <br />
            AI Engineering Building, Room 103
          </p>
          <a className="footer-email" href="mailto:keylee@gachon.ac.kr">
            keylee@gachon.ac.kr ↗
          </a>
        </div>
        <nav className="footer-navigation" aria-label="Footer navigation">
          <a href="professor.html">Professor</a>
          <a href="members.html">Members</a>
          <a href="contact.html">Contact</a>
          <a href="ccl-introduction.html">Lab Profile ↗</a>
          <a href="department.html" hrefLang="ko">
            Department Profile ↗
          </a>
        </nav>
      </div>
      <div className="container university-footer">
        <a href={footer.href} target="_blank" rel="noopener">
          <img
            src={footer.logo}
            alt="Gachon University"
            width="1652"
            height="431"
            loading="lazy"
          />
        </a>
        <div>
          {footer.text
            .split("\n")
            .map((line) => line.trim())
            .filter(Boolean)
            .map((line) => (
              <p key={line}>{line}</p>
            ))}
        </div>
      </div>
      <div className="container footer-bottom">
        <span>© 2026 Cognitive Computing Lab, Gachon University</span>
        <a href="#main">Back to top ↑</a>
      </div>
    </footer>
  );
}
