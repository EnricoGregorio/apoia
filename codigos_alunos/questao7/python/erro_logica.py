capacidade_total_gb = 500
espaco_ocupado_gb = 420

porcentagem_ocupada = capacidade_total_gb / espaco_ocupado_gb * 100

if porcentagem_ocupada > 80:
    print("Alerta Crítico: Armazenamento quase cheio")
else:
    print("Status do armazenamento: Estável")