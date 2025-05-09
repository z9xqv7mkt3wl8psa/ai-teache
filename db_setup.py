import chromadb
import PyPDF2
import os

# Initialize ChromaDB Persistent Client
DB_PATH = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection("books")


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text if text else "No readable text found in PDF."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def store_book_in_chroma(pdf_path):
    """Read PDF and store its content in ChromaDB"""
    book_text = extract_text_from_pdf(pdf_path)

    if not book_text.strip() or "Error" in book_text:
        print(f"Failed to read book: {book_text}")
        return

    book_id = os.path.basename(pdf_path)  # Use filename as book ID

    # Check if the book already exists
    existing_books = collection.get(include=["documents"])  # Fixed line
    existing_docs = existing_books.get("documents", [])

    if book_text in existing_docs:
        print(f"Book '{book_id}' is already stored in ChromaDB. Skipping duplicate entry.")
        return

    # Store in ChromaDB
    collection.add(
        ids=[book_id],
        documents=[book_text]
    )
    print(f"Book '{book_id}' stored successfully in ChromaDB!")


if __name__ == "__main__":
    pdf_path = "apj book.pdf"  # Update with the actual file path
    store_book_in_chroma(pdf_path)
