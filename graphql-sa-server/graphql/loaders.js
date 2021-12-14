const _ = require("lodash");

const axios = require('axios');


const userFriendlyUnexpectedError = () => {
  return new Error("An unexpected error occurred");
}

const logError = (err) => {
  var stack = new Error().stack,
      caller = stack.split('\n')[2].trim();
  console.log("Error in " + caller + ":", err);
}

/**
 * Runs the sentiment analysis based on the search term
 * @param {*} root 
 * @param {*} param1 
 */
const runSearchAndAnalysis = async (root, { searchTerm, method }) => {
  let term = searchTerm.replace(" ", "+");
  console.log(term, method)
  let url = `http://127.0.0.1:5000/sentAnalysis?method=${method}&searchTerm=${term}`;
  try {
    const response = await axios.get(url);
    return response.data;
  } catch (err) {
    console.log(err.response.body);
    logError(err);
    throw userFriendlyUnexpectedError();
  }
}

module.exports.runSearchAndAnalysis = runSearchAndAnalysis;