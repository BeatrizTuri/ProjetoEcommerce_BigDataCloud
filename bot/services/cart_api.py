import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CartAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

    def adicionar_ao_carrinho(self, id_usuario: str, id_produto: int, quantidade: int):
        try:
            url = f"{self.base_url}/carrinho/"
            payload = {
                "id_usuario": id_usuario,
                "id_produto": id_produto,
                "quantidade": quantidade
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao adicionar ao carrinho: {e}")
            raise
