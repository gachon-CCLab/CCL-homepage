const keywords = [
  "Artificial Intelligence",
  "IoT",
  "Healthcare",
  "Cognitive Computing",
  "Cloud",
];

export function Hero() {
  return (
    <section className="home-hero">
      <div className="container">
        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">
              <i aria-hidden="true" /> GACHON UNIVERSITY · CCL
            </p>
            <h1>
              Cognitive
              <br />
              Computing Lab<span>.</span>
            </h1>
            <p className="hero-affiliation">
              Gachon University · Computer Engineering
            </p>
            <p className="hero-summary">
              Exploring real-world problems across disciplines
              <br />
              through AI and cognitive computing.
            </p>
            <div className="actions">
              <a className="button" href="research.html">
                Explore Research <span aria-hidden="true">↗</span>
              </a>
              <a className="text-link" href="ccl-introduction.html">
                Lab Profile <span aria-hidden="true">↗</span>
              </a>
            </div>
          </div>
          <figure className="hero-visual">
            <img
              src="assets/ccl-hero-selected.png"
              alt="Federated learning across mobile, manufacturing and robotics, with local data and model exchange"
              width="1374"
              height="1145"
              fetchPriority="high"
              decoding="async"
            />
            <figcaption>
              <span>LOCAL LEARNING. SHARED INTELLIGENCE.</span>
              <span>CCL / GACHON</span>
            </figcaption>
          </figure>
        </div>
        <div className="keyword-line">
          {keywords.map((keyword) => (
            <span key={keyword}>{keyword}</span>
          ))}
        </div>
      </div>
    </section>
  );
}
