import data from "../content/pages/main.json";
import type { PageContent } from "../content/types";
import { Hero } from "../features/home/Hero";
import { RichContent } from "../components/content/RichContent";

export const page = data as PageContent;
const remainingSections = page.content.filter(
  (node) => typeof node === "string" || node.attrs.class !== "home-hero",
);

export default function HomePage() {
  return (
    <>
      <Hero />
      <RichContent nodes={remainingSections} />
    </>
  );
}
