from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import numpy as np

# Load model and tokenizer
model_name = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name).to("cuda")

# Example input
text = "Omri Mantin is 17 years old and lives in New York."

# Tokenize and move to GPU
inputs = tokenizer(text, return_tensors="pt").to("cuda")

# Inference
with torch.no_grad():
    outputs = model(**inputs)

# Extract predicted class per token
logits = outputs.logits
predictions = torch.argmax(logits, dim=2)

# Decode tokens and predictions
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
labels = predictions[0].cpu().numpy()

print("🧪 NER Results:")
for token, label_id in zip(tokens, labels):
    if label_id != 0:  # label 0 is usually 'O' (outside entity)
        print(f"{token} → {model.config.id2label[label_id]}")
