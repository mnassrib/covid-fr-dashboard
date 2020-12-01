from flask import Flask, render_template, request, redirect, url_for

class RenderPage(object):
    """
    docstring
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, '{}'.format(k), v)

    def appview(self):
        return render_template(
            "graphs.html",
            map_covid_reg = self.map_covid_reg,
            map_covid_dep = self.map_covid_dep,

            charts_impacted_dep = self.charts_impacted_dep,
            charts_and_parameters_covid_data = self.charts_and_parameters_covid_data,

            charts_pca_global = self.charts_pca_global,
            charts_pca_hosp_reg = self.charts_pca_hosp_reg,

            label = self.label,

            region = self.region,
            department = self.department,
            first_day_fr = self.first_day_fr,
            last_day_fr = self.last_day_fr,
            map_choice = self.map_choice,
            criterion_choice = self.criterion_choice,
            number_all_dep = self.number_all_dep,
            global_pc = self.global_pc,
            normalize_states = self.normalize_states,
            alpha_smooth = self.alpha_smooth,
            pc_reg = self.pc_reg,
            map_select = self.map_select,
            top_dep = self.top_dep,
            criterion_select = self.criterion_select,
            pcdim = self.pcdim,
            normalize = self.normalize,
            start_d_learn_fr = self.start_d_learn_fr,
            end_d_learn_fr = self.end_d_learn_fr,
            alpha = self.alpha,
            pcdim_reg = self.pcdim_reg,
            normalize_reg = self.normalize_reg,
            start_d_learn_fr_reg = self.start_d_learn_fr_reg,
            end_d_learn_fr_reg = self.end_d_learn_fr_reg,
            alpha_reg = self.alpha_reg,
        )