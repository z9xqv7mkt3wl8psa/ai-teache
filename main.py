from search_chroma import search_chroma

query = "what is main message of book "
search_results = search_chroma(query)

context = "\n".join([res["text"] for res in search_results])
query_with_context = f"Context:\n{context}\n\nUser Query: {query}"

print("🚀 Sending this to Mistral for final response...")

# Now you can pass `query_with_context` to Mistral for answering.
# (Use llama.cpp or Hugging Face for inference)
