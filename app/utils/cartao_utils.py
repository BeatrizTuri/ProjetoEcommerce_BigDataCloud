from datetime import date

def autorizar_cartao_compra(cartao, valor):
    if cartao.dtExpiracao < date.today():
        return False, "Cartão expirado."
    if cartao.saldo < valor:
        return False, "Sem saldo para realizar a compra."
    return True, "Compra autorizada."