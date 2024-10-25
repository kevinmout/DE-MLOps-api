import pandas as pd
from pydantic import BaseModel

from helper import Helper


class Feedback(BaseModel):
    input_text: str
    predicted_class: str
    correct_class: str

class FeedbackManager:
    def __init__(self, feedback: Feedback):
        self.feedback = feedback

    def create_feedback_df(self, file_path):
        # Create a DataFrame from the feedback
        df = pd.DataFrame([self.feedback.model_dump()])
        
        # Save DataFrame to a CSV file
        df.to_csv(file_path, index=False)

    def append_feedback_df(self, file_path, content):
        # read the feedback file
        df = Helper.convert_str_to_df(content)
        
        # Creating a new row to add to the DataFrame
        new_row = {"input_text": self.feedback.input_text, "predicted_class": self.feedback.predicted_class, "correct_class": self.feedback.correct_class}

        # Adding the new row to the DataFrame
        df = df._append(new_row, ignore_index=True)

        # Save DataFrame to a CSV file
        df.to_csv(file_path, index=False)
