package Questao3.java;

import java.util.function.Function;

public class ErroAtalho {
    public static void main(String[] args) {
        int temperatura_celsius = 40;
        
        Function<Integer, Double> conversor = c -> (c * 1.8) + 32;
        double temperatura_fahrenheit = conversor.apply(temperatura_celsius);
        
        if (temperatura_fahrenheit > 100) {
            System.out.println("Alerta de calor");
        } else {
            System.out.println("Temperatura normal");
        }
    }
}
