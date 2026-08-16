from __future__ import annotations
import argparse
import os
import json
import csv
import glob
import time
from avaliador import AvaliadorIA

"""
Ponto de entrada e orquestrador de arquivos do sistema ApoIA.
Responsável por varrer o repositório local, coordenar correções em lote 
e gerar relatórios consolidados em CSV.
"""

def ler_arquivo(caminho: str) -> str | None:
    if not os.path.exists(caminho):
        print(f"ERRO: Arquivo não encontrado: {caminho}")
        return None
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

def modo_lote(avaliador: AvaliadorIA, args: argparse.Namespace) -> None:
    print(f"\n--- INICIANDO CORREÇÃO EM LOTE (Raiz: {args.pasta_alunos}) ---")

    tempo_inicio_total = time.time()
    
    diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_rubrica = os.path.join(diretorio_base, args.rubrica)
    caminho_respostas = os.path.join(diretorio_base, args.pasta_alunos)
    caminho_exemplos = os.path.join(diretorio_base, args.exemplos)
    
    pasta_correcoes = os.path.join(diretorio_base, "correcoes")
    os.makedirs(pasta_correcoes, exist_ok=True)
    
    texto_rubrica = ler_arquivo(caminho_rubrica)
    texto_exemplos_json = ler_arquivo(caminho_exemplos)

    if not texto_rubrica or not texto_exemplos_json:
        print("Abordando correção: Arquivos de configuração ausentes.")
        return
        
    json_rubrica = json.loads(texto_rubrica)
    base_exemplos = json.loads(texto_exemplos_json)
    
    padrao_busca = os.path.join(caminho_respostas, "*", "*", "*.*")
    arquivos_alunos = glob.glob(padrao_busca)
    
    if not arquivos_alunos:
        print("Nenhum código encontrado. Verifique se a estrutura está como: codigos_alunos/questaoX/linguagem/arquivo")
        return

    relatorio_geral = []

    for caminho_resposta in arquivos_alunos:
        partes_caminho = caminho_resposta.split(os.sep)
        nome_arquivo = partes_caminho[-1]
        linguagem = partes_caminho[-2].lower()
        questao = partes_caminho[-3].lower()

        print(f"\n> Verificando arquivo {nome_arquivo} | Questão: {questao.replace("questao", "questao ").capitalize()} | Linguagem: {linguagem.capitalize()}...")

        # Extrai o enunciado dinamicamente da fonte única, o JSON.
        texto_enunciado = base_exemplos.get(questao, {}).get("enunciado", "Enunciado não fornecido.")
        exemplos_dinamicos = base_exemplos.get(questao, {}).get(linguagem, {})
        
        # O sistema continuará ignorando questões que ainda não estão mapeadas no JSON
        if not exemplos_dinamicos:
             print(f"[ATENÇÃO] Gabarito RAG ausente para {questao}/{linguagem}. Pulando avaliação para evitar poluição de dados.")
             continue

        tempo_inicio_aluno = time.time()
        
        texto_codigo = ler_arquivo(caminho_resposta)

        resultado = avaliador.avaliar(
            enunciado=texto_enunciado, 
            rubrica=json_rubrica, 
            codigo=texto_codigo, 
            exemplos=exemplos_dinamicos, 
            linguagem=linguagem
        )
        
        nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
        nome_arquivo_json = f"{linguagem}_{nome_sem_extensao}.json"
        caminho_json = os.path.join(pasta_correcoes, nome_arquivo_json)
        
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)

        tempo_fim_aluno = time.time()
        duracao_individual = tempo_fim_aluno - tempo_inicio_aluno
        
        nota = resultado.get("nota_final", 0.0)
        print(f"  -> Nota: {nota} | Tempo: {duracao_individual:.2f}s | Raciocínio: {resultado.get('raciocinio', '')[:60]}...")

        texto_negativo = str(resultado.get("pontos_negativos", [])).lower()
        is_violacao = "violação" in texto_negativo or "erro crítico" in texto_negativo or "proibida" in texto_negativo
        
        feedback_limpo = resultado.get("feedback", "").replace('\n', ' ').replace('\r', '').replace(';', ',')

        relatorio_geral.append({
            "Questão": questao.replace('_', ' ').capitalize(),
            "Linguagem": linguagem.capitalize(),
            "Arquivo": nome_arquivo,
            "Nota": str(nota).replace('.', ','),
            "Status AST": "VIOLAÇÃO" if is_violacao else "OK",
            "Tempo (s)": f"{duracao_individual:.2f}",
            "Feedback Resumido": feedback_limpo[:150]
        })

    if relatorio_geral:
        caminho_csv = os.path.join(diretorio_base, "Relatorio_Geral.csv")
        with open(caminho_csv, "w", newline='', encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["Questão", "Linguagem", "Arquivo", "Nota", "Status AST", "Tempo (s)", "Feedback Resumido"], delimiter=';')
            writer.writeheader()
            writer.writerows(relatorio_geral)
        print(f"\nCONCLUÍDO! Planilha salva em: {caminho_csv}")
        print(f"Correções individuais salvas em: {pasta_correcoes}")
    else:
        print("\nNenhum arquivo foi avaliado. Verifique se o base_exemplos.json está preenchido corretamente.")

    tempo_fim_total = time.time()
    duracao_total = tempo_fim_total - tempo_inicio_total

    minutos = int(duracao_total // 60)
    segundos = int(duracao_total % 60)
    print(f"Tempo total de processamento: {minutos}m {segundos:.2f}s")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--modelo', default="gemma4:12b")
    parser.add_argument('--rubrica', default="configs/rubrica.json")
    parser.add_argument('--exemplos', default="configs/base_exemplos.json")
    parser.add_argument('--pasta_alunos', default="codigos_alunos")

    parser.add_argument('--ip_local', default="192.168.18.141", help="IP fixo do PC na rede da casa")
    parser.add_argument('--ip_tunel', default="100.85.59.121", help="IP do PC no túnel (Tailscale)")
    
    args = parser.parse_args()

    try:
        # Passa os IPs para a classe avaliar.
        avaliador = AvaliadorIA(args.modelo, args.ip_local, args.ip_tunel)
        modo_lote(avaliador, args)
    except ConnectionError as erro_rede:
        # Captura o erro customizado e exibe a mensagem de ligar o túnel.
        print(erro_rede)
        exit(1)

if __name__ == "__main__":
    main()
