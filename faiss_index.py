
import faiss
import numpy as np
from qa import get_cohere_embeddings

def create_faiss_index(embeddings):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

def retrieve_relevant_chunks(question, index, chunks, k=3):
    question_embedding = get_cohere_embeddings([question])[0]
    distances, indices = index.search(np.array([question_embedding]), k)
    relevant_chunks = [chunks[i] for i in indices[0]]
    return relevant_chunks
