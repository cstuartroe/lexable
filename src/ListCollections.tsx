import React, {useMemo, useState} from "react";

import {Collection} from "./models";
import {Link} from "react-router-dom";

export default function ListCollections(_props: {}) {
  const [collections, setCollections] = useState<Collection[]>([]);

  useMemo(
    () => {
      fetch(`/api/collections?language=cmn`)
        .then(res => res.json())
        .then(data => setCollections(data));
    },
    [],
  )

  return (
    <ul>
      {collections.map((collection) => (
        <li key={collection.id}>
          <Link to={`/collection/${collection.id}`}>
            {collection.title}
          </Link>
        </li>
      ))}
    </ul>
  );
}
