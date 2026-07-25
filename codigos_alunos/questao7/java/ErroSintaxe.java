package Questao7.java;

public class ErroSintaxe {
    public static void main(String[] args) {
        int capacidade_total_gb = 500;
        int espaco_ocupado_gb = 420;
        int porcentagem_ocupada = espaco_ocupado_gb / capacidade_total_gb * 100;
        
        if (porcentgem_ocupada > 80) { 
            System.out.println("Alerta Crítico: Armazenamento quase cheio");
        } else {
            System.out.println("Status do armazenamento: Estável");
        }
    }
}
