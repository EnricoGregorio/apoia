programa {
	funcao inicio() {
		inteiro capacidade_total_gb = 500
		inteiro espaco_ocupado_gb = 420
		
		inteiro porcentagem_ocupada = capacidade_total_gb / espaco_ocupado_gb * 100
		
		se (porcentagem_ocupada > 80) {
			escreva("Alerta Crítico: Armazenamento quase cheio")
		} senao {
			escreva("Status do armazenamento: Estável")
		}
	}
}