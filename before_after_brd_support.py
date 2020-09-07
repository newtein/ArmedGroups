from data_reader import DataReader
from battle_related_deaths import BRDModule
import pandas as pd


class SupportersAfterBeforeBRD:
    def __init__(self):
        data_obj = DataReader()
        self.pk = "nagcode_1"
        self.df = data_obj.get_pandas_df()
        self.brd_obj = BRDModule()


    def get_supporters(self, nag_id):
        first_support_year = None
        df = self.df[self.df[self.pk] == nag_id]
        yearList = df['year'].tolist()
        supporterList = df['supporter'].tolist()
        _, _, respone= self.brd_obj.get_years_from_brd1and2(nag_id)
        brd1_year, brd2_year = respone['brd1_year'], respone['brd2_year']
        years_to_brd1, years_to_brd2 = respone['years_to_brd1'], respone['years_to_brd2']
        before_brd1_supporters, after_brd1_supporters = set(), set()
        before_brd2_supporters, after_brd2_supporters = set(), set()  
        for year, supporter in zip(yearList, supporterList):
            if not pd.isna(supporter):
                if brd1_year:
                    if year < brd1_year:
                        before_brd1_supporters.add(supporter)
                    elif year >= brd1_year:
                        after_brd1_supporters.add(supporter)
                if brd2_year:
                    if year < brd2_year:
                        before_brd2_supporters.add(supporter)
                    elif year >= brd2_year:
                        after_brd2_supporters.add(supporter)
        return (before_brd1_supporters, after_brd1_supporters), (before_brd2_supporters, after_brd2_supporters)
