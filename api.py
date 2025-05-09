from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
import os
from sentence_transformers import SentenceTransformer
from ctransformers import AutoModelForCausalLM  # GGUF Model Loader

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("book_collection")
except Exception as e:
    print(f"❌ Error initializing ChromaDB: {e}")
    collection = None

# Initialize Embedding Model
try:
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    print(f"❌ Error loading embedding model: {e}")
    embed_model = None

# Load GGUF Model
model_path = "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"


if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found at path: {model_path}")

try:
    llm_model = AutoModelForCausalLM.from_pretrained(model_path, model_type="mistral")
    print("✅ GGUF Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading GGUF model: {e}")
    llm_model = None


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!"})


@app.route("/search", methods=["POST"])
def search():
    if not collection or not embed_model:
        return jsonify({"error": "Server not properly initialized"}), 500

    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    try:
        query_embedding = embed_model.encode(query).tolist()
        search_results = collection.query(query_embeddings=[query_embedding], n_results=3)
        documents = search_results.get("documents", [[]])[0]

        if documents:
            response = "\n".join(documents[:2])
        else:
            response = "⚠️ No relevant answer found in the book."

        return jsonify({"result": response})

    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
