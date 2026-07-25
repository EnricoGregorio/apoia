programa {
	funcao inicio() {
		real valor_compra = 200.0
		
		se (valor_compra > 150.0) {
			real valor_com_desconto = valor_compra * 0.90
			escreva("Compra com desconto: ", valor_com_desconto)
		} senao {
			escreva("Valor normal: ", valor_compra)
		}
	}
}