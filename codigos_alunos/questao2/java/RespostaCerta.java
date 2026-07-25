package Questao2.java;

public class RespostaCerta {
	public static void main(String[] args) {
		int ano_nascimento = 2005;
		int ano_atual = 2026;
		int idade = ano_atual - ano_nascimento;
		
		if (idade >= 18) {
			System.out.println("Acesso permitido");
		} else {
			System.out.println("Acesso negado");
		}
	}
}
