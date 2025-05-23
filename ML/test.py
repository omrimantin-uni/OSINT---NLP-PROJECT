import spacy

nlp = spacy.load("../output/model-best")
for token in nlp("best psychologist"):
    print(token.text)

text = "He is good psychologist."
doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)
