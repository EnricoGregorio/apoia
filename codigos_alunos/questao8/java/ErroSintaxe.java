package Questao8.java;

public class ErroSintaxe {
    public static void main(String[] args) {
        int dias_com_sintomas = 16;
        
        if (dias_com_sintomas > 14) {
            print("Atenção: Encaminhar para exames laboratoriais detalhados");
        } else {
            print("Encaminhar para consulta médica padrão");
        }
    }
}
