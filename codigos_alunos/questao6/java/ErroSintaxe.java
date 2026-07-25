package Questao6.java;

public class ErroSintaxe {
    public static void main(String[] args) {
        int numero_secreto = 42;
        
        if (numero_secreto % 2 = 0) {
            System.out.println("O número é par");
        } else {
            System.out.println("O número é ímpar");
        }
    }
}
