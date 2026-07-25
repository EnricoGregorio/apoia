package Questao1.java;

public class ErroLogica {
    public static void main(String[] args) {
        int moedas_coletadas = 12;
        int monstros_derrotados = 3;
        
        int pontuacao_total = (moedas_coletadas + monstros_derrotados) * 60;
        
        System.out.println("A pontuação total é: " + pontuacao_total);
    }
}