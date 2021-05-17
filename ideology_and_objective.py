from data_reader import DataReader
from conditional_probability import IDEOLOGY_MAP
from conditional_prob_obj import OBJECTIVE_MAP
import pandas as pd


class IdeologicalObjectiveModule:
    def __init__(self):
        data_obj = DataReader()
        df = data_obj.get_pandas_df()
        self.pk = "NAGcode_1"
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

    def ideology_exists(self, nag_id):
        ideologies = self.get_ideology(nag_id)
        _id = {"leftist", "religious", "ethno_nationalist"}
        flag = -1
        for ideology in ideologies:
            if ideology in _id:
                flag = 1
                break
            elif ideology == 'no_ideology':
                flag = 0
        return flag

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



