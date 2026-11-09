import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import type {
  AnchorHTMLAttributes,
  MouseEvent,
  PropsWithChildren,
} from "react";
import type { PhotoGroups } from "../../content/types";

type OpenPhoto = (
  group: string,
  index: number,
  opener: HTMLAnchorElement,
) => void;
const PhotoContext = createContext<OpenPhoto | null>(null);

export function PhotoProvider({
  photos,
  children,
}: PropsWithChildren<{ photos: PhotoGroups }>) {
  const [active, setActive] = useState<{ group: string; index: number } | null>(
    null,
  );
  const dialog = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLAnchorElement | null>(null);
  const isOpen = active !== null;
  const group = active ? (photos[active.group] ?? []) : [];
  const photo = active ? group[active.index] : undefined;

  const openPhoto = useCallback<OpenPhoto>(
    (group, index, element) => {
      if (!photos[group]?.[index]) return;
      opener.current = element;
      setActive({ group, index });
    },
    [photos],
  );

  const close = useCallback(() => {
    setActive(null);
    opener.current?.focus({ preventScroll: true });
  }, []);

  useEffect(() => {
    const element = dialog.current;
    if (!element) return;
    if (isOpen && !element.open) element.showModal();
    if (!isOpen && element.open) element.close();
    document.documentElement.classList.toggle("viewer-open", isOpen);
    return () => document.documentElement.classList.remove("viewer-open");
  }, [isOpen]);

  function step(delta: number) {
    setActive((value) =>
      value
        ? {
            ...value,
            index: Math.max(
              0,
              Math.min(
                value.index + delta,
                (photos[value.group]?.length ?? 1) - 1,
              ),
            ),
          }
        : null,
    );
  }

  return (
    <PhotoContext.Provider value={openPhoto}>
      {children}
      <dialog
        className="photo-viewer"
        aria-label="Photo viewer"
        ref={dialog}
        onClose={close}
        onCancel={close}
        onKeyDown={(event) => {
          if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
            event.preventDefault();
            step(event.key === "ArrowLeft" ? -1 : 1);
          }
        }}
        onClick={(event) => {
          if (event.target !== event.currentTarget) return;
          const rect = event.currentTarget.getBoundingClientRect();
          if (
            event.clientX < rect.left ||
            event.clientX > rect.right ||
            event.clientY < rect.top ||
            event.clientY > rect.bottom
          )
            close();
        }}
      >
        <button
          className="viewer-close"
          type="button"
          aria-label="Close photo"
          onClick={close}
        >
          ×
        </button>
        <div className="viewer-image">
          <button
            className="viewer-prev"
            type="button"
            aria-label="Previous photo"
            disabled={!active || active.index === 0}
            hidden={group.length < 2}
            onClick={() => step(-1)}
          >
            ←
          </button>
          <img src={photo?.src} alt={photo?.alt ?? ""} />
          <button
            className="viewer-next"
            type="button"
            aria-label="Next photo"
            disabled={!active || active.index === group.length - 1}
            hidden={group.length < 2}
            onClick={() => step(1)}
          >
            →
          </button>
        </div>
        <div className="viewer-caption">
          <p>{photo?.alt}</p>
          <span className="viewer-count">
            {active ? `${active.index + 1} / ${group.length}` : ""}
          </span>
        </div>
      </dialog>
    </PhotoContext.Provider>
  );
}

export function PhotoLink({
  group,
  index,
  children,
  onClick,
  ...props
}: PropsWithChildren<
  AnchorHTMLAttributes<HTMLAnchorElement> & { group: string; index: number }
>) {
  const openPhoto = useContext(PhotoContext);
  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    onClick?.(event);
    if (
      event.defaultPrevented ||
      event.ctrlKey ||
      event.metaKey ||
      event.shiftKey ||
      event.altKey ||
      event.button !== 0 ||
      !openPhoto
    )
      return;
    event.preventDefault();
    openPhoto(group, index, event.currentTarget);
  }
  return (
    <a {...props} data-photo={group} onClick={handleClick}>
      {children}
    </a>
  );
}
