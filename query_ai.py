import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "book_collection"
collection = chroma_client.get_or_create_collection(collection_name)

# Initialize Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Check if the database is empty
if collection.count() == 0:
    print("\n⚠️ ERROR: No data found in ChromaDB. Run 'store_book.py' first!")
    exit()


# Query Function
def query_ai(user_query):
    print(f"\n🔍 Searching ChromaDB for: {user_query}")

    query_results = collection.query(
        query_embeddings=[model.encode(user_query).tolist()],  # Search by embedding
        n_results=3  # Get top 3 matches
    )

    # Debugging: Print results
    print("\n📌 Query Results:", query_results)

    if not query_results or "documents" not in query_results or not query_results["documents"]:
        return "⚠️ No relevant answer found in the book."

    return query_results["documents"][0][0]  # Return the best match


# Interactive Query Loop
while True:
    user_query = input("\nAsk a question (or type 'exit' to quit): ").strip()
    if user_query.lower() == "exit":
        break
    answer = query_ai(user_query)
    print(f"\n✅ Answer:\n{answer}")
