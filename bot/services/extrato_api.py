import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ExtratoAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

    def consultar_extrato_cartoes_por_cpf(self, cpf: str):
        try:
            url = f"{self.base_url}/cartao_de_credito/0/extrato/{cpf}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao consultar extrato de cartões por CPF: {e}")
        return []

    def buscar_usuario_por_cpf(self, cpf: str):
        try:
            url = f"{self.base_url}/usuarios/buscar-id-por-cpf?cpf={cpf}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()  # Espera-se que retorne um dict com pelo menos o campo "id"
        except Exception as e:
            print(f"Erro ao buscar usuário por CPF: {e}")
            return None