package Questao4.java;

public class ErroAtalho {
    public static void main(String[] args) {
        int tentativas_falhas = 4;
        int limite_tentativas = 3;
        
        assert tentativas_falhas <= limite_tentativas : "Conta bloqueada por segurança";
        
        System.out.println("Acesso liberado para nova tentativa");
    }
}
