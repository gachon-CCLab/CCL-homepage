export type ContentNode =
  | string
  | {
      tag: string;
      attrs: Record<string, string | boolean | undefined>;
      children?: ContentNode[];
    };

export interface Photo {
  src: string;
  alt: string;
}
export type PhotoGroups = Record<string, Photo[]>;

export interface PageContent {
  id: string;
  filename: string;
  title: string;
  description: string;
  heading: ContentNode | null;
  anchors: ContentNode[];
  content: ContentNode[];
  photos: PhotoGroups;
}

export interface Member {
  id: string;
  order: number;
  name: string;
  status: string;
  department: string;
  email: string | null;
  notes: string[];
  links: { href: string; label: string }[];
  membership: "current" | "former";
  photo: string;
}

export interface Seminar {
  id: string;
  order: number;
  date: string;
  organization: string;
  details: string[];
  links: { href: string; label: string }[];
  images: string[];
}

export interface NavigationItem {
  label: string;
  href: string;
  children: { label: string; href: string }[];
}
