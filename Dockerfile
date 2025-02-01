FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos necessários
COPY requirements.txt requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Expor a porta
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
