from typing import Any
from javalang import tree, parse, parser, tokenizer
from .analisador_base import AnalisadorBase

"""
Módulo responsável pela análise estática de códigos em Java.
Utiliza a biblioteca 'javalang' para parsear o código e validar restrições pedagógicas.
"""

class AnalisadorJava(AnalisadorBase):
    """
    Analisador sintático para Java.
    
    Implementa a varredura estrutural buscando por nós específicos do Java,
    como declarações de métodos, loops, expressões de importação e condicionais.
    """
    
    def _verificar_loops(self, ast_tree: Any) -> list[str]:
        violacoes: list[str] = []
        if list(ast_tree.filter(tree.WhileStatement)) or list(ast_tree.filter(tree.DoStatement)):
            violacoes.append("Uso de laço 'WHILE/DO-WHILE'")
        if list(ast_tree.filter(tree.ForStatement)):
            violacoes.append("Uso de laço 'FOR'")
        return violacoes

    def _verificar_recursao(self, ast_tree: Any) -> list[str]:
        nomes_metodos: list[str] = [node.name for path, node in ast_tree.filter(tree.MethodDeclaration)]
        for path, node in ast_tree.filter(tree.MethodInvocation):
            if node.member in nomes_metodos:
                return ["Uso de Recursividade"]
        return []

    def _verificar_funcoes_prontas(self, ast_tree: Any, lista_proibida: list[str]) -> list[str]:
        violacoes: list[str] = []
        for path, node in ast_tree.filter(tree.MethodInvocation):
            if node.member in lista_proibida:
                violacoes.append(f"Uso da função proibida '{node.member}()'")
        return violacoes

    def _verificar_condicionais(self, ast_tree: Any) -> list[str]:
        violacoes: list[str] = []
        if list(ast_tree.filter(tree.IfStatement)):
            violacoes.append("Uso de condicional 'IF'")
        if list(ast_tree.filter(tree.SwitchStatement)):
            violacoes.append("Uso de condicional 'SWITCH'")
        return violacoes

    def _verificar_importacoes(self, ast_tree: Any) -> list[str]:
        violacoes: list[str] = []
        if list(ast_tree.filter(tree.Import)):
            violacoes.append("Uso proibido de importação ('import')")
        return violacoes

    def analisar(self, codigo: str, config: dict[str, Any]) -> str:
        try:
            # Transforma a string de texto na Árvore Sintática usando os submódulos importados
            ast_tree = parse.parse(codigo)
            relatorio_erros: list[str] = []

            if config.get("proibir_loops", False):
                relatorio_erros.extend(self._verificar_loops(ast_tree))

            proibidas: list[str] = config.get("proibir_funcoes_prontas", [])
            if proibidas:
                relatorio_erros.extend(self._verificar_funcoes_prontas(ast_tree, proibidas))

            if config.get("proibir_recursao", False):
                relatorio_erros.extend(self._verificar_recursao(ast_tree))

            if config.get("proibir_condicionais", False):
                relatorio_erros.extend(self._verificar_condicionais(ast_tree))
                
            if config.get("proibir_importacoes", False):
                relatorio_erros.extend(self._verificar_importacoes(ast_tree))

            if not relatorio_erros:
                return "SUCESSO"
            
            return "VIOLAÇÕES DETECTADAS: " + ", ".join(set(relatorio_erros))

        # Captura os erros usando os módulos explícitos
        except (parser.JavaSyntaxError, tokenizer.LexerError):
            return "ERRO CRÍTICO: Código com erro de sintaxe (não compila)."
        except Exception as e:
            return f"ERRO NO ANALISADOR JAVA: {str(e)}"
