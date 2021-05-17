from data_reader import DataReader


class DeprivationModule:
    def __init__(self):
        data_obj = DataReader()
        self.df = data_obj.get_pandas_df()
        self.pk = "NAGcode_1"
        self.selected_columns = ['statesup', 'defacto']
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

    @staticmethod
    def availability(a):
        n = len(a)
        count = 1
        num, denum = 0, 0
        for i in a:
            if i >= 1:
                num += count / n
            denum += count / n
            count += 1
        return num / float(denum)

    def get_deprivation_score(self, nag_id):
        df = self.df[self.df[self.pk] == nag_id]
        df = df.groupby('Year')[self.selected_columns].sum().reset_index()
        df = df.sort_values('Year')
        deprivation_object = {}
        for column in self.selected_columns:
            timeline = df[column].tolist()
            deprivation_score = self.calculated_weighted_mean(timeline)
            column1 = "{}_dep_score".format(column)
            availability_score = self.availability(timeline)
            column2 = "{}_avail_score".format(column)
            deprivation_object[column1] = deprivation_score
            deprivation_object[column2] = availability_score
        return deprivation_object


if __name__ == "__main__":
    obj = DeprivationModule()
    print(obj.get_deprivation_score(1))
    #print (obj.get_deprivation_score(2))
