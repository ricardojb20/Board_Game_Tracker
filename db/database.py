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
        url_saltadacaixa TEXT, 
        image_path TEXT
    )
    """) # TODO: Alterar url_saltadacaixa e url_gameplaypt

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

    conn.commit()
    conn.close()


def insert_game(id_game, name, year, rank, rating, weight, image_path=None,url_saltadacaixa=None, url_gameplaypt=None):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO game (
                id_game, name, year, rank, rating, weight, image_path,
                url_saltadacaixa, url_gameplaypt
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_game, name, year, rank, rating, weight, image_path,
              url_saltadacaixa, url_gameplaypt))
        print(f"Jogo '{name}' inserido com sucesso.")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao inserir jogo '{name}': {e}")

    conn.commit()
    conn.close()



def show_all_games(sort=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # colunas válidas para ordenar
    valid_columns = ["id_game", "name", "year", "rank", "rating", "weight"]
    
    order_by = "name"  # default
    if sort in valid_columns:
        order_by = sort

    query = f"SELECT id_game, name, year, rank, rating, weight, image_path FROM game ORDER BY {order_by}"
    cur.execute(query)
    jogos = cur.fetchall()
    
    if not jogos:
        print("Não há jogos na base de dados.")
    else:
        for jogo in jogos:
            print(f"ID: {jogo[0]} | Nome: {jogo[1]} | Ano: {jogo[2]} | Rank: {jogo[3]} | "
                  f"Rating: {jogo[4]} | Peso: {jogo[5]}")
    
    conn.close()

def show_all_games_links():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    query = f"SELECT id_game, name, url_saltadacaixa, url_gameplaypt FROM game ORDER BY id_game"
    cur.execute(query)
    jogos = cur.fetchall()
    
    if not jogos:
        print("Não há jogos na base de dados.")
    else:
        for jogo in jogos:
            print(f"ID: {jogo[0]} | Nome: {jogo[1]} | Url_saltadacaixa: {jogo[2]} | Url_gameplaypt: {jogo[3]}")
    conn.close()

def create_user(name,email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO user (name,email) VALUES (?, ?)",
        (name,email,)
    )
    user_id = cur.lastrowid

    conn.commit()
    conn.close()

    print(f"Utilizador '{name}' criado com ID {user_id}.")
    return user_id

def create_wishlist(user_id, wishlist_name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # verifica se o utilizador existe
    cur.execute("SELECT 1 FROM user WHERE id_user = ?", (user_id,))
    if not cur.fetchone():
        print(f"Erro: utilizador {user_id} não existe.")
        conn.close()
        return None

    cur.execute(
        "INSERT INTO wishList (id_user, name) VALUES (?, ?)",
        (user_id, wishlist_name)
    )
    wishlist_id = cur.lastrowid

    conn.commit()
    conn.close()

    print(f"Wishlist '{wishlist_name}' criada com ID {wishlist_id} para o utilizador {user_id}.")
    return wishlist_id

def add_games_to_wishlist(id_wishlist, game_ids):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    for game_id in game_ids:
        # verifica se o jogo existe na tabela game
        cur.execute("SELECT 1 FROM game WHERE id_game = ?", (game_id,))
        if not cur.fetchone():
            print(f"Jogo {game_id} não existe na base de dados. Ignorado.")
            continue
        
        # verifica se já está na wishlist para evitar duplicados
        cur.execute(
            "SELECT 1 FROM wishlist_game WHERE id_wishList = ? AND id_game = ?",
            (id_wishlist, game_id)
        )
        if cur.fetchone():
            print(f"Jogo {game_id} já está na wishlist {id_wishlist}. Ignorado.")
            continue

        # insere na wishlist
        cur.execute(
            "INSERT INTO wishlist_game (id_wishList, id_game) VALUES (?, ?)",
            (id_wishlist, game_id)
        )
        print(f"Jogo {game_id} adicionado à wishlist {id_wishlist}.")

    conn.commit()
    conn.close()

def show_wishlist(wishlist_id=None, wishlist_name=None, sort="name"):
    """
    Mostra todos os jogos de uma wishlist específica (apenas ID e Nome).

    Args:
        wishlist_id (int, optional): ID da wishlist.
        wishlist_name (str, optional): Nome da wishlist.
        sort (str, optional): Atributo para ordenar os jogos (default="name").
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    valid_columns = ["id_game", "name"]
    if sort not in valid_columns:
        sort = "name"

    # escolher a wishlist
    if wishlist_id:
        cur.execute("SELECT name FROM wishList WHERE id_wishList = ?", (wishlist_id,))
        row = cur.fetchone()
        if not row:
            print(f"Wishlist com ID {wishlist_id} não encontrada.")
            conn.close()
            return
        wishlist_name = row[0]
    elif wishlist_name:
        cur.execute("SELECT id_wishList FROM wishList WHERE name = ?", (wishlist_name,))
        row = cur.fetchone()
        if not row:
            print(f"Wishlist '{wishlist_name}' não encontrada.")
            conn.close()
            return
        wishlist_id = row[0]
    else:
        print("Deve fornecer wishlist_id ou wishlist_name.")
        conn.close()
        return

    # buscar os jogos da wishlist
    cur.execute(f"""
        SELECT g.id_game, g.name
        FROM wishlist_game wg
        JOIN game g ON wg.id_game = g.id_game
        WHERE wg.id_wishList = ?
        ORDER BY g.{sort}
    """, (wishlist_id,))

    jogos = cur.fetchall()
    if not jogos:
        print(f"A wishlist '{wishlist_name}' não tem jogos.")
    else:
        print(f"Jogos na wishlist '{wishlist_name}':")
        for jogo in jogos:
            print(f"ID: {jogo[0]} | Nome: '{jogo[1]}'")

    conn.close()


def add_store(name, croped_link):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # verifica se a loja já existe
    cur.execute("SELECT id_store FROM store WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        store_id = row[0]
        print(f"Loja '{name}' já existe com ID {store_id}.")
    else:
        # insere a nova loja
        cur.execute(
            "INSERT INTO store (name, croped_link) VALUES (?, ?)",
            (name, croped_link)
        )
        store_id = cur.lastrowid
        print(f"Loja '{name}' inserida com ID {store_id}.")

    conn.commit()
    conn.close()
    return store_id

def populate_prices_from_wishlist(wishlist_id, scrapers):
    """
    Popula a tabela price com os preços dos jogos de uma wishlist.

    Args:
        wishlist_id (int): ID da wishlist a processar.
        scrapers (dict): dicionário com chave=id_store e valor=function de scraping
                         Cada função recebe id_game e retorna (price, stock)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Obter todos os jogos da wishlist
    cur.execute("""
        SELECT g.id_game, g.name
        FROM wishlist_game wg
        JOIN game g ON wg.id_game = g.id_game
        WHERE wg.id_wishList = ?
    """, (wishlist_id,))
    jogos = cur.fetchall()

    if not jogos:
        print("Wishlist vazia.")
        conn.close()
        return

    # Obter todas as lojas
    cur.execute("SELECT id_store, name FROM store")
    lojas = cur.fetchall()
    if not lojas:
        print("Não há lojas na base de dados.")
        conn.close()
        return

    # Iterar sobre jogos e lojas
    for jogo in jogos:
        id_game, name_game = jogo
        for loja in lojas:
            id_store, loja_name = loja
            scraper_func = scrapers.get(id_store)
            if not scraper_func:
                print(f"Nenhum scraper definido para a loja '{loja_name}'. Ignorado.")
                continue
            try:
                # chamar o scraper: retorna (preco, stock)
                price, stock = scraper_func(id_game)

                # inserir na tabela price
                cur.execute("""
                    INSERT INTO price (id_game, id_store, price, stock, date)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (id_game, id_store, price, stock))

                print(f"{name_game} ({id_game}) | {loja_name}: {price} | {stock}")

            except Exception as e:
                print(f"Erro ao processar {name_game} na loja {loja_name}: {e}")

    conn.commit()
    conn.close()
    print("Preços da wishlist inseridos com sucesso.")


def update_game_urls(id_game, url_saltadacaixa=None, url_gameplaypt=None):
    # Atualiza as URLs de um jogo na tabela game.
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE game
        SET url_saltadacaixa = COALESCE(?, url_saltadacaixa),
            url_gameplaypt = COALESCE(?, url_gameplaypt)
        WHERE id_game = ?
    """, (url_saltadacaixa, url_gameplaypt, id_game))

    if cur.rowcount == 0:
        print(f"Nenhum jogo encontrado com ID {id_game}.")
    else:
        print(f"URLs atualizadas para o jogo ID {id_game}.")

    conn.commit()
    conn.close()


def update_email_user(id_user, email):
    # Atualiza o email de um utilizador na tabela user.
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE user
        SET email = ?
        WHERE id_user = ?
    """, (email, id_user))

    if cur.rowcount == 0:
        print(f"Nenhum user encontrado com ID {id_user}.")
    else:
        print(f"Email atualizadas para o user ID {id_user}.")

    conn.commit()
    conn.close()

def show_table_schema(tabela):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({tabela})")
    for col in cur.fetchall():
        print(col)

    conn.close()

def show_table_data(table_name):
    # Mostra todos os dados de uma tabela específica.
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()

        if not rows:
            print(f"Tabela '{table_name}' está vazia.")
            return

        # nomes das colunas
        column_names = [description[0] for description in cur.description]
        print(" | ".join(column_names))
        print("-" * 80)

        for row in rows:
            print(" | ".join(str(value) for value in row))

    except sqlite3.OperationalError as e:
        print(f"Erro: {e}")

    conn.close()

def clear_table_data(table_name):
    # Limpa todos os dados de uma tabela específica.
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(f"DELETE FROM {table_name}")
    print(f"Todos os dados da tabela '{table_name}' foram removidos.")

    conn.commit()
    conn.close()

def reset_autoincrement(table_name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(f"DELETE FROM {table_name}")
    cur.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))

    print(f"Autoincrement da tabela '{table_name}' foi resetado.")
    conn.commit()
    conn.close()

def get_prices_of_wishlist_games(date_str):
    """
    date_str no formato: 'YYYY-MM-DD'
    exemplo: '2026-02-04'
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.id_game,
            g.name,
            p.id_store,
            p.price,
            p.stock,
            p.date
        FROM price p
        JOIN wishList_game w ON p.id_game = w.id_game
        JOIN game g ON p.id_game = g.id_game
        WHERE DATE(p.date) = ?
        ORDER BY g.name, p.id_store
    """, (date_str,))

    results = cur.fetchall()
    conn.close()
    return results