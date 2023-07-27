import spacy

def classify_verb(verb):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(verb)
    return doc[0].lemma_

def detect_setting(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    location_terms = []
    for token in doc:
        if token.pos_ == "NOUN" and token.dep_ in ("pobj", "dobj"):
            location_terms.append(token.text)

    return location_terms

def water(array):
    nlp = spacy.load("en_core_web_sm")
    for i in array:
         if i.lower() == "water":
            return True