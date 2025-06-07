import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class ProductAPI:
    def __init__(self):
        # Remove possível barra no final para evitar problemas em requests
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
        

    def consultar_produtos(self, product_name: str):
        try:
            url = f"{self.base_url}/produtos/search"
            params = {"nome": product_name}
            response = requests.get(url, params=params)
            if response.status_code == 404:
                return []  # Nenhum produto encontrado
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao consultar produtos por nome: {e}")
            return []
        
    


