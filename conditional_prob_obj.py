from data_reader import DataReader
from copy import deepcopy

OBJECTIVE_MAP = {
            "toppling_an_existing_leadership": 'NAGObj_1',
            "change_of_regime_type": 'NAGObj_2',
            "demands_for_autonomy": 'NAGObj_3',
            "territorial_demand": 'NAGObj_4',
            "demands_for_policy_change": 'NAGObj_5',
            "other": 'NAGObj_6'
        }

class ObjectiveProbabilityModule:
    def __init__(self):
        data_obj = DataReader()
        self.df = data_obj.get_pandas_df()
        self.pk = "nagcode_1"
        self.mode_map = {
            "active": "statesup",
            "defacto": "defacto"
        }

        self.objective_map = OBJECTIVE_MAP
        self.memory = {}

    def memory_exists(self, memory_name):
        if memory_name in self.memory:
            return True
        return False

    def memorise(self, memory_name, value):
        self.memory[memory_name] = value

    def get_memory(self, memory_name):
        memory = self.memory[memory_name]
        return memory

    def get_objective_probability(self, mode, objective, year=None, bb=None):
        df = deepcopy(self.df)
        memory_name = "{}_{}_{}".format(mode, objective, year) if year else "{}_{}_{}".format(mode, objective, bb)
        if not self.memory_exists(memory_name):
            # df[self.objective_map[objective]] = df[self.objective_map[objective]].fillna(0)
            if year:
                df = df[df['year']==year]
                objective_filter = ((df[self.objective_map[objective]].astype(str).str.contains('1')) | (df[self.objective_map[objective]] == 1))
                nag_total = df[objective_filter][self.pk].unique().shape[0]
                nag_with_support = df[objective_filter & (df[self.mode_map[mode]]>=1)][self.pk].unique().shape[0]
            else:
                df = df[df['year'] < bb]
                objective_filter = ((df[self.objective_map[objective]].astype(str).str.contains('1')) | (df[self.objective_map[objective]] == 1))
                nag_total = df[objective_filter][self.pk].unique().shape[0]
                nag_with_support = df[objective_filter & (df[self.mode_map[mode]] >= 1)][self.pk].unique().shape[0]
            value = nag_with_support/nag_total if nag_total !=0 else None
            self.memorise(memory_name, value)
        return self.get_memory(memory_name)

if __name__ == "__main__":
    obj = ObjectiveProbabilityModule()
    for year in range(1945, 1949):
        print(year, obj.get_objective_probability("defacto", "toppling_an_existing_leadership", year=year))