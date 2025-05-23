from faker import Faker
import json
import random
import spacy
import requests

fake = Faker()
nlp = spacy.blank("en")

api_key = 'PWwCSD2/yO/cRA5nwY++JQ==DZ1pEtfxMKtDg4DZ'
url = 'https://api.api-ninjas.com/v1/hobbies'
headers = {'X-Api-Key': api_key}
response = requests.get(url, headers=headers)


templates = [
    "{name} works as a {profession} at {company}.",
    "{name}, who is {age} years old, recently joined {company} as a {profession}.",
    "While visiting {location}, I met {name}. He's into {interest}.",
    "Did you know that {name} from {location} loves {interest}?",
    "{name} told me at the {location} that he enjoys {interest} in his free time.",
    "Back in {location}, {name} was painting a beautiful mural.",
    "{name} works at {company} and spends weekends {interest}.",
    "I ran into {name} near the {location}. He mentioned his job as a {profession} at {company}.",
    "{name} is a {profession} and his main hobby is {interest}.",
    "People from {company} say {name} is their best {profession}.",
    "{name} said he has been a {profession} for years, currently at {company}.",
    "{name}, who works at {company}, was talking about how much he enjoys {interest}.",
    "{name} is passionate about {interest} and works as a {profession}.",
    "My friend {name} from {location} started working at {company}.",
    "{name} likes {interest} and lives near {location}.",
    "{name} works remotely as a {profession} for {company} and often talks about {interest}.",
    "{name} just turned {age} and began working as a {profession} at {company}.",
    "During a walk in {location}, I bumped into {name}, who loves {interest}.",
    "{name} recently left {company} where he worked as a {profession}.",
    "{name} was seen giving a talk at {company} about his passion for {interest}.",
    "{name}, a well-known {profession} from {location}, also enjoys {interest}.",
    "After {age} years of service at {company}, {name} retired from his role as a {profession}.",
    "{name}, based in {location}, mentioned that {interest} helps him unwind after work.",
    "{name}'s LinkedIn says he is a {profession} working at {company}, also interested in {interest}.",
    "Though {name} works at {company} as a {profession}, he always makes time for {interest}.",
    "At a cafe in {location}, {name} explained how he got into {interest}.",
    "{name}, age {age}, has been a {profession} for a decade at {company}.",
    "You can always find {name} at {company}, unless he's out {interest}.",
    "Despite being a {profession}, {name} often visits {location} to pursue {interest}.",
    "Everyone at {company} knows {name} not just for his {profession} skills, but for his love of {interest}.",
    "{name} is considered the best {profession} in {company}.",
    "Everyone calls {name} the lead {profession} at {company}.",
    "{name}, a senior {profession}, works remotely from {location}.",
    "At {company}, {name} is known as a top {profession}.",
    "{name} works as a highly skilled {profession} based in {location}.",
    "{name} is the head {profession} at {company}.",
    "{name} is the best {profession} we've ever worked with.",
    "The talented {profession}, {name}, joined {company} recently."
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
    if response.status_code == 200:
        data = response.json()
        interest = data.get('hobby')
    else:
        print(f"Error {response.status_code}: {response.text}")
        interest = None
    template = random.choice(templates)
    name = fake.name()
    company = fake.company()
    profession = fake.job().lower()
    location = fake.city()

    age = random.randint(10, 70)
    age_str = str(age)

    values = {
        "name": name,
        "age": age,
        "company": company,
        "interest": interest,
        "profession": profession,
        "location": location,
    }

    try:
        sentence = template.format(**values)
        doc = nlp.make_doc(sentence)

        spans = []

        def try_add_span(text_value, label):
            if text_value in sentence:
                offsets = find_offsets(sentence, text_value)
                span = doc.char_span(*offsets, label=label, alignment_mode="expand")
                if span:
                    spans.append(span)

        try_add_span(name, "NAME")
        try_add_span(location, "LOCATION")
        try_add_span(interest, "INTEREST")
        try_add_span(profession, "PROFESSION")
        try_add_span(company, "COMPANY")

        if age_str in sentence:
            age_pos = sentence.find(age_str)
            age_span = doc.char_span(age_pos, age_pos + len(age_str), label="AGE", alignment_mode="contract")
            if age_span:
                spans.append(age_span)

        if not spans:
            return None

        entity_spans = [(span.start_char, span.end_char, span.label_) for span in spans]
        return (sentence, {"entities": entity_spans})

    except Exception:
        return None

    # Convert to token spans (start, end)
    entity_spans = [(span.start_char, span.end_char, span.label_) for span in spans]
    return (sentence, {"entities": entity_spans})

# Generate and filter
TRAIN_DATA = []
max_samples = 10000
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
