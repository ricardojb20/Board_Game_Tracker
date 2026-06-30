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

    product_block = soup.select_one("div.details-info")

    #STOCK
    stock_tag = product_block.select_one("div.pr-availability").select_one("span")
    stock = stock_tag.get_text(strip=True) 
    if stock == "Indisponível":
        return 0,stock

    #PREÇO
    price_tag = soup.select_one("span#js-product-price.price")
    if price_tag:
        preco_text = price_tag.get_text(strip=True)
        preco = float(preco_text.replace("€", "").replace(",", "."))
    else:
        preco = None

    return preco,stock
