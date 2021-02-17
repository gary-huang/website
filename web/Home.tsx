import React from "react";
import { Box, Container, makeStyles } from "@material-ui/core";
// import Background from './assets/church-home.jpg'

const useStyles = makeStyles({
  root: {
    minHeight: "100vh",
    position: "relative",
    // backgroundImage:`url(${Background})`,
    backgrounSize: 'cover'
  },
});

type HomeProps = {};

const Home: React.FC<HomeProps> = () => {
  const classes = useStyles();
  return (
    <Container>
      <Box className={classes.root}>
        {/* <h1>Hello</h1>
        <h1>Hello</h1> */}
        <img src={require('/static/img/crossroads.png')} />
      </Box>
    </Container>
  );
};

export default Home;
