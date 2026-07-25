programa {
	funcao inicio() {
		inteiro temperatura_celsius = 40
		
		real temperatura_fahrenheit = temperatura_celsius * 1,8 + 32
		
		se (temperatura_fahrenheit > 100) {
			escreva("Alerta de calor")
		} senao {
			escreva("Temperatura normal")
		}
	}
}