from data_reader import DataReader
import numpy as np

class SupportModule:
    def __init__(self):
        data_obj = DataReader()
        self.df = data_obj.get_pandas_df()
        self.s_pk = "SupNum_COW"
        self.pk = "NAGcode_1"
        self.s_names = 'StateSupporter'

    def get_supporter_names(self):
        return self.df[self.s_names].unique()

    def get_supporter_codes(self):
        return self.df[self.s_pk].unique()

    def get_support_name(self, support_cow):
        name = self.df[self.df[self.s_pk]==support_cow]['StateSupporter'].unique()
        return name

    def get_nags_from_support(self, support_cow):
        f1 = (self.df[self.s_pk] == support_cow)
        f2 = (self.df['statesup'] == 1)
        df = self.df[f1 & f2]
        return df['NAGcode_1'].unique().tolist()

    def get_supporter_from_NAGcode(self, nag_id):
        f1 = (self.df[self.pk] == nag_id)
        f2 = (self.df['statesup'] == 1)
        df = self.df[f1 & f2]
        return df[self.s_pk].unique().tolist()

    def get_defacto_supporter_from_NAGcode(self, nag_id):
        f1 = (self.df[self.pk] == nag_id)
        f2 = (self.df['defacto'] == 1)
        df = self.df[f1 & f2]
        return df[self.s_pk].unique().tolist()

    def get_lifespan_from_support(self, supporter_COW):
        f1 = (self.df[self.s_pk] == supporter_COW)
        f2 = (self.df['statesup'] == 1)
        t_df = self.df[f1 & f2].groupby([self.pk])['Year'].apply(
            list).reset_index()
        support_lifespan = []
        num_nags = t_df.shape[0]
        for index, row in t_df.iterrows():
            nagcode = row[self.pk]
            yearmin = min(row['Year'])
            yearmax = max(row['Year'])
            support_lifespan.append(yearmax - yearmin + 1)
        data = {
            "supporter_COW": supporter_COW,
            "num_of_nags": num_nags,
            "sup_duration_mean": np.mean(support_lifespan),
            "sup_duration_std": np.std(support_lifespan)
        }
        return data

    def get_active_support_duration(self, nagid, supporter_COW):
        f1 = (self.df[self.s_pk] == supporter_COW)
        f2 = (self.df['statesup'] == 1)
        f3 = (self.df[self.pk] == nagid)
        years = self.df[f1 & f2 & f3]['Year'].tolist()
        return max(years) - min(years) + 1

    def get_defacto_support_duration(self, nagid, supporter_COW):
        f1 = (self.df[self.s_pk] == supporter_COW)
        f2 = (self.df['defacto'] == 1)
        f3 = (self.df[self.pk] == nagid)
        years = self.df[f1 & f2 & f3]['Year'].tolist()
        try:
            return max(years) - min(years) + 1
        except:
            return np.nan

if __name__ == "__main__":
    obj = SupportModule()
    print (obj.get_support_duration(1, 800))