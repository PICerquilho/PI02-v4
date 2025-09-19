# Use uma imagem base oficial do Python para garantir um ambiente consistente.
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Copie o arquivo de requisitos e instale todas as bibliotecas.
# `--no-cache-dir` otimiza o tamanho final da imagem.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o resto do seu projeto para o contêiner.
COPY . .

# Exponha a porta 8000 para que o servidor possa ser acessado de fora do contêiner.
EXPOSE 8000

# Defina o comando que será executado quando o contêiner for iniciado.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]