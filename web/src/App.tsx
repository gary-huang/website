import { useQuery } from 'react-apollo'
import gql from 'graphql-tag';
import React from "react";

export const GET_USER_DATA = gql`
    query {
        currentUser {
            username
            firstName
            lastName
        }
    }
`
type AppProps = {}


const App: React.FC<AppProps> = props => {
    const { data, loading } = useQuery(GET_USER_DATA)
    return (
        <h1>{data?.currentUser?.firstName ?? 'kyle'} is a 🍑</h1>
    );
}

export default App;
