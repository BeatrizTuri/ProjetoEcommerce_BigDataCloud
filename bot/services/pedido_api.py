import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class PedidoAPI:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
        
    def consultar_pedido_por_cpf(self, cpf: str):
        try:
            # Passo 1: buscar o ID do usuário pelo CPF
            url_id = f"{self.base_url}/usuarios/buscar-id-por-cpf"
            params_id = {"cpf": cpf}
            response_id = requests.get(url_id, params=params_id)
            response_id.raise_for_status()

            usuario_id = response_id.json().get("id_usuario")
            if not usuario_id:
                print("ID de usuário não encontrado para o CPF fornecido.")
                return []

            # Passo 2: consultar os pedidos com o ID obtido
            url_pedidos = f"{self.base_url}/pedidos/search"
            params_pedidos = {"usuario_id": usuario_id}
            response_pedidos = requests.get(url_pedidos, params=params_pedidos)
            if response_pedidos.status_code == 404:
                return []
            response_pedidos.raise_for_status()
            return response_pedidos.json()

        except Exception as e:
            print(f"Erro ao consultar extrato por CPF: {e}")
            return []
        
    def buscar_id_por_cpf(self, cpf: str):
        try:
            url = f"{self.base_url}/usuarios/buscar-id-por-cpf"
            params = {"cpf": cpf}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get("id_usuario")
        except Exception as e:
            print(f"Erro ao buscar ID por CPF: {e}")
            return None
        
    def consultar_pedido_por_id(self, pedido_id: str):
        try:
            url = f"{self.base_url}/pedidos/{pedido_id}"
            response = requests.get(url)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao consultar pedido por ID: {e}")
            return None