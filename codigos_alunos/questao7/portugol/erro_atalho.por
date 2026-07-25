programa {
	funcao inicio() {
		real capacidade_total_gb = 500.0
		real espaco_ocupado_gb = 420.0
		
		se (espaco_ocupado_gb / capacidade_total_gb > 0.8) {
			escreva("Alerta Crítico: Armazenamento quase cheio")
		} senao {
			escreva("Status do armazenamento: Estável")
		}
	}
}