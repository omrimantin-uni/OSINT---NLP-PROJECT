import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from spacy.scorer import Scorer
from sklearn.model_selection import train_test_split
import random
import json

# Load the training data from file
with open("ML/train_data.json", "r", encoding="utf-8") as f:
    TRAIN_DATA = json.load(f)

# Create blank English model
nlp = spacy.blank("en")

# ---------- Filter invalid spans ----------
def filter_valid_examples(nlp, data):
    valid_data = []
    for text, ann in data:
        doc = nlp.make_doc(text)
        spans = []
        for start, end, label in ann["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is not None:
                spans.append((start, end, label))
        if spans:
            valid_data.append((text, {"entities": spans}))
    return valid_data

# Filter examples to ensure alignment
TRAIN_DATA = filter_valid_examples(nlp, TRAIN_DATA)
print(f"✅ Loaded {len(TRAIN_DATA)} valid training examples.")
# Debugging: Print one example after filtering
print("\n🔍 Example of a filtered training sentence:")
print(json.dumps(TRAIN_DATA[0], indent=2))

# Split data into train and test
train_data, test_data = train_test_split(TRAIN_DATA, test_size=0.2, random_state=42)

# Add NER pipeline if needed
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add labels based on training data
for text, annotations in train_data:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Train the model
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    nlp.initialize()
    for itn in range(20):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            examples = []
            for text, annots in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(nlp(text), annots)
                examples.append(example)
            if examples:
                nlp.update(examples, drop=0.2, losses=losses)
        print(f"Iteration {itn+1} - Losses: {losses.get('ner', 0):.6f}")

# Save the model
nlp.to_disk("custom_ner_model")
print("📦 Model saved to 'custom_ner_model/'.")

# ---------- Evaluation ----------
def evaluate_model(nlp, data):
    examples = []
    for text, annotations in data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(nlp(text), annotations)
        examples.append(example)
    scorer = Scorer()
    scores = scorer.score(examples)
    return scores

# Evaluate on train data
print("\n📊 Evaluation on training data:")
results_train = evaluate_model(nlp, train_data)
print(f"Precision: {results_train['ents_p']:.3f}")
print(f"Recall:    {results_train['ents_r']:.3f}")
print(f"F1-score:  {results_train['ents_f']:.3f}")

# Evaluate on test data
print("\n📊 Evaluation on test data:")
results_test = evaluate_model(nlp, test_data)
print(f"Precision: {results_test['ents_p']:.3f}")
print(f"Recall:    {results_test['ents_r']:.3f}")
print(f"F1-score:  {results_test['ents_f']:.3f}")
