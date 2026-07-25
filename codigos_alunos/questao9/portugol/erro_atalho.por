programa {
	inclua biblioteca Matematica --> mat
	
	funcao inicio() {
		inteiro inscritos_confirmados = 120
		inteiro capacidade_auditorio = 80
		inteiro cadeiras_extras_disponiveis = 20
		
		inteiro capacidade_total = capacidade_auditorio + cadeiras_extras_disponiveis
		
		inteiro sobra = inscritos_confirmados - capacidade_total
		
		se (sobra > 0) {
			escreva("Evento lotado. Pessoas na lista de espera: ", mat.valor_absoluto(sobra))
		} senao {
			escreva("Lotação controlada. Evento pronto para iniciar")
		}
	}
}