import React from "react";
import {createBrowserRouter, RouterProvider} from "react-router-dom";

import "../static/scss/main.scss";

export default function App(_props: {}) {
  return (
    <RouterProvider router={createBrowserRouter([
      {
        path: "/",
        element: <div>Hello world!</div>,
      },
    ])}/>
  );
}
