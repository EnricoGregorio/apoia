package Questao2.java;

public class ErroAtalho {
    public static void main(String[] args) {
        int ano_nascimento = 2005;
        int ano_atual = 2026;
        int idade = ano_atual - ano_nascimento;
        
        System.out.println(idade >= 18 ? "Acesso permitido" : "Acesso negado");
    }
}
