import sqlite3
import streamlit as st

def init_favorites_db():
    conn = sqlite3.connect("favorites.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def save_favorite(question: str, answer: str) -> bool:
    conn = sqlite3.connect("favorites.db")
    c = conn.cursor()
    # 중복 체크
    c.execute("SELECT COUNT(*) FROM favorites WHERE question = ? AND answer = ?", (question, answer))
    exists = c.fetchone()[0]
    
    if exists == 0:
        c.execute("INSERT INTO favorites (question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()
        conn.close()
        return True  # 저장 성공
    else:
        conn.close()
        return False  # 이미 존재



def delete_favorite(fav_id: int):
    conn = sqlite3.connect("favorites.db")
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
    conn.commit()
    conn.close()



def get_favorites():
    conn = sqlite3.connect("favorites.db")
    c = conn.cursor()
    c.execute("SELECT id, question FROM favorites ORDER BY created_at DESC")
    results = c.fetchall()
    conn.close()
    return results
