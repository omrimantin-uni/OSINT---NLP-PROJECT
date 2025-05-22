from faker import Faker
import json
import random
import spacy

fake = Faker()
nlp = spacy.blank("en")

templates = [
    "I’m {name} from {city}, {age} years old.",
    "My name’s {name} and I live in {city}.",
    "Hello, I’m {name}, a {age}-year-old from {city}.",
    "They call me {name}; I’m {age} and I live in {city}.",
    "I’m {name}, living in {city}, age {age}.",
    "Hey, I’m {name}, {age} years old, from {city}.",
    "This is {name} from {city}, and I’m {age}.",
    "I go by {name}, living in {city}, aged {age}.",
    "People call me {name}. I’m {age} and I come from {city}.",
    "Name’s {name}, {age} years young, from {city}.",
    "{name} here, {age} years old, from {city}.",
    "I am {name}, a {age}-year-old residing in {city}.",
    "My friends call me {name}. I’m {age}, living in {city}.",
    "I’m known as {name} from {city}, age {age}.",
    "You can call me {name}. I’m {age} and live in {city}."
]

def find_offsets(text, substring, occurrence=1):
    start = -1
    for _ in range(occurrence):
        start = text.find(substring, start + 1)
        if start == -1:
            break
    if start == -1:
        raise ValueError(f"'{substring}' not found in: {text}")
    end = start + len(substring)
    return (start, end)

def generate_valid_example():
    template = random.choice(templates)
    name = fake.name()
    city = fake.city()
    dob = fake.date_of_birth(minimum_age=14, maximum_age=18)
    age = 2025 - dob.year
    age_str = str(age)

    sentence = template.format(name=name, city=city, age=age)
    doc = nlp.make_doc(sentence)

    spans = []
    try:
        name_offsets = find_offsets(sentence, name)
        name_span = doc.char_span(*name_offsets, label="NAME", alignment_mode="contract")
        if name_span is None:
            return None
        spans.append(name_span)

        city_offsets = find_offsets(sentence, city)
        city_span = doc.char_span(*city_offsets, label="LOCATION", alignment_mode="contract")
        if city_span is None:
            return None
        spans.append(city_span)

        if age_str in sentence:
            age_pos = sentence.find(age_str)
            age_span = doc.char_span(age_pos, age_pos + len(age_str), label="AGE", alignment_mode="contract")
            if age_span:
                spans.append(age_span)
    except Exception:
        return None

    # Convert to token spans (start, end)
    entity_spans = [(span.start_char, span.end_char, span.label_) for span in spans]
    return (sentence, {"entities": entity_spans})

# Generate and filter
TRAIN_DATA = []
max_samples = 1000
attempts = 0
while len(TRAIN_DATA) < max_samples and attempts < max_samples * 2:
    result = generate_valid_example()
    if result:
        TRAIN_DATA.append(result)
    attempts += 1

print(f"✅ Generated {len(TRAIN_DATA)} clean, aligned examples.")

# Save
with open("train_data.json", "w", encoding="utf-8") as f:
    json.dump(TRAIN_DATA, f, ensure_ascii=False, indent=2)

print("📁 Saved to train_data.json")
