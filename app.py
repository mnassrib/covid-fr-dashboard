from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import numpy as np
import json

from cutils.covidclass import CovidFr

app = Flask(__name__)

covfr = CovidFr()
if covfr.need_update():
    covid = covfr.load_df()
    oddaj_dep = covfr.overall_departments_data_as_json()
    oddaj_reg = covfr.overall_regions_data_as_json()

    daily = covfr.dailycases(data=covid, pca=True)
    #daily_reg = covfr.regiondailycases(data=covid, feature='dc')
    daily_reg = covfr.regiondailycases(data=covid, feature='hosp')

default_top_select = 10
default_map_select = "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"]
#--default params for global pca
default_pcdim = 2
default_normalize = True
default_start_d_learn = '2020-05-15'
default_start_date = json.dumps(datetime.strptime(default_start_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
default_end_d_learn = '2020-08-25'
default_end_date = json.dumps(datetime.strptime(default_end_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
default_alpha = 0.8
#--default params for hosps pca
default_pcdim_reg = 2
default_normalize_reg = False

@app.route('/', methods=['GET', 'POST'])
def graphs():
    """Country page of the app"""
    charts_and_parameters = covfr.charts(top_number=default_top_select)

    pcdim = default_pcdim
    normalize = default_normalize
    start_d_learn = default_start_d_learn
    end_d_learn = default_end_d_learn
    alpha = default_alpha

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_day_fr"]),
        label = covfr.request_label(department=None, region=None),

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'], 
        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],
        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],

        top_select = default_top_select,

        topn = list(range(1, covfr.department_base_data.shape[0]+1)),
        global_pc = list(range(1, daily.shape[1]+1)),
        normalize_states = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2)),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"]],

        pcdim = pcdim, 
        normalize = normalize,
        alpha = alpha,

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=default_pcdim_reg, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),

        map_select = default_map_select,
    )

@app.route('/maps', methods=['GET', 'POST'])
def maps():
    """Country page of the app"""
    charts_and_parameters = covfr.charts(top_number=default_top_select)

    map_select = request.form.get('map_select')

    pcdim = default_pcdim
    normalize = default_normalize
    start_d_learn = default_start_d_learn
    end_d_learn = default_end_d_learn
    alpha = default_alpha
        
    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_day_fr"]),
        label = covfr.request_label(department=None, region=None),

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'], 
        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],
        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],

        top_select = default_top_select,

        topn = list(range(1, covfr.department_base_data.shape[0]+1)),
        global_pc = list(range(1, daily.shape[1]+1)),
        normalize_states = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2)),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"]],

        pcdim = pcdim,
        normalize = normalize,
        alpha = alpha,

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=default_pcdim_reg, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),

        map_select = map_select,
    )

@app.route("/top_criteria_settings", methods=['GET', 'POST'])
def top_criteria_settings():
    """Country page of the app"""
    top_select = request.form.getlist('top_dep')
    
    charts_and_parameters = covfr.charts(top_number=int(top_select[0]))

    pcdim = default_pcdim
    normalize = default_normalize
    start_d_learn = default_start_d_learn
    end_d_learn = default_end_d_learn
    alpha = default_alpha

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_day_fr"]),
        label = covfr.request_label(department=None, region=None),

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'], 
        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],
        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],

        top_select = int(top_select[0]),

        topn = list(range(1, covfr.department_base_data.shape[0]+1)),
        global_pc = list(range(1, covfr.dailycases(data=covid, pca=True).shape[1]+1)),
        normalize_states = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2)),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"]],

        pcdim = pcdim,
        normalize = normalize,
        alpha = alpha,

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=default_pcdim_reg, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),

        map_select = default_map_select,
    )

@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():
    """Country page of the app"""
    charts_and_parameters = covfr.charts(top_number=default_top_select)

    global_select = request.form.getlist('global_parameters')

    pcdim = int(global_select[0])
    normalize = eval(global_select[1])
    start_d_learn = datetime.strptime(global_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d")
    default_start_date = json.dumps(datetime.strptime(start_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
    end_d_learn = datetime.strptime(global_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d")
    default_end_date = json.dumps(datetime.strptime(end_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
    alpha = float(global_select[3])

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_day_fr"]),
        label = covfr.request_label(department=None, region=None),

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'], 
        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],
        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],

        top_select = default_top_select,

        topn = list(range(1, covfr.department_base_data.shape[0]+1)),
        global_pc = list(range(1, daily.shape[1]+1)),
        normalize_states = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2)),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"]],

        pcdim = pcdim,
        normalize = normalize,
        alpha = alpha,

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=default_pcdim_reg, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),

        map_select = default_map_select,
    )

@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():
    """Country page of the app"""
    charts_and_parameters = covfr.charts(top_number=default_top_select)

    hosp_select = request.form.getlist('hosp_parameters')

    pcdim = default_pcdim
    normalize = default_normalize
    start_d_learn = default_start_d_learn
    end_d_learn = default_end_d_learn
    alpha = default_alpha

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_day_fr"]),
        label = covfr.request_label(department=None, region=None),

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'], 
        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],
        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],

        top_select = default_top_select,

        topn = list(range(1, covfr.department_base_data.shape[0]+1)),
        global_pc = list(range(1, covfr.dailycases(data=covid, pca=True).shape[1]+1)),
        normalize_states = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2)),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"]],

        pcdim = pcdim,
        normalize = normalize,
        alpha = alpha,

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=int(hosp_select[0]), normalize=eval(hosp_select[1]), start_d_learn=datetime.strptime(hosp_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d"), end_d_learn=datetime.strptime(hosp_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d"), alpha=hosp_select[3]),

        map_select = default_map_select,
    )

@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):
    """Department page of the app"""
    charts_and_parameters = covfr.charts(data=None, department=department, region=None, top_number=default_top_select)
    label = covfr.request_label(department=department, region=None)

    pcdim = default_pcdim
    normalize = default_normalize
    start_d_learn = default_start_d_learn
    end_d_learn = default_end_d_learn
    alpha = default_alpha
    
    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"], 
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_day_fr"]),
        label = label,
        department = department,

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'], 
        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],
        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],

        top_select = default_top_select,

        topn = list(range(1, covfr.department_base_data.shape[0]+1)),
        global_pc = list(range(1, daily.shape[1]+1)),
        normalize_states = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2)),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"]],

        pcdim = pcdim,
        normalize = normalize,
        alpha = alpha,

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=default_pcdim_reg, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),

        map_select = default_map_select,
    )

@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):
    """Region page of the app"""
    charts_and_parameters = covfr.charts(data=None, department=None, region=region, top_number=default_top_select)
    label = covfr.request_label(department=None, region=region)

    pcdim = default_pcdim
    normalize = default_normalize
    start_d_learn = default_start_d_learn
    end_d_learn = default_end_d_learn
    alpha = default_alpha

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"], 
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_day_fr"]),
        label = label,
        region = region,

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'], 
        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],
        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],
        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],

        top_select = default_top_select,

        topn = list(range(1, covfr.department_base_data.shape[0]+1)),
        global_pc = list(range(1, daily.shape[1]+1)),
        normalize_states = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2)),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"]],

        pcdim = pcdim,
        normalize = normalize,
        alpha = alpha,

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=default_pcdim_reg, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha),

        map_select = default_map_select,
    )

if __name__ == '__main__':
    app.run(debug=True)