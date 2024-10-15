import torch
from transformers import AutoTokenizer, BertForSequenceClassification


class Prediction:
    
    @staticmethod
    def classification(input_text):
        #Load saved model and tokenizer
        model_path = "./saved_model"  #Adjust this path if needed

        #Load the pre-trained BERT model
        best_model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)
        best_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        #Load the tokenizer
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

        #Tokenize the input text
        inputs = tokenizer(
            input_text,
            padding=True,
            truncation=True,
            return_tensors="pt"  #Return PyTorch tensors
        )

        #Set the model to evaluation mode (important for inference)
        best_model.eval()

        #Run the input through the model (no gradients needed)
        with torch.no_grad():
            outputs = best_model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

        #Get the predicted label (highest softmax probability)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).detach().cpu().numpy()[0]  # Detach and convert to NumPy

        #Map the predicted class to sentiment labels
        label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}  # Adjust the mapping as per your label encoding
        predicted_label = label_map[predicted_class]

        #Return the predicted class label
        return predicted_label