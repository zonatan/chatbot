import json
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
from database import get_feedback_data, get_rating_data, init_db

def train_model():
    init_db()  # Ensure tables exist
    feedback_data = get_feedback_data()
    if not feedback_data:
        print("Tidak ada data pelatihan, menggunakan model default.")
        return None, None
    
    # Prepare data for BERT
    texts, intents = zip(*feedback_data)
    intent_map = {"greeting": 0, "question": 1, "statement": 2, "custom": 3}
    labels = [intent_map.get(intent, 3) for intent in intents]
    
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    encodings = tokenizer(list(texts), truncation=True, padding=True, max_length=128)
    
    class Dataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    dataset = Dataset(encodings, labels)
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=4)
    
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )
    
    trainer.train()
    return model, tokenizer

def update_responses(input_text, response_text, intent, responses):
    with open("responses.json", "r") as f:
        data = json.load(f)
    
    if intent not in data:
        data[intent] = {}
    data[intent][input_text] = {"response": response_text, "score": 1.0}  # Initial score
    
    # Update score based on ratings
    ratings = get_rating_data()
    for rated_input, _, score in ratings:
        if rated_input == input_text:
            data[intent][input_text]["score"] = max(data[intent][input_text]["score"], score / 5.0)
    
    with open("responses.json", "w") as f:
        json.dump(data, f, indent=4)
    
    # Retrain the model
    train_model()

def auto_learn(input_text, response_text, intent, responses):
    # Simple auto-learning: add frequent inputs with high-rated responses
    ratings = get_rating_data()
    input_counts = {}
    for rated_input, _, score in ratings:
        if score >= 4:  # Only learn from high-rated responses
            input_counts[rated_input] = input_counts.get(rated_input, 0) + 1
            if input_counts[rated_input] >= 3:  # Threshold for frequent input
                update_responses(rated_input, response_text, intent, responses)