package Questao4.java;

public class ErroLogica {
    public static void main(String[] args) {
        int tentativas_falhas = 4;
        int limite_tentativas = 3;
        
        if (tentativas_falhas <= limite_tentativas) {
            System.out.println("Conta bloqueada por segurança");
        } else {
            System.out.println("Acesso liberado para nova tentativa");
        }
    }
}
