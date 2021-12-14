const { gql } = require('apollo-server-express');

// // The GraphQL schema
const typeDefs = gql`

  type Query {
    runSearchAndAnalysis(searchTerm: String, method: String): String
  }

  schema {
    query: Query
  }
`;

module.exports.typeDefs = typeDefs;