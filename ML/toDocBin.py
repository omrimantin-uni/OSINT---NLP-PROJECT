import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
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
        if span is None:
            print(f"⚠️ Skipping invalid span: {start}-{end} ({label}) in text: {text}")
        else:
            ents.append(span)
    ents = filter_spans(ents)
    doc.ents = ents
    doc_bin.add(doc)

doc_bin.to_disk("train.spacy")
print("✅ Saved train.spacy")
