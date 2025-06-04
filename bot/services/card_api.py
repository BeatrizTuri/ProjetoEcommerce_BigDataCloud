import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CardAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

    def listar_cartoes_por_usuario(self, id_usuario: int):
        try:
            url = f"{self.base_url}/cartao/usuario/{id_usuario}"
            response = requests.get(url)
            if response.status_code == 404:
                return []
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar cartões: {e}")
            return []
