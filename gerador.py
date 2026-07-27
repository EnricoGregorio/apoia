import json
import os
import sys

def gerar_bloco_json(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo não encontrado: {caminho_arquivo}")
        return
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    nome_arquivo = os.path.basename(caminho_arquivo).lower()
    
    if "certa" in nome_arquivo or "correto" in nome_arquivo:
        chave = "exemplo_correto"
        nota = 10.0
    elif "logica" in nome_arquivo:
        chave = "exemplo_erro_logica"
        nota = 4.0
    elif "sintaxe" in nome_arquivo:
        chave = "exemplo_erro_sintaxe"
        nota = 0.0
    else:
        chave = "exemplo_erro_atalho"
        nota = 5.0
        
    # A estrutura pedagógica padronizada embutida nos placeholders
    bloco = {
        chave: {
            "codigo": codigo,
            "saida_esperada": {
                "raciocinio": "[PREENCHER: Ação do aluno + Impacto técnico + Justificativa (Em 3ª pessoa)]",
                "nota_final": nota,
                "pontos_positivos": [
                    "[PREENCHER: Substantivo + Contexto Técnico]"
                ],
                "pontos_negativos": [
                    "[PREENCHER: Substantivo + Contexto Técnico]"
                ],
                "feedback": "[PREENCHER: Reconhecimento do esforço + Apontamento técnico + Dica de resolução (Em 2ª pessoa)]"
            }
        }
    }
    
    json_formatado = json.dumps(bloco, indent=2, ensure_ascii=False)
    json_para_copiar = "\n".join(json_formatado.split("\n")[1:-1]).strip()
    
    print(f"\n{'='*60}")
    print(f" BLOCO JSON GERADO PARA: {nome_arquivo}")
    print(f"{'='*60}\n")
    print(json_para_copiar)
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        gerar_bloco_json(sys.argv[1])
    else:
        print("Uso correto: python src/gerador.py <caminho_do_arquivo>")
        print("Exemplo: python src/gerador.py codigos_alunos/questao_2/python/resposta_certa.py")