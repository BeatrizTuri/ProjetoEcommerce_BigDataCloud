import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CompraAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

    def adicionar_ao_carrinho(self, id_usuario: str, item: dict):
        try:
            url = f"{self.base_url}/carrinho/{id_usuario}/adicionar"
            response = requests.post(url, json=item)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao adicionar ao carrinho: {e}")
            return None

    def finalizar_carrinho(self, id_usuario: str, cvv: str = None):
        try:
            url = f"{self.base_url}/carrinho/{id_usuario}/finalizar"
            payload = {"cvv": cvv} if cvv else {}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            try:
                # Tenta extrair mensagem detalhada do backend
                return {"erro": response.json().get("detail", str(e))}
            except Exception:
                return {"erro": str(e)}
        except Exception as e:
            print(f"Erro ao finalizar o carrinho: {e}")
            return {"erro": str(e)}