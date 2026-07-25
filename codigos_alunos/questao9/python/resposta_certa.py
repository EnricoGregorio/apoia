inscritos_confirmados = 120
capacidade_auditorio = 80
cadeiras_extras_disponiveis = 20

capacidade_total = capacidade_auditorio + cadeiras_extras_disponiveis

if inscritos_confirmados > capacidade_total:
	pessoas_de_fora = inscritos_confirmados - capacidade_total
	print("Evento lotado. Pessoas na lista de espera: ", pessoas_de_fora)
else:
	print("Lotação controlada. Evento pronto para iniciar")