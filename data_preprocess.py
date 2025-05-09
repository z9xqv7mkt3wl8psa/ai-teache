import fitz  # PyMuPDF for extracting text
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="book_data")

# Load the PDF text
def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = []
    for page in doc:
        text.append(page.get_text("text"))  # Extract text per page
    return text

# Embed and store data
def embed_and_store(pdf_path):
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Small, efficient model
    book_text = load_pdf(pdf_path)

    for i, paragraph in enumerate(book_text):
        embedding = model.encode(paragraph).tolist()
        collection.add(ids=[str(i)], embeddings=[embedding], metadatas=[{"text": paragraph}])

    print("Book data stored successfully in ChromaDB!")

embed_and_store("apj book.pdf")  # Use your actual PDF file
