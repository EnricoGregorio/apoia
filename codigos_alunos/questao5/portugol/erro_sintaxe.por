programa {
	funcao inicio() {
		real valor da compra = 200.0
		
		se (valor da compra > 150.0) {
			real valor_com_desconto = valor da compra - (valor da compra * 0.10)
			escreva("Compra com desconto: ", valor_com_desconto)
		} senao {
			escreva("Valor normal: ", valor da compra)
		}
	}
}