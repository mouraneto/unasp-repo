# Use uma imagem base Python
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o container
COPY . /app

# Instale dependências se houver requirements.txt
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Exponha a porta usada pelo servidor
EXPOSE 5000

# Comando para iniciar o servidor
CMD ["python", "server.py"]