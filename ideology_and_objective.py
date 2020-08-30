from data_reader import DataReader
from conditional_probability import IDEOLOGY_MAP
from conditional_prob_obj import OBJECTIVE_MAP
import pandas as pd


class IdeologicalObjectiveModule:
    def __init__(self):
        data_obj = DataReader()
        df = data_obj.get_pandas_df()
        self.pk = "nagcode_1"
        self.df = df.groupby(self.pk).agg(set).reset_index()

    def get_ideology(self, nag_id):
        df = self.df[self.df[self.pk]==nag_id]
        _id = set()
        for ideology, ideology_col in IDEOLOGY_MAP.items():
            values = df[ideology_col].tolist()[0]
            for element in values:
                if not pd.isna(element) and '1' in str(element):
                    _id.add(ideology)
                try:
                    if not pd.isna(element) and int(element) == 1:
                        _id.add(ideology)
                except:
                    pass
        return list(_id)

    def get_objective(self, nag_id):
        df = self.df[self.df[self.pk]==nag_id]
        _id = set()
        for objective, objective_col in OBJECTIVE_MAP.items():
            values = df[objective_col].tolist()[0]
            for element in values:
                if not pd.isna(element) and '1' in str(element):
                    _id.add(objective)
                try:
                    if not pd.isna(element) and int(element) == 1:
                        _id.add(objective)
                except:
                    pass
        return list(_id)

if __name__ == "__main__":
    obj = IdeologicalObjectiveModule()
    print(obj.get_ideology(7))
    print(obj.get_objective(7))



