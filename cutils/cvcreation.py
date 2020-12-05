
class CvCreation():
    """docstring for CvCreation"""

    def __init__(self, classinstance):
        self.classinstance = classinstance

    def cv_load(self, daily, daily_reg, covid_state, positive_state):
        return dict(
            covid_state = covid_state,
            positive_state = positive_state,
            map_covid_reg = self.classinstance.overall_regions_data_as_json(),
            map_covid_dep = self.classinstance.overall_departments_data_as_json(),
            map_positive_reg = self.classinstance.overall_regions_positive_data_as_json(),
            map_positive_dep = self.classinstance.overall_departments_positive_data_as_json(),
            charts_impacted_dep = self.classinstance.charts_impacted_dep(),
            charts_and_parameters_positive_data = self.classinstance.charts_positive_data(),
            charts_and_parameters_covid_data = self.classinstance.charts(),
            charts_pca_global = self.classinstance.pca_charts(data=daily, pcdim=self.classinstance.default_pcdim, normalize=self.classinstance.default_normalize, start_d_learn=self.classinstance.default_start_d_learn_fr, end_d_learn=self.classinstance.default_end_d_learn_fr, alpha=self.classinstance.default_alpha),
            charts_pca_hosp_reg = self.classinstance.pca_charts(data=daily_reg, pcdim=self.classinstance.default_pcdim_reg, normalize=self.classinstance.default_normalize_reg, start_d_learn=self.classinstance.default_start_d_learn_fr_reg, end_d_learn=self.classinstance.default_end_d_learn_fr_reg, alpha=self.classinstance.default_alpha_reg),
            label = self.classinstance.request_label(),
            department = self.classinstance.default_department,
            region = self.classinstance.default_region,
            first_day_fr = self.classinstance.first_day_fr,
            last_day_fr = self.classinstance.last_day_fr,
            map_choice = self.classinstance.map_choice,
            criterion_choice = self.classinstance.criterion_choice,
            number_all_dep = self.classinstance.number_all_dep,
            global_pc = self.classinstance.global_pc,
            normalize_states = self.classinstance.normalize_states,
            alpha_smooth = self.classinstance.alpha_smooth,
            pc_reg = self.classinstance.pc_reg,
            map_select = self.classinstance.default_map_select,
            top_dep = self.classinstance.default_top_dep,
            criterion_select = self.classinstance.default_criterion_select,
            pcdim = self.classinstance.default_pcdim,
            normalize = self.classinstance.default_normalize,
            start_d_learn_fr = self.classinstance.default_start_d_learn_fr,
            end_d_learn_fr = self.classinstance.default_end_d_learn_fr,
            alpha = self.classinstance.default_alpha,
            pcdim_reg = self.classinstance.default_pcdim_reg,
            normalize_reg = self.classinstance.default_normalize_reg,
            start_d_learn_fr_reg = self.classinstance.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = self.classinstance.default_end_d_learn_fr_reg,
            alpha_reg = self.classinstance.default_alpha_reg,
        )