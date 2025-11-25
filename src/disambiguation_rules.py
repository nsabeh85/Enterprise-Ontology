import json
import re
import os

class Disambiguator:
    def __init__(self, ontology_path=None):
        # If no path is provided, construct the path
        if ontology_path is None:
            # Construct path relative to the script's location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ontology_path = os.path.join(script_dir, '..', 'data', 'ontology_runtime.json')
        
        # Print the path to verify
        print(f"Loading ontology from: {ontology_path}")
        
        # Open and load the file
        try:
            with open(ontology_path, 'r') as f:
                self.ontology = json.load(f)
            
            self.entities = self.ontology.get('entities', {})
        except FileNotFoundError:
            print(f"Error: Ontology file not found at {ontology_path}")
            self.entities = {}

    def normalize_query(self, query: str) -> str:
        # Convert to lowercase
        query = query.lower()
        
        # Remove punctuation and special characters
        query = re.sub(r'[^\w\s]', '', query)
        
        # Remove extra whitespaces
        query = ' '.join(query.split())
        
        # Remove common stop words or noise
        stop_words = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'tell', 'me', 'about']
        query_words = [word for word in query.split() if word not in stop_words]
        
        return ' '.join(query_words).strip()

    def get_entity_keywords(self, entity_name):
        # Extract keywords from entity
        entity = self.entities.get(entity_name, {})
        keywords = []
        keywords.extend(entity.get('synonyms', []))
        keywords.extend(entity.get('related_terms', []))
        keywords = [kw.lower() for kw in keywords]
        return keywords

    def disambiguate_term(self, term: str, query: str) -> str:
        query_lower = self.normalize_query(query)
        term_lower = term.lower()

        # Dynamically find potential entities that match the term
        potential_entities = []
        for entity_name, entity_details in self.entities.items():
            # Check synonyms
            synonyms = [syn.lower() for syn in entity_details.get('synonyms', [])]
            # Check related terms
            related_terms = [rt.lower() for rt in entity_details.get('related_terms', [])]
            
            # Combine all possible matching terms
            matching_terms = synonyms + related_terms + [entity_name.lower()]
            
            # Check if the term is in any of these matching terms
            if any(term_lower in mt for mt in matching_terms):
                potential_entities.append(entity_name)

        # If we found potential entities, try to select the most relevant
        for entity in potential_entities:
            entity_details = self.entities.get(entity, {})
            keywords = entity_details.get('related_terms', []) + entity_details.get('synonyms', [])
            keywords = [kw.lower() for kw in keywords]
            
            if any(kw in query_lower for kw in keywords):
                return entity

        # Default: return first potential entity or original term
        return potential_entities[0] if potential_entities else term

    def get_disambiguation_context(self, query: str) -> dict:
        results = {}
        normalized_query = self.normalize_query(query)
        
        # Directly use ontology to find ambiguous terms
        for term, entity_details in self.entities.items():
            synonyms = entity_details.get('synonyms', [])
            related_terms = entity_details.get('related_terms', [])
            
            # Check if any synonym or related term is in the normalized query
            matching_terms = [
                syn.lower() for syn in synonyms + related_terms
                if syn.lower() in normalized_query
            ]
            
            # If matching terms found, add to disambiguation context
            if matching_terms:
                disambiguated = self.disambiguate_term(term, query)
                results[term.lower()] = disambiguated
        
        return results

# Test function
if __name__ == "__main__":
    disambiguator = Disambiguator()
    
    test_queries = [
        "What's the Service.   fabric topology at DFW10?",
        "Is ServiceFabric available at DFW10?",
        "Tell me about fabric connectivity in Dallas",
        "What's the power capacity at PHX10?",
        "How much rack space is available in the data center?",
        "Explain Metro Connect availability",
        "Discuss colo services at DFW10",
        "What are the connectivity options for Scale deployment?",
        "Describe PlatformDIGITAL infrastructure",
        "How does Data Gravity impact my deployment?",
        "What are the DRIX interconnection services?"
    ]
    
    for query in test_queries:
        context = disambiguator.get_disambiguation_context(query)
        print(f"\nQuery: {query}")
        print(f"Normalized Query: {disambiguator.normalize_query(query)}")
        print(f"Disambiguation Context: {context}")