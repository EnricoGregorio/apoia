package Questao1.java;

import java.util.Arrays;

public class ErroAtalho {
    public static void main(String[] args) {
        int moedas_coletadas = 12;
        int monstros_derrotados = 3;

        int pontuacao_total = Arrays.stream(new int[]{moedas_coletadas * 10, monstros_derrotados * 50}).sum();
        
        System.out.println("A pontuação total é: " + pontuacao_total);
    }
}
