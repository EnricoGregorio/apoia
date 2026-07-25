capacidade_total_gb = 500
espaco_ocupado_gb = 420

if (espaco_ocupado_gb / capacidade_total_gb) > 0.8:
    print(f"O espaço ocupado é {espaco_ocupado_gb / capacidade_total_gb:.0%}. Alerta Crítico!")
else:
    print("Status do armazenamento: Estável")