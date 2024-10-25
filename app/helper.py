from io import StringIO
import pandas as pd


class Helper:
    @staticmethod
    def convert_str_to_df(content):
        # Use StringIO to convert the string to a file-like object for pandas
        csv_data = StringIO(content)

        # Use pandas to read the CSV data
        df = pd.read_csv(csv_data)

        return df