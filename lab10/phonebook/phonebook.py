import os
from dotenv import load_dotenv
import psycopg2, csv

load_dotenv()

DB_PARAMS = {
    "dbname":   os.getenv("DB_NAME"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host":     os.getenv("DB_HOST"),
    "port":     os.getenv("DB_PORT")
}

def get_conn():
    return psycopg2.connect(**DB_PARAMS)

def insert_from_csv(path):
    sql = "INSERT INTO phonebook(username,phone) VALUES (%s,%s) ON CONFLICT (username) DO NOTHING"
    with get_conn() as conn, conn.cursor() as cur, open(path) as f:
        reader = csv.reader(f)
        for user, phone in reader:
            cur.execute(sql, (user.strip(), phone.strip()))

def insert_from_console():
    u = input("username> ").strip()
    p = input("phone> ").strip()
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO phonebook(username,phone) VALUES (%s,%s)",
            (u, p)
        )

def update_username(old, new):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE phonebook SET username=%s WHERE username=%s",
            (new, old)
        )

def update_phone(user, new_phone):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE username=%s",
            (new_phone, user)
        )

def query_all():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT username,phone FROM phonebook")
        return cur.fetchall()

def query_by_username(pattern):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT username,phone FROM phonebook WHERE username ILIKE %s",
            (f"%{pattern}%",)
        )
        return cur.fetchall()

def query_by_phone(pattern):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT username,phone FROM phonebook WHERE phone LIKE %s",
            (f"%{pattern}%",)
        )
        return cur.fetchall()

def delete_by_username(user):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM phonebook WHERE username=%s", (user,))

def delete_by_phone(phone):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))

def menu():
    print("""
1) load CSV  
2) add one  
3) update user  
4) update phone  
5) show all  
6) find user  
7) find phone  
8) delete user  
9) delete phone  
0) exit
""")
    return input("choose> ").strip()

if __name__ == "__main__":
    while True:
        cmd = menu()
        if   cmd == "1":
            insert_from_csv(input("csv path> "))
        elif cmd == "2":
            insert_from_console()
        elif cmd == "3":
            o = input("old username> ")
            n = input("new username> ")
            update_username(o, n)
        elif cmd == "4":
            u = input("username> ")
            p = input("new phone> ")
            update_phone(u, p)
        elif cmd == "5":
            for u, p in query_all():
                print(u, p)
        elif cmd == "6":
            for u, p in query_by_username(input("pattern> ")):
                print(u, p)
        elif cmd == "7":
            for u, p in query_by_phone(input("pattern> ")):
                print(u, p)
        elif cmd == "8":
            delete_by_username(input("username> "))
        elif cmd == "9":
            delete_by_phone(input("phone> "))
        elif cmd == "0":
            break
        else:
            print("unknown")
