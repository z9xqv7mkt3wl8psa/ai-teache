from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load book text dynamically
def load_book(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Load and preprocess book data
book_text = load_book("apj book.pdf")  # Replace with your book file path
documents = book_text.split("\n\n")  # Split book into paragraphs

# Generate embeddings
document_embeddings = model.encode(documents)
document_embeddings = np.array(document_embeddings)

# Build FAISS index
dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(document_embeddings)

# Improved search with semantic similarity
def search(query, k=3):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding)
    distances, indices = index.search(query_embedding, k)

    results = [documents[idx] for idx in indices[0]]

    # Ranking based on cosine similarity
    similarities = [util.cos_sim(query_embedding, model.encode([doc]))[0][0].item() for doc in results]
    ranked_results = [result for _, result in sorted(zip(similarities, results), reverse=True)]

    return ranked_results
