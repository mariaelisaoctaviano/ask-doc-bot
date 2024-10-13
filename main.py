
import os
from helpers import extract_text_from_file, chunk_text
from faiss_index import create_faiss_index, retrieve_relevant_chunks
from qa import get_cohere_embeddings, ask_cohere_question, evaluate_similarity

def interactive_qa():
    print("Bem-vindo ao sistema de perguntas! Digite 'sair' para encerrar.")
    
    # Diretório onde os arquivos estarão disponíveis (sempre dentro da pasta 'files')
    files_dir = "files"
    
    # Listar os arquivos disponíveis na pasta 'files'
    files = os.listdir(files_dir)
    if not files:
        print("Nenhum arquivo encontrado na pasta 'files'.")
        return
    
    print("Arquivos disponíveis na pasta 'files':")
    for idx, file in enumerate(files):
        print(f"{idx + 1}: {file}")
    
    file_index = int(input("Digite o número do arquivo que deseja processar: ")) - 1
    if file_index < 0 or file_index >= len(files):
        print("Índice inválido.")
        return
    
    # Caminho completo do arquivo selecionado
    file_path = os.path.join(files_dir, files[file_index])
    
    # Processar o arquivo selecionado
    context = extract_text_from_file(file_path)
    chunks = chunk_text(context)

    # Criar e indexar os embeddings
    chunk_embeddings = get_cohere_embeddings(chunks)
    index = create_faiss_index(chunk_embeddings)

    # Avaliação da qualidade dos chunks
    if len(chunks) > 1:
        # Avaliar a similaridade entre o primeiro e o segundo chunks como exemplo
        chunk_quality = evaluate_similarity(chunk_embeddings[0], chunk_embeddings[1])
        print(f"Métrica de qualidade dos chunks (similaridade entre os dois primeiros): {chunk_quality}\n")

    while True:
        question = input("Digite sua pergunta (ou 'sair' para encerrar): ")
        if question.lower() == 'sair':
            print("Encerrando o sistema de perguntas.")
            break

        relevant_chunks = retrieve_relevant_chunks(question, index, chunks)
        context = " ".join(relevant_chunks)
        
        # Gerar a resposta usando o modelo Cohere
        answer = ask_cohere_question(question, context)
        print(f"Pergunta: {question}")
        print(f"Resposta: {answer}\n")
        
        # Avaliar a similaridade entre a pergunta e o contexto recuperado como métrica de qualidade da resposta
        question_embedding = get_cohere_embeddings([question])[0]
        context_embedding = get_cohere_embeddings([context])[0]
        response_quality = evaluate_similarity(question_embedding, context_embedding)
        print(f"Métrica de qualidade da resposta (similaridade entre pergunta e contexto): {response_quality}\n")

if __name__ == "__main__":
    interactive_qa()
