from scrappers.bgg_info import *
from db.database import *


lista_jogos = [
    {"id": 224517, "url": "https://boardgamegeek.com/boardgame/224517/brass-birmingham"},
    {"id": 329500, "url": "https://boardgamegeek.com/boardgame/329500/unconscious-mind"},
    {"id": 316554, "url": "https://boardgamegeek.com/boardgame/316554/dune-imperium"},
    {"id": 418059, "url": "https://boardgamegeek.com/boardgame/418059/seti-search-for-extraterrestrial-intelligence"},
    {"id": 359871, "url": "https://boardgamegeek.com/boardgame/359871/arcs"},
    {"id": 175640, "url": "https://boardgamegeek.com/boardgame/175640/vinhos-deluxe-edition"},
    {"id": 237179, "url": "https://boardgamegeek.com/boardgame/237179/weather-machine"}
]

create_db()

conn, cur = connect_db()

for jogo in lista_jogos:
    try:
        # obtém info via scraper
        name,year,rank,rating,weight,image_path = get_bgg_info(jogo["url"], jogo["id"])
        
        # prepara tupla para a BD
        game_data = (jogo["id"], name, year, rank, rating, weight, image_path)
        
        # insere na BD
        insert_game(cur, game_data)
        print(f"Jogo {name} inserido com sucesso.")
        
    except Exception as e:
        print(f"Erro ao processar {jogo['url']}: {e}")

conn.commit()
conn.close()