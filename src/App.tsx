import React, { Component } from "react";
import {createBrowserRouter, RouterProvider} from "react-router-dom";

import "../static/scss/main.scss";

class App extends Component {
    render() {
        return (
            <RouterProvider router={createBrowserRouter([
                {
                    path: "/",
                    element: <div>Hello world!</div>,
                },
            ])}/>
        );
    }
}

export default App;
