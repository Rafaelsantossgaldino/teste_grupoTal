from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Permite requisições entre domínios (se necessário)
from search import buscar_produtos  # Importando a função de busca
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições do frontend

@app.route("/")
def index():
    return render_template("index.html")  # Servindo a página HTML

@app.route("/buscar", methods=["GET"])
def buscar():
    nome_produto = request.args.get("produto")
    preco = request.args.get("preco", type=float)

    if not nome_produto:
        return jsonify({"error": "Informe um produto na URL, exemplo: /buscar?produto=iphone"}), 400

    produtos = buscar_produtos(nome_produto, preco)
    return jsonify(produtos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render define a porta como variável de ambiente
    app.run(host="0.0.0.0", port=port, debug=False)

# if __name__ == "__main__":
#     app.run(debug=True)