from flask import Flask, render_template, request, redirect, url_for

class ViewPage(object):
    """
    docstring
    """
    def __init__(self, 
        overall_regions_data_dc,
        overall_regions_quantiles_dc,
        overall_departments_data_dc,
        overall_departments_quantiles_dc,

        overall_regions_data_r_dc_rad,
        overall_regions_quantiles_r_dc_rad,
        overall_departments_data_r_dc_rad,
        overall_departments_quantiles_r_dc_rad,

        overall_regions_data_rad,
        overall_regions_quantiles_rad,
        overall_departments_data_rad,
        overall_departments_quantiles_rad,

        overall_regions_data_hosp,
        overall_regions_quantiles_hosp,
        overall_departments_data_hosp,
        overall_departments_quantiles_hosp,

        overall_regions_data_rea,
        overall_regions_quantiles_rea,
        overall_departments_data_rea,
        overall_departments_quantiles_rea,

        overall_regions_data_P,
        overall_regions_quantiles_P,
        overall_departments_data_P,
        overall_departments_quantiles_P,

        impacted_dep_graphJSON,
        positive_graphJSON,
        covid_graphJSON,

        label,
        region,
        department,

        first_day_fr,
        last_day_fr,

        map_choice,
        criterion_choice,
        number_all_dep,
        global_pc,
        normalize_states,
        alpha_smooth,
        pc_reg,
        map_select,
        top_dep,
        criterion_select,
        pcdim,
        normalize,
        alpha,
        start_d_learn_fr,
        end_d_learn_fr,
        pcdim_reg,
        normalize_reg,
        alpha_reg,
        start_d_learn_fr_reg,
        end_d_learn_fr_reg,

        graphJSON_pca_global,
        graphJSON_pca_hosp_reg, 
        **kwargs):
        self.overall_regions_data_dc = overall_regions_data_dc
        self.overall_regions_quantiles_dc = overall_regions_quantiles_dc
        self.overall_departments_data_dc = overall_departments_data_dc 
        self.overall_departments_quantiles_dc = overall_departments_quantiles_dc

        self.overall_regions_data_r_dc_rad = overall_regions_data_r_dc_rad
        self.overall_regions_quantiles_r_dc_rad = overall_regions_quantiles_r_dc_rad
        self.overall_departments_data_r_dc_rad = overall_departments_data_r_dc_rad
        self.overall_departments_quantiles_r_dc_rad = overall_departments_quantiles_r_dc_rad

        self.overall_regions_data_rad = overall_regions_data_rad
        self.overall_regions_quantiles_rad = overall_regions_quantiles_rad
        self.overall_departments_data_rad = overall_departments_data_rad
        self.overall_departments_quantiles_rad = overall_departments_quantiles_rad 

        self.overall_regions_data_hosp = overall_regions_data_hosp
        self.overall_regions_quantiles_hosp = overall_regions_quantiles_hosp
        self.overall_departments_data_hosp = overall_departments_data_hosp
        self.overall_departments_quantiles_hosp = overall_departments_quantiles_hosp

        self.overall_regions_data_rea = overall_regions_data_rea
        self.overall_regions_quantiles_rea = overall_regions_quantiles_rea
        self.overall_departments_data_rea = overall_departments_data_rea
        self.overall_departments_quantiles_rea = overall_departments_quantiles_rea

        self.overall_regions_data_P = overall_regions_data_P
        self.overall_regions_quantiles_P = overall_regions_quantiles_P
        self.overall_departments_data_P = overall_departments_data_P
        self.overall_departments_quantiles_P = overall_departments_quantiles_P

        self.impacted_dep_graphJSON = impacted_dep_graphJSON
        self.positive_graphJSON = positive_graphJSON
        self.covid_graphJSON = covid_graphJSON

        self.label = label
        self.region = region
        self.department = department

        self.first_day_fr = first_day_fr
        self.last_day_fr = last_day_fr

        self.map_choice = map_choice
        self.criterion_choice = criterion_choice
        self.number_all_dep = number_all_dep
        self.global_pc = global_pc
        self.normalize_states = normalize_states
        self.alpha_smooth = alpha_smooth
        self.pc_reg = pc_reg
        self.map_select = map_select
        self.top_dep = top_dep
        self.criterion_select = criterion_select
        self.pcdim = pcdim
        self.normalize = normalize
        self.alpha = alpha
        self.start_d_learn_fr = start_d_learn_fr
        self.end_d_learn_fr = end_d_learn_fr
        self.pcdim_reg = pcdim_reg
        self.normalize_reg = normalize_reg
        self.alpha_reg = alpha_reg
        self.start_d_learn_fr_reg = start_d_learn_fr_reg
        self.end_d_learn_fr_reg = end_d_learn_fr_reg

        self.graphJSON_pca_global = graphJSON_pca_global
        self.graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg

    def appview(self):
        return render_template(
            "graphs.html",
            overall_regions_data_dc = self.overall_regions_data_dc,
            overall_regions_quantiles_dc = self.overall_regions_quantiles_dc,
            overall_departments_data_dc = self.overall_departments_data_dc,
            overall_departments_quantiles_dc = self.overall_departments_quantiles_dc,

            overall_regions_data_r_dc_rad = self.overall_regions_data_r_dc_rad,
            overall_regions_quantiles_r_dc_rad = self.overall_regions_quantiles_r_dc_rad,
            overall_departments_data_r_dc_rad = self.overall_departments_data_r_dc_rad,
            overall_departments_quantiles_r_dc_rad = self.overall_departments_quantiles_r_dc_rad,

            overall_regions_data_rad = self.overall_regions_data_rad,
            overall_regions_quantiles_rad = self.overall_regions_quantiles_rad,
            overall_departments_data_rad = self.overall_departments_data_rad,
            overall_departments_quantiles_rad = self.overall_departments_quantiles_rad,

            overall_regions_data_hosp = self.overall_regions_data_hosp,
            overall_regions_quantiles_hosp = self.overall_regions_quantiles_hosp,
            overall_departments_data_hosp = self.overall_departments_data_hosp,
            overall_departments_quantiles_hosp = self.overall_departments_quantiles_hosp,

            overall_regions_data_rea = self.overall_regions_data_rea,
            overall_regions_quantiles_rea = self.overall_regions_quantiles_rea,
            overall_departments_data_rea = self.overall_departments_data_rea,
            overall_departments_quantiles_rea = self.overall_departments_quantiles_rea,

            overall_regions_data_P = self.overall_regions_data_P,
            overall_regions_quantiles_P = self.overall_regions_quantiles_P,
            overall_departments_data_P = self.overall_departments_data_P,
            overall_departments_quantiles_P = self.overall_departments_quantiles_P,

            impacted_dep_graphJSON = self.impacted_dep_graphJSON,
            positive_graphJSON = self.positive_graphJSON,
            covid_graphJSON = self.covid_graphJSON,

            first_day_fr = self.first_day_fr,
            last_day_fr = self.last_day_fr,
            label = self.label,
            department = self.department,
            region = self.region,

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

            graphJSON_pca_global = self.graphJSON_pca_global,
            graphJSON_pca_hosp_reg = self.graphJSON_pca_hosp_reg,
        )