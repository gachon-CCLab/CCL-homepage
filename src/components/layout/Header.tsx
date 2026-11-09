import { useEffect, useRef, useState } from "react";
import navigation from "../../content/navigation.json";

export function Header({ filename }: { filename: string }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [researchOpen, setResearchOpen] = useState(false);
  const header = useRef<HTMLElement>(null);
  const research = useRef<HTMLDivElement>(null);
  const menuButton = useRef<HTMLButtonElement>(null);
  const researchButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const desktop = window.matchMedia("(min-width: 901px)");
    function reset() {
      setMenuOpen(false);
      setResearchOpen(false);
    }
    function outside(event: PointerEvent) {
      if (!research.current?.contains(event.target as Node))
        setResearchOpen(false);
      if (!desktop.matches && !header.current?.contains(event.target as Node))
        setMenuOpen(false);
    }
    desktop.addEventListener("change", reset);
    document.addEventListener("pointerdown", outside);
    return () => {
      desktop.removeEventListener("change", reset);
      document.removeEventListener("pointerdown", outside);
    };
  }, []);

  return (
    <header
      className="site-header"
      ref={header}
      onKeyDown={(event) => {
        if (event.key !== "Escape") return;
        if (researchOpen) {
          setResearchOpen(false);
          researchButton.current?.focus();
        } else if (menuOpen) {
          setMenuOpen(false);
          menuButton.current?.focus();
        }
      }}
    >
      <div className="container brand-row">
        <a className="brand" href="index.html" aria-label="CCL home">
          <span className="brand-symbol">
            CCL<span>.</span>
          </span>
          <span className="brand-name">
            Cognitive Computing Lab<small>GACHON UNIVERSITY</small>
          </span>
        </a>
        <a className="header-profile" href="ccl-introduction.html">
          Lab Profile <span aria-hidden="true">↗</span>
        </a>
        <button
          className="menu-toggle"
          type="button"
          aria-expanded={menuOpen}
          aria-controls="primary-navigation"
          aria-label={menuOpen ? "Close menu" : "Open menu"}
          ref={menuButton}
          onClick={() => {
            setMenuOpen((open) => !open);
            setResearchOpen(false);
          }}
        >
          <span />
          <span />
        </button>
      </div>
      <div className="nav-border">
        <nav
          className={`container primary-navigation${menuOpen ? " open" : ""}`}
          id="primary-navigation"
          aria-label="Main navigation"
        >
          {navigation.map((item) => {
            const active =
              filename === item.href ||
              (item.href === "research.html" &&
                filename.startsWith("research-"));
            const link = (
              <a
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
              >
                {item.label}
              </a>
            );
            return item.children.length ? (
              <div
                className={`nav-group${researchOpen ? " open" : ""}`}
                key={item.href}
                ref={research}
                onMouseEnter={() => {
                  if (window.matchMedia("(min-width: 901px)").matches)
                    setResearchOpen(true);
                }}
                onMouseLeave={(event) => {
                  if (
                    window.matchMedia("(min-width: 901px)").matches &&
                    !event.currentTarget.contains(document.activeElement)
                  )
                    setResearchOpen(false);
                }}
                onBlur={(event) => {
                  if (!event.currentTarget.contains(event.relatedTarget))
                    setResearchOpen(false);
                }}
              >
                {link}
                <button
                  type="button"
                  className="subnav-toggle"
                  aria-label="Research submenu"
                  aria-expanded={researchOpen}
                  aria-controls="research-subnav"
                  ref={researchButton}
                  onClick={() => setResearchOpen((open) => !open)}
                >
                  <svg
                    width="10"
                    height="10"
                    viewBox="0 0 10 10"
                    aria-hidden="true"
                  >
                    <path d="m2 4 3 3 3-3" fill="none" stroke="currentColor" />
                  </svg>
                </button>
                <div id="research-subnav" className="subnav">
                  {item.children.map((child) => (
                    <a
                      key={child.href}
                      href={child.href}
                      aria-current={
                        filename === child.href ? "page" : undefined
                      }
                    >
                      {child.label}
                    </a>
                  ))}
                </div>
              </div>
            ) : (
              link
            );
          })}
        </nav>
      </div>
    </header>
  );
}
