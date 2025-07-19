import json
import sqlite3
from datetime import datetime
from decouple import config
import spacy
from textblob import TextBlob
from database import init_db, save_message, get_history, save_feedback, save_rating
from nlp_utils import process_input, get_response
from train import train_model, update_responses, auto_learn

class Chatbot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.context = {}
        self.responses = self.load_responses()
        self.classifier, self.tokenizer = train_model()  # Train the BERT classifier
        init_db()

    def load_responses(self):
        try:
            with open("responses.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"greeting": {}, "question": {}, "statement": {}, "custom": {}}

    def handle_command(self, user_input, user_id):
        if user_input == "/help":
            return "Commands: /help, /history, /clear, /train <input> | <response> | <intent>, /rate <score>"
        elif user_input == "/history":
            history = get_history()
            return "\n".join([f"{row[1]} ({row[5]}): {row[2]} -> {row[3]}" for row in history]) or "No history yet."
        elif user_input == "/clear":
            self.context.clear()
            return "Context cleared."
        elif user_input.startswith("/train"):
            # Split command and arguments explicitly
            input_parts = user_input.split(" ", 1)  # Split on first space to separate /train
            if len(input_parts) < 2:
                return "Usage: /train <input> | <response> | <intent> (contoh: /train Apa kabar? | Saya baik! | question)"
            command, args = input_parts
            if command.strip() != "/train":
                return "Invalid command. Use: /train <input> | <response> | <intent>"
            # Split arguments by |
            parts = [part.strip() for part in args.split("|")]
            print(f"Debug: parts = {parts}")  # Debug input parts
            if len(parts) != 3 or not all(parts):  # Expect 3 parts: input, response, intent
                return "Usage: /train <input> | <response> | <intent> (contoh: /train Apa kabar? | Saya baik! | question)"
            train_input, train_response, train_intent = parts
            train_intent = train_intent.lower()
            train_input = train_input.lower()  # Normalize input to lowercase
            save_feedback(user_id, train_input, train_response, train_intent)
            update_responses(train_input, train_response, train_intent, self.responses)
            self.responses = self.load_responses()  # Reload responses to ensure update
            return f"Trained: Intent '{train_intent}' with input '{train_input}' and response '{train_response}'"
        elif user_input.startswith("/rate"):
            try:
                score = int(user_input.split()[1])
                if 1 <= score <= 5:
                    last_message = get_history()[-1] if get_history() else None
                    if last_message:
                        save_rating(user_id, last_message[2], last_message[3], score)
                        return f"Response rated: {score}/5"
                    return "No response to rate."
                return "Score must be between 1 and 5."
            except (IndexError, ValueError):
                return "Usage: /rate <score> (1-5)"
        return None

    def process_message(self, user_input, user_id="user1"):
        self.context[user_id] = self.context.get(user_id, {})
        self.context[user_id]["last_input"] = user_input  # Store raw input for matching
        command_response = self.handle_command(user_input, user_id)
        if command_response:
            save_message(user_id, user_input, command_response, "neutral")
            return command_response

        # Process input with NLP
        intent, entities = process_input(user_input, self.nlp, self.classifier, self.tokenizer)
        sentiment = TextBlob(user_input).sentiment.polarity
        sentiment_label = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"

        # Update context
        self.context[user_id]["last_intent"] = intent
        self.context[user_id]["entities"] = entities

        # Get response
        response = get_response(intent, entities, self.responses, self.context, user_id, user_input)

        # Auto-learn from frequent patterns
        auto_learn(user_input, response, intent, self.responses)

        # Save to database
        save_message(user_id, user_input, response, sentiment_label)
        return response

def main():
    bot = Chatbot()
    user_id = config("USER_ID", default="user1")
    print("GrokBot Enhanced started! Type /help for commands or /quit to exit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "/quit":
            print("Goodbye!")
            break
        response = bot.process_message(user_input, user_id)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()