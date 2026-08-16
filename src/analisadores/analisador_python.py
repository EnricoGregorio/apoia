import ast
from typing import Any
from .analisador_base import AnalisadorBase

"""
Módulo responsável pela análise estática de códigos em Python.
Utiliza a biblioteca nativa 'ast' para validar restrições pedagógicas 
sem executar o código do aluno.
"""

class AnalisadorPython(AnalisadorBase):
    """
    Analisador sintático para Python. 
    
    Herda o contrato de AnalisadorBase e implementa a varredura dos nós
    da Árvore Sintática Abstrata do Python para 
    detectar violações de regras estruturais.
    """

    def _verificar_loops(self, tree: ast.AST) -> list[str]:
        violacoes: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.While): violacoes.append("Uso de laço 'WHILE'")
            if isinstance(node, ast.For): violacoes.append("Uso de laço 'FOR'")
        return violacoes

    def _verificar_recursao(self, tree: ast.AST) -> list[str]:
        nomes_funcoes: list[str] = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in nomes_funcoes: return ["Uso de Recursividade"]
        return []

    def _verificar_funcoes_prontas(self, tree: ast.AST, lista_proibida: list[str]) -> list[str]:
        violacoes: list[str] = []
        for node in ast.walk(tree):
            nome = None
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name): nome = node.func.id
                elif isinstance(node.func, ast.Attribute): nome = node.func.attr
            if nome and nome in lista_proibida:
                violacoes.append(f"Uso da função proibida '{nome}()'")
        return violacoes

    # Método para bloquear if, elif, else e match/case
    def _verificar_condicionais(self, tree: ast.AST) -> list[str]:
        violacoes: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                violacoes.append("Uso de condicional 'IF'")
            # Validação para Python 3.10+ (match/case)
            elif hasattr(ast, 'Match') and isinstance(node, getattr(ast, 'Match')):
                violacoes.append("Uso de condicional 'MATCH/CASE'")
        return violacoes

    # Método para bloquear importação de bibliotecas prontas (import math, etc).
    def _verificar_importacoes(self, tree: ast.AST) -> list[str]:
        violacoes: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                violacoes.append("Uso proibido de importação ('import')")
        return violacoes

    def analisar(self, codigo: str, config: dict[str, Any]) -> str:
        try:
            tree: ast.AST = ast.parse(codigo)
            relatorio_erros: list[str] = []

            if config.get("proibir_loops", False):
                relatorio_erros.extend(self._verificar_loops(tree))

            proibidas: list[str] = config.get("proibir_funcoes_prontas", [])
            if proibidas:
                relatorio_erros.extend(self._verificar_funcoes_prontas(tree, proibidas))

            if config.get("proibir_recursao", False):
                relatorio_erros.extend(self._verificar_recursao(tree))

            # Disparo das novas regras de acordo com o rubrica.json
            if config.get("proibir_condicionais", False):
                relatorio_erros.extend(self._verificar_condicionais(tree))
                
            if config.get("proibir_importacoes", False):
                relatorio_erros.extend(self._verificar_importacoes(tree))

            if not relatorio_erros:
                return "SUCESSO"
            
            return "ele detectou as seguintes violações presentes no código: " + ", ".join(set(relatorio_erros))

        except SyntaxError:
            return "O código possui erro de sintaxe, portanto não pôde ser compilado."
        except Exception as e:
            return f"ERRO NO ANALISADOR: {str(e)}"
