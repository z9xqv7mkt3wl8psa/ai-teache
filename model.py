from transformers import pipeline

# Explicitly specify the model
model_name = "distilbert/distilbert-base-cased-distilled-squad"
qa_pipeline = pipeline("question-answering", model=model_name)

# Define a context and question
context = "Prasunet is a forward-thinking technology company founded by a passionate entrepreneur Pramod Prajapat with a strong focus on innovation, excellence, and impactful solutions. At Prasunet, we are driven by the mission to create transformative technologies that empower industries and improve everyday lives."
question = "What does Prasunet do?"

# Get the answer
result = qa_pipeline(question=question, context=context)

# Print the result
print("Answer:", result['answer'])
print("Confidence Score:", result['score'])
