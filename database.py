import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            sentiment TEXT,
            timestamp TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            input_text TEXT,
            response_text TEXT,
            intent TEXT,
            timestamp TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            score INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(user_id, user_message, bot_response, sentiment):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO messages (user_id, user_message, bot_response, sentiment, timestamp) VALUES (?, ?, ?, ?, ?)",
        (user_id, user_message, bot_response, sentiment, timestamp)
    )
    conn.commit()
    conn.close()

def save_feedback(user_id, input_text, response_text, intent):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO feedback (user_id, input_text, response_text, intent, timestamp) VALUES (?, ?, ?, ?, ?)",
        (user_id, input_text, response_text, intent, timestamp)
    )
    conn.commit()
    conn.close()

def save_rating(user_id, user_message, bot_response, score):
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO ratings (user_id, user_message, bot_response, score, timestamp) VALUES (?, ?, ?, ?, ?)",
        (user_id, user_message, bot_response, score, timestamp)
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10")
    history = c.fetchall()
    conn.close()
    return history

def get_feedback_data():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("SELECT input_text, intent FROM feedback")
    data = c.fetchall()
    conn.close()
    return data

def get_rating_data():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    try:
        c.execute("SELECT user_message, bot_response, score FROM ratings")
        data = c.fetchall()
    except sqlite3.OperationalError:
        data = []
    conn.close()
    return data