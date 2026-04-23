import faiss
import numpy as np
from app.rag.embedding import get_embedding

# Knowledge base
documents = [
    "Basic Plan: $29/month, 10 videos, 720p resolution",
    "Pro Plan: $79/month, unlimited videos, 4K resolution, AI captions",
    "No refunds after 7 days",
    "24/7 support only available for Pro plan"
]

# Create embeddings
embeddings = [get_embedding(doc) for doc in documents]

dimension = len(embeddings[0])

# FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))