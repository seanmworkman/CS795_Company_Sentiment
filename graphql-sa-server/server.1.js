const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');
const { typeDefs } = require('./graphql/schema');
const { resolvers } = require('./graphql/resolvers');
const fs = require('fs');
const https = require('https');
const http = require('http');

const configurations = {
    // Note: You may need sudo to run on port 443
    production: { ssl: true, port: 80, hostname: 'localhost' },
    development: { ssl: false, port: 4000, hostname: 'localhost' }
};

const environment = process.env.NODE_ENV || 'production';
const config = configurations[environment];

const apollo = new ApolloServer({ typeDefs, resolvers });

const app = express();

apollo.applyMiddleware({ app });

// Create the HTTPS or HTTP server, per configuration
var server;

if (config.ssl) {
    // Assumes certificates are in .ssl folder from package root. Make sure the files
    // are secured.
    server = https.createServer(
        {
            key: fs.readFileSync(`./ssl/server.key`),
            cert: fs.readFileSync(`./ssl/server.crt`)
        },
        app
    );
} else {
    server = http.createServer(app);
}

// Add subscription support
apollo.installSubscriptionHandlers(server);


server.listen({ port: config.port }, () =>
  console.log(
    'Server ready at',
    `http${config.ssl ? 's' : ''}://${config.hostname}:${config.port}${apollo.graphqlPath}`
  )
);