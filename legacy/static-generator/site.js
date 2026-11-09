document.documentElement.classList.add("js");
const header = document.querySelector(".site-header");
const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#primary-navigation");
const subnavButton = document.querySelector(".subnav-toggle");
const navGroup = document.querySelector(".nav-group");
const desktop = window.matchMedia("(min-width: 901px)");

function setSubnav(open) {
  navGroup?.classList.toggle("open", open);
  subnavButton?.setAttribute("aria-expanded", String(open));
}
function setMenu(open) {
  navigation?.classList.toggle("open", open);
  menuButton?.setAttribute("aria-expanded", String(open));
  menuButton?.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  if (!open) setSubnav(false);
}
menuButton?.addEventListener("click", () =>
  setMenu(menuButton.getAttribute("aria-expanded") !== "true"),
);
subnavButton?.addEventListener("click", () =>
  setSubnav(subnavButton.getAttribute("aria-expanded") !== "true"),
);
navGroup?.addEventListener("mouseenter", () => {
  if (desktop.matches) setSubnav(true);
});
navGroup?.addEventListener("mouseleave", () => {
  if (desktop.matches && !navGroup.contains(document.activeElement))
    setSubnav(false);
});
navGroup?.addEventListener("focusout", (e) => {
  if (!navGroup.contains(e.relatedTarget)) setSubnav(false);
});
document.addEventListener("click", (e) => {
  if (!navGroup?.contains(e.target)) setSubnav(false);
  if (!header?.contains(e.target) && !desktop.matches) setMenu(false);
});
desktop.addEventListener("change", () => setMenu(false));

const viewer = document.querySelector(".photo-viewer");
const viewerImage = viewer?.querySelector(".viewer-image>img");
const previous = viewer?.querySelector(".viewer-prev");
const next = viewer?.querySelector(".viewer-next");
let photos = [];
let photoIndex = 0;
let opener;
function showPhoto(index) {
  if (!photos.length || !viewerImage) return;
  photoIndex = Math.max(0, Math.min(index, photos.length - 1));
  const link = photos[photoIndex];
  const caption = link.querySelector("img")?.alt || "CCL lab photo";
  viewerImage.src = link.href;
  viewerImage.alt = caption;
  viewer.querySelector(".viewer-caption p").textContent = caption;
  viewer.querySelector(".viewer-count").textContent =
    `${photoIndex + 1} / ${photos.length}`;
  previous.disabled = photoIndex === 0;
  next.disabled = photoIndex === photos.length - 1;
  previous.hidden = next.hidden = photos.length < 2;
}
document.addEventListener("click", (e) => {
  const link = e.target.closest("a[data-photo]");
  if (
    !link ||
    !viewer?.showModal ||
    e.ctrlKey ||
    e.metaKey ||
    e.shiftKey ||
    e.altKey
  )
    return;
  e.preventDefault();
  opener = link;
  photos = [...document.querySelectorAll("a[data-photo]")].filter(
    (p) => p.dataset.photo === link.dataset.photo,
  );
  showPhoto(photos.indexOf(link));
  viewer.showModal();
  document.documentElement.classList.add("viewer-open");
});
previous?.addEventListener("click", () => showPhoto(photoIndex - 1));
next?.addEventListener("click", () => showPhoto(photoIndex + 1));
viewer
  ?.querySelector(".viewer-close")
  .addEventListener("click", () => viewer.close());
viewer?.addEventListener("click", (e) => {
  if (e.target !== viewer) return;
  const rect = viewer.getBoundingClientRect();
  if (
    e.clientX < rect.left ||
    e.clientX > rect.right ||
    e.clientY < rect.top ||
    e.clientY > rect.bottom
  )
    viewer.close();
});
viewer?.addEventListener("close", () => {
  document.documentElement.classList.remove("viewer-open");
  viewerImage?.removeAttribute("src");
  opener?.focus({ preventScroll: true });
});
document.addEventListener("keydown", (e) => {
  if (viewer?.open) {
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      showPhoto(photoIndex - 1);
    }
    if (e.key === "ArrowRight") {
      e.preventDefault();
      showPhoto(photoIndex + 1);
    }
    return;
  }
  if (e.key !== "Escape") return;
  if (subnavButton?.getAttribute("aria-expanded") === "true") {
    setSubnav(false);
    subnavButton.focus();
  } else if (menuButton?.getAttribute("aria-expanded") === "true") {
    setMenu(false);
    menuButton.focus();
  }
});
