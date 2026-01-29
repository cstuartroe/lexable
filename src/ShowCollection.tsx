import React, {useMemo} from "react";
import {Link, useParams} from "react-router-dom";
import {CollectionWithDocuments} from "./models";

export default function ShowCollection(_props: {}) {
  const params = useParams()
  const id = params.id!;

  const [collection, setCollection] = React.useState<CollectionWithDocuments | null>(null);

  useMemo(
    () => {
      setCollection(null);

      fetch(`/api/collection?id=${id}`)
        .then(res => res.json())
        .then(data => setCollection(data));
    },
    [id],
  );

  if (collection === null) {
    return null;
  }

  return (
    <div>
      <div>
        <Link to="/collections">
          All collections
        </Link>
      </div>
      <div>
        <a href={collection.link} target="_blank">
          {collection.title}
        </a>
        {!collection.published && " (not published)"}
      </div>
      <div>by {collection.author}</div>
      {/* TODO: make better alt text */}
      <img
        alt={`cover image for collection ${collection.title}`}
        src={collection.image}
      />
      <div>{collection.description}</div>
      <ol>
        {collection.documents.map((doc) => (
          <li key={doc.id}><Link to={`/document/${doc.id}`}>{doc.title}</Link></li>
        ))}
      </ol>
    </div>
  );
}
