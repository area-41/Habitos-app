# 1. Usa uma imagem oficial leve do Python
FROM python:3.10-slim

# 2. Define o diretório de trabalho dentro do servidor
WORKDIR /app

# 3. Instala dependências do sistema necessárias para o Flet rodar no Linux
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia os arquivos de requerimentos e instala as bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o restante do código do seu projeto para o servidor
COPY . .

# 6. Expõe a porta padrão do Render (10000)
EXPOSE 10000

# 7. Comando que inicia o app
CMD ["python", "habitos_app.py"]