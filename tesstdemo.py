import sqlite3
import requests
import json

# Cấu hình API AI
API_KEY = "AIzaSyDzftjjua58oJFqYgr5YHdt36ps72zhpXk"
GEMINI_API_URL = "https://gemini.googleapis.com/v1/your_endpoint"

# Cấu hình tính cách chatbot
BOT_PERSONALITY = {
    "name": "Dr. Y",
    "style": "hài hước, thân thiện nhưng uyên bác",
    "response_format": "Ngắn gọn nhưng đầy đủ thông tin",
    "catchphrase": "Đừng lo, Dr. Y ở đây!"
}

def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

def query_database(question):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM chat_history WHERE question = ?", (question,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def send_message_to_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": f"{BOT_PERSONALITY['catchphrase']}\n{BOT_PERSONALITY['style']}\n{BOT_PERSONALITY['response_format']}\nCâu hỏi: {prompt}\nTrả lời:",
        "max_tokens": 150,
        "temperature": 0.7,
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("response", "Xin lỗi, tôi không có câu trả lời cho câu hỏi này.")
    else:
        return "Có lỗi xảy ra khi kết nối với AI."

def save_to_database(question, answer):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO chat_history (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def main():
    init_db()
    print(f"{BOT_PERSONALITY['name']}: Xin chào! Tôi là {BOT_PERSONALITY['name']}, sẵn sàng giúp bạn.")
    print("Gõ 'exit' để thoát.")
    while True:
        question = input("Bạn: ").strip()
        if question.lower() == "exit":
            break
        
        answer = query_database(question)
        if not answer:
            answer = send_message_to_ai(question)
            save_to_database(question, answer)
        
        print(f"{BOT_PERSONALITY['name']}: {answer}")

if __name__ == "__main__":
    main()
    