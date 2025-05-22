import subprocess
import spacy
import sys
import os

# === Step 1: Train the model ===
print("🎯 Training model...")
result = subprocess.run([
    sys.executable, "-m", "spacy", "train", "config.cfg",
    "--output", "output",
    "--paths.train", "train.spacy",
    "--paths.dev", "train.spacy",
    "--verbose"
])

if result.returncode != 0:
    print("❌ Training failed. Exiting.")
    sys.exit(1)

# === Step 2: Check model exists ===
model_path = "output/model-best"
if not os.path.exists(model_path):
    print("❌ Trained model not found at output/model-best.")
    sys.exit(1)

# === Step 3: Load and test ===
print("\n🧪 Test prediction:")
nlp = spacy.load(model_path)

text = "My name is Omri Mantin, 17 years old, living in New York."
doc = nlp(text)

if not doc.ents:
    print("⚠ No entities found.")
else:
    for ent in doc.ents:
        print(f"{ent.text} → {ent.label_}")
