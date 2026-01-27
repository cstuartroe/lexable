export type Language = (
  "arb"
  | "cmn"
  | "deu"
  | "eng"
  | "epo"
  | "fra"
  | "heb"
  | "hin"
  | "ita"
  | "jpn"
  | "kor"
  | "nld"
  | "por"
  | "rus"
  | "spa"
  | "tur"
);

type SentenceType = (
  "h1"
  | "h2"
  | "h3"
  | "np" // new paragraph
  | "npi" // new block-indented paragraph
  | "p" // paragraph continuation
  | "hr" // horizontal rule
  | "img"
);

export type Sentence = {
  id: number,
  sentence_type: SentenceType,
  text: string,
}

export type Section = {
  id: number,
  sentences: Sentence[],
}

export type Document = {
  id: number,
  title: string,
  link: string,
  collection: Collection,
}

export type DocumentWithContent = Document & {
  sections: Section[],
}

export type Collection = {
  id: number,
  language: Language,
  title: string,
  author: string,
  description: string,
  link: string,
  image: string,
  free: boolean,
}
export type CollectionWithDocuments = Collection & {
  documents: Document[],
}
