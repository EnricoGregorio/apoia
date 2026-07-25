inscritos_confirmados = 120
capacidade_auditorio = 80
cadeiras_extras_disponiveis = 20

capacidade_total = capacidade_auditorio + cadeiras_extras_disponiveis

pessoas_de_fora = max(0, inscritos_confirmados - capacidade_total)

if pessoas_de_fora > 0:
    print("Evento lotado. Pessoas na lista de espera: ", pessoas_de_fora)
else:
    print("Lotação controlada. Evento pronto para iniciar")