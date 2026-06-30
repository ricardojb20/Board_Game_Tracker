from bs4 import BeautifulSoup
import requests
import re
import os

def download_image(img_url, game_id, folder="images"):
    """
    Descarrega a imagem de um jogo e guarda localmente de forma organizada.
    
    Args:
        img_url (str): URL da imagem.
        game_id (int/str): ID único do jogo, usado como nome do ficheiro.
        folder (str): Pasta base para guardar imagens.
        
    Returns:
        str: Caminho relativo do ficheiro salvo, ou None se falhar.
    """
    if not img_url:
        return None

    # cria a pasta base se não existir
    os.makedirs(folder, exist_ok=True)

    # extrai a extensão do ficheiro da URL
    ext = img_url.split(".")[-1].split("?")[0]  # remove query
    filename = f"{game_id}.{ext}"
    path = os.path.join(folder, filename)

    # se já existir, não descarrega novamente
    if os.path.exists(path):
        return path

    try:
        r = requests.get(img_url, timeout=10)
        r.raise_for_status()

        with open(path, "wb") as f:
            f.write(r.content)

        return path

    except Exception as e:
        print(f"Erro ao descarregar {img_url}: {e}")
        return None



def get_bgg_info(bgg_url,id_game):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(bgg_url, headers=headers)
    response.raise_for_status()
    
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.content, "html.parser")
    html = response.text

    # ----- NOME -----
    name_match = re.search(r'<title>(.*?)\s*\|', html)
    name = name_match.group(1) if name_match else None

    # ----- ANO -----
    year_match = re.search(r'"yearpublished"\s*:\s*"([0-9]{4})"',html)
    year = int(year_match.group(1)) if year_match else None
    
    # ----- RATING -----
    rating_match = re.search(r'"average"\s*:\s*"([0-9.]+)"', html)
    rating = float(rating_match.group(1)) if rating_match else None

    # ----- PESO -----
    weight_match = re.search(r'"avgweight"\s*:\s*"([0-9.]+)"', html)
    weight = float(weight_match.group(1)) if weight_match else None

    # ----- RANK -----
    rank_match = re.search(r'"rank"\s*:\s*"([0-9]+)"', html)
    rank = int(rank_match.group(1)) if rank_match else None

    # ----- IMAGEM -----
    link_tags = soup.find_all("link", rel="preload")
    image_url = None
    for link in link_tags:
        href = link.get("href", "")
        if "fit-in/246x300" in href:
            image_url = href
            break
    image_path = download_image(image_url,id_game)

    return name,year,rank,rating,weight,image_path

