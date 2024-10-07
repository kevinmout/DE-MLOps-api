from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

import tensorflow as tf

import pandas as pd


class Prediction:


    @staticmethod
    def initialize():
        #Load "roberta-base-openai-detector" (source: https://huggingface.co/openai-community/roberta-base-openai-detector)
        model_name = "roberta-base-openai-detector"

        #Load the tokenizer and model from Hugging Face Model Hub
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
        #Save the model and tokenizer
        model.save_pretrained('./saved_model')
        tokenizer.save_pretrained('./saved_tokenizer')
    
    @staticmethod
    def classification(input_text):

        # if the model and tokenizer are not saved, initialize them
        try:
            model = TFAutoModelForSequenceClassification.from_pretrained('./saved_model')
            tokenizer = AutoTokenizer.from_pretrained('./saved_tokenizer')
        except:
            Prediction.initialize()
            model = TFAutoModelForSequenceClassification.from_pretrained('./saved_model')
            tokenizer = AutoTokenizer.from_pretrained('./saved_tokenizer')

        #Load saved model + tokenizer
        model = TFAutoModelForSequenceClassification.from_pretrained('./saved_model')
        tokenizer = AutoTokenizer.from_pretrained('./saved_tokenizer')

        #Tokenize the input text
        inputs = tokenizer(
            input_text,
            return_tensors="tf",
            padding=True,
            truncation=True,
            max_length=512
        )

        #Run the input through the model
        outputs = model(inputs['input_ids'], attention_mask=inputs['attention_mask'])

        #Get the predicted label (highest softmax probability)
        logits = outputs.logits
        predicted_class = tf.argmax(logits, axis=1).numpy()[0]  # Get class with highest score

        #Return the predicted class
        return predicted_class