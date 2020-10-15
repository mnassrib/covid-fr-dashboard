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

start_d_learn = '2020-05-15'
end_d_learn = '2020-08-25'
default_start_date = json.dumps(datetime.strptime(start_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
default_end_date = json.dumps(datetime.strptime(end_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))

@app.route('/', methods=['GET', 'POST'])
def graphs():
    """Country page of the app"""
    charts_and_parameters = covfr.charts()
    
    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_update_fr"]["day"]),
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

        global_pc = list(range(1, daily.shape[1]+1)),
        normalize = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = np.arange(0.1, 1, 0.05).round(2),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_update_fr"]["day"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_update_fr"]["day"]],

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=2, normalize=True, start_d_learn=start_d_learn, end_d_learn=end_d_learn),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=2, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn),

        map_select = "Nombre de décès",
    )

@app.route('/maps', methods=['GET', 'POST'])
def maps():
    """Country page of the app"""
    charts_and_parameters = covfr.charts()

    map_select = request.form.get('map_select')
        
    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_update_fr"]["day"]),
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

        global_pc = list(range(1, daily.shape[1]+1)),
        normalize = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = np.arange(0.1, 1, 0.05).round(2),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_update_fr"]["day"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_update_fr"]["day"]],

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=2, normalize=True, start_d_learn=start_d_learn, end_d_learn=end_d_learn),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=2, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn),

        map_select = map_select,
    )

@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():
    """Country page of the app"""
    charts_and_parameters = covfr.charts()

    global_select = request.form.getlist('global_parameters')

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_update_fr"]["day"]),
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

        global_pc = list(range(1, daily.shape[1]+1)),
        normalize = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = np.arange(0.1, 1, 0.05).round(2),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_update_fr"]["day"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_update_fr"]["day"]],

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=int(global_select[0]), normalize=eval(global_select[1]), start_d_learn=datetime.strptime(global_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d"), end_d_learn=datetime.strptime(global_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d"), alpha=global_select[3]),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=2, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn),

        map_select = "Nombre de décès",
    )

@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():
    """Country page of the app"""
    charts_and_parameters = covfr.charts()

    hosp_select = request.form.getlist('hosp_parameters')

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_update_fr"]["day"]),
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

        global_pc = list(range(1, covfr.dailycases(data=covid, pca=True).shape[1]+1)),
        normalize = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = np.arange(0.1, 1, 0.05).round(2),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_update_fr"]["day"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_update_fr"]["day"]],

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=2, normalize=True, start_d_learn=start_d_learn, end_d_learn=end_d_learn),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=int(hosp_select[0]), normalize=eval(hosp_select[1]), start_d_learn=datetime.strptime(hosp_select[2].split(" - ")[0], "%d/%m/%Y").strftime("%Y-%m-%d"), end_d_learn=datetime.strptime(hosp_select[2].split(" - ")[1], "%d/%m/%Y").strftime("%Y-%m-%d"), alpha=hosp_select[3]),

        map_select = "Nombre de décès",
    )

@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):
    """Department page of the app"""
    charts_and_parameters = covfr.charts(data=None, department=department, region=None)
    label = covfr.request_label(department=department, region=None)
    
    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"], 
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_update_fr"]["day"]),
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

        global_pc = list(range(1, daily.shape[1]+1)),
        normalize = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = np.arange(0.1, 1, 0.05).round(2),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_update_fr"]["day"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_update_fr"]["day"]],

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=2, normalize=True, start_d_learn=start_d_learn, end_d_learn=end_d_learn),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=2, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn),

        map_select = "Nombre de décès",
    )

@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):
    """Region page of the app"""
    charts_and_parameters = covfr.charts(data=None, department=None, region=region)
    label = covfr.request_label(department=None, region=region)

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"], 
        counters = charts_and_parameters["counters"],
        default_start_date = default_start_date,
        default_end_date = default_end_date,
        first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y")),
        last_day = json.dumps(charts_and_parameters["counters"]["last_update_fr"]["day"]),
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

        global_pc = list(range(1, daily.shape[1]+1)),
        normalize = [True, False],
        pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1)),
        alpha_smooth = np.arange(0.1, 1, 0.05).round(2),

        mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_update_fr"]["day"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_update_fr"]["day"]],

        graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=2, normalize=True, start_d_learn=start_d_learn, end_d_learn=end_d_learn),
        graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=2, normalize=False, start_d_learn=start_d_learn, end_d_learn=end_d_learn),

        map_select = "Nombre de décès",
    )

if __name__ == '__main__':
    app.run(debug=True)