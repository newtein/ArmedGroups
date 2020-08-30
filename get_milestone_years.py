from get_longevity import LongevityModule
from battle_related_deaths import BRDModule


class NAGMilestone:
    def __init__(self):
        self.pk = "nagcode_1"
        self.longevity_obj = LongevityModule()
        self.brd_module = BRDModule()
        self.selected_columns = ["year_of_first_observation(y1)", "brd1_year(y2)", "brd2_year(y3)",
                                 "year_of_second_last_observation(y4)", "year_of_last_observation(y5)"]

    def get_last_second_year(self, born_year, dead_year):
        last_second_year = dead_year-1
        if last_second_year<=born_year:
            last_second_year=born_year
        return last_second_year

    def get_milestone_years(self, nag_id):
        _, born_year, dead_year = self.longevity_obj.calculate_longevity(nag_id)
        brd1_year, brd2_year = self.brd_module.get_years_from_brd1and2(nag_id)[1]
        last_second_year = self.get_last_second_year(born_year, dead_year)
        return {"year_of_first_observation(y1)": born_year, "brd1_year(y2)":brd1_year, "brd2_year(y3)": brd2_year,
                "year_of_second_last_observation(y4)": last_second_year, "year_of_last_observation(y5)": dead_year}

if __name__ == "__main__":
    obj = NAGMilestone()
    print(obj.get_milestone_years(20))
