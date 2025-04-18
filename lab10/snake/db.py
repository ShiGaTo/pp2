import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Загрузка настроек из .env
load_dotenv()
DB_PARAMS = {
    "dbname":   os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host":     os.getenv("DB_HOST"),
    "port":     os.getenv("DB_PORT")
}

def get_conn():
    """Создаёт и возвращает новое соединение."""
    return psycopg2.connect(**DB_PARAMS)

def get_or_create_user(username):
    """
    Ищет пользователя по имени; если нет — создаёт.
    Возвращает его id.
    """
    with get_conn() as conn, conn.cursor() as cur:
        # ищем
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        # создаём
        cur.execute("INSERT INTO users(username) VALUES (%s) RETURNING id", (username,))
        return cur.fetchone()[0]

def get_user_level(user_id):
    """
    Возвращает максимальный сохранённый level для данного user_id.
    Если записей нет — возвращает 1.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT MAX(level) FROM user_score WHERE user_id = %s",
            (user_id,)
        )
        result = cur.fetchone()[0]
        return result if result is not None else 1

def save_score(user_id, score, level):
    """
    Сохраняет текущее состояние игры: score, level и timestamp.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO user_score(user_id, score, level) VALUES (%s, %s, %s)",
            (user_id, score, level)
        )

if __name__ == "__main__":
    # простой тест
    uid = get_or_create_user("testuser")
    print("User ID:", uid)
    lvl = get_user_level(uid)
    print("Level:", lvl)
    save_score(uid, 123, lvl)
    print("Score saved.")
