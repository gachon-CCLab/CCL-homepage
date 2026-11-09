import { createElement, Fragment } from "react";
import type { AnchorHTMLAttributes, ReactNode } from "react";
import type { ContentNode } from "../../content/types";
import { PhotoLink } from "../media/PhotoViewer";

const propertyNames: Record<string, string> = {
  class: "className",
  for: "htmlFor",
  tabindex: "tabIndex",
  colspan: "colSpan",
  rowspan: "rowSpan",
  allowfullscreen: "allowFullScreen",
  frameborder: "frameBorder",
  referrerpolicy: "referrerPolicy",
  fetchpriority: "fetchPriority",
  srcset: "srcSet",
  crossorigin: "crossOrigin",
  datetime: "dateTime",
  cellpadding: "cellPadding",
  cellspacing: "cellSpacing",
  readonly: "readOnly",
  autoplay: "autoPlay",
  playsinline: "playsInline",
  contenteditable: "contentEditable",
  viewbox: "viewBox",
  "stroke-width": "strokeWidth",
  "stroke-linecap": "strokeLinecap",
};
const blockedTags = new Set(["script", "style", "object", "embed"]);
const booleanAttributes = new Set([
  "hidden",
  "open",
  "disabled",
  "allowFullScreen",
  "readOnly",
  "controls",
  "autoPlay",
  "playsInline",
]);

function renderNode(node: ContentNode, key: number): ReactNode {
  if (typeof node === "string") return <Fragment key={key}>{node}</Fragment>;
  if (blockedTags.has(node.tag)) return null;
  const props: Record<string, unknown> = {};
  for (const [name, value] of Object.entries(node.attrs)) {
    if (value === undefined || name.startsWith("on") || name === "style")
      continue;
    const property = propertyNames[name] ?? name;
    props[property] = booleanAttributes.has(property)
      ? value === "" || value === "true" || value === true
      : value;
  }
  const children = node.children?.map(renderNode);
  if (node.tag === "a" && typeof node.attrs["data-photo"] === "string") {
    return (
      <PhotoLink
        key={key}
        {...(props as AnchorHTMLAttributes<HTMLAnchorElement>)}
        group={node.attrs["data-photo"]}
        index={Number(node.attrs["data-photo-index"] ?? 0)}
      >
        {children}
      </PhotoLink>
    );
  }
  return children
    ? createElement(node.tag, { ...props, key }, ...children)
    : createElement(node.tag, { ...props, key });
}

/** Structured original research content becomes React nodes, without HTML injection. */
export function RichContent({ nodes }: { nodes: ContentNode[] }) {
  return <>{nodes.map(renderNode)}</>;
}
