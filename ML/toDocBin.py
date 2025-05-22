import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.blank("en")
doc_bin = DocBin()

with open("train_data.json", "r", encoding="utf-8") as f:
    TRAIN_DATA = json.load(f)

for text, annot in TRAIN_DATA:
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is not None:
            ents.append(span)
    doc.ents = ents
    doc_bin.add(doc)

doc_bin.to_disk("train.spacy")
print("✅ Saved train.spacy")


