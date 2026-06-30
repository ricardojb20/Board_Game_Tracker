from scrappers.gameplay_pt import get_game_info as digGam
from scrappers.salta_caixa_pt import get_game_info as digSal
from db.database import *

def get_all_games_with_urls():
    # Recupera todos os jogos que possuem URLs para as lojas 
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT id_game,
               url_saltadacaixa,
               url_gameplaypt
        FROM game
        WHERE url_saltadacaixa IS NOT NULL
           OR url_gameplaypt IS NOT NULL
    """)

    games = cur.fetchall()
    conn.close()
    return games

def insert_price(id_game, id_store, price, stock):
    # Insere um novo registro de preço na tabela price.
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO price (id_game, id_store, price, stock)
        VALUES (?, ?, ?, ?)
    """, (id_game, id_store, price, stock))
    conn.commit()
    conn.close()

def populate_prices_for_all_games():
    # Popula a tabela de preços para todos os jogos com URLs disponíveis.
    games = get_all_games_with_urls()  # lista estática no momento da chamada

    for id_game, url_salta, url_gameplay in games:
        # SALTA DA CAIXA
        if url_salta:
            try:
                price, stock = digSal(url_salta)
                insert_price(id_game, 1, price, stock)
            except Exception as e:
                print(f"[Salta da Caixa] Jogo {id_game}: {e}")

        # GAMEPLAY.PT
        if url_gameplay:
            try:
                price, stock = digGam(url_gameplay)
                insert_price(id_game, 2, price, stock)
            except Exception as e:
                print(f"[Gameplay.pt] Jogo {id_game}: {e}")


if __name__ == "__main__":
    populate_prices_for_all_games()