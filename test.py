import spacy

nlp = spacy.load("en_core_web_sm")

def extract_settings(text):
    doc = nlp(text)

    settings = set()
    for token in doc:
        if token.dep_ == "pobj" or token.dep_ == "prep" or token.dep_ == "dobj":
            if token.pos_ == "NOUN":
                settings.add(token.text.lower())

    return settings

input_text = "Jesus walks on water, Jacob was praying while flying a gun, rock, and a sword. Goliath was walking down the street while flying a slingshot. Moses is talking in the mountains."

settings = extract_settings(input_text)
print(settings)
