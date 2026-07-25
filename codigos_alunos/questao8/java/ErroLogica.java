package Questao8.java;

public class ErroLogica {
    public static void main(String[] args) {
        int dias_com_sintomas = 16;
        
        if (dias_com_sintomas >= 14) {
            System.out.println("Atenção: Encaminhar para exames laboratoriais detalhados");
        } else {
            System.out.println("Encaminhar para consulta médica padrão");
        }
    }
}
