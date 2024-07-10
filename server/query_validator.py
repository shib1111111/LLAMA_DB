import re
import spacy
from word_lists import non_query_words_list,abusive_words_list

class QueryValidator:
    def __init__(self):
        self.non_dml_keywords = ["create", "alter", "drop", "truncate", "rename", "grant", "revoke", "commit", "rollback", "savepoint", "set", "show", "use", "lock", "unlock", "merge"]
        self.restricted_phrases = ["show me", "graph", "visualize", "pivot table", "crosstab"]
        self.non_query_responses = non_query_words_list
        self.abusive_patterns = abusive_words_list

    
    # Check if the query is a non-DML query
    def is_non_dml_query(self, user_query: str) -> str:
        if any(keyword in user_query.lower() for keyword in self.non_dml_keywords):
            return "Please only query DML related questions."
        if any(phrase in user_query.lower() for phrase in self.restricted_phrases):
            return "Please only query DML related questions."
        return ""


    # Check if the query contains non-query responses or abusive language
    def contains_non_query_response(self, user_query: str) -> str:
        if any(response.lower() in user_query.lower() for response in self.non_query_responses):
            return "Please provide your query,if you need any help..."
        if any(re.search(pattern, user_query.lower()) for pattern in self.abusive_patterns):
            return "Please don't use abusive language."
        return ""

    # Validate the query
    def validate_query(self, user_query: str) -> str:
        non_dml_message = self.is_non_dml_query(user_query)
        if non_dml_message:
            return non_dml_message
        
        non_query_message = self.contains_non_query_response(user_query)
        if non_query_message:
            return non_query_message
        
        return "Query is valid."
    
    
    
# Function to check if the query is complex
def is_complex_sentence(user_query: str) -> bool:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(user_query)
    num_clauses = sum(1 for token in doc if token.dep_ == "conj" or token.dep_ == "cc")
    sentence_length = len(doc)
    # If more than one conjunction or longer than 20 words
    return num_clauses > 1 or sentence_length > 20