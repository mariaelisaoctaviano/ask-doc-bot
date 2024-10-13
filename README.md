
# Projeto de Perguntas com Embeddings e Similaridade

Este projeto permite fazer perguntas com base em documentos e responde utilizando modelos de embeddings. O sistema também calcula a métrica de qualidade dos chunks e das respostas para cada pergunta enviada.

## Tecnologias utilizadas
- **Cohere** para embeddings e geração de texto.
- **FAISS** para indexação e busca eficiente de embeddings.
- **Docker** para facilitar a execução do projeto.
- **Python** com bibliotecas como `numpy`, `faiss-cpu`, `pdfplumber`, e `scikit-learn`.

## Requisitos

- **Docker** instalado na máquina.
- **Conta na Cohere** para obter uma chave da API. Você pode se inscrever gratuitamente em [Cohere](https://cohere.com/) e obter a sua chave de API na seção de **API Keys**.

## Como rodar o projeto

### Passos para Linux/MacOS:

1. Clone este repositório:

```bash
git clone https://github.com/mariaelisaoctaviano/ask-doc-bot
cd ask-doc-bot
```

2. Adicione a sua chave de API da Cohere no arquivo `.env`:

```bash
echo "COHERE_API_KEY=SUA_CHAVE_API_AQUI" > .env
```

3. Construa a imagem Docker:

```bash
docker build -t ask-doc-bot .
```

4. Rode o container montando a pasta de arquivos:

```bash
docker run -it --rm --name ask-doc-bot -v $(pwd)/files:/app/files ask-doc-bot
```

### Passos para Windows:

1. Clone este repositório usando o Git Bash ou o terminal do Windows:

```bash
git clone https://github.com/mariaelisaoctaviano/ask-doc-bot
cd ask-doc-bot
```

2. Adicione a sua chave de API da Cohere no arquivo `.env` (utilize o PowerShell ou o CMD):

```bash
echo COHERE_API_KEY=SUA_CHAVE_API_AQUI > .env
```

3. Construa a imagem Docker:

```bash
docker build -t ask-doc-bot .
```

4. Rode o container montando a pasta de arquivos (usando caminho completo do host):

```bash
docker run -it --rm --name ask-doc-bot -v %cd%\files:/app/files ask-doc-bot
```

> **Nota:** Se você estiver usando o PowerShell, use `${PWD}` em vez de `%cd%`:
> ```bash
> docker run -it --rm --name ask-doc-bot -v ${PWD}\files:/app/files ask-doc-bot
> ```

## Estrutura do Projeto

- **main.py**: O arquivo principal que roda a aplicação interativa.
- **helpers.py**: Funções auxiliares para extração de texto e chunking.
- **faiss_index.py**: Funções para criar o índice FAISS e buscar chunks relevantes.
- **qa.py**: Funções para gerar embeddings e respostas usando a API da Cohere.
- **.env**: Arquivo contendo a chave da API da Cohere (não incluído no repositório por segurança).
- **files**: Diretório onde os arquivos que serão processados devem ser armazenados. Coloque seus documentos (PDF, Word, TXT) dentro desta pasta.

## Como funciona

1. Coloque os arquivos que deseja processar na pasta **`files`**. O sistema sempre buscará os arquivos dentro dessa pasta.
2. O sistema listará os arquivos disponíveis na pasta **`files`**.
3. O sistema processa o arquivo selecionado e o divide em chunks.
4. Os embeddings dos chunks são gerados e indexados usando FAISS.
5. O usuário faz perguntas, e o sistema busca os chunks mais relevantes e gera uma resposta usando a Cohere.
6. O sistema também calcula a métrica de qualidade dos chunks e das respostas para cada pergunta.

## Exemplo de uso:

```bash
Bem-vindo ao sistema de perguntas! Digite 'sair' para encerrar.
Arquivos disponíveis na pasta 'files':
1: Cuidado_felino.pdf
Digite o número do arquivo que deseja processar: 1
Métrica de qualidade dos chunks (similaridade entre os dois primeiros): 0.87

Digite sua pergunta (ou 'sair' para encerrar): Qual é a idade ideal para adotar um gato?
Pergunta: Qual é a idade ideal para adotar um gato?
Resposta: A idade ideal para adotar um gato filhote é por volta de dois meses.

Métrica de qualidade da resposta (similaridade entre pergunta e contexto): 0.92
```

## Perguntas sugeridas de exemplo:

Aqui estão algumas perguntas sugeridas que você pode fazer após o processamento de um arquivo de exemplo como **`Cuidado_felino.pdf`**:

1. **Qual a idade ideal para adotar um gato?**
2. **Cite itens essenciais para o gato.**
3. **A partir de quantos meses é recomendada a castração?**
4. **Quantos tópicos tem no texto?**
5. **Quando deve ser aplicada a vacina antirrábica?**
6. **Cite brincadeiras que os gatos costumam gostar.**

## Observações
- A métrica de qualidade é baseada na similaridade do cosseno entre os embeddings dos chunks e da pergunta.
- O diretório **`files`** deve conter os documentos que serão processados, e o volume é montado entre o host e o container para que o Docker tenha acesso aos arquivos.
