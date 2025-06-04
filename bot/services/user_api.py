import os
import requests
from dotenv import load_dotenv

load_dotenv()

class UserAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

    def buscar_usuario_por_cpf(self, cpf: str):
        try:
            url = f"{self.base_url}/usuario/cpf/{cpf}"
            response = requests.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
