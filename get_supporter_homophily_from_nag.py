from data_reader import DataReader
import pickle
import pandas as pd
from collections import Counter
from supporter_countries import SupportModule
from ideology_and_objective import IdeologicalObjectiveModule, IDEOLOGY_MAP
import numpy as np


class SupporterHomophillyFromNAG:
    def __init__(self):
        self.sup_homo_df = pd.read_csv("files/supporter_homophilly_ideology_score.csv")
        self.lookup = {row['supporter_COW']: dict(zip(self.sup_homo_df, row)) for index, row in self.sup_homo_df.iterrows()}
        self.binary_sup_homo_df = pd.read_csv("files/binary_supporter_homophilly_ideology_score.csv")
        self.binary_lookup = {row['supporter_COW']: dict(zip(self.binary_sup_homo_df, row)) for index, row in self.binary_sup_homo_df.iterrows()}
        self.sup_lifespan_homo_df = pd.read_csv("files/supporter_lifespan_homophilly.csv")
        self.sup_lifespan_lookup = {row['supporter_COW']: dict(zip(self.sup_lifespan_homo_df, row)) for index, row in
                              self.sup_lifespan_homo_df.iterrows()}

    def get_supporter_info(self, support_cow):
        return self.lookup.get(support_cow)

    def get_binary_supporter_info(self, support_cow):
        return self.binary_lookup.get(support_cow)

    def get_lifespan_homophily(self, support_cow):
        return self.sup_lifespan_lookup.get(support_cow)

