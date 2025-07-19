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

def get_history():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10")
    history = c.fetchall()
    conn.close()
    return history