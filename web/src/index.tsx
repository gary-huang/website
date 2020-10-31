import 'react-hot-loader' // Has to be imported before react + react-dom
import { ApolloClient } from 'apollo-client'
import { InMemoryCache } from 'apollo-cache-inmemory'
import { ApolloLink } from 'apollo-link'
import { setContext } from 'apollo-link-context'
import { HttpLink } from 'apollo-link-http'
import { onError } from 'apollo-link-error'
import React from 'react'
import ReactDOM from 'react-dom'
import { App } from './App'
import { ApolloProvider } from '@apollo/react-hooks'

import '../index.html'
import { ThemeProvider, CssBaseline, createMuiTheme } from '@material-ui/core'

declare global {
  interface Window {
    CSRF_TOKEN: string
  }
}

const authLink = setContext((_, { headers }) => {
  // return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      authorization: window.CSRF_TOKEN ? `Bearer ${window.CSRF_TOKEN}` : '',
    },
  }
})

const client = new ApolloClient({
  link: authLink.concat(
    ApolloLink.from([
      onError(({ graphQLErrors, networkError }) => {
        if (graphQLErrors)
          graphQLErrors.forEach(({ message, locations, path }) =>
            console.log(
              `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
            )
          )
        if (networkError) console.log(`[Network error]: ${networkError}`)
      }),
      new HttpLink({
        uri: '/gql/',
      }),
    ])
  ),
  cache: new InMemoryCache(),
})

const theme = createMuiTheme({
  palette: {
    type: 'dark',
  },
})

ReactDOM.render(
  <ApolloProvider client={client}>
    <ThemeProvider theme={theme}>
      <CssBaseline>
        <App />
      </CssBaseline>
    </ThemeProvider>
  </ApolloProvider>,
  document.getElementById('react-app')
)
