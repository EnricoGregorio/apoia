programa {
	funcao inicio() {
		inteiro inscritos_confirmados = 120
		inteiro capacidade_auditorio = 80
		inteiro cadeiras_extras_disponiveis = 20
		
		inteiro capacidade_total = capacidade_auditorio + cadeiras_extras_disponiveis
		
		se (inscritos_confirmados > capacidade_total) {
			inteiro pessoas_de_fora = capacidade_total - inscritos_confirmados
			escreva("Evento lotado. Pessoas na lista de espera: ", pessoas_de_fora)
		} senao {
			escreva("Lotação controlada. Evento pronto para iniciar")
		}
	}
}