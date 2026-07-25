programa {
	funcao inicio() {
		inteiro dias_com_sintomas = 16
		
		inteiro status = 0
		se (dias_com_sintomas > 14) { status = 1 }
		
		escolha (status) {
			caso 1: 
				escreva("Atenção: Encaminhar para exames laboratoriais detalhados")
				pare
			caso 0: 
				escreva("Encaminhar para consulta médica padrão")
				pare
		}
	}
}