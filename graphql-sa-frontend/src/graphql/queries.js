import { gql } from "apollo-boost";

export const SEARCH = 
  gql`query runSearchAndAnalysis($searchTerm: String, $method: String) {
      runSearchAndAnalysis(searchTerm: $searchTerm, method: $method) 
  }`