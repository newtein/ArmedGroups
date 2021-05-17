from data_reader import DataReader
import pickle
import pandas as pd
from collections import Counter
from supporter_countries import SupportModule
from ideology_and_objective import IdeologicalObjectiveModule, IDEOLOGY_MAP
import numpy as np


class IdeologyHomophillyScore:
    def __init__(self):
        self.ideology_obj = IdeologicalObjectiveModule()
        self.ideologies = list(IDEOLOGY_MAP)
        self.sup_obj = SupportModule()

    def get_ideology_wise_score(self, ideo_list, num_of_nags):
        ideo_dict = dict(Counter(ideo_list))
        if 0 not in ideo_dict:
            ideo_dict[0] = 0
        if 1 not in ideo_dict:
            ideo_dict[1] = 0
        print(ideo_dict)
        return_dict = {}
        denum = ideo_dict.get(1) + ideo_dict.get(0)
        if denum != 0:
            return_dict['ideology_percent'] = ideo_dict.get(1) / denum
            return_dict['nonideology_percent'] = ideo_dict.get(0) / denum
        else:
            return_dict['ideology_percent'] = np.nan
            return_dict['nonideology_percent'] = np.nan
        sorted_ideo_dict = sorted({i:j for i,j in return_dict.items() if not pd.isna(j)}, key=return_dict.get, reverse=True)
        return_dict['predominant_ideology'] = sorted_ideo_dict[0].replace("_percent", "") if sorted_ideo_dict and \
                                                                     return_dict.get(sorted_ideo_dict[0]) > 0.5 else np.nan

        return_dict['ideology'] = ideo_dict.get(1)
        return_dict['nonideology'] = ideo_dict.get(0)

        return_dict['likelihood'] = return_dict.get(sorted_ideo_dict[0]) if sorted_ideo_dict and return_dict['predominant_ideology'] else np.nan
        return_dict['num_of_nags'] = num_of_nags
        return return_dict

    def get_score(self):
        support_score = {}
        for sup_code in self.sup_obj.get_supporter_codes():
            print(sup_code)
            ideo_list = []
            nag_list = self.sup_obj.get_nags_from_support(sup_code)
            for nag_code in nag_list:
                ideology_exists = self.ideology_obj.ideology_exists(nag_code)
                ideo_list.append(ideology_exists)
            return_dict = self.get_ideology_wise_score(ideo_list, len(nag_list))
            support_score[sup_code] = return_dict
        columns = ['supporter_COW', 'StateSupporter', 'num_of_nags', 'ideology', 'nonideology']+\
                   ['ideology_percent', 'nonideology_percent', 'predominant_ideology', 'likelihood']
        support_country_homophilly_df = pd.DataFrame(columns=columns)
        support_score_list = [i for i in support_score]
        support_country_homophilly_df['supporter_COW'] = support_score_list
        support_country_homophilly_df['StateSupporter'] = [self.sup_obj.get_support_name(i) for i in support_score_list]
        support_country_homophilly_df['num_of_nags'] = [support_score.get(i).get("num_of_nags") for i in support_score_list]
        support_country_homophilly_df['predominant_ideology'] = [support_score.get(i).get("predominant_ideology") for i in support_score_list]
        support_country_homophilly_df['likelihood'] = [support_score.get(i).get("likelihood") for i in support_score_list]
        for ideology in ['ideology', 'nonideology']:
            support_country_homophilly_df[ideology] = [support_score.get(i).get(ideology, np.nan) for i in support_score_list]
            support_country_homophilly_df[ideology+"_percent"] = [support_score.get(i).get(ideology+"_percent", np.nan) for i in support_score_list]
        support_country_homophilly_df.to_csv("files/binary_supporter_homophilly_ideology_score.csv", index=False)


if __name__ == "__main__":
    obj = IdeologyHomophillyScore()
    obj.get_score()
