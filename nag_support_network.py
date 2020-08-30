from data_reader import DataReader
import numpy as np
import networkx as nx
from copy import deepcopy


class NAGSupportNetwork:
    def __init__(self):
        data_obj = DataReader()
        self.pk = "nagcode_1"
        self.df = data_obj.get_pandas_df()
        self.mode_map = {
            "active": "statesup",
            "defacto": "defacto"
        }
        self.memory = {}
        centralities = ["in-degree", "betweenness", "closeness"]
        self.selected_columns = ["{}_{}_centrality".format(mode, c) for c in centralities for mode in self.mode_map ]

    def get_unique(self, header):
        print(self.df.columns)
        return self.df[header].unique()

    def filter_df(self, mode, year):
        replace_map = {
            np.nan: "No territory",
            "":"No territory",
            "-":"No territory",
            ".": "No territory",
            0: "No territory",
            "0": "No territory"
        }

        no_label = [np.nan, "", ".", "-", 0, "0"]
        df = self.df[~self.df['supporter'].isin(no_label)]
        df = deepcopy(df[(df[self.mode_map[mode]] >= 1) & (df['year'] == year)])
        df['terr'] = df['terr'].replace(replace_map)
        df = df.groupby(['supporter', 'terr'])[self.pk].count().reset_index()
        df.columns = ["Support state", "NAG territory", "Count"]
        return df

    def filter_df_overall(self, mode, bb):
        replace_map = {
            np.nan: "No territory",
            "":"No territory",
            "-":"No territory",
            ".": "No territory",
            0: "No territory",
            "0": "No territory"
        }

        no_label = [np.nan, "", ".", "-", 0, "0"]
        df = deepcopy(self.df[~self.df['supporter'].isin(no_label)])
        df = deepcopy(df[(df[self.mode_map[mode]] >= 1) & (df['year'] < bb)])
        df['terr'] = df['terr'].replace(replace_map)
        df = df.drop_duplicates(subset=['supporter', 'terr', 'year'], keep='first')
        df = df.groupby(['supporter', 'terr'])[self.pk].count().reset_index()
        df.columns = ["Support state", "NAG territory", "Count"]
        return df

    def filter_territories(self, object, territories):
        return {i:j for i,j in object.items() if i in territories}

    def centralities(self, G):
        c = {
            "in-degree": nx.in_degree_centrality(G),
            "betweenness": nx.betweenness_centrality(G),
            "closeness": nx.closeness_centrality(G)
        }
        return c

    def memory_exists(self, memory_name):
        if memory_name in self.memory:
            return True
        return False

    def memorise(self, memory_name, value):
        self.memory[memory_name] = value

    def get_memory(self, memory_name, terr):
        memory = self.memory[memory_name]
        mode = memory_name.split('_')[0]
        object = {}
        for network_centralities in memory:
            name = "{}_{}_centrality".format(mode, network_centralities)
            object[name] = memory[network_centralities].get(terr, 0)
        return object

    def create_network(self, mode, terr, year=None, bb=None):
        memory_name = "{}_{}".format(mode, year) if mode and year else "{}_{}".format(mode, bb)
        if not self.memory_exists(memory_name):
            if year:
                df = self.filter_df(mode, year)
            else:
                df = self.filter_df_overall(mode, bb)
            G = nx.DiGraph()
            for index, row in df.iterrows():
                support, terr, weight = row["Support state"], row["NAG territory"], row["Count"]
                G.add_edge(support, terr, weight=weight)
            value = self.centralities(G)
            self.memorise(memory_name, value)
        return self.get_memory(memory_name, terr)

    def create_network_overall(self):
        print (self.filter_df_overall())



if __name__ == "__main__":
    obj = NAGSupportNetwork()
    # print (obj.create_network_overall())
    print (obj.create_network("active",'Cambodia' ,year=2000))
    print (obj.create_network("active",'No territory' ,year=2000))