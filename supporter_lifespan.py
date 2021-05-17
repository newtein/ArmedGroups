from data_reader import DataReader
import pickle
import pandas as pd
from collections import Counter
from supporter_countries import SupportModule
from ideology_and_objective import IdeologicalObjectiveModule, IDEOLOGY_MAP
import numpy as np


class SupporterLifespan:
    def __init__(self):
        self.sup_obj = SupportModule()

    def get_score(self):
        support_score = {}
        for sup_code in self.sup_obj.get_supporter_codes():
            return_dict = self.sup_obj.get_lifespan_from_support(sup_code)
            support_score[sup_code] = return_dict
        columns = ["supporter_COW", 'StateSupporter', "num_of_nags", "sup_duration_mean","sup_duration_std"]
        support_country_homophilly_df = pd.DataFrame(columns=columns)
        support_score_list = [i for i in support_score]
        support_country_homophilly_df['supporter_COW'] = support_score_list
        support_country_homophilly_df['StateSupporter'] = [self.sup_obj.get_support_name(i) for i in support_score_list]
        for col in ['num_of_nags', "sup_duration_mean","sup_duration_std"]:
            support_country_homophilly_df[col] = [support_score.get(i).get(col, np.nan) for i in
                                                       support_score_list]
        support_country_homophilly_df.to_csv("files/supporter_lifespan_homophilly.csv", index=False)


if __name__ == "__main__":
    obj = SupporterLifespan()
    obj.get_score()