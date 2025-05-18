import requests

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")  # remove barra final, se tiver

    def get_produtos(self):
        url = f"{self.base_url}/produtos/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_pedidos(self):
        url = f"{self.base_url}/pedidos/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_carrinho(self, id_usuario: int):
        url = f"{self.base_url}/carrinho/{id_usuario}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def finalizar_carrinho(self, id_usuario: int):
        url = f"{self.base_url}/carrinho/{id_usuario}/finalizar"
        response = requests.post(url)
        response.raise_for_status()
        return response.json()
