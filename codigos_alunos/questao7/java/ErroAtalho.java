package Questao7.java;

public class ErroAtalho {
    public static void main(String[] args) {
        double capacidade_total_gb = 500.0;
        double espaco_ocupado_gb = 420.0;
        
        if ((espaco_ocupado_gb / capacidade_total_gb) > 0.8) {
            System.out.printf("Ocupado: %.0f%%. Alerta Crítico!\n", (espaco_ocupado_gb / capacidade_total_gb) * 100);
        } else {
            System.out.println("Status do armazenamento: Estável");
        }
    }
}
