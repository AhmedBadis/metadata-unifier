import spacy
import json

def process_text_with_spacy(extracted_text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(extracted_text)

    nlp_output = {
        "tokens": [],
        "entities": [],
        "sentences": [],
        "noun_chunks": []
    }

    for sent in doc.sents:
        sentence = sent.text
        sent_tokens = []
        for token in sent:
            nlp_output["tokens"].append({"token": token.text, "pos": token.pos_})
            sent_tokens.append({
                "token": token.text,
                "pos": token.pos_,
                "dependency": token.dep_,
                "head": token.head.text
            })
        nlp_output["sentences"].append({"sentence": sentence, "tokens": sent_tokens})

    for ent in doc.ents:
        nlp_output["entities"].append({"text": ent.text, "type": ent.label_})

    for chunk in doc.noun_chunks:
        nlp_output["noun_chunks"].append(chunk.text)

    return json.dumps(nlp_output, indent=4), doc