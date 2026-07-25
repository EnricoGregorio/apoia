package Questao8.java;

public class ErroAtalho {
    public static void main(String[] args) {
        int dias_com_sintomas = 16;
        
        String mensagem = switch (dias_com_sintomas > 14 ? 1 : 0) {
            case 1 -> "Atenção: Encaminhar para exames laboratoriais detalhados";
            default -> "Encaminhar para consulta médica padrão";
        };
        System.out.println(mensagem);
    }
}
