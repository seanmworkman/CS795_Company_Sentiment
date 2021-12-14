const { ApolloServer, gql } = require('apollo-server-express');
var bodyParser = require('body-parser');
var cors = require('cors');
const express = require('express');
const http = require('http');
var path = require("path");

const fileUpload = require('express-fileupload');
var fs = require('fs');

const { typeDefs } = require('./graphql/schema.js');
const { resolvers } = require('./graphql/resolvers.js');


const configurations = {
    // Note: You may need sudo to run on port 443
    production: { port: 4000, hostname: 'sa-server' },
    development: { port: 4000, hostname: 'localhost' },
    test: { port: 4000, hostname: 'localhost' }
};

const environment = process.env.NODE_ENV || 'development';
const config = configurations[environment];

const app = express();

app.use(fileUpload());

const apollo = new ApolloServer({
  typeDefs,
  resolvers
});


app.use(cors());

app.use('/', express.static(path.join(__dirname,'./build')));

app.get( '/', function(req, res) {
  
    res.sendFile(path.join(__dirname, './build/index.html'));
});

//support parsing of application/json type post data
app.use(bodyParser.json());

apollo.applyMiddleware({ app, path: '/graphql' });

// Create the HTTPS or HTTP server, per configuration
var server = http.createServer(app);

// Add subscription support
apollo.installSubscriptionHandlers(server);


server.listen({ port: config.port }, () =>
  console.log(
    'Server ready at',
    `http://${config.hostname}:${config.port}${apollo.graphqlPath}`
  )
);