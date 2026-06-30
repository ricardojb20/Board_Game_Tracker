import requests
from bs4 import BeautifulSoup

def get_game_info(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.content, "html.parser")

    product_block = soup.select_one("div.product_first_section")

    #PREÇO
    price_tag = product_block.select_one("span.price_product_impuesto")
    preco_txt = price_tag["content"] if price_tag else "Preço não encontrado"
    preco = float(preco_txt)

    #STOCK
    stock_tag = product_block.select_one("span.icon-check")
    if stock_tag is not None:
        stock = "Em Stock"
    else:
        stock_tag = product_block.select_one("span.icon-warning")
        if stock_tag is not None:
            stock = "Em Stock"
        else:
            stock = "Indisponível"
    
    return preco,stock
