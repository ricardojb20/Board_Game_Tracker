from backend.database import get_connection

BASE_URL = "http://127.0.0.1:8000"


def add_image_url(game: dict):
    if game["image_path"]:
        filename = game["image_path"].replace("\\", "/").split("/")[-1]
        game["image_url"] = f"{BASE_URL}/images/{filename}"
    else:
        game["image_url"] = None

    del game["image_path"]
    return game


def get_all_games():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_game, name, year, rank, rating, weight, image_path
        FROM game
        ORDER BY rank
    """)

    games = [add_image_url(dict(row)) for row in cursor.fetchall()]

    conn.close()
    return games


def get_game_by_id(game_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_game, name, year, rank, rating, weight, image_path
        FROM game
        WHERE id_game = ?
    """, (game_id,))

    row = cursor.fetchone()
    conn.close()
    if row is None: return None

    return add_image_url(dict(row))