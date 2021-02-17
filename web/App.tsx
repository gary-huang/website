import { hot } from "react-hot-loader/root"; // has to be imported before react and react-dom
import React from "react";
import { gql, useQuery } from "@apollo/client";
import { Helmet } from "react-helmet";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import Auth from "./Auth";
import Home from "./Home";
import Giving from "./Giving";

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
        <Navbar user={data?.currentUser}></Navbar>
        <div style={{ marginTop: 75 }}>
          <Switch>
            <Route path="/give">
              <Giving />
            </Route>
            <Route path="/login">
              <Auth />
            </Route>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </div>
        <Footer />
      </Router>
    </React.Fragment>
  );
};

export const App = hot(AppBase);
