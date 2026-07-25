package Questao5.java;

public class ErroLogica {
    public static void main(String[] args) {
        double valor_compra = 200.0;
        
        if (valor_compra > 150.0) {
            double valor_com_desconto = valor_compra * 0.10;
            System.out.println("Compra com desconto: " + valor_com_desconto);
        } else {
            System.out.println("Valor normal: " + valor_compra);
        }
    }
}
