import pandas as pd
import csv
from copy import deepcopy
import numpy as np

class DataReader:
    def __init__(self):
        # self.filename = "source_data/pipeFormat.csv"
        self.filename = "source_data/NAG_dataset_26April2020.csv"
        self.sep = "|"
        empty = ['', '.', '-', '_']
        empty_dict = {i:np.nan for i in empty}
        # , sep=self.sep, encoding = "ISO-8859-1"
        self.df = pd.read_csv(self.filename, sep=self.sep, encoding = "ISO-8859-1" )
        # self.df = pd.read_stata(self.filename)
        self.df = self.df.replace(empty_dict)

    def get_pandas_df(self):
        return deepcopy(self.df)

    def get_csv_iter(self):
        with open(self.filename, "r") as f:
            headers = next(f).strip().split(self.sep)
            reader = csv.reader(f, delimiter=self.sep)
            for row in reader:
                yield dict(zip(headers, row))