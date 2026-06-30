import sqlite3

conn = sqlite3.connect("db/boardgames.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(game)")

for coluna in cursor.fetchall():
    print(coluna)