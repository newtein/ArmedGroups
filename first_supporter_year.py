from data_reader import DataReader
import pandas as pd


class FirstSupportYear:
    def __init__(self):
        data_obj = DataReader()
        self.pk = "nagcode_1"
        self.df = data_obj.get_pandas_df()

    def get_first_support_year(self, nag_id):
        first_support_year = None
        df = self.df[self.df[self.pk] == nag_id]
        yearList = df['year'].tolist()
        supporterList = df['supporter'].tolist()
        for year, supporter in zip(yearList, supporterList):
            if not pd.isna(supporter):
                first_support_year = year
                break
        return first_support_year, supporter
