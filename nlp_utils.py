import spacy
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from fuzzywuzzy import fuzz
import sqlite3

def process_input(user_input, nlp, classifier, tokenizer):
    doc = nlp(user_input.lower())
    
    # Basic intent detection using direct string matching for Indonesian phrases
    greeting_keywords = ["hello", "hi", "hey", "halo", "selamat malam", "selamat pagi", "selamat siang"]
    question_keywords = ["apa", "kapan", "dimana", "siapa", "mengapa", "bagaimana"]
    basic_intent = "greeting" if any(keyword in user_input.lower() for keyword in greeting_keywords) else \
                   "question" if any(keyword in user_input.lower() for keyword in question_keywords) or any(token.tag_ == "WP" for token in doc) else \
                   "statement"
    
    # Check if enough training data exists for BERT
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feedback")
        feedback_count = cursor.fetchone()[0]
        conn.close()
    except sqlite3.OperationalError:
        feedback_count = 0

    # Use BERT only if enough training data (>10 entries)
    predicted_intent = basic_intent
    if classifier and tokenizer and feedback_count > 10:
        inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True, max_length=128)
        outputs = classifier(**inputs)
        predicted_idx = torch.argmax(outputs.logits, dim=1).item()
        intent_map = {0: "greeting", 1: "question", 2: "statement", 3: "custom"}
        predicted_intent = intent_map.get(predicted_idx, basic_intent)
    
    # Disable entity recognition for non-English inputs
    entities = {}
    print(f"Debug: user_input='{user_input}', predicted_intent='{predicted_intent}', basic_intent='{basic_intent}', entities={entities}, feedback_count={feedback_count}")
    return predicted_intent, entities

def get_response(intent, entities, responses, context, user_id, user_input):
    intent_responses = responses.get(intent, {})
    if not intent_responses:
        print(f"Debug: No responses found for intent '{intent}'")
        return "I don't know how to respond to that yet. Try /train to teach me!"

    # Try to match exact input first (case-insensitive)
    user_input_lower = user_input.lower().strip()
    print(f"Debug: Checking intent '{intent}' with user_input_lower='{user_input_lower}', available keys={list(intent_responses.keys())}")
    for input_text, response_data in intent_responses.items():
        if fuzz.ratio(input_text.lower(), user_input_lower) > 90:  # Fuzzy matching with threshold
            print(f"Debug: Matched input '{input_text}' with response '{response_data['response']}'")
            return response_data["response"]

    # Select response with highest score if no exact match
    if intent_responses:
        best_response = max(intent_responses.items(), key=lambda x: x[1].get("score", 0), default=(None, {"response": "No response available"}))
        response_text = best_response[1]["response"]
        print(f"Debug: No exact match, using default response for intent '{intent}': '{response_text}'")
        
        if intent == "greeting":
            return response_text
        elif intent == "question":
            if "PERSON" in entities:
                return response_text.format(name=entities.get("PERSON", "someone")) if "{name}" in response_text else response_text
            return response_text
        else:
            if "DATE" in entities:
                return response_text.format(date=entities.get("DATE", "some date")) if "{date}" in response_text else response_text
            return response_text