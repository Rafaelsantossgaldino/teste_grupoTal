import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis do arquivo .env
load_dotenv()

# Acessar a variável MONGO_URI do arquivo .env
MONGO_URI = os.getenv("MONGO_URI")

def get_mongo_collection():
    """Cria uma conexão com o MongoDB dentro do worker"""
    client = MongoClient(MONGO_URI)
    db = client["gropotal"]  # Nome do banco de dados
    collection = db["produtos"]  # Nome da coleção
    return client, collection  # Retornamos o cliente para fechá-lo depois

def buscar_produtos(nome_produto, preco=None):
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

    # Criar a conexão com o MongoDB dentro do worker
    client, collection = get_mongo_collection()

    try:
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

                produto = {
                    "titulo": titulo_elem.text.strip(),
                    "preco": float(preco),
                    "link": f"https://www.buscape.com.br{link_elem}",
                    "data_criacao": datetime.now().strftime("%d/%m/%Y")
                }

                # Verifica se o produto já existe no banco
                produto_existente = collection.find_one({
                    "titulo": produto["titulo"],
                    "preco": produto["preco"],
                    "link": produto["link"],
                    "data_criacao": produto["data_criacao"]
                })
                
                if not produto_existente:
                    resultado = collection.insert_one(produto)
                    produto["_id"] = str(resultado.inserted_id)

                produtos.append(produto)

    except Exception as e:
        return {"error": str(e)}
    
    finally:
        client.close()  # Fechar a conexão após o uso

    if not produtos:
        return {"error": "Nenhum produto encontrado"}

    return produtos