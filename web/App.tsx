import { hot } from "react-hot-loader/root"; // has to be imported before react and react-dom
import React from "react";
import { gql, useQuery } from "@apollo/client";
import { Helmet } from "react-helmet";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import Home from "./Home";
import Giving from "./Giving";
import { Service, Services } from "./Service";

type AppProps = {};

export const GET_USER_DATA = gql`
  query {
    currentUser {
      username
      firstName
      lastName
    }
  }
`;

const AppBase: React.FC<AppProps> = () => {
  const { data, loading } = useQuery(GET_USER_DATA);
  console.log(loading, data);

  return (
    <React.Fragment>
      <Helmet>
        <title>Crossroads</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Helmet>
      <Router>
        <Navbar></Navbar>
        <Switch>
          <Route path="/services">
            <Services />
          </Route>
          <Route path="/service/:slug">
            <Service />
          </Route>
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

export const App = hot(AppBase);
