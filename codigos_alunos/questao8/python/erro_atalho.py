dias_com_sintomas = 16  

respostas = {
    True: "Atenção: Encaminhar para exames laboratoriais detalhados", 
    False: "Encaminhar para consulta médica padrão"
}
print(respostas[dias_com_sintomas > 14])