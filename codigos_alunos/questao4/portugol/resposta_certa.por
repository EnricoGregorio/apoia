programa {
	funcao inicio() {
		inteiro tentativas_falhas = 4
		inteiro limite_tentativas = 3
		
		se (tentativas_falhas > limite_tentativas) {
			escreva("Conta bloqueada por segurança")
		} senao {
			escreva("Acesso liberado para nova tentativa")
		}
	}
}