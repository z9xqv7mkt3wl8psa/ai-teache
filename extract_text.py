import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file."""
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return None  # Exit if file doesn't exist

    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

if __name__ == "__main__":
    pdf_path = "apj book.pdf"  # Replace with your PDF file
    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text:  # Only save if extraction was successful
        with open("book_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print("Text extraction complete. Saved to 'book_text.txt'.")
    else:
        print("Failed to extract text.")
