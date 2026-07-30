from typing import Any

"""
Módulo que define a interface padrão para os analisadores sintáticos e léxicos.
Implementa o Padrão Strategy para garantir que todas as linguagens suportadas
pelo sistema possuam a mesma estrutura de orquestração.
"""

class AnalisadorBase:
    """
    Classe abstrata.
    
    Atua como um molde para o sistema. Garante que qualquer novo analisador 
    adicionado ao Motor Híbrido (ex: Python, Java, Portugol, C++) implemente 
    obrigatoriamente o método 'analisar', permitindo o uso do polimorfismo 
    pelo AvaliadorIA.
    """

    def analisar(self, codigo: str, config: dict[str, Any]) -> str:
        """
        Método de execução da análise. Deve ser sobrescrito pelas subclasses
        para aplicar as regras de varredura específicas de cada linguagem.
        
        Args:
            codigo (str): O código-fonte bruto fornecido pelo aluno.
            config (dict): O dicionário contendo as regras de bloqueio (ex: proibir_loops).
        
        Returns:
            str: "SUCESSO" ou o log formatado das violações detectadas.
            
        Raises:
            NotImplementedError: Se a classe herdeira esquecer de implementar este método.
        """
        
        raise NotImplementedError("O método 'analisar' deve ser implementado nas subclasses.")
