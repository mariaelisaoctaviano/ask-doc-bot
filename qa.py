
import os
import time
import cohere
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

# Inicializar o cliente da Cohere
co = cohere.Client(cohere_api_key)

def get_cohere_embeddings(texts, batch_size=10):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            response = co.embed(model='large', texts=batch)
            embeddings.extend(response.embeddings)
            time.sleep(1)
        except cohere.error.CohereError as e:
            print(f"Erro da API Cohere: {e.message}")
            time.sleep(10)
            continue
    return embeddings

def ask_cohere_question(question, context):
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=f"Contexto: {context}\nPergunta: {question}",
        max_tokens=100,
        temperature=0
    )
    return response.generations[0].text.strip()

def evaluate_similarity(embedding_1, embedding_2):
    return cosine_similarity([embedding_1], [embedding_2])[0][0]
