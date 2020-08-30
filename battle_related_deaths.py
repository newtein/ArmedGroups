from data_reader import DataReader
import pandas as pd


class BRDModule:
    def __init__(self):
        data_obj = DataReader()
        self.pk = "nagcode_1"
        self.df = data_obj.get_pandas_df()
        self.selected_columns = ["years_to_brd1", "years_to_brd2"]

    def create_brd_year(self, brd):
        if not pd.isna(brd):
            if '/' in brd:
                brd = brd.split('/')[-1]
                brd = '19' + brd if 21 <= int(brd) <= 99 else '20' + brd
            elif '-' in brd:
                brd = brd.split('-')[-1]
            else:
                print(brd)
            return int(brd)
        return None


    def get_years_from_brd1and2(self, nag_id):
        """
        Todo: try to convert brd days intead of substraction of years
        :param nag_id:
        :return:
        """
        df = self.df[self.df[self.pk] == nag_id]
        foundational_year = min(df['year'].tolist())
        brd1, brd2 = None, None
        for index, row in df.iterrows():
            brd1 = row['startdate1']
            brd2 = row['startdate2']
            if brd1 or brd2:
                break
        if brd1 is not None:
            brd1 = self.create_brd_year(brd1)
        if brd2 is not None:
            brd2 = self.create_brd_year(brd2)
        brd1_diff, brd2_diff = None, None
        if brd1:
            brd1_diff = 0 if (brd1-foundational_year)<0 else brd1-foundational_year
        if brd2:
            brd2_diff = 0 if (brd2-foundational_year)<0 else brd2-foundational_year
        response = {
            "year_of_first_observation": foundational_year,
            "brd1_year": brd1,
            "brd2_year": brd2,
            "years_to_brd1": brd1_diff,
            "years_to_brd2": brd2_diff
        }
        return (brd1_diff, brd2_diff), (brd1, brd2), response


if __name__ == "__main__":
    obj = BRDModule()
    print(obj.get_years_from_brd1and2(6))
    print (obj.get_years_from_brd1and2(7))
    print(obj.get_years_from_brd1and2(8))