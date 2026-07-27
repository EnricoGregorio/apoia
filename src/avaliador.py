import json
import re
import requests # Para se comunicar com o Ollama via rede.
from analisadores import AnalisadorPython, AnalisadorJava, AnalisadorPortugol

"""
Módulo centralizador de avaliação do Motor Híbrido.
Gerencia o fluxo de bloqueio sintático e invoca o Modelo de Linguagem Local.
"""

class AvaliadorIA:
    """
    Maestro de Orquestração.
    
    Esta classe aplica o Padrão Strategy para delegar a análise sintática 
    ao 'porteiro' correto (Python, Java ou Portugol) e, em caso de sucesso, 
    encaminha o código do aluno junto com os exemplos RAG para a API do Ollama.
    """
    
    def __init__(self, nome_modelo):
        print(f">>> Inicializando Motor Híbrido conectado ao Ollama (Modelo: {nome_modelo})...")
        self.modelo = nome_modelo 
        self.url_ollama = "http://localhost:11434/api/generate" 

    def avaliar(self, enunciado, rubrica, codigo_aluno, exemplos=None, linguagem="python"):
        # Filtro inteligente: o Analisador chama o modelo analisador correspondente à linguagem.
        analisador = None
        if linguagem.lower() == "python":
            analisador = AnalisadorPython()
        elif linguagem.lower() == "java":
            analisador = AnalisadorJava()
        elif linguagem.lower() == "portugol":
            analisador = AnalisadorPortugol()

        # Se existir um analisador para a lingugagem, ele atua como porteiro.
        if analisador:
            config_ast = rubrica.get("configuracao_ast", {})
            relatorio_ast = analisador.analisar(codigo_aluno, config_ast)
            
            if "ERRO CRÍTICO" in relatorio_ast or "VIOLAÇÕES" in relatorio_ast:
                print(f">>> BLOQUEIO AST: {relatorio_ast}")
                return {
                    "raciocinio": f"O código foi rejeitado automaticamente pela análise estática. Motivo: {relatorio_ast}",
                    "nota_final": 0.0,
                    "pontos_positivos": [],
                    "pontos_negativos": [relatorio_ast],
                    "feedback": f"Seu código não pôde ser avaliado. Erro estrutural grave: {relatorio_ast}"
                }

        texto_exemplos = ""
        if exemplos:
            texto_exemplos = "### EXEMPLOS DE AVALIAÇÃO (Siga estritamente este padrão para definir notas e tom de feedback):\n"
            for chave, dados in exemplos.items():
                titulo = chave.replace('_', ' ').upper()
                texto_exemplos += f"\n[{titulo}]\n"
                texto_exemplos += f"Código do Aluno:\n{dados['codigo']}\n"
                texto_exemplos += f"Sua Resposta Esperada (JSON):\n{json.dumps(dados['saida_esperada'], indent=2, ensure_ascii=False)}\n"
                texto_exemplos += "-" * 40 + "\n"
       
        prompt = f"""
Você é um professor universitário de programação avaliando o código de um aluno.
Sua única função é ler o código, analisá-lo com base no enunciado e retornar ESTRITAMENTE um objeto JSON válido.

### INSTRUÇÕES DE AVALIAÇÃO:
1. Se a lógica estiver correta e resolver o problema: Nota 10.
2. Se tiver erros de lógica (índices, loop infinito, cálculo errado): Variação da nota de 1 a 9.
3. Se fugir do tema (ex: fez a média em vez de ordenação): Nota 0.
4. Escreva o 'feedback' dirigindo-se diretamente ao aluno (ex: "Seu código falhou porque...").

{texto_exemplos}

### AGORA É A SUA VEZ:
### ENUNCIADO DO PROBLEMA:
{enunciado}

### CÓDIGO DO ALUNO A SER AVALIADO:
{codigo_aluno}
"""
        
        print(f">>> ESTRUTURA OK. Enviando código e exemplos para a IA (Ollama)...")
        
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
            
            # Sanitizador Rigoroso de JSON via Regex
            match = re.search(r'\{.*\}', texto_gerado, re.DOTALL)
            if match:
                texto_limpo = match.group(0)
            else:
                texto_limpo = texto_gerado
                
            return json.loads(texto_limpo.strip())
            
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
