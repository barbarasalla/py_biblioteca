# Imagem base contendo Python.
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Copia o arquivo de dependências para o container.
#
# Fazemos isso antes de copiar o código para que o Docker
# consiga reutilizar a camada de instalação das dependências
# quando apenas o código da aplicação mudar.
COPY requirements.txt .

# Instala as dependências da aplicação dentro do container.
#
# --no-cache-dir evita armazenar o cache do pip na imagem,
# deixando a imagem menor.
RUN pip install --no-cache-dir -r requirements.txt


# Copia o restante do projeto para dentro do container.
COPY . .

# Documenta a porta utilizada pela aplicação.
EXPOSE 8000

# Comando executado quando o container iniciar.
#
# Usamos python -m para executar o Uvicorn através
# do Python existente dentro do container.
#
# 0.0.0.0 permite que a aplicação seja acessada
# através da porta publicada pelo Docker.
# CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Comentado o CMD que estava iniciando diretamente o Uvicorn
# Adicionado script responsável por preparar o banco e depois iniciar a aplicação.
ENTRYPOINT ["sh", "./entrypoint.sh"]