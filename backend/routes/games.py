from fastapi import APIRouter, HTTPException
from backend.services.game_service import *
from backend.services.price_service import *

router = APIRouter()

@router.get("/games")
def get_games():
    return get_all_games()

@router.get("/games/{id_game}")
def get_game(id_game: int):

    game = get_game_by_id(id_game)
    if game is None:
        raise HTTPException(status_code=404,detail="Game not found")

    return game

@router.get("/games/{id_game}/prices")
def get_game_prices(id_game: int):
    return get_prices_by_game_id(id_game)