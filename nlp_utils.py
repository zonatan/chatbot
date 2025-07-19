def process_input(user_input, nlp):
    doc = nlp(user_input.lower())
    intent = "greeting" if any(token.lemma_ in ["hello", "hi", "hey"] for token in doc) else \
             "question" if any(token.tag_ == "WP" for token in doc) else \
             "statement"
    
    entities = {ent.label_: ent.text for ent in doc.ents}
    return intent, entities

def get_response(intent, entities, responses, context, user_id):
    context_data = context.get(user_id, {})
    last_intent = context_data.get("last_intent", "")
    
    if intent == "greeting":
        return responses["greeting"]["default"]
    elif intent == "question":
        if "PERSON" in entities:
            return responses["question"]["person"].format(name=entities["PERSON"])
        if last_intent == "greeting":
            return responses["question"]["after_greeting"]
        return responses["question"]["default"]
    else:
        if "DATE" in entities:
            return responses["statement"]["date"].format(date=entities["DATE"])
        return responses["statement"]["default"]