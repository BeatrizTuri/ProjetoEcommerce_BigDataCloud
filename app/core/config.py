import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Pegar a URL do banco de dados do .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Verifica se a variável foi carregada corretamente
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não está definida no .env!")
