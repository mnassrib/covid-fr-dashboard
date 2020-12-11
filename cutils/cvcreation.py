class CvCreation():
    """
    docstring for CvCreation
    """
    from cutils.covidclass import CovidFr
    covobject = CovidFr()
    covid = covobject.load_df()
    nprate, rprate, dprate = covobject.load_positive_df()
    daily = covobject.dailycases(data=covid, pca=True)
    daily_reg = covobject.regiondailycases(data=covid, feature='hosp')

    def __init__(self):
        pass

    def cv_load(self, **kwargs):
        """
        Returns required html page contexte variables
        """
        cv = dict(
            covid_state = kwargs.get('covid_state', False),
            positive_state = kwargs.get('positive_state', False),
            map_covid_reg = CvCreation.covobject.map_covid_reg(),
            map_covid_dep = CvCreation.covobject.map_covid_dep(),
            map_positive_reg = CvCreation.covobject.map_positive_reg(),
            map_positive_dep = CvCreation.covobject.map_positive_dep(),
            charts_impacted_dep = CvCreation.covobject.charts_impacted_dep(),
            charts_and_parameters_positive_data = CvCreation.covobject.charts_and_parameters_positive_data(),
            charts_and_parameters_covid_data = CvCreation.covobject.charts_and_parameters_covid_data(),
            charts_pca_global = CvCreation.covobject.pca_charts(data=CvCreation.daily, pcdim=CvCreation.covobject.default_pcdim, normalize=CvCreation.covobject.default_normalize, start_d_learn=CvCreation.covobject.default_start_d_learn_fr, end_d_learn=CvCreation.covobject.default_end_d_learn_fr, alpha=CvCreation.covobject.default_alpha),
            charts_pca_hosp_reg = CvCreation.covobject.pca_charts(data=CvCreation.daily, pcdim=CvCreation.covobject.default_pcdim_reg, normalize=CvCreation.covobject.default_normalize_reg, start_d_learn=CvCreation.covobject.default_start_d_learn_fr_reg, end_d_learn=CvCreation.covobject.default_end_d_learn_fr_reg, alpha=CvCreation.covobject.default_alpha_reg),
            label = CvCreation.covobject.request_label(),
            department = CvCreation.covobject.default_department,
            region = CvCreation.covobject.default_region,
            first_day_fr = CvCreation.covobject.first_day_fr,
            last_day_fr = CvCreation.covobject.last_day_fr,
            map_choice = CvCreation.covobject.map_choice,
            criterion_choice = CvCreation.covobject.criterion_choice,
            number_all_dep = CvCreation.covobject.number_all_dep,
            global_pc = CvCreation.covobject.global_pc,
            normalize_states = CvCreation.covobject.normalize_states,
            alpha_smooth = CvCreation.covobject.alpha_smooth,
            pc_reg = CvCreation.covobject.pc_reg,
            map_select = CvCreation.covobject.default_map_select,
            top_dep = CvCreation.covobject.default_top_dep,
            criterion_select = CvCreation.covobject.default_criterion_select,
            pcdim = CvCreation.covobject.default_pcdim,
            normalize = CvCreation.covobject.default_normalize,
            start_d_learn_fr = CvCreation.covobject.default_start_d_learn_fr,
            end_d_learn_fr = CvCreation.covobject.default_end_d_learn_fr,
            alpha = CvCreation.covobject.default_alpha,
            pcdim_reg = CvCreation.covobject.default_pcdim_reg,
            normalize_reg = CvCreation.covobject.default_normalize_reg,
            start_d_learn_fr_reg = CvCreation.covobject.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = CvCreation.covobject.default_end_d_learn_fr_reg,
            alpha_reg = CvCreation.covobject.default_alpha_reg,
        )
        return CvCreation.covobject, CvCreation.daily, CvCreation.daily_reg, cv