from cutils.covidclass import CovidFr

class CvCreation():
    """
    docstring for CvCreation
    """
    def __init__(self):
        self.covobject = CovidFr()
        self.covid = self.covobject.load_df()
        self.daily = self.covobject.dailycases(data=self.covid, pca=True)
        self.daily_reg = self.covobject.regiondailycases(data=self.covid, feature='hosp')
 
    def cv_load(self, **kwargs):
        """
        Returns required html page contexte variables
        """
        cv = dict(
            covid_state = kwargs.get('covid_state', False),
            map_covid_reg = self.covobject.map_covid_reg(),
            map_covid_dep = self.covobject.map_covid_dep(),
            charts_impacted_dep = self.covobject.charts_impacted_dep(),
            charts_and_parameters_covid_data = self.covobject.charts_and_parameters_covid_data(),
            charts_pca_global = self.covobject.pca_charts(data=self.daily, pcdim=self.covobject.default_pcdim, normalize=self.covobject.default_normalize, start_d_learn=self.covobject.default_start_d_learn_fr, end_d_learn=self.covobject.default_end_d_learn_fr, alpha=self.covobject.default_alpha),
            charts_pca_hosp_reg = self.covobject.pca_charts(data=self.daily, pcdim=self.covobject.default_pcdim_reg, normalize=self.covobject.default_normalize_reg, start_d_learn=self.covobject.default_start_d_learn_fr_reg, end_d_learn=self.covobject.default_end_d_learn_fr_reg, alpha=self.covobject.default_alpha_reg),
            label = self.covobject.request_label(),
            department = self.covobject.default_department,
            region = self.covobject.default_region,
            first_day_fr = self.covobject.first_day_fr,
            last_day_fr = self.covobject.last_day_fr,
            map_choice = self.covobject.map_choice,
            criterion_choice = self.covobject.criterion_choice,
            number_all_dep = self.covobject.number_all_dep,
            global_pc = self.covobject.global_pc,
            normalize_states = self.covobject.normalize_states,
            alpha_smooth = self.covobject.alpha_smooth,
            pc_reg = self.covobject.pc_reg,
            map_select = self.covobject.default_map_select,
            top_dep = self.covobject.default_top_dep,
            criterion_select = self.covobject.default_criterion_select,
            pcdim = self.covobject.default_pcdim,
            normalize = self.covobject.default_normalize,
            start_d_learn_fr = self.covobject.default_start_d_learn_fr,
            end_d_learn_fr = self.covobject.default_end_d_learn_fr,
            alpha = self.covobject.default_alpha,
            pcdim_reg = self.covobject.default_pcdim_reg,
            normalize_reg = self.covobject.default_normalize_reg,
            start_d_learn_fr_reg = self.covobject.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = self.covobject.default_end_d_learn_fr_reg,
            alpha_reg = self.covobject.default_alpha_reg,
        )
        return self.covobject, self.daily, self.daily_reg, cv