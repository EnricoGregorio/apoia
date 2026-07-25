package Questao9.java;

public class ErroAtalho {
    public static void main(String[] args) {
        int inscritos_confirmados = 120;
        int capacidade_auditorio = 80;
        int cadeiras_extras_disponiveis = 20;
        
        int capacidade_total = capacidade_auditorio + cadeiras_extras_disponiveis;

        int pessoas_de_fora = Math.max(0, inscritos_confirmados - capacidade_total);
        
        if (pessoas_de_fora > 0) {
            System.out.println("Evento lotado. Pessoas na lista de espera: " + pessoas_de_fora);
        } else {
            System.out.println("Lotação controlada. Evento pronto para iniciar");
        }
    }
}
