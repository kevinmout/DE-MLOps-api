import pandas as pd
from pydantic import BaseModel

from helper import Helper


class Feedback(BaseModel):
    input_text: str
    predicted_class: int
    correct_class: int

class FeedbackManager:
    CLASS_MAP = {'positive': 2, 'neutral': 1, 'negative': 0}

    def __init__(self, feedback_input):
        # Convert `predicted_class` and `correct_class` to integer values
        self.feedback = Feedback(
            input_text=feedback_input.input_text,
            predicted_class=self.CLASS_MAP.get(feedback_input.predicted_class, -1),
            correct_class=self.CLASS_MAP.get(feedback_input.correct_class, -1)
        )


    def create_feedback_df(self, file_path):
        # Create a DataFrame from the feedback
        df = pd.DataFrame([self.feedback.dict()])
        
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
