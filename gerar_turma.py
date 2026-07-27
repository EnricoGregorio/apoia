import os
import random

def gerar_turma():
    # Define o caminho da pasta espelhando a estrutura do orquestrador
    pasta_destino = os.path.join("codigos_alunos", "questao2", "python")
    
    # Cria a pasta caso ela não exista
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Modelos de códigos (comportamentos mapeados no nosso RAG e comportamentos inéditos)
    modelos = [
        # 1. Correto (Nota 10)
        "ano_nascimento = 2005\nano_atual = 2026\nidade = ano_atual - ano_nascimento\n\nif idade >= 18:\n    print('Acesso permitido')\nelse:\n    print('Acesso negado')\n",
        
        # 2. Erro de Lógica (Nota 4) - Subtração invertida
        "ano_nascimento = 2005\nano_atual = 2026\nidade = ano_nascimento - ano_atual\n\nif idade >= 18:\n    print('Acesso permitido')\nelse:\n    print('Acesso negado')\n",
        
        # 3. Erro de Sintaxe (Nota 0) - Faltando os dois pontos no if
        "ano_nascimento = 2005\nano_atual = 2026\nidade = ano_atual - ano_nascimento\n\nif idade >= 18\n    print('Acesso permitido')\nelse:\n    print('Acesso negado')\n",
        
        # 4. Uso de Atalho (Nota 5) - Operador Ternário
        "ano_nascimento = 2005\nano_atual = 2026\nidade = ano_atual - ano_nascimento\n\nprint('Acesso permitido' if idade >= 18 else 'Acesso negado')\n",
        
        # 5. Erro Inédito de Runtime - Chamando variável que não existe (Falta declarar 'idade')
        "ano_nascimento = 2005\nano_atual = 2026\n\nif idade >= 18:\n    print('Acesso permitido')\nelse:\n    print('Acesso negado')\n",
        
        # 6. Correto Inédito - Nomes de variáveis diferentes (Para testar se a IA generaliza o conceito)
        "nascimento = 2005\nhoje = 2026\ncalculo = hoje - nascimento\n\nif calculo >= 18:\n    print('Acesso permitido')\nelse:\n    print('Acesso negado')\n"
    ]

    print(f"Gerando 30 alunos na pasta: {pasta_destino}...")

    # Gera 30 arquivos aleatórios
    for i in range(1, 31):
        nome_arquivo = f"aluno_{i:02d}.py"
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
        codigo_escolhido = random.choice(modelos)
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(codigo_escolhido)

    print("✅ Turma gerada com sucesso! Você já pode rodar o 'python src/main.py'.")

if __name__ == "__main__":
    gerar_turma()