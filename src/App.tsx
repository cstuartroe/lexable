import React from "react";
import {createBrowserRouter, RouterProvider} from "react-router-dom";

import "../static/scss/main.scss";
import ListCollections from "./ListCollections";
import ShowCollection from "./ShowCollection";
import Document from "./Document";

export default function App(_props: {}) {
  return (
    <RouterProvider router={createBrowserRouter([
      {
        path: "/",
        element: <div>Hello world!</div>,
      },
      {
        path: "/collections",
        element: <ListCollections/>,
      },
      {
        path: "/collection/:id",
        element: <ShowCollection/>,
      },
      {
        path: "/document/:id",
        element: <Document/>,
      },
    ])}/>
  );
}
