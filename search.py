import requests
from bs4 import BeautifulSoup

def buscar_produtos(nome_produto, preco_max=None, preco_min=None):
    url = f"https://www.buscape.com.br/search?q={nome_produto.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Erro ao acessar o Buscapé: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")
    produtos = []

    for item in soup.select("a[data-testid='product-card::card']"):
        titulo_elem = item.select_one("h2[data-testid='product-card::name']")
        preco_elem = item.select_one("p[data-testid='product-card::price']")
        link_elem = item["href"] if "href" in item.attrs else None

        if titulo_elem and preco_elem and link_elem:
            preco_texto = preco_elem.text.strip().replace("R$", "").replace(".", "").replace(",", ".")

            try:
                preco = float(preco_texto)
            except ValueError:
                continue  # Ignora se o preço não for válido

            # 🔹 Debug para verificar valores
            print(f"Preço encontrado: {preco} | Min: {preco_min} | Max: {preco_max}")

            # 🔹 Aplicando corretamente o filtro de preço
            if preco_min is not None and preco < preco_min:
                continue  # Ignora se o preço for menor que o mínimo definido
            if preco_max is not None and preco > preco_max:
                continue  # Ignora se o preço for maior que o máximo definido

            links_ofertas = []
            for oferta in item.select("a[data-testid='product-card::offer']"):
                link_oferta = oferta["href"] if "href" in oferta.attrs else None
                if link_oferta:
                    links_ofertas.append(f"https://www.buscape.com.br{link_oferta}")

            produtos.append({
                "titulo": titulo_elem.text.strip(),
                "preco": preco,
                "link": f"https://www.buscape.com.br{link_elem}",
                "ofertas": links_ofertas
            })

    if not produtos:
        return {"error": "Nenhum produto encontrado"}

    return produtos
    






