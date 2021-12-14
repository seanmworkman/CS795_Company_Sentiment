// Imported loaders 
const { 
  runSearchAndAnalysis
} = require('./loaders');

// All resolvers used for queries/mutations 
const resolvers = {
  
  Query: {
    runSearchAndAnalysis
  }
  
};

module.exports.resolvers = resolvers;