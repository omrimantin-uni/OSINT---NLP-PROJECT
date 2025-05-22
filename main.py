import spacy

nlp = spacy.load("output/model-best")

text = "My name is Omri mantin, 17 years old, living in New York."
doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)
