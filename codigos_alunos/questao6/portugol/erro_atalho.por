programa {
	inclua biblioteca Tipos --> t
	inclua biblioteca Texto --> txt
	
	funcao inicio() {
		inteiro numero_secreto = 42
		
		cadeia num_texto = t.inteiro_para_cadeia(numero_secreto, 10)
		caracter ultimo_digito = txt.obter_caracter(num_texto, txt.numero_caracteres(num_texto) - 1)
		
		se (ultimo_digito == '0' ou ultimo_digito == '2' ou ultimo_digito == '4' ou ultimo_digito == '6' ou ultimo_digito == '8') {
			escreva("O número é par")
		} senao {
			escreva("O número é ímpar")
		}
	}
}