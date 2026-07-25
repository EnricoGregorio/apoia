tentativas_falhas = 4
limite_tentativas = 3

assert tentativas_falhas <= limite_tentativas, "Conta bloqueada por segurança"
print("Acesso liberado para nova tentativa")