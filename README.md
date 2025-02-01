# Aplicacao Flask para Busca de Produtos
Este projeto consiste em uma API Flask que busca produtos no site Buscapé e armazena os resultados em um banco de dados MongoDB. A aplicação também inclui um Dockerfile e um arquivo docker-compose.yml para facilitar a implantação.

📌 Tecnologias Utilizadas
- Python 3.10
- Flask
- Flask-CORS
- Requests
- BeautifulSoup (para web scraping)
- MongoDB
- PyMongo
- Dotenv (para variáveis de ambiente)
- Docker
- Docker Compose

Requisitos:
Antes de executar a API, certifique-se de ter:

- Python 3 instalado
- MongoDB rodando localmente ou remotamente
- Um arquivo .env com a variável MONGO_URI configurada

🚀 Instalação
1. Clone o repositório:
   ```sh
    git clone https://github.com/seu-repositorio/api-busca-produtos.git
    cd api-busca-produtos
   ```
2. Crie um ambiente virtual e ative-o:
   ```sh
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```sh
    pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto e adicione sua URI do MongoDB:
 ```sh
    MONGO_URI=mongodb://seu_usuario:senha@host:porta
 ```
Neste caso eu tenho um banco de dados publico no mongo Atlas entao minha url de conexao é:
```sh
   MONGO_URI=mongodb+srv://rafaelsantossgaldino2:Elpxco1HubbSNqeM@cluster7.1agzz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster7
```
🐳 Docker
Construir e Subir os Containers
```sh
  docker-compose up --build
```

▶️ Execução

Para iniciar a API, execute:
 ```sh
   python app.py
 ```
ou
 ```sh
   flask run
 ```
A API rodará por padrão na porta 5000. Se desejar alterar, defina a variável de ambiente PORT.

🔗 Endpoints:

GET /buscar

Busca produtos no Buscapé e retorna uma lista de produtos encontrados.

Parâmetros:
- produto (obrigatório): Nome do produto a ser buscado.
- preco (opcional): Filtra produtos com preço até o valor informado.

Exemplo de Requisição:
 ```sh
   curl "http://localhost:5000/buscar?produto=iphone"
 ```
ou
```sh
   curl "http://localhost:5000/buscar?produto=iphone&preco=4499.99"
 ```
Exemplo de Resposta:
 ```sh
  [
  {
    "titulo": "iPhone 13 128GB",
    "preco": 4499.99,
    "link": "https://www.buscape.com.br/produto/iphone-13",
    "data_criacao": "30/01/2025"
  }
]
 ```

Estrutura do Projeto
```sh
  api-busca-produtos/
|-- app.py  # Servidor Flask
|-- search.py  # Funções de busca e armazenamento no MongoDB
|-- requirements.txt  # Dependências do projeto
|-- Dockerfile  # Configuração do container
|-- docker-compose.yml  # Orquestração dos containers
|-- .env  # Variáveis de ambiente
```
# Na web acesse 
```sh
   http://localhost:5000/
```
![image](https://github.com/user-attachments/assets/4f4bc674-1ae4-47ae-b521-cdcc1c9b9cd2)

Digite o nome do produto e o preço 
![image](https://github.com/user-attachments/assets/d9ba8fc7-9d27-4ca5-8c3c-47d48c6a7283)




📢 Conclusão

Este projeto fornece uma maneira simples e eficiente de buscar produtos no Buscapé, utilizando Flask, MongoDB e Docker para escalabilidade e facilidade de implantação. 🚀
   
