import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faEllipsisVertical} from "@fortawesome/free-solid-svg-icons";
import React, {useMemo, useState} from "react";
import {Link, useParams} from "react-router-dom";

import {DocumentWithContent, Section, Sentence} from "./models";

function groupToJSX(group: Sentence[]) {
  const childNodes: React.ReactNode[] = [];
  group.forEach(sentence => {
    childNodes.push(<FontAwesomeIcon icon={faEllipsisVertical} key={sentence.id}/>);
    childNodes.push(sentence.text);
  })

  const key = group[0].id;

  switch (group[0].sentence_type) {
    case "h1":
      return <h1 key={key}>{childNodes}</h1>;
    case "h2":
      return <h2 key={key}>{childNodes}</h2>;
    case "h3":
      return <h3 key={key}>{childNodes}</h3>;
    case "np":
      return <p key={key}>{childNodes}</p>;
    case "npi":
      return <p key={key} style={{paddingLeft: "2em"}}>{childNodes}</p>;
    case "hr":
      if (group.length > 1 || group[0].text != "") {
        throw new Error("Content inside hr");
      }
      return <hr key={key}/>;
    case "img":
      if (group.length > 1) {
        throw new Error("Sentences inside img");
      }
      return <img key={key} src={group[0].text}/>;
    case "p":
      throw new Error("Group starting with p");
  }
}

function sectionToJSX(section: Section) {
  const groups: Sentence[][] = [];

  section.sentences.forEach(sentence => {
    if (sentence.sentence_type === "p") {
      if (groups.length > 1) {
        groups[groups.length-1].push(sentence);
      } else {
        throw new Error("First sentence has type p");
      }
    } else {
      groups.push([sentence]);
    }
  });

  return groups.map(group => groupToJSX(group));
}

export default function Document(_props: {}) {
  const params = useParams()
  const id = params.id!;

  const [document, setDocument] = useState<DocumentWithContent | null>(null);

  useMemo(
    () => {
      setDocument(null);

      fetch(`/api/document?id=${id}`)
        .then(res => res.json())
        .then(data => setDocument(data));
    },
    [id],
  )

  if (document === null) {
    return null;
  }

  return (
    <div>
      <div>
        <a href={document.link} target="_blank">
          {document.title}
        </a>
      </div>
      <div>
        <Link to={`/collection/${document.collection.id}`}>
          Go up to {document.collection.title}
        </Link>
      </div>
      <div>{document.sections.map(section => (
        <div key={section.id} style={{borderLeft: "1px solid black", marginBottom: "1em", paddingLeft: "1em"}}>
          {sectionToJSX(section)}
        </div>
      ))}</div>
    </div>
  );
}
