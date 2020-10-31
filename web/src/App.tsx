import { useQuery } from "react-apollo";
import { hot } from "react-hot-loader";
import gql from "graphql-tag";
import React from "react";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import { Box, makeStyles } from "@material-ui/core";

export const GET_USER_DATA = gql`
  query {
    currentUser {
      username
      firstName
      lastName
    }
  }
`;
const useStyles = makeStyles({
  root: {
    minHeight: "100vh",
    position: "relative",
  },
});

type AppProps = {};

const AppBase: React.FC<AppProps> = (props) => {
  const { data, loading } = useQuery(GET_USER_DATA);
  const classes = useStyles();
  return (
    <Box className={classes.root}>
      <Navbar></Navbar>
      <h1>
        {data?.currentUser?.firstName ?? "kyle"}
        is a 🍑 dalskjfal
      </h1>
      <Footer />
    </Box>
  );
};

export const App = hot(module)(AppBase);
