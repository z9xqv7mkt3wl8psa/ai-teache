import chromadb
from sentence_transformers import SentenceTransformer
import PyPDF2
import os

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "book_collection"
collection = chroma_client.get_or_create_collection(collection_name)

# Initialize Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load PDF and extract text
pdf_path = "apj book.pdf"  # Change this to your book filename
text_chunks = []

if not os.path.exists(pdf_path):
    print(f"⚠️ ERROR: File '{pdf_path}' not found! Please check the filename.")
    exit()

with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            text_chunks.append((str(idx), text))  # Store as (ID, Text)

# Store in ChromaDB
if text_chunks:
    for idx, chunk in text_chunks:
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[idx],  # Unique ID for each chunk
            embeddings=[embedding],
            documents=[chunk]
        )

    print(f"\n✅ Book Data Stored in ChromaDB Successfully! Total Chunks: {collection.count()}")
else:
    print("\n⚠️ ERROR: No text extracted from the PDF. Try another file!")
