programa {
	funcao inicio() {
		inteiro ano_nascimento = 2005
		inteiro ano_atual = 2026
		
		inteiro idade = ano_nascimento - ano_atual
		
		se (idade >= 18) {
			escreva("Acesso permitido")
		} senao {
			escreva("Acesso negado")
		}
	}
}