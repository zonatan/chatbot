import json
import sqlite3
from datetime import datetime
from decouple import config
import spacy
from textblob import TextBlob
from database import init_db, save_message, get_history
from nlp_utils import process_input, get_response

class Chatbot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.context = {}
        self.responses = self.load_responses()
        init_db()

    def load_responses(self):
        with open("responses.json", "r") as f:
            return json.load(f)

    def handle_command(self, user_input):
        if user_input == "/help":
            return "Commands: /help, /history, /clear"
        elif user_input == "/history":
            history = get_history()
            return "\n".join([f"{row[1]} ({row[3]}): {row[2]}" for row in history]) or "No history yet."
        elif user_input == "/clear":
            self.context.clear()
            return "Context cleared."
        return None

    def process_message(self, user_input, user_id="user1"):
        command_response = self.handle_command(user_input)
        if command_response:
            save_message(user_id, user_input, command_response, "neutral")
            return command_response

        # Process input with NLP
        intent, entities = process_input(user_input, self.nlp)
        sentiment = TextBlob(user_input).sentiment.polarity
        sentiment_label = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"

        # Update context
        self.context[user_id] = self.context.get(user_id, {})
        self.context[user_id]["last_intent"] = intent
        self.context[user_id]["entities"] = entities

        # Get response
        response = get_response(intent, entities, self.responses, self.context, user_id)

        # Save to database
        save_message(user_id, user_input, response, sentiment_label)
        return response

def main():
    bot = Chatbot()
    user_id = config("USER_ID", default="user1")
    print("GrokBot started! Type /help for commands or /quit to exit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "/quit":
            print("Goodbye!")
            break
        response = bot.process_message(user_input, user_id)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()