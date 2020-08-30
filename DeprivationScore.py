from data_reader import DataReader


class DeprivationModule:
    def __init__(self):
        data_obj = DataReader()
        self.df = data_obj.get_pandas_df()
        self.pk = "nagcode_1"
        self.selected_columns = ['s_safemem', 's_safelead',
                        's_headquar', 's_traincamp',
                        's_training', 's_weaponlog',
                        's_finaid', 's_transport',
                        's_troop',
                        'ds_safemem',
                        'ds_safelead', 'ds_headquar',
                        'ds_traincamp', 'ds_training',
                        'ds_weaponlog', 'ds_finaid',
                        'ds_transport',
                        'domsup']
        self.write_columns = ["{}_dep_score".format(column) for column in self.selected_columns]

    def print_columns(self):
        return self.df.columns

    def get_unique(self, header):
        return self.df[header].unique()

    @staticmethod
    def calculated_weighted_mean(a):
        n = len(a)
        count = 1
        num, denum = 0, 0
        for i in a:
            if i == 0:
                num += count / n
            denum += count / n
            count += 1
        return num / float(denum)

    def get_deprivation_score(self, nag_id):
        df = self.df[self.df[self.pk] == nag_id]
        df = df.groupby('year')[self.selected_columns].sum().reset_index()
        deprivation_object = {}
        for column in self.selected_columns:
            timeline = df[column].tolist()
            deprivation_score = self.calculated_weighted_mean(timeline)
            column = "{}_dep_score".format(column)
            deprivation_object[column] = deprivation_score
        return deprivation_object


if __name__ == "__main__":
    obj = DeprivationModule()
    print(obj.get_deprivation_score(1))
    print (obj.get_deprivation_score(2))
