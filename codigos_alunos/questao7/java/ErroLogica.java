package Questao7.java;

public class ErroLogica {
    public static void main(String[] args) {
        int capacidade_total_gb = 500;
        int espaco_ocupado_gb = 420;
        
        int porcentagem_ocupada = capacidade_total_gb / espaco_ocupado_gb * 100;
        
        if (porcentagem_ocupada > 80) {
            System.out.println("Alerta Crítico: Armazenamento quase cheio");
        } else {
            System.out.println("Status do armazenamento: Estável");
        }
    }
}
