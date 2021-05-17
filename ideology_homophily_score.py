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
        return_dict = {}
        for ideology in self.ideologies:
            num_score = ideo_dict.get(ideology, np.nan)
            denum_score = num_of_nags
            score = num_score / float(denum_score) if denum_score != 0 else np.nan
            return_dict[ideology+"_score"] = score
        sorted_ideo_dict = sorted({i:j for i,j in return_dict.items() if not pd.isna(j)}, key=return_dict.get, reverse=True)
        print(return_dict)
        print(sorted_ideo_dict)
        return_dict['predominant_ideology'] = sorted_ideo_dict[0].replace("_score", "") if sorted_ideo_dict and \
                                                                     return_dict.get(sorted_ideo_dict[0]) > 0.33 else np.nan
        return_dict['likelihood'] = return_dict.get(sorted_ideo_dict[0]) if sorted_ideo_dict and return_dict['predominant_ideology'] else np.nan
        return_dict.update(ideo_dict)
        return_dict['num_of_nags'] = num_of_nags
        return return_dict

    def get_score(self):
        support_score = {}
        for sup_code in self.sup_obj.get_supporter_codes():
            print(sup_code)
            ideo_list = []
            nag_list = self.sup_obj.get_nags_from_support(sup_code)
            for nag_code in nag_list:
                nag_ideologies = self.ideology_obj.get_ideology(nag_code)
                ideo_list.extend(nag_ideologies)
            return_dict = self.get_ideology_wise_score(ideo_list, len(nag_list))
            support_score[sup_code] = return_dict
        columns = ['supporter_COW', 'StateSupporter', 'num_of_nags']+self.ideologies+\
                  [i+"_score" for i in self.ideologies] + ['predominant_ideology', 'likelihood']
        support_country_homophilly_df = pd.DataFrame(columns=columns)
        support_score_list = [i for i in support_score]
        support_country_homophilly_df['supporter_COW'] = support_score_list
        support_country_homophilly_df['StateSupporter'] = [self.sup_obj.get_support_name(i) for i in support_score_list]
        support_country_homophilly_df['num_of_nags'] = [support_score.get(i).get("num_of_nags") for i in support_score_list]
        support_country_homophilly_df['predominant_ideology'] = [support_score.get(i).get("predominant_ideology") for i in support_score_list]
        support_country_homophilly_df['likelihood'] = [support_score.get(i).get("likelihood") for i in support_score_list]
        for ideology in self.ideologies:
            support_country_homophilly_df[ideology] = [support_score.get(i).get(ideology, np.nan) for i in support_score_list]
            support_country_homophilly_df[ideology+"_score"] = [support_score.get(i).get(ideology+"_score", np.nan) for i in support_score_list]
        support_country_homophilly_df.to_csv("files/supporter_homophilly_ideology_score.csv", index=False)


if __name__ == "__main__":
    obj = IdeologyHomophillyScore()
    obj.get_score()
