import { hot } from "react-hot-loader";
import React from "react";
import { Helmet } from "react-helmet";
import { BrowserRouter as Router, Link, Switch, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import Home from "./Home";
import Giving from "./Giving";

type AppProps = {};

const AppBase: React.FC<AppProps> = (props) => {
  return (
    <React.Fragment>
      <Helmet>
        <title>Crossroads</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Helmet>
      <Router>
        <Navbar></Navbar>
        <Switch>
          <Route path="/give">
            <Giving />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
        <Footer />
      </Router>
    </React.Fragment>
  );
};

export const App = hot(module)(AppBase);
