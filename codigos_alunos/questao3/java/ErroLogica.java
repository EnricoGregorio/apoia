package Questao3.java;

public class ErroLogica {
    public static void main(String[] args) {
        int temperatura_celsius = 40;
        
        double temperatura_fahrenheit = temperatura_celsius * (1.8 + 32);
        
        if (temperatura_fahrenheit > 100) {
            System.out.println("Alerta de calor");
        } else {
            System.out.println("Temperatura normal");
        }
    }
}
