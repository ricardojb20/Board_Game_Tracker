import sqlite3
from datetime import datetime

DB_PATH = "boardgames.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    return conn, cur

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game (
        id_game INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL UNIQUE,
        year INTEGER NOT NULL,
        rank INTEGER NOT NULL,
        rating REAL NOT NULL,
        weight REAL NOT NULL,
        url_saltadacaixa TEXT,
        url_gameplaypt TEXT, 
        image_path TEXT
    )
    """) 

    cur.execute("""
    CREATE TABLE IF NOT EXISTS store (
        id_store INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        croped_link TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS price (
        id_price INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_game INTEGER NOT NULL,
        id_store INTEGER NOT NULL,
        price REAL NOT NULL,
        stock TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (id_game) REFERENCES game(id_game),
        FOREIGN KEY (id_store) REFERENCES store(id_store)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS wishList (
        id_wishList INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_user INTEGER NOT NULL,
        name TEXT NOT NULL,

        FOREIGN KEY (id_user) REFERENCES user(id_user)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS wishList_game (
        id_wishList INTEGER NOT NULL,
        id_game INTEGER NOT NULL,

        PRIMARY KEY (id_wishList, id_game),
        FOREIGN KEY (id_wishList) REFERENCES wishList(id_wishList),
        FOREIGN KEY (id_game) REFERENCES game(id_game)
    )
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_price_game_store_date
    ON price(id_game, id_store, date)
    """)
    conn.commit()
    conn.close()

