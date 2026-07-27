# ApoIA - Motor Híbrido de Avaliação de Códigos

O **ApoIA** é um motor de correção automatizada de exercícios de programação. Ele utiliza uma arquitetura híbrida que combina **Análise Estática de Código (AST)** com um **Modelo de Linguagem Grande (LLM) Local (Ollama)** enriquecido por **RAG (Retrieval-Augmented Generation)**. O sistema corrige trabalhos em Python, Java e Portugol, atribuindo notas e gerando feedbacks personalizados de forma escalável.

## 🏗️ Arquitetura do Sistema

O motor opera em um padrão de *Pipeline* de duas etapas (Motor Híbrido):
1. **O Porteiro (AST):** Verifica erros críticos, de sintaxe e violações de restrições pedagógicas (ex: uso proibido de `while` ou funções prontas) antes de enviar o código para a IA.
2. **O Professor (LLM + RAG):** Recebe o código validado pelo AST junto com um JSON de exemplos (RAG). A IA compara a lógica do aluno com o conhecimento injetado e devolve uma avaliação JSON com nota, raciocínio e feedback estruturado.

## 📂 Estrutura de Diretórios

O repositório está organizado utilizando o princípio de Separação de Preocupações (SoC):

```text
apoia/
├── codigos_alunos/         # Entrada: Submissões dos alunos organizadas por questão e linguagem.
├── configs/
│   ├── base_exemplos.json  # Base de Conhecimento (RAG) da IA.
│   └── rubrica.json        # Pesos e bloqueios sintáticos do AST (ex: proibir_loops).
├── correcoes/              # Saída: Feedbacks detalhados em JSON para cada aluno avaliado.
├── src/
│   ├── analisadores/       # Módulo Strategy para os parsers AST de cada linguagem.
│   │   ├── analisador_base.py     # Contrato/Interface abstrata.
│   │   ├── analisador_java.py     # Analisador usando a biblioteca 'javalang'.
│   │   ├── analisador_portugol.py # Analisador léxico usando Expressões Regulares.
│   │   └── analisador_python.py   # Analisador usando a biblioteca nativa 'ast'.
│   ├── avaliador.py        # Faz a ponte entre os analisadores e a API do Ollama.
│   ├── gerar_exemplos.py   # Ferramenta para transformar gabaritos no formato JSON RAG.
│   └── main.py             # Orquestrador central que varre pastas e gera o CSV final.
├── gerar_turma.py          # Script de testes para simular turmas com N alunos.
├── requirements.txt        # Dependências do projeto.
└── Relatorio_Notas_Turma.csv # Saída: Planilha consolidada com todas as notas da turma.
```

## ⚙️ Como Funciona (Fluxo de Execução)

1. **Configuração da Base:** O professor ou o sistema insere o gabarito no `base_exemplos.json` (gerado via `gerar_exemplos.py`). O `rubrica.json` é configurado para determinar restrições de código.
2. **Entrada de Dados:** Os códigos dos alunos são dispostos em `codigos_alunos/<questaoX>/<linguagem>/<nome_aluno.ext>`.
3. **Orquestração:** Ao rodar o `main.py`, o script lê dinamicamente as submissões.
4. **Validação (AST):** O `AvaliadorIA` aciona o analisador correspondente (Python, Java ou Portugol). Se houver violação (ex: falta de indentação ou uso de pacote proibido), o aluno recebe nota `0.0` instantaneamente, economizando processamento.
5. **Avaliação Semântica (IA):** Se a sintaxe for válida, o código é enviado à API local do Ollama (`http://localhost:11434/api/generate`). O prompt injeta o enunciado e os exemplos do RAG para parametrizar a correção.
6. **Saída:** O sistema salva um JSON detalhado na pasta `correcoes/` para cada aluno e consolida todas as notas e tempos de execução no `Relatorio_Notas_Turma.csv`.

## 🚀 Como Executar

### 1. Pré-requisitos
* **Python 3.10+** instalado.
* **Ollama** rodando localmente com o modelo desejado (Padrão: `gemma4:12b` ou `llama3`).
* Instalar dependências:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Executando Correções em Lote
Após organizar os códigos dentro da pasta `codigos_alunos/`, rode o maestro na raiz do projeto:

```bash
python src/main.py
```

Argumentos opcionais suportados pelo CLI:
* `--modelo`: Define o LLM a ser utilizado (default: *gemma4:12b*).
* `--rubrica`: Caminho do arquivo de configurações AST (default: *configs/rubrica.json*).
* `--exemplos`: Caminho do banco RAG (default: *configs/base_exemplos.json*).
* `--pasta_alunos`: Diretório alvo da correção (default: *codigos_alunos*).

### 3. Teste de Carga (Simulação)
Para simular a presença de alunos no sistema:
```bash
python gerar_turma.py
```
Isso populará a pasta de submissões com 30 alunos contendo erros lógicos, atalhos e acertos mapeados, permitindo auditar o tempo de processamento e a precisão do Motor Híbrido.