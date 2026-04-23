from app.rag.embedding import get_embedding
from app.rag.vector_store import index, documents
import numpy as np


def get_answer(query: str, k=2):
    query_embedding = get_embedding(query)

    D, I = index.search(np.array([query_embedding]), k)

    results = [documents[i] for i in I[0]]

    return "\n".join(results)