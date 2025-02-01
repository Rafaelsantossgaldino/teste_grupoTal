import unittest
from unittest.mock import patch, MagicMock
from search import buscar_produtos

class TestBuscarProdutos(unittest.TestCase):
    
    @patch("search.requests.get")  # Mockando a requisição HTTP
    @patch("search.get_mongo_collection")  # Mockando a conexão com o MongoDB
    def test_buscar_produtos(self, mock_get_mongo, mock_requests_get):
        # Simulando a resposta HTML do Buscapé
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.text = """
        <a data-testid='product-card::card' href='/produto-123'>
            <h2 data-testid='product-card::name'>Produto Teste</h2>
            <p data-testid='product-card::price'>R$ 100,00</p>
        </a>
        """

        # Simulando a conexão com o MongoDB
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_get_mongo.return_value = (mock_client, mock_collection)

        # Simulando a verificação do banco de dados (produto não existente)
        mock_collection.find_one.return_value = None
        mock_collection.insert_one.return_value.inserted_id = "fake_id"

        # Chamando a função com um produto fictício
        resultado = buscar_produtos("produto teste")

        # Verificações
        self.assertEqual(len(resultado), 1)  # Deve retornar um produto
        self.assertEqual(resultado[0]["titulo"], "Produto Teste")
        self.assertEqual(resultado[0]["preco"], 100.00)
        self.assertIn("https://www.buscape.com.br/produto-123", resultado[0]["link"])

if __name__ == "__main__":
    unittest.main()