from data_reader import DataReader
from copy import deepcopy

IDEOLOGY_MAP = {
            "no_ideology": 'NAGID_1',
            "ethno_nationalist": 'NAGID_2',
            "religious": 'NAGID_3',
            "leftist": 'NAGID_4',
            "other": 'NAGID_5'
        }

class IdeologicalProbabilityModule:
    def __init__(self):
        """
        Identity of NAG (Numeric): 1- NOID, 2-
        Ethno-nationalist, 3- religious, 4- leftist, 5-
        other
        'nagid_2', 'nagid_3', 'nagid_4', 'nagid_5',
        """
        data_obj = DataReader()
        self.df = data_obj.get_pandas_df()
        self.pk = "nagcode_1"
        self.mode_map = {
            "active": "statesup",
            "defacto": "defacto"
        }

        self.ideology_map = IDEOLOGY_MAP
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

    def get_ideological_probability(self, mode, ideology, year=None, bb=None):
        df = deepcopy(self.df)
        memory_name = "{}_{}_{}".format(mode, ideology, year) if year else "{}_{}_{}".format(mode, ideology,bb)
        if not self.memory_exists(memory_name):
            # df[self.ideology_map[ideology]] = df[self.ideology_map[ideology]].fillna(0)
            if year:
                df = df[df['year']==year]
                ideology_filter = ((df[self.ideology_map[ideology]].astype(str).str.contains('1')) | (df[self.ideology_map[ideology]] == 1))
                nag_total = df[ideology_filter][self.pk].unique().shape[0]
                nag_with_support = df[ideology_filter & (df[self.mode_map[mode]]>=1)][self.pk].unique().shape[0]
            else:
                df = df[df['year'] < bb]
                ideology_filter = ((df[self.ideology_map[ideology]].astype(str).str.contains('1')) | (df[self.ideology_map[ideology]] == 1))
                nag_total = df[ideology_filter][self.pk].unique().shape[0]
                nag_with_support = df[ideology_filter & (df[self.mode_map[mode]] >= 1)][self.pk].unique().shape[0]
            value = nag_with_support/nag_total if nag_total !=0 else None
            self.memorise(memory_name, value)
        return self.get_memory(memory_name)

if __name__ == "__main__":
    obj = IdeologicalProbabilityModule()
    for year in range(1945, 1949):
        print(year, obj.get_ideological_probability("defacto", "other", year=year))