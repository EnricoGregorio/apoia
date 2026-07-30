import re
from typing import Any
from .analisador_base import AnalisadorBase

"""
Módulo responsável pela análise léxica de pseudocódigo em Portugol.
Baseado nas especificações do Portugol Web Studio e VisuAlg.
"""

class AnalisadorPortugol(AnalisadorBase):
    """
    Analisador léxico baseado em Expressões Regulares.
    
    Como o Portugol não possui suporte nativo à geração de Árvores Sintáticas
    no ecossistema Python, esta classe atua validando a presença e o formato 
    de tokens léxicos chave para garantir as restrições didáticas.
    """
    
    def _limpar_comentarios(self, codigo: str) -> str:
        # Remove comentários de linha (//) e de bloco (/* */).
        codigo_sem_linha: str = re.sub(r'//.*', '', codigo)
        codigo_limpo: str = re.sub(r'/\*.*?\*/', '', codigo_sem_linha, flags=re.DOTALL)
        return codigo_limpo

    def _verificar_loops(self, codigo: str) -> list[str]:
        violacoes: list[str] = []
        if re.search(r'\b(enquanto|faca)\b', codigo, re.IGNORECASE):
            violacoes.append("Uso de laço 'ENQUANTO/FACA'")
        if re.search(r'\bpara\b', codigo, re.IGNORECASE):
            violacoes.append("Uso de laço 'PARA'")
        return violacoes

    def _verificar_condicionais(self, codigo: str) -> list[str]:
        violacoes: list[str] = []
        if re.search(r'\b(se|senao)\b', codigo, re.IGNORECASE):
            violacoes.append("Uso de condicional 'SE/SENAO'")
        if re.search(r'\b(escolha|caso)\b', codigo, re.IGNORECASE):
            violacoes.append("Uso de condicional 'ESCOLHA/CASO'")
        return violacoes

    def _verificar_importacoes(self, codigo: str) -> list[str]:
        violacoes: list[str] = []
        # Captura "inclua biblioteca NomeDaBiblioteca".
        if re.search(r'\binclua\s+biblioteca\b', codigo, re.IGNORECASE):
            violacoes.append("Uso proibido de importação ('inclua biblioteca')")
        return violacoes

    def _verificar_recursao(self, codigo: str) -> list[str]:
        # Busca declarações de funções: funcao inteiro calcular() ou funcao calcular()).
        # O (?:...) é um grupo não capturante para ignorar o tipo de retorno, capturando apenas o nome.
        funcoes: list[str] = re.findall(r'\bfuncao\s+(?:\w+\s+)?([a-zA-Z_]\w*)\s*\(', codigo, re.IGNORECASE)
        
        for func in funcoes:
            # Conta quantas vezes 'nome_da_funcao(' aparece. 
            # 1 vez = a própria declaração. >1 vez = a função está chamando a si mesma ou sendo chamada no 'inicio'.
            # Como no Portugol tudo começa na funcao 'inicio', chamadas fora do escopo principal configuram alerta.
            ocorrencias: list[str] = re.findall(rf'\b{func}\s*\(', codigo, re.IGNORECASE)
            if len(ocorrencias) > 1 and func.lower() != "inicio":
                return ["Uso de Recursividade"]
        return []

    def _verificar_funcoes_prontas(self, codigo: str, lista_proibida: list[str]) -> list[str]:
        violacoes: list[str] = []
        for func in lista_proibida:
            # Trata funções de biblioteca e funções nativas.
            padrao = rf'\b{func.replace(".", r"\.")}\s*\('
            if re.search(padrao, codigo, re.IGNORECASE):
                violacoes.append(f"Uso da função proibida '{func}()'")
        return violacoes

    def analisar(self, codigo: str, config: dict[str, Any]) -> str:
        try:
            codigo_limpo: str = self._limpar_comentarios(codigo)
            relatorio_erros: list[str] = []

            if config.get("proibir_loops", False):
                relatorio_erros.extend(self._verificar_loops(codigo_limpo))

            if config.get("proibir_condicionais", False):
                relatorio_erros.extend(self._verificar_condicionais(codigo_limpo))
                
            if config.get("proibir_importacoes", False):
                relatorio_erros.extend(self._verificar_importacoes(codigo_limpo))
                
            if config.get("proibir_recursao", False):
                relatorio_erros.extend(self._verificar_recursao(codigo_limpo))
                
            proibidas: list[str] = config.get("proibir_funcoes_prontas", [])
            if proibidas:
                relatorio_erros.extend(self._verificar_funcoes_prontas(codigo_limpo, proibidas))

            if not relatorio_erros:
                return "SUCESSO"
            
            return "VIOLAÇÕES DETECTADAS: " + ", ".join(set(relatorio_erros))

        except Exception as e:
            return f"ERRO NO ANALISADOR PORTUGOL: {str(e)}"
