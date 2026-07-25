programa {
	funcao inicio() {
		inteiro ano_nascimento = 2005
		inteiro ano_atual = 2026
		inteiro idade = ano_atual - ano_nascimento
		
		logico maior_de_idade = idade >= 18
		
		se (maior_de_idade == verdadeiro) {
			escreva("Acesso permitido")
		} senao {
			escreva("Acesso negado")
		}
	}
}