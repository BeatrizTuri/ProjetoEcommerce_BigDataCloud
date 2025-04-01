from pydantic import BaseModel
from decimal import Decimal

class CartaoCreditoUpdateSaldo(BaseModel):
    saldo: Decimal
