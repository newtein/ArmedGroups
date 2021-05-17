from data_reader import DataReader
from copy import deepcopy

class DSupModule:
    def __init__(self):
        data_obj = DataReader()
        self.df = data_obj.get_pandas_df()
        self.pk = "NAGcode_1"
        self.var = 'Tar_DomSup'
        self.var_pp = 'PolParDummy'

    def get(self, nag_id=None):
        df = self.df[self.df[self.pk] == nag_id]
        domsup = df[self.var].tolist()
        atleast_one = 1 if sum(domsup)>=1 else 0
        return atleast_one, domsup

    def get_political_party(self, nag_id):
        df = self.df[self.df[self.pk] == nag_id]
        pp = df[self.var_pp].tolist()
        atleast_one = 1 if sum(pp) >= 1 else 0
        return atleast_one, pp

if __name__ == "__main__":
    obj = DSupModule()
    print(obj.get(6))
