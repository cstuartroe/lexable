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
    <div>
      {collections.map((collection) => (
        <Link to={`/collection/${collection.id}`} key={collection.id}>{collection.title}</Link>
      ))}
    </div>
  );
}
