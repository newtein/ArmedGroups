from data_reader import DataReader
from copy import deepcopy

OBJECTIVE_MAP = {
            "toppling_an_existing_leadership": 'nagobj_1',
            "change_of_regime_type": 'nagobj_2',
            "demands_for_autonomy": 'nagobj_3',
            "territorial_demand": 'nagobj_4',
            "demands_for_policy_change": 'nagobj_5',
            "other": 'nagobj_6'
        }


class ObjectiveProbabilityModule:
    def __init__(self):
        data_obj = DataReader()
        df = data_obj.get_pandas_df()
        self.pk = "nagcode_1"
        self.df = df.groupby(self.pk).agg(set).reset_index()

    def get_objective_probability(self, nag_id):
        df = deepcopy(self.df)

        return self.get_memory(memory_name)