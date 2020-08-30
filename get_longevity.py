from data_reader import DataReader
from copy import deepcopy

class LongevityModule:
    def __init__(self):
        data_obj = DataReader()
        self.df = data_obj.get_pandas_df()
        self.pk = "nagcode_1"

    def calculate_longevity(self, nag_id=None):
        df = self.df[self.df[self.pk] == nag_id]
        yearList = df['year'].tolist()
        max_year, min_year = max(yearList), min(yearList)
        return max_year-min_year+1, min_year, max_year

if __name__ == "__main__":
    obj = LongevityModule()
    print(obj.calculate_longevity(6))
    print (obj.calculate_longevity(7))
    print(obj.calculate_longevity(8))