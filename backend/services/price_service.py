from backend.database import get_connection

def get_prices_by_game_id(game_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.id_store,
            s.name AS store,
            p.price,
            p.stock,
            p.date
        FROM price p
        JOIN store s
            ON s.id_store = p.id_store
        WHERE p.id_game = ?
        AND p.date = (
            SELECT MAX(date)
            FROM price
            WHERE id_game = p.id_game
              AND id_store = p.id_store
        )
        ORDER BY p.price ASC;
    """, (game_id,))

    prices = cursor.fetchall()
    conn.close()
    return [dict(price) for price in prices]