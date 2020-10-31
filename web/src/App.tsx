import { useQuery } from 'react-apollo'
import { hot } from 'react-hot-loader'
import gql from 'graphql-tag'
import React from 'react'

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

const AppBase: React.FC<AppProps> = (props) => {
  const { data, loading } = useQuery(GET_USER_DATA)
  return <h1>{data?.currentUser?.firstName ?? 'log'} is a 🍑</h1>
}

export const App = hot(module)(AppBase)
