import json
import ast
import requests # Para se comunicar com o Ollama via rede.

class AvaliadorIA:
    def __init__(self, nome_modelo):
        print(f">>> Inicializando Motor Híbrido conectado ao Ollama (Modelo: {nome_modelo})...")
        self.modelo = nome_modelo 
        self.url_ollama = "http://localhost:11434/api/generate" 

    def _verificar_loops(self, tree):
        violacoes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.While): violacoes.append("Uso de laço 'WHILE'")
            if isinstance(node, ast.For): violacoes.append("Uso de laço 'FOR'")
        return violacoes

    def _verificar_recursao(self, tree):
        nomes_funcoes = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in nomes_funcoes: return [] 
        return []

    def _verificar_funcoes_prontas(self, tree, lista_proibida):
        violacoes = []
        for node in ast.walk(tree):
            nome = None
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name): nome = node.func.id
                elif isinstance(node.func, ast.Attribute): nome = node.func.attr
            if nome and nome in lista_proibida:
                violacoes.append(f"Uso da função proibida '{nome}()'")
        return violacoes

    def _analise_estatica_dinamica(self, codigo, config):
        try:
            tree = ast.parse(codigo)
            relatorio_erros = []

            if config.get("proibir_loops", False):
                erros = self._verificar_loops(tree)
                if erros: relatorio_erros.extend(erros)

            proibidas = config.get("proibir_funcoes_prontas", [])
            if proibidas:
                erros = self._verificar_funcoes_prontas(tree, proibidas)
                if erros: relatorio_erros.extend(erros)

            if config.get("proibir_recursao", False):
                nomes_funcoes = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                recursivo = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        if node.func.id in nomes_funcoes: recursivo = True
                if recursivo: relatorio_erros.append("Uso de Recursividade")

            if not relatorio_erros:
                return "SUCESSO"
            
            return "VIOLAÇÕES DETECTADAS: " + ", ".join(set(relatorio_erros))

        except SyntaxError:
            return "ERRO CRÍTICO: Código com erro de sintaxe (não compila)."
        except Exception as e:
            return f"ERRO NO ANALISADOR: {str(e)}"

    def avaliar(self, enunciado, rubrica, codigo_aluno):
        config_ast = rubrica.get("configuracao_ast", {})
        relatorio_ast = self._analise_estatica_dinamica(codigo_aluno, config_ast)
        
        if "ERRO CRÍTICO" in relatorio_ast or "VIOLAÇÕES" in relatorio_ast:
            print(f">>> BLOQUEIO AST: {relatorio_ast}")
            return {
                "raciocinio": f"O código foi rejeitado automaticamente pela análise estática. Motivo: {relatorio_ast}",
                "nota_final": 0.0,
                "pontos_positivos": [],
                "pontos_negativos": [relatorio_ast],
                "feedback": f"Seu código não pôde ser avaliado. Erro estrutural grave: {relatorio_ast}"
            }
       
        prompt = f"""
Você é um professor universitário de programação avaliando o código de um aluno.
Sua única função é ler o código, analisá-lo com base no enunciado e retornar ESTRITAMENTE um objeto JSON válido.

### ENUNCIADO DO PROBLEMA:
{enunciado}

### CÓDIGO DO ALUNO:
{codigo_aluno}

### INSTRUÇÕES DE AVALIAÇÃO:
1. Se a lógica estiver correta e resolver o problema: Nota 10.
2. Se tiver erros de lógica (índices, loop infinito, cálculo errado): Variação da nota de 1 a 9.
3. Se fugir do tema (ex: fez a média em vez de ordenação): Nota 0.
4. Escreva o 'feedback' dirigindo-se diretamente ao aluno (ex: "Seu código falhou porque...").

### FORMATO DE RESPOSTA OBRIGATÓRIO (Somente JSON puro, sem formatação markdown):
{{
  "raciocinio": "Texto explicando a análise técnica",
  "nota_final": 0.0,
  "pontos_positivos": ["Lista de acertos"],
  "pontos_negativos": ["Lista de erros"],
  "feedback": "Feedback pedagógico"
}}
"""
        
        print(f">>> ESTRUTURA OK. Enviando código para a IA (Ollama)...")
        
        payload = {
            "model": self.modelo,
            "prompt": prompt,
            "stream": False,  
            "format": "json", 
            "options": {
                "temperature": 0.1 
            }
        }
        
        try:
            resposta = requests.post(self.url_ollama, json=payload)
            resposta.raise_for_status() 
            texto_gerado = resposta.json().get("response", "")
            return json.loads(texto_gerado.strip())
            
        except requests.exceptions.RequestException as e:
            return {
                "raciocinio": "Erro de comunicação com o Ollama.",
                "nota_final": 0.0,
                "pontos_positivos": [],
                "pontos_negativos": [f"Falha de Rede: {str(e)}"],
                "feedback": "Verifique se o aplicativo do Ollama está aberto no seu Mac e rodando."
            }
        except json.JSONDecodeError as e:
            return {
                "raciocinio": "Erro ao processar a resposta da IA.",
                "nota_final": 0.0,
                "pontos_positivos": [],
                "pontos_negativos": ["O modelo gerou um texto que não é um JSON válido."],
                "feedback": f"Erro interno de formatação. Detalhes: {str(e)}"
            }