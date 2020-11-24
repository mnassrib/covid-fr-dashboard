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

cv = dict(
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


@app.route('/', methods=['GET', 'POST'])
def graphs():

    return render_template("graphs.html", cv=cv)


@app.route('/maps', methods=['GET', 'POST'])
def maps():

    cv["map_select"] = request.form.get('map_select')

    return render_template("graphs.html", cv=cv)


@app.route("/top_dep_settings", methods=['GET', 'POST'])
def top_dep_settings():

    cv["top_dep"] = int(request.form.getlist('top_dep_settings')[0])
    cv["criterion"] = request.form.getlist('top_dep_settings')[1]
    cv["charts_and_parameters"] = covfr.charts(top_number=top_dep)
    cv["charts_and_parameters_positive_data"] = covfr.charts_positive_data(top_number=top_dep)

    return render_template("graphs.html", cv=cv)


@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():

    global_select = request.form.getlist('global_parameters')

    cv["pcdim"] = int(global_select[0])
    cv["normalize"] = eval(global_select[1])
    start_d_learn = pd.Timestamp(global_select[2].split(" - ")[0]).strftime("%Y-%m-%d")
    end_d_learn = pd.Timestamp(global_select[2].split(" - ")[1]).strftime("%Y-%m-%d")
    cv["start_d_learn_fr"] = global_select[2].split(" - ")[0]
    cv["end_d_learn_fr"] = global_select[2].split(" - ")[1]
    cv["alpha"] = float(global_select[3])

    cv["graphJSONquadratics"] = covfr.pca_charts(data=daily, pcdim=cv["pcdim"], normalize=cv["normalize"], start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=cv["alpha"])

    print("************", cv["graphJSONquadratics"])

    return render_template("graphs.html", cv=cv)


@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():

    hosp_select = request.form.getlist('hosp_parameters')

    cv["pcdim_reg"] = int(hosp_select[0])
    cv["normalize_reg"] = eval(hosp_select[1])
    cv["start_d_learn_reg"] = pd.Timestamp(hosp_select[2].split(" - ")[0]).strftime("%Y-%m-%d")
    cv["end_d_learn_reg"] = pd.Timestamp(hosp_select[2].split(" - ")[1]).strftime("%Y-%m-%d")
    cv["start_d_learn_fr_reg"] = hosp_select[2].split(" - ")[0]
    cv["end_d_learn_fr_reg"] = hosp_select[2].split(" - ")[1]
    cv["alpha_reg"] = float(hosp_select[3])

    cv["graphJSONquadratics_reg"] = covfr.pca_charts(data=daily_reg, pcdim=cv["pcdim_reg"], normalize=cv["normalize_reg"], start_d_learn=cv["start_d_learn_reg"], end_d_learn=cv["end_d_learn_reg"], alpha=cv["alpha_reg"])

    return render_template("graphs.html", cv=cv)


@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):

    cv["charts_and_parameters"] = covfr.charts(data=None, department=department, region=cv["region"], top_number=cv["top_dep"])
    cv["charts_and_parameters_positive_data"] = covfr.charts_positive_data(data=None, department=department, region=cv["region"], top_number=cv["top_dep"])
    cv["label"] = covfr.request_label(department=department, region=cv["region"])

    return render_template("graphs.html", cv=cv)


@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):

    cv["charts_and_parameters"] = covfr.charts(data=None, department=cv["department"], region=region, top_number=cv["top_dep"])
    cv["charts_and_parameters_positive_data"] = covfr.charts_positive_data(data=None, department=cv["department"], region=region, top_number=cv["top_dep"])
    cv["label"] = covfr.request_label(department=cv["department"], region=region)

    return render_template("graphs.html", cv=cv)

if __name__ == '__main__':
    app.run(debug=True)