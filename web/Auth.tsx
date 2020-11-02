import React from "react";
import { gql, useMutation } from "@apollo/client";
import { Box, Container, makeStyles } from "@material-ui/core";

const useStyles = makeStyles({
  root: {
    minHeight: "100vh",
    position: "relative",
  },
});

type AuthProps = {};

const Auth: React.FC<AuthProps> = (props) => {
  return <Container>
  <h1>Giving</h1>
  </Container>;
};

export default Auth;
