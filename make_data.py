from data_reader import DataReader
from get_milestone_years import NAGMilestone
from DeprivationScore import DeprivationModule
from nag_support_network import NAGSupportNetwork
from conditional_probability import IdeologicalProbabilityModule
from conditional_prob_obj import ObjectiveProbabilityModule
from ideology_and_objective import IdeologicalObjectiveModule
from battle_related_deaths import BRDModule
from get_longevity import LongevityModule
import pandas as pd
import numpy as np


class MakeData:
    def __init__(self):
        self.milestone_object = NAGMilestone()
        self.deprivation_object = DeprivationModule()
        self.nag_network_object = NAGSupportNetwork()
        self.ideology_object = IdeologicalProbabilityModule()
        self.objective_object = ObjectiveProbabilityModule()
        self.io = IdeologicalObjectiveModule()
        self.brd_object = BRDModule()
        self.longevity_object = LongevityModule()
        self.filter_features = ["terr", "target", "supporter"] + self.milestone_object.selected_columns
        self.pk = "nagcode_1"
        columns = ["nagcode_1", "nag_name", "terr"]
        concat = ["nagcode_1", "target", "supporter"]
        t_df1 = self.get_non_duplictaes(columns)
        t_df1['terr'] = t_df1['terr'].fillna('No territory')
        t_df2 = self.get_aggregate_columns(concat)
        self.df = t_df1.merge(t_df2, on='nagcode_1')
        self.unique_nag_ids = self.df[self.pk].unique().tolist()
        self.df.to_csv("output/NAG_DETAILS.csv", index=False)

        # Milestones
        t_df4 = self.get_milestones(self.unique_nag_ids)
        t_df4.to_csv("output/MILESTONE_YEARS.csv", index=False)
        self.df = self.df.merge(t_df4, on='nagcode_1')
        self.df.to_csv("output/NAG_DETAILS_v2.csv", index=False)

        # Getting deprivation
        t_df3 = self.get_deprivation_score(self.unique_nag_ids)
        t_df3.to_csv("output/DEPRIVATION_SCORE.csv", index=False)
        self.df = self.df.merge(t_df3, on='nagcode_1')
        self.df.to_csv("output/NAG_DETAILS_v3.csv", index=False)

        # Territory
        t_df5 = self.get_territory_network_score(self.df)
        t_df5.to_csv("output/TERRITORY_SUPPORT_NETWORK_CENTRALITY.csv", index=False)
        self.df = self.df.merge(t_df5, on='nagcode_1')
        self.df.to_csv("output/NAG_DETAILS_v4.csv", index=False)

        # Ideology
        t_df6 = self.get_global_trends_in_ideology(self.df)
        t_df6.to_csv("output/GLOBAL_TRENDS_IN_IDEOLOGY.csv", index=False)
        self.df = self.df.merge(t_df6, on='nagcode_1')
        self.df.to_csv("output/NAG_DETAILS_v5.csv", index=False)

        # Objective
        t_df7 = self.get_global_trends_in_objective(self.df)
        t_df7.to_csv("output/GLOBAL_TRENDS_IN_OBJECTIVE.csv", index=False)
        self.df = self.df.merge(t_df7, on='nagcode_1')
        self.df.to_csv("output/NAG_DETAILS_v6.csv", index=False)

        # BRD
        t_df8 = self.get_years_from_brd(self.unique_nag_ids)
        t_df8.to_csv("output/BRD_Analysis.csv", index=False)
        select_cols = [self.pk] + self.brd_object.selected_columns
        self.df = self.df.merge(t_df8[select_cols], on='nagcode_1')
        self.df.to_csv("output/NAG_DETAILS_v7.csv", index=False)

        # Longevity
        t_df9 = self.get_longevity(self.unique_nag_ids)
        t_df9.to_csv("output/Longevity.csv", index=False)
        self.df = self.df.merge(t_df9, on='nagcode_1')
        columns =[i for i in self.df.columns if i not in self.filter_features]
        self.df[columns].to_csv("output/NAG_DETAILS_v8.csv", index=False)

        print(self.df.shape)

    def get_milestones(self, nag_ids):
        columns = [self.pk] + self.milestone_object.selected_columns
        df_t = pd.DataFrame(columns=columns)
        for nag_id in nag_ids:
            milestones = self.milestone_object.get_milestone_years(nag_id)
            milestones.update({self.pk: nag_id})
            df_t = df_t.append(milestones, ignore_index=True)
        return df_t

    def get_deprivation_score(self, nag_ids):
        columns = [self.pk] + self.deprivation_object.write_columns
        df_t = pd.DataFrame(columns=columns)
        for nag_id in nag_ids:
            dep_scores = self.deprivation_object.get_deprivation_score(nag_id)
            dep_scores.update({self.pk: nag_id})
            df_t = df_t.append(dep_scores, ignore_index=True)
        return df_t

    def get_territory_network_score(self, df):
        columns = self.nag_network_object.selected_columns
        columns = [self.pk] + ["{}_{}".format(c, i) for i in ['bb','y1', 'y2', 'y3', 'y4', 'y5'] for c in columns]
        df_t = pd.DataFrame(columns=columns)
        for index, row in df.iterrows():
            nag_id, terr = row[self.pk], row['terr']
            years = [row[col] for col in self.milestone_object.selected_columns]
            born_before = years[0]
            network_wrap = {}
            for year, nom in zip(years, ['y1', 'y2', 'y3', 'y4', 'y5']):
                rs1 = self.nag_network_object.create_network("active", terr, year=year)
                rs2 = self.nag_network_object.create_network("defacto", terr, year=year)
                rs1 = {"{}_{}".format(key, nom): value for key, value in rs1.items()}
                rs2 = {"{}_{}".format(key, nom): value for key, value in rs2.items()}
                network_wrap.update(rs1)
                network_wrap.update(rs2)
            rs1 = self.nag_network_object.create_network("active", terr, bb=born_before)
            rs2 = self.nag_network_object.create_network("defacto", terr, bb=born_before)
            rs1 = {"{}_bb".format(key): value for key, value in rs1.items()}
            rs2 = {"{}_bb".format(key): value for key, value in rs2.items()}
            network_wrap.update(rs1)
            network_wrap.update(rs2)
            network_wrap.update({self.pk: nag_id})
            df_t = df_t.append(network_wrap, ignore_index=True)
        return df_t

    @staticmethod
    def init_ideology_object():
        c = {}
        columns = ["ideology(s)", "number_of_ideologies"]
        for year in ['bb','y1', 'y2', 'y3', 'y4', 'y5']:
            key1 = "ideology_active_support_trend_{}".format(year)
            c[key1] = []
            columns.append(key1)
        for year in ['bb','y1', 'y2', 'y3', 'y4', 'y5']:
            key1 = "ideology_defacto_support_trend_{}".format(year)
            c[key1] = []
            columns.append(key1)
        return c, columns

    @staticmethod
    def init_objective_object():
        c = {}
        columns = ["objective(s)", "number_of_objectives"]
        for year in ['bb','y1', 'y2', 'y3', 'y4', 'y5']:
            key1 = "objective_active_support_trend_{}".format(year)
            c[key1] = []
            columns.append(key1)
        for year in ['bb','y1', 'y2', 'y3', 'y4', 'y5']:
            key1 = "objective_defacto_support_trend_{}".format(year)
            c[key1] = []
            columns.append(key1)
        return c, columns

    def get_global_trends_in_ideology(self, df):
        _, columns = self.init_ideology_object()
        columns = [self.pk] + columns
        df_t = pd.DataFrame(columns=columns)
        for index, row in df.iterrows():
            nag_id = row[self.pk]
            print(nag_id)
            years = [row[col] for col in self.milestone_object.selected_columns]
            born_before = years[0]
            ideologies = self.io.get_ideology(nag_id)
            column_wrap, _ = self.init_ideology_object()
            for ideology in ideologies:
                for year, nom in zip(years, ['y1', 'y2', 'y3', 'y4', 'y5']):
                    p1 = self.ideology_object.get_ideological_probability("active", ideology, year=year)
                    p2 = self.ideology_object.get_ideological_probability("defacto", ideology, year=year)
                    key1 = "ideology_active_support_trend_{}".format(nom)
                    key2 = "ideology_defacto_support_trend_{}".format(nom)
                    column_wrap[key1].append(p1)
                    column_wrap[key2].append(p2)
                p1 = self.ideology_object.get_ideological_probability("active", ideology, bb=born_before)
                p2 = self.ideology_object.get_ideological_probability("defacto", ideology, bb=born_before)
                key1 = "ideology_active_support_trend_bb"
                key2 = "ideology_defacto_support_trend_bb"
                column_wrap[key1].append(p1)
                column_wrap[key2].append(p2)
            column_wrap.update({self.pk: nag_id})
            for key in list(column_wrap):
                value = column_wrap[key]
                if type(value) == list:
                    value = [i for i in value if i]
                    column_wrap[key] = np.mean(value) if value else None
            column_wrap.update({"ideology(s)": ideologies})
            column_wrap.update({"number_of_ideologies": len(ideologies) if ideologies else 0})
            df_t = df_t.append(column_wrap, ignore_index=True)
        return df_t

    def get_global_trends_in_objective(self, df):
        _, columns = self.init_objective_object()
        columns = [self.pk] + columns
        df_t = pd.DataFrame(columns=columns)
        for index, row in df.iterrows():
            nag_id = row[self.pk]
            print(nag_id)
            years = [row[col] for col in self.milestone_object.selected_columns]
            born_before = years[0]
            objectives = self.io.get_objective(nag_id)
            column_wrap, _ = self.init_objective_object()
            for objective in objectives:
                for year, nom in zip(years, ['y1', 'y2', 'y3', 'y4', 'y5']):
                    p1 = self.objective_object.get_objective_probability("active", objective, year=year)
                    p2 = self.objective_object.get_objective_probability("defacto", objective, year=year)
                    key1 = "objective_active_support_trend_{}".format(nom)
                    key2 = "objective_defacto_support_trend_{}".format(nom)
                    column_wrap[key1].append(p1)
                    column_wrap[key2].append(p2)
                p1 = self.objective_object.get_objective_probability("active", objective, bb=born_before)
                p2 = self.objective_object.get_objective_probability("defacto", objective, bb=born_before)
                key1 = "objective_active_support_trend_bb"
                key2 = "objective_defacto_support_trend_bb"
                column_wrap[key1].append(p1)
                column_wrap[key2].append(p2)
            column_wrap.update({self.pk: nag_id})
            for key in list(column_wrap):
                value = column_wrap[key]
                if type(value) == list:
                    value = [i for i in value if i]
                    column_wrap[key] = np.mean(value) if value else None
            column_wrap.update({"objective(s)": objectives})
            column_wrap.update({"number_of_objectives": len(objectives) if objectives else 0})
            df_t = df_t.append(column_wrap, ignore_index=True)
        return df_t

    def get_years_from_brd(self, nag_ids):
        aux_cols = ["year_of_first_observation", "brd1_year", "brd2_year"]
        columns = [self.pk] + aux_cols + self.brd_object.selected_columns
        df_t = pd.DataFrame(columns=columns)
        for nag_id in nag_ids:
            _, _, brd_dict = self.brd_object.get_years_from_brd1and2(nag_id)
            brd_dict.update({self.pk: nag_id})
            df_t = df_t.append(brd_dict, ignore_index=True)
        return df_t

    def get_longevity(self, nag_ids):
        columns = [self.pk, "lifespan"]
        df_t = pd.DataFrame(columns=columns)
        for nag_id in nag_ids:
            longevity, _, _ = self.longevity_object.calculate_longevity(nag_id)
            longevity_dict = {self.pk: nag_id,
                              "lifespan": longevity}
            df_t = df_t.append(longevity_dict, ignore_index=True)
        return df_t

    def get_non_duplictaes(self, columns):
        data_obj = DataReader()
        df = data_obj.get_pandas_df()
        df = df.drop_duplicates(self.pk, keep='first').reset_index()
        df = df[columns]
        return df

    def get_aggregate_columns(self, columns):
        data_obj = DataReader()
        df = data_obj.get_pandas_df()
        df = df.groupby(self.pk).agg(set).reset_index()
        df = df[columns]
        df['number_of_supporters'] = df['supporter'].apply(lambda x:len([i for i in x if not pd.isna(i)]))
        df['number_of_targets'] = df['target'].apply(lambda x: len([i for i in x if not pd.isna(i)]))
        df['support_target_ratio'] = df['number_of_supporters']/df['number_of_targets']
        return df


if __name__ == "__main__":
    obj = MakeData()
