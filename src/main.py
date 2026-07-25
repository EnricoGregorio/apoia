import argparse
import os
import json
import csv
import glob
import time
from avaliador import AvaliadorIA

def ler_arquivo(caminho):
    if not os.path.exists(caminho):
        print(f"ERRO: Arquivo não encontrado: {caminho}")
        return None
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

def modo_lote(avaliador, args):
    print(f"\n--- INICIANDO CORREÇÃO EM LOTE (Raiz: {args.pasta_alunos}) ---")

    tempo_inicio_total = time.time()
    
    diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_enunciado = os.path.join(diretorio_base, args.enunciado)
    caminho_rubrica = os.path.join(diretorio_base, args.rubrica)
    caminho_alunos = os.path.join(diretorio_base, args.pasta_alunos)

    caminho_exemplos = os.path.join(diretorio_base, "configuracoes/base_exemplos.json")
    
    texto_enunciado = ler_arquivo(caminho_enunciado)
    texto_rubrica = ler_arquivo(caminho_rubrica)
    texto_exemplos_json = ler_arquivo(caminho_exemplos)

    if not texto_enunciado or not texto_rubrica or not texto_exemplos_json:
        print("Abordando correção: Arquivos de configuração ausentes.")
        return
        
    json_rubrica = json.loads(texto_rubrica)
    base_exemplos = json.loads(texto_exemplos_json)
    
    # Busca recursiva em todos os arquivos de todas as linguagens dentro das subpastas
    padrao_busca = os.path.join(caminho_alunos, "*", "*", "*.*")
    arquivos_alunos = glob.glob(padrao_busca)
    
    if not arquivos_alunos:
        print("Nenhum código encontrado. Verifique se a estrutura está como: codigos_alunos/questao_X/linguagem/arquivo")
        return

    relatorio_geral = []

    for caminho_aluno in arquivos_alunos:
        # Extração dinâmica das categorias baseada nas pastas
        partes_caminho = caminho_aluno.split(os.sep)
        nome_aluno = partes_caminho[-1]
        linguagem = partes_caminho[-2].lower()
        questao = partes_caminho[-3].lower()

        print(f"\n> Avaliando: {nome_aluno} | Questão: {questao.upper()} | Linguagem: {linguagem.capitalize()}...")

        # Busca o gabarito no JSON injetando as chaves dinamicamente
        exemplos_dinamicos = base_exemplos.get(questao, {}).get(linguagem, {})
        if not exemplos_dinamicos:
             print(f"  [Aviso] Nenhum gabarito RAG encontrado para {questao}/{linguagem}. Avaliando em modo Zero-Shot.")

        tempo_inicio_aluno = time.time()
        
        texto_codigo = ler_arquivo(caminho_aluno)

        # Injeta os exemplos exatos (se encontrados) no prompt do Ollama
        resultado = avaliador.avaliar(texto_enunciado, json_rubrica, texto_codigo, exemplos=exemplos_dinamicos)
        
        caminho_json = caminho_aluno.replace(os.path.splitext(caminho_aluno)[1], "_resultado.json")
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
            "Arquivo": nome_aluno,
            "Nota": str(nota).replace('.', ','),
            "Status AST": "VIOLAÇÃO" if is_violacao else "OK",
            "Tempo (s)": f"{duracao_individual:.2f}",
            "Feedback Resumido": feedback_limpo[:150]
        })

    caminho_csv = os.path.join(diretorio_base, "Relatorio_Notas_Turma.csv")
    with open(caminho_csv, "w", newline='', encoding="utf-8-sig") as f:
        # Tabela CSV atualizada com rastreabilidade completa para cruzamento de dados
        writer = csv.DictWriter(f, fieldnames=["Questão", "Linguagem", "Arquivo", "Nota", "Status AST", "Tempo (s)", "Feedback Resumido"], delimiter=';')
        writer.writeheader()
        writer.writerows(relatorio_geral)

    tempo_fim_total = time.time()
    duracao_total = tempo_fim_total - tempo_inicio_total

    minutos = int(duracao_total // 60)
    segundos = int(duracao_total % 60)
    
    print(f"\nCONCLUÍDO! Planilha salva em: {caminho_csv}")
    print(f"Tempo total de processamento: {minutos}m {segundos:.2f}s")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--modelo', default="gemma4:12b")
    parser.add_argument('--enunciado', default="configuracoes/enunciado.txt")
    parser.add_argument('--rubrica', default="configuracoes/rubrica.json")
    parser.add_argument('--pasta_alunos', default="codigos_alunos")
    
    args = parser.parse_args()
    avaliador = AvaliadorIA(args.modelo)
    modo_lote(avaliador, args)

if __name__ == "__main__":
    main()