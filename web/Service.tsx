import React from "react";
import { Link, useParams } from "react-router-dom";
import { gql, useQuery } from "@apollo/client";
import { Container } from "@material-ui/core";

const GET_SERVICE_PAGE = gql`
  query($slug: String!) {
    services(slug: $slug) {
      edges {
        node {
          id
          slug
          title
          description
        }
      }
    }
  }
`;

const GET_SERVICES = gql`
  query {
    services {
      edges {
        node {
          slug
          title
          description
        }
      }
    }
  }
`;

type ServiceProps = {};

const Service: React.FC<ServiceProps> = () => {
  let { slug } = useParams();
  const { loading, error, data } = useQuery(GET_SERVICE_PAGE, {
    variables: {
      slug,
    },
  });
  const page = data ? data.services.edges[0].node : null;
  console.log(loading, data);

  return (
    <Container>
      <h1>Log in</h1>
      {data && (
        <React.Fragment>
          <h1>{page.title}</h1>
          <div dangerouslySetInnerHTML={{ __html: page.description }} />
        </React.Fragment>
      )}
    </Container>
  );
};

type ServicesProps = {};

const Services: React.FC<ServicesProps> = () => {
  const { loading, error, data } = useQuery(GET_SERVICES, {
    variables: {},
  });
  const pages = data?.services?.edges;
  console.log(loading, data);

  return (
    <Container>
      <h1>Services</h1>
      {data && (
        <React.Fragment>
          <ul>
            {pages.map((page: any, i: number) => (
              <li key={i}>
                <Link to={`/service/${page.node.slug}`}>{page.node.title}</Link>
              </li>
            ))}
          </ul>
        </React.Fragment>
      )}
    </Container>
  );
};
export { Service, Services };
