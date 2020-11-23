from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import numpy as np
import json

from cutils.covidclass import CovidFr

app = Flask(__name__)

covfr = CovidFr()
covid = covfr.load_df()
nprate, rprate, dprate = covfr.load_positive_df()
ordaj_reg = covfr.overall_regions_data_as_json()
oddaj_dep = covfr.overall_departments_data_as_json()
orpdaj_reg = covfr.overall_regions_positive_data_as_json()
odpdaj_dep = covfr.overall_departments_positive_data_as_json()
daily = covfr.dailycases(data=covid, pca=True)
daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
charts_and_parameters = covfr.charts(top_number=covfr.default_top_dep)
charts_and_parameters_positive_data = covfr.charts_positive_data(top_number=covfr.default_top_dep)
label = covfr.request_label(department=covfr.department, region=covfr.region)
graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn, end_d_learn=covfr.default_end_d_learn, alpha=covfr.default_alpha)
graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_reg, end_d_learn=covfr.default_end_d_learn_reg, alpha=covfr.default_alpha_reg)

##########################################################
# required html page variables
###############################
first_day_fr = covfr.first_day_fr
last_day_fr = covfr.last_day_fr
department = covfr.department
region = covfr.region
map_choice = covfr.map_choice
criterion_choice = covfr.criterion_choice
number_all_dep = covfr.number_all_dep
global_pc = covfr.global_pc
normalize_states = covfr.normalize_states
alpha_smooth = covfr.alpha_smooth
pc_reg = covfr.pc_reg
map_select = covfr.default_map_select
top_dep = covfr.default_top_dep
criterion = covfr.default_criterion
pcdim = covfr.default_pcdim
normalize = covfr.default_normalize
start_d_learn = covfr.default_start_d_learn
end_d_learn = covfr.default_end_d_learn
start_d_learn_fr = covfr.default_start_d_learn_fr
end_d_learn_fr = covfr.default_end_d_learn_fr
alpha = covfr.default_alpha
pcdim_reg = covfr.default_pcdim_reg
normalize_reg = covfr.default_normalize_reg
start_d_learn_reg = covfr.default_start_d_learn_reg
end_d_learn_reg = covfr.default_end_d_learn_reg
start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
alpha_reg = covfr.default_alpha_reg
##########################################################

@app.route('/', methods=['GET', 'POST'])
def graphs():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        upcovfr = CovidFr()
        covid = upcovfr.load_df()
        nprate, rprate, dprate = upcovfr.load_positive_df()
        ordaj_reg = upcovfr.overall_regions_data_as_json()
        oddaj_dep = upcovfr.overall_departments_data_as_json()
        orpdaj_reg = upcovfr.overall_regions_positive_data_as_json()
        odpdaj_dep = upcovfr.overall_departments_positive_data_as_json()
        daily = upcovfr.dailycases(data=covid, pca=True)
        daily_reg = upcovfr.regiondailycases(data=covid, feature='hosp')
        charts_and_parameters = upcovfr.charts(top_number=upcovfr.default_top_dep)
        charts_and_parameters_positive_data = upcovfr.charts_positive_data(top_number=upcovfr.default_top_dep)
        label = upcovfr.request_label(department=upcovfr.department, region=upcovfr.region)
        graphJSONquadratics = upcovfr.pca_charts(data=daily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn, end_d_learn=upcovfr.default_end_d_learn, alpha=upcovfr.default_alpha)
        graphJSONquadratics_reg = upcovfr.pca_charts(data=daily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_reg, end_d_learn=upcovfr.default_end_d_learn_reg, alpha=upcovfr.default_alpha_reg)

        ##########################################################
        # required html page variables
        ###############################
        first_day_fr = upcovfr.first_day_fr
        last_day_fr = upcovfr.last_day_fr
        department = upcovfr.department
        region = upcovfr.region
        map_choice = upcovfr.map_choice
        criterion_choice = upcovfr.criterion_choice
        number_all_dep = upcovfr.number_all_dep
        global_pc = upcovfr.global_pc
        normalize_states = upcovfr.normalize_states
        alpha_smooth = upcovfr.alpha_smooth
        pc_reg = upcovfr.pc_reg
        map_select = upcovfr.default_map_select
        top_dep = upcovfr.default_top_dep
        criterion = upcovfr.default_criterion
        pcdim = upcovfr.default_pcdim
        normalize = upcovfr.default_normalize
        start_d_learn = upcovfr.default_start_d_learn
        end_d_learn = upcovfr.default_end_d_learn
        start_d_learn_fr = upcovfr.default_start_d_learn_fr
        end_d_learn_fr = upcovfr.default_end_d_learn_fr
        alpha = upcovfr.default_alpha
        pcdim_reg = upcovfr.default_pcdim_reg
        normalize_reg = upcovfr.default_normalize_reg
        start_d_learn_reg = upcovfr.default_start_d_learn_reg
        end_d_learn_reg = upcovfr.default_end_d_learn_reg
        start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg
        end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg
        alpha_reg = upcovfr.default_alpha_reg
        ##########################################################

        return render_template(
            "graphs.html",
            graphJSON = charts_and_parameters,
            positive_graphJSON = charts_and_parameters_positive_data,
            counters = charts_and_parameters["counters"],
            positive_counters = charts_and_parameters_positive_data["counters"],

            overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
            overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
            overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
            overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

            overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
            overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
            overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
            overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

            overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
            overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
            overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
            overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

            overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
            overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
            overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
            overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

            overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
            overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
            overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
            overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

            overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
            overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
            overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
            overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

            first_day_fr = first_day_fr,
            last_day_fr = last_day_fr,
            label = label,
            department = department,
            region = region,

            map_choice = map_choice,
            criterion_choice = criterion_choice,
            number_all_dep = number_all_dep,
            global_pc = global_pc,
            normalize_states = normalize_states,
            alpha_smooth = alpha_smooth,
            pc_reg = pc_reg,

            map_select = map_select,
            top_dep = top_dep,
            criterion = criterion,
            pcdim = pcdim,
            normalize = normalize,
            start_d_learn_fr = start_d_learn_fr,
            end_d_learn_fr = end_d_learn_fr,
            alpha = alpha,
            pcdim_reg = pcdim_reg,
            normalize_reg = normalize_reg,
            start_d_learn_fr_reg = start_d_learn_fr_reg,
            end_d_learn_fr_reg = end_d_learn_fr_reg,
            alpha_reg = alpha_reg,

            graphJSONquadratics = graphJSONquadratics["graphJSON"],
            graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
        )
    else:
        return render_template(
            "graphs.html",
            graphJSON = charts_and_parameters,
            positive_graphJSON = charts_and_parameters_positive_data,
            counters = charts_and_parameters["counters"],
            positive_counters = charts_and_parameters_positive_data["counters"],

            overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
            overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
            overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
            overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

            overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
            overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
            overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
            overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

            overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
            overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
            overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
            overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

            overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
            overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
            overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
            overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

            overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
            overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
            overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
            overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

            overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
            overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
            overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
            overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

            first_day_fr = first_day_fr,
            last_day_fr = last_day_fr,
            label = label,
            department = department,
            region = region,

            map_choice = map_choice,
            criterion_choice = criterion_choice,
            number_all_dep = number_all_dep,
            global_pc = global_pc,
            normalize_states = normalize_states,
            alpha_smooth = alpha_smooth,
            pc_reg = pc_reg,

            map_select = map_select,
            top_dep = top_dep,
            criterion = criterion,
            pcdim = pcdim,
            normalize = normalize,
            start_d_learn_fr = start_d_learn_fr,
            end_d_learn_fr = end_d_learn_fr,
            alpha = alpha,
            pcdim_reg = pcdim_reg,
            normalize_reg = normalize_reg,
            start_d_learn_fr_reg = start_d_learn_fr_reg,
            end_d_learn_fr_reg = end_d_learn_fr_reg,
            alpha_reg = alpha_reg,

            graphJSONquadratics = graphJSONquadratics["graphJSON"],
            graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
        )

@app.route('/maps', methods=['GET', 'POST'])
def maps():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        covfr = CovidFr()
        covid = covfr.load_df()
        nprate, rprate, dprate = covfr.load_positive_df()
        ordaj_reg = covfr.overall_regions_data_as_json()
        oddaj_dep = covfr.overall_departments_data_as_json()
        orpdaj_reg = covfr.overall_regions_positive_data_as_json()
        odpdaj_dep = covfr.overall_departments_positive_data_as_json()
        daily = covfr.dailycases(data=covid, pca=True)
        daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
        charts_and_parameters = covfr.charts(top_number=covfr.default_top_dep)
        charts_and_parameters_positive_data = covfr.charts_positive_data(top_number=covfr.default_top_dep)
        label = covfr.request_label(department=covfr.department, region=covfr.region)
        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn, end_d_learn=covfr.default_end_d_learn, alpha=covfr.default_alpha)
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_reg, end_d_learn=covfr.default_end_d_learn_reg, alpha=covfr.default_alpha_reg)

        ##########################################################
        # required html page variables
        ###############################
        first_day_fr = covfr.first_day_fr
        last_day_fr = covfr.last_day_fr
        department = covfr.department
        region = covfr.region
        map_choice = covfr.map_choice
        criterion_choice = covfr.criterion_choice
        number_all_dep = covfr.number_all_dep
        global_pc = covfr.global_pc
        normalize_states = covfr.normalize_states
        alpha_smooth = covfr.alpha_smooth
        pc_reg = covfr.pc_reg
        top_dep = covfr.default_top_dep
        criterion = covfr.default_criterion
        pcdim = covfr.default_pcdim
        normalize = covfr.default_normalize
        start_d_learn = covfr.default_start_d_learn
        end_d_learn = covfr.default_end_d_learn
        start_d_learn_fr = covfr.default_start_d_learn_fr
        end_d_learn_fr = covfr.default_end_d_learn_fr
        alpha = covfr.default_alpha
        pcdim_reg = covfr.default_pcdim_reg
        normalize_reg = covfr.default_normalize_reg
        start_d_learn_reg = covfr.default_start_d_learn_reg
        end_d_learn_reg = covfr.default_end_d_learn_reg
        start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
        end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
        alpha_reg = covfr.default_alpha_reg

        map_select = request.form.get('map_select')
        ##########################################################

    map_select = request.form.get('map_select')

    return render_template(
        "graphs.html",
        graphJSON = charts_and_parameters,
        positive_graphJSON = charts_and_parameters_positive_data,
        counters = charts_and_parameters["counters"],
        positive_counters = charts_and_parameters_positive_data["counters"],

        overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

        overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

        overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
        overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

        first_day_fr = first_day_fr,
        last_day_fr = last_day_fr,
        label = label,
        department = department,
        region = region,

        map_choice = map_choice,
        criterion_choice = criterion_choice,
        number_all_dep = number_all_dep,
        global_pc = global_pc,
        normalize_states = normalize_states,
        alpha_smooth = alpha_smooth,
        pc_reg = pc_reg,

        map_select = map_select,
        top_dep = top_dep,
        criterion = criterion,
        pcdim = pcdim,
        normalize = normalize,
        start_d_learn_fr = start_d_learn_fr,
        end_d_learn_fr = end_d_learn_fr,
        alpha = alpha,
        pcdim_reg = pcdim_reg,
        normalize_reg = normalize_reg,
        start_d_learn_fr_reg = start_d_learn_fr_reg,
        end_d_learn_fr_reg = end_d_learn_fr_reg,
        alpha_reg = alpha_reg,

        graphJSONquadratics = graphJSONquadratics["graphJSON"],
        graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
    )

@app.route("/top_dep_settings", methods=['GET', 'POST'])
def top_dep_settings():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        covfr = CovidFr()
        covid = covfr.load_df()
        nprate, rprate, dprate = covfr.load_positive_df()
        ordaj_reg = covfr.overall_regions_data_as_json()
        oddaj_dep = covfr.overall_departments_data_as_json()
        orpdaj_reg = covfr.overall_regions_positive_data_as_json()
        odpdaj_dep = covfr.overall_departments_positive_data_as_json()
        daily = covfr.dailycases(data=covid, pca=True)
        daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
        label = covfr.request_label(department=covfr.department, region=covfr.region)
        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn, end_d_learn=covfr.default_end_d_learn, alpha=covfr.default_alpha)
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_reg, end_d_learn=covfr.default_end_d_learn_reg, alpha=covfr.default_alpha_reg)

        ##########################################################
        # required html page variables
        ###############################
        first_day_fr = covfr.first_day_fr
        last_day_fr = covfr.last_day_fr
        department = covfr.department
        region = covfr.region
        map_choice = covfr.map_choice
        criterion_choice = covfr.criterion_choice
        number_all_dep = covfr.number_all_dep
        global_pc = covfr.global_pc
        normalize_states = covfr.normalize_states
        alpha_smooth = covfr.alpha_smooth
        pc_reg = covfr.pc_reg
        map_select = covfr.default_map_select
        pcdim = covfr.default_pcdim
        normalize = covfr.default_normalize
        start_d_learn = covfr.default_start_d_learn
        end_d_learn = covfr.default_end_d_learn
        start_d_learn_fr = covfr.default_start_d_learn_fr
        end_d_learn_fr = covfr.default_end_d_learn_fr
        alpha = covfr.default_alpha
        pcdim_reg = covfr.default_pcdim_reg
        normalize_reg = covfr.default_normalize_reg
        start_d_learn_reg = covfr.default_start_d_learn_reg
        end_d_learn_reg = covfr.default_end_d_learn_reg
        start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
        end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
        alpha_reg = covfr.default_alpha_reg

        top_dep = int(request.form.getlist('top_dep_settings')[0])
        criterion = request.form.getlist('top_dep_settings')[1]
        charts_and_parameters = covfr.charts(top_number=top_dep)
        charts_and_parameters_positive_data = covfr.charts_positive_data(top_number=top_dep)
        ##########################################################

    top_dep = int(request.form.getlist('top_dep_settings')[0])
    criterion = request.form.getlist('top_dep_settings')[1]
    charts_and_parameters = covfr.charts(top_number=top_dep)
    charts_and_parameters_positive_data = covfr.charts_positive_data(top_number=top_dep)

    return render_template(
        "graphs.html",
        graphJSON = charts_and_parameters,
        positive_graphJSON = charts_and_parameters_positive_data,
        counters = charts_and_parameters["counters"],
        positive_counters = charts_and_parameters_positive_data["counters"],

        overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

        overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

        overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
        overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

        first_day_fr = first_day_fr,
        last_day_fr = last_day_fr,
        label = label,
        department = department,
        region = region,

        map_choice = map_choice,
        criterion_choice = criterion_choice,
        number_all_dep = number_all_dep,
        global_pc = global_pc,
        normalize_states = normalize_states,
        alpha_smooth = alpha_smooth,
        pc_reg = pc_reg,

        map_select = map_select,
        top_dep = top_dep,
        criterion = criterion,
        pcdim = pcdim,
        normalize = normalize,
        start_d_learn_fr = start_d_learn_fr,
        end_d_learn_fr = end_d_learn_fr,
        alpha = alpha,
        pcdim_reg = pcdim_reg,
        normalize_reg = normalize_reg,
        start_d_learn_fr_reg = start_d_learn_fr_reg,
        end_d_learn_fr_reg = end_d_learn_fr_reg,
        alpha_reg = alpha_reg,

        graphJSONquadratics = graphJSONquadratics["graphJSON"],
        graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
    )

@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        covfr = CovidFr()
        covid = covfr.load_df()
        nprate, rprate, dprate = covfr.load_positive_df()
        ordaj_reg = covfr.overall_regions_data_as_json()
        oddaj_dep = covfr.overall_departments_data_as_json()
        orpdaj_reg = covfr.overall_regions_positive_data_as_json()
        odpdaj_dep = covfr.overall_departments_positive_data_as_json()
        daily = covfr.dailycases(data=covid, pca=True)
        daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
        charts_and_parameters = covfr.charts(top_number=covfr.default_top_dep)
        charts_and_parameters_positive_data = covfr.charts_positive_data(top_number=covfr.default_top_dep)
        label = covfr.request_label(department=covfr.department, region=covfr.region)

        ##########################################################
        # required html page variables
        ###############################
        first_day_fr = covfr.first_day_fr
        last_day_fr = covfr.last_day_fr
        department = covfr.department
        region = covfr.region
        map_choice = covfr.map_choice
        criterion_choice = covfr.criterion_choice
        number_all_dep = covfr.number_all_dep
        global_pc = covfr.global_pc
        normalize_states = covfr.normalize_states
        alpha_smooth = covfr.alpha_smooth
        pc_reg = covfr.pc_reg
        map_select = covfr.default_map_select
        top_dep = covfr.default_top_dep
        criterion = covfr.default_criterion
        pcdim_reg = covfr.default_pcdim_reg
        normalize_reg = covfr.default_normalize_reg
        start_d_learn_reg = covfr.default_start_d_learn_reg
        end_d_learn_reg = covfr.default_end_d_learn_reg
        start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
        end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
        alpha_reg = covfr.default_alpha_reg

        global_select = request.form.getlist('global_parameters')

        pcdim = int(global_select[0])
        normalize = eval(global_select[1])
        start_d_learn = datetime.strptime(global_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d")
        end_d_learn = datetime.strptime(global_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d")
        start_d_learn_fr = json.dumps(datetime.strptime(start_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
        end_d_learn_fr = json.dumps(datetime.strptime(end_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
        alpha = float(global_select[3])

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha)
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=pcdim_reg, normalize=normalize_reg, start_d_learn=start_d_learn_reg, end_d_learn=end_d_learn_reg, alpha=alpha_reg)
        ##########################################################

    global_select = request.form.getlist('global_parameters')

    pcdim = int(global_select[0])
    normalize = eval(global_select[1])
    start_d_learn = datetime.strptime(global_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d")
    end_d_learn = datetime.strptime(global_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d")
    start_d_learn_fr = json.dumps(datetime.strptime(start_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
    end_d_learn_fr = json.dumps(datetime.strptime(end_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
    alpha = float(global_select[3])

    graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha)
    graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=pcdim_reg, normalize=normalize_reg, start_d_learn=start_d_learn_reg, end_d_learn=end_d_learn_reg, alpha=alpha_reg)

    return render_template(
        "graphs.html",
        graphJSON = charts_and_parameters,
        positive_graphJSON = charts_and_parameters_positive_data,
        counters = charts_and_parameters["counters"],
        positive_counters = charts_and_parameters_positive_data["counters"],

        overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

        overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

        overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
        overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

        first_day_fr = first_day_fr,
        last_day_fr = last_day_fr,
        label = label,
        department = department,
        region = region,

        map_choice = map_choice,
        criterion_choice = criterion_choice,
        number_all_dep = number_all_dep,
        global_pc = global_pc,
        normalize_states = normalize_states,
        alpha_smooth = alpha_smooth,
        pc_reg = pc_reg,

        map_select = map_select,
        top_dep = top_dep,
        criterion = criterion,
        pcdim = pcdim,
        normalize = normalize,
        start_d_learn_fr = start_d_learn_fr,
        end_d_learn_fr = end_d_learn_fr,
        alpha = alpha,
        pcdim_reg = pcdim_reg,
        normalize_reg = normalize_reg,
        start_d_learn_fr_reg = start_d_learn_fr_reg,
        end_d_learn_fr_reg = end_d_learn_fr_reg,
        alpha_reg = alpha_reg,

        graphJSONquadratics = graphJSONquadratics["graphJSON"],
        graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
    )

@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        covfr = CovidFr()
        covid = covfr.load_df()
        nprate, rprate, dprate = covfr.load_positive_df()
        ordaj_reg = covfr.overall_regions_data_as_json()
        oddaj_dep = covfr.overall_departments_data_as_json()
        orpdaj_reg = covfr.overall_regions_positive_data_as_json()
        odpdaj_dep = covfr.overall_departments_positive_data_as_json()
        daily = covfr.dailycases(data=covid, pca=True)
        daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
        charts_and_parameters = covfr.charts(top_number=covfr.default_top_dep)
        charts_and_parameters_positive_data = covfr.charts_positive_data(top_number=covfr.default_top_dep)
        label = covfr.request_label(department=covfr.department, region=covfr.region)

        ##########################################################
        # required html page variables
        ###############################
        first_day_fr = covfr.first_day_fr
        last_day_fr = covfr.last_day_fr
        department = covfr.department
        region = covfr.region
        map_choice = covfr.map_choice
        criterion_choice = covfr.criterion_choice
        number_all_dep = covfr.number_all_dep
        global_pc = covfr.global_pc
        normalize_states = covfr.normalize_states
        alpha_smooth = covfr.alpha_smooth
        pc_reg = covfr.pc_reg
        map_select = covfr.default_map_select
        top_dep = covfr.default_top_dep
        criterion = covfr.default_criterion
        pcdim = covfr.default_pcdim
        normalize = covfr.default_normalize
        start_d_learn = covfr.default_start_d_learn
        end_d_learn = covfr.default_end_d_learn
        start_d_learn_fr = covfr.default_start_d_learn_fr
        end_d_learn_fr = covfr.default_end_d_learn_fr
        alpha = covfr.default_alpha

        hosp_select = request.form.getlist('hosp_parameters')

        pcdim_reg = int(hosp_select[0])
        normalize_reg = eval(hosp_select[1])
        start_d_learn_reg = datetime.strptime(hosp_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d")
        end_d_learn_reg = datetime.strptime(hosp_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d")
        start_d_learn_fr_reg = json.dumps(datetime.strptime(start_d_learn_reg, '%Y-%m-%d').strftime("%d/%m/%Y"))
        end_d_learn_fr_reg = json.dumps(datetime.strptime(end_d_learn_reg, '%Y-%m-%d').strftime("%d/%m/%Y"))
        alpha_reg = float(hosp_select[3])

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha)
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=pcdim_reg, normalize=normalize_reg, start_d_learn=start_d_learn_reg, end_d_learn=end_d_learn_reg, alpha=alpha_reg)
        ##########################################################

    hosp_select = request.form.getlist('hosp_parameters')

    pcdim_reg = int(hosp_select[0])
    normalize_reg = eval(hosp_select[1])
    start_d_learn_reg = datetime.strptime(hosp_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d")
    end_d_learn_reg = datetime.strptime(hosp_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d")
    start_d_learn_fr_reg = json.dumps(datetime.strptime(start_d_learn_reg, '%Y-%m-%d').strftime("%d/%m/%Y"))
    end_d_learn_fr_reg = json.dumps(datetime.strptime(end_d_learn_reg, '%Y-%m-%d').strftime("%d/%m/%Y"))
    alpha_reg = float(hosp_select[3])

    graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha)
    graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=pcdim_reg, normalize=normalize_reg, start_d_learn=start_d_learn_reg, end_d_learn=end_d_learn_reg, alpha=alpha_reg)

    return render_template(
        "graphs.html",
        graphJSON = charts_and_parameters,
        positive_graphJSON = charts_and_parameters_positive_data,
        counters = charts_and_parameters["counters"],
        positive_counters = charts_and_parameters_positive_data["counters"],

        overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

        overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

        overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
        overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

        first_day_fr = first_day_fr,
        last_day_fr = last_day_fr,
        label = label,
        department = department,
        region = region,

        map_choice = map_choice,
        criterion_choice = criterion_choice,
        number_all_dep = number_all_dep,
        global_pc = global_pc,
        normalize_states = normalize_states,
        alpha_smooth = alpha_smooth,
        pc_reg = pc_reg,

        map_select = map_select,
        top_dep = top_dep,
        criterion = criterion,
        pcdim = pcdim,
        normalize = normalize,
        start_d_learn_fr = start_d_learn_fr,
        end_d_learn_fr = end_d_learn_fr,
        alpha = alpha,
        pcdim_reg = pcdim_reg,
        normalize_reg = normalize_reg,
        start_d_learn_fr_reg = start_d_learn_fr_reg,
        end_d_learn_fr_reg = end_d_learn_fr_reg,
        alpha_reg = alpha_reg,

        graphJSONquadratics = graphJSONquadratics["graphJSON"],
        graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
    )

@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        covfr = CovidFr()
        covid = covfr.load_df()
        nprate, rprate, dprate = covfr.load_positive_df()
        ordaj_reg = covfr.overall_regions_data_as_json()
        oddaj_dep = covfr.overall_departments_data_as_json()
        orpdaj_reg = covfr.overall_regions_positive_data_as_json()
        odpdaj_dep = covfr.overall_departments_positive_data_as_json()
        daily = covfr.dailycases(data=covid, pca=True)
        daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn, end_d_learn=covfr.default_end_d_learn, alpha=covfr.default_alpha)
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_reg, end_d_learn=covfr.default_end_d_learn_reg, alpha=covfr.default_alpha_reg)

        ##########################################################
        # required html page variables
        ###############################
        first_day_fr = covfr.first_day_fr
        last_day_fr = covfr.last_day_fr
        department = department
        region = covfr.region
        map_choice = covfr.map_choice
        criterion_choice = covfr.criterion_choice
        number_all_dep = covfr.number_all_dep
        global_pc = covfr.global_pc
        normalize_states = covfr.normalize_states
        alpha_smooth = covfr.alpha_smooth
        pc_reg = covfr.pc_reg
        map_select = covfr.default_map_select
        top_dep = covfr.default_top_dep
        criterion = covfr.default_criterion
        pcdim = covfr.default_pcdim
        normalize = covfr.default_normalize
        start_d_learn = covfr.default_start_d_learn
        end_d_learn = covfr.default_end_d_learn
        start_d_learn_fr = covfr.default_start_d_learn_fr
        end_d_learn_fr = covfr.default_end_d_learn_fr
        alpha = covfr.default_alpha
        pcdim_reg = covfr.default_pcdim_reg
        normalize_reg = covfr.default_normalize_reg
        start_d_learn_reg = covfr.default_start_d_learn_reg
        end_d_learn_reg = covfr.default_end_d_learn_reg
        start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
        end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
        alpha_reg = covfr.default_alpha_reg

        charts_and_parameters = covfr.charts(data=None, department=department, region=region, top_number=top_dep)
        charts_and_parameters_positive_data = covfr.charts_positive_data(data=None, department=department, region=region, top_number=top_dep)
        label = covfr.request_label(department=department, region=region)
        ##########################################################

    charts_and_parameters = covfr.charts(data=None, department=department, region=region, top_number=top_dep)
    charts_and_parameters_positive_data = covfr.charts_positive_data(data=None, department=department, region=region, top_number=top_dep)
    label = covfr.request_label(department=department, region=region)

    return render_template(
        "graphs.html",
        graphJSON = charts_and_parameters,
        positive_graphJSON = charts_and_parameters_positive_data,
        counters = charts_and_parameters["counters"],
        positive_counters = charts_and_parameters_positive_data["counters"],

        overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

        overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

        overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
        overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

        first_day_fr = first_day_fr,
        last_day_fr = last_day_fr,
        label = label,
        department = department,
        region = region,

        map_choice = map_choice,
        criterion_choice = criterion_choice,
        number_all_dep = number_all_dep,
        global_pc = global_pc,
        normalize_states = normalize_states,
        alpha_smooth = alpha_smooth,
        pc_reg = pc_reg,

        map_select = map_select,
        top_dep = top_dep,
        criterion = criterion,
        pcdim = pcdim,
        normalize = normalize,
        start_d_learn_fr = start_d_learn_fr,
        end_d_learn_fr = end_d_learn_fr,
        alpha = alpha,
        pcdim_reg = pcdim_reg,
        normalize_reg = normalize_reg,
        start_d_learn_fr_reg = start_d_learn_fr_reg,
        end_d_learn_fr_reg = end_d_learn_fr_reg,
        alpha_reg = alpha_reg,

        graphJSONquadratics = graphJSONquadratics["graphJSON"],
        graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
    )

@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        covfr = CovidFr()
        covid = covfr.load_df()
        nprate, rprate, dprate = covfr.load_positive_df()
        ordaj_reg = covfr.overall_regions_data_as_json()
        oddaj_dep = covfr.overall_departments_data_as_json()
        orpdaj_reg = covfr.overall_regions_positive_data_as_json()
        odpdaj_dep = covfr.overall_departments_positive_data_as_json()
        daily = covfr.dailycases(data=covid, pca=True)
        daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn, end_d_learn=covfr.default_end_d_learn, alpha=covfr.default_alpha)
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_reg, end_d_learn=covfr.default_end_d_learn_reg, alpha=covfr.default_alpha_reg)

        ##########################################################
        # required html page variables
        ###############################
        first_day_fr = covfr.first_day_fr
        last_day_fr = covfr.last_day_fr
        department = covfr.department
        region = region
        map_choice = covfr.map_choice
        criterion_choice = covfr.criterion_choice
        number_all_dep = covfr.number_all_dep
        global_pc = covfr.global_pc
        normalize_states = covfr.normalize_states
        alpha_smooth = covfr.alpha_smooth
        pc_reg = covfr.pc_reg
        map_select = covfr.default_map_select
        top_dep = covfr.default_top_dep
        criterion = covfr.default_criterion
        pcdim = covfr.default_pcdim
        normalize = covfr.default_normalize
        start_d_learn = covfr.default_start_d_learn
        end_d_learn = covfr.default_end_d_learn
        start_d_learn_fr = covfr.default_start_d_learn_fr
        end_d_learn_fr = covfr.default_end_d_learn_fr
        alpha = covfr.default_alpha
        pcdim_reg = covfr.default_pcdim_reg
        normalize_reg = covfr.default_normalize_reg
        start_d_learn_reg = covfr.default_start_d_learn_reg
        end_d_learn_reg = covfr.default_end_d_learn_reg
        start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
        end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
        alpha_reg = covfr.default_alpha_reg

        charts_and_parameters = covfr.charts(data=None, department=department, region=region, top_number=top_dep)
        charts_and_parameters_positive_data = covfr.charts_positive_data(data=None, department=department, region=region, top_number=top_dep)
        label = covfr.request_label(department=department, region=region)
        ##########################################################

    charts_and_parameters = covfr.charts(data=None, department=department, region=region, top_number=top_dep)
    charts_and_parameters_positive_data = covfr.charts_positive_data(data=None, department=department, region=region, top_number=top_dep)
    label = covfr.request_label(department=department, region=region)

    return render_template(
        "graphs.html",
        graphJSON = charts_and_parameters,
        positive_graphJSON = charts_and_parameters_positive_data,
        counters = charts_and_parameters["counters"],
        positive_counters = charts_and_parameters_positive_data["counters"],

        overall_regions_data_dc = ordaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = ordaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],
        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],

        overall_regions_data_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = ordaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = ordaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = ordaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],

        overall_regions_data_hosp = ordaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = ordaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_rea = ordaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = ordaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        overall_regions_data_P = orpdaj_reg["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["overall_regions_P_as_json"]['quantiles_P'],
        overall_departments_data_P = odpdaj_dep["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["overall_departments_P_as_json"]['quantiles_P'],

        first_day_fr = first_day_fr,
        last_day_fr = last_day_fr,
        label = label,
        department = department,
        region = region,

        map_choice = map_choice,
        criterion_choice = criterion_choice,
        number_all_dep = number_all_dep,
        global_pc = global_pc,
        normalize_states = normalize_states,
        alpha_smooth = alpha_smooth,
        pc_reg = pc_reg,

        map_select = map_select,
        top_dep = top_dep,
        criterion = criterion,
        pcdim = pcdim,
        normalize = normalize,
        start_d_learn_fr = start_d_learn_fr,
        end_d_learn_fr = end_d_learn_fr,
        alpha = alpha,
        pcdim_reg = pcdim_reg,
        normalize_reg = normalize_reg,
        start_d_learn_fr_reg = start_d_learn_fr_reg,
        end_d_learn_fr_reg = end_d_learn_fr_reg,
        alpha_reg = alpha_reg,

        graphJSONquadratics = graphJSONquadratics["graphJSON"],
        graphJSONquadratics_reg = graphJSONquadratics_reg["graphJSON"],
    )

if __name__ == '__main__':
    app.run(debug=True)