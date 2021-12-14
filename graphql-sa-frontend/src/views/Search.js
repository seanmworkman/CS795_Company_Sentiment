/**
 * @fileoverview This file contains the Splash page implementation.
 */

 import Alert from 'react-bootstrap/Alert';
 import React, { Component } from 'react';
 import ApolloClient from "apollo-boost";
 import {
   Button,
   Input,
   Label,
   Card, CardBody
 } from 'reactstrap';

 import {
  SEARCH
} from '../graphql/queries.js';

let client;

client = new ApolloClient({
  uri: "http://127.0.0.1:4000/graphql"
});


 class Search extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        searchTerm: "",
        method: "0",
        alertMessage: "",
        showDangerAlert: false,
        result: "0.0"
      };
    }  
  
    componentDidMount() {

    }
  
    /**
     * Sets the success alert message and the show state.
     */
    setDangerAlert = (message) => {
      this.setState({
        alertMessage: message,
        showDangerAlert: true
      });
    }
  
    /**
     * Displays the danger alert. This method is called in render.
     */
    showDangerAlert = () => {
      if (this.showDangerAlert) {
        return (
          <Alert variant="danger" onClose={() => this.setState({ showDangerAlert: false })} dismissible>
            <h4>{this.state.alertMessage}</h4>
          </Alert>
        );
      }
    }
  
    clickedElementIsButton = (element) => {
      return typeof element.target.className === 'string' && element.target.className.includes("btn");
    }
  
    closeAlertMessage = (e) => {
      if ((this.state.showDangerAlert === true)
        && !this.clickedElementIsButton(e)) {
        this.setState({ showDangerAlert: false });
      }
    }

    runSearch = async () => {
      try {
        console.log('searchTerm:', this.state.searchTerm)
        console.log('method:', this.state.method)
        let res = await client.query({
          query: SEARCH,
          variables: {
            searchTerm: this.state.searchTerm,
            method: this.state.method
          },
          fetchPolicy: 'network-only'
        });
        this.setState({
          result: res.data.runSearchAndAnalysis
        });
      } catch (err) {
        console.log(JSON.stringify(err, null, 2));
      }
    }

    displayResult = () => {
      let result = parseFloat(this.state.result);
      let polarity = "Neutral";
      if (result < 0.0) polarity = "Negative";
      if (result > 0.0) polarity = "Positive";
      return (
        <Card>
            <CardBody>
                Polarity: {polarity}<br />
                Aggregate Sentiment: {result}
            </CardBody>
        </Card>
      );
    }
  
    render() {
      return (
        <div style={{ marginLeft: "5px", marginRight: "5px" }} onClick={(e) => this.closeAlertMessage(e)}>
          <div id="message">
            <div style={{ padding: "5px" }}>
              <div id="inner-message">
                {this.state.showDangerAlert ? this.showDangerAlert() : null}
              </div>
            </div>
          </div>
          <Label>Company Search
            <Input 
              placeholder='i.e. "Apple", "AAPL"'
              onChange={(e) => this.setState({ searchTerm: e.target.value })}
            />
            <Button
              color="secondary"
              onClick={(e) => this.runSearch()}
            >SEARCH</Button>
          </Label>
          <br />
          <Label>
            <input
              style={{ padding: "5px" }}
              type="radio"
              value="0"
              checked={this.state.method === "0"}
              onChange={(e) => this.setState({ method: e.target.value })}
            />
            Unigram
          </Label>
          <br />
          <Label>
            <input
              style={{ padding: "5px" }}
              type="radio"
              value="1"
              checked={this.state.method === "1"}
              onChange={(e) => this.setState({ method: e.target.value })}
            />
            Bigram
          </Label>
          <br />
          <Label>
            <input
              style={{ padding: "5px" }}
              type="radio"
              value="2"
              checked={this.state.method === "2"}
              onChange={(e) => this.setState({ method: e.target.value })}
            />
            NLTK
          </Label>
          <br />
          <div>Results</div>
          <div>{this.displayResult()}</div>
        </div>
      );
    }
  }
  
  export default Search;