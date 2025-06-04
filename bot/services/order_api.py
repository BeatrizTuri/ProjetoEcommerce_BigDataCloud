import os
import requests
from dotenv import load_dotenv

load_dotenv()

class OrderAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

    def finalizar_pedido(self, id_usuario: int, id_cartao: int):
        try:
            url = f"{self.base_url}/pedido/"
            payload = {
                "id_usuario": id_usuario,
                "id_cartao": id_cartao
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao finalizar pedido: {e}")
            raise
