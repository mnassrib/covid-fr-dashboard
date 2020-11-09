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
    ordaj_reg = covfr.overall_regions_data_as_json()

    daily = covfr.dailycases(data=covid, pca=True)
    #daily_reg = covfr.regiondailycases(data=covid, feature='dc')
    daily_reg = covfr.regiondailycases(data=covid, feature='hosp')

    nprate, rprate, dprate = covfr.load_positive_df()
    odpdaj_dep = covfr.overall_departments_positive_data_as_json()
    orpdaj_reg = covfr.overall_regions_positive_data_as_json()
  
###############################
# required processing settings
###############################
mapchoice = ["Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre de guérisons", "Nombre d'hospitalisations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de réanimations le "+covfr.charts()["counters"]["last_day_fr"], "Nombre de cas positifs le "+covfr.charts_positive_data()["counters"]["positive_last_day_fr"]]
number_all_dep = list(range(1, covfr.department_base_data.shape[0]+1))
global_pc = list(range(1, daily.shape[1]+1))
normalize_states = [True, False]
alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2))
pc_reg = list(range(1, covfr.regiondailycases(data=covid, feature='hosp').shape[1]+1))
criterion_choice = ["Cas positifs au "+covfr.charts_positive_data()["counters"]["positive_last_day_fr"], "Hospitalisations au "+covfr.charts()["counters"]["last_day_fr"], "Réanimations au "+covfr.charts()["counters"]["last_day_fr"]]

first_day = json.dumps(covid["jour"][0].strftime("%d/%m/%Y"))
last_day = json.dumps(datetime.strptime(covfr.last_day, "%Y-%m-%d").strftime("%d/%m/%Y"))

####################
# default settings
####################
#-- default selected map
default_map_select = mapchoice[5]
## default selected number of top departments
default_top_dep = 10
default_criterion = criterion_choice[0]
#-- default settings for pca-based global monitoring
default_pcdim = 2
default_normalize = True
default_start_d_learn = '2020-05-15'
default_end_d_learn = '2020-08-25'
default_alpha = 0.6
default_start_d_learn_fr = json.dumps(datetime.strptime(default_start_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
default_end_d_learn_fr = json.dumps(datetime.strptime(default_end_d_learn, '%Y-%m-%d').strftime("%d/%m/%Y"))
#-- default settings for pca-based region hospitalization monitoring
default_pcdim_reg = 2
default_normalize_reg = False
default_start_d_learn_reg = '2020-05-15'
default_end_d_learn_reg = '2020-08-25'
default_alpha_reg = 0.7
default_start_d_learn_fr_reg = json.dumps(datetime.strptime(default_start_d_learn_reg, '%Y-%m-%d').strftime("%d/%m/%Y"))
default_end_d_learn_fr_reg = json.dumps(datetime.strptime(default_end_d_learn_reg, '%Y-%m-%d').strftime("%d/%m/%Y"))

###############################
# required html page variables
###############################
map_select = default_map_select    
top_dep = default_top_dep
criterion = default_criterion
pcdim = default_pcdim
normalize = default_normalize
start_d_learn = default_start_d_learn
end_d_learn = default_end_d_learn
start_d_learn_fr = default_start_d_learn_fr
end_d_learn_fr = default_end_d_learn_fr
alpha = default_alpha
pcdim_reg = default_pcdim_reg
normalize_reg = default_normalize_reg
start_d_learn_reg = default_start_d_learn_reg
end_d_learn_reg = default_end_d_learn_reg
start_d_learn_fr_reg = default_start_d_learn_fr_reg
end_d_learn_fr_reg = default_end_d_learn_fr_reg
alpha_reg = default_alpha_reg

charts_and_parameters = covfr.charts(top_number=top_dep)

charts_and_parameters_positive_data = covfr.charts_positive_data(top_number=top_dep)

label = covfr.request_label(department=None, region=None)

graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn, end_d_learn=end_d_learn, alpha=alpha)

graphJSONquadratics_reg = covfr.pca_charts(data=daily_reg, pcdim=pcdim_reg, normalize=normalize_reg, start_d_learn=start_d_learn_reg, end_d_learn=end_d_learn_reg, alpha=alpha_reg)

@app.route('/', methods=['GET', 'POST'])
def graphs():

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

        overall_regions_data_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['quantiles_P'], 
        overall_departments_data_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['quantiles_P'],  

        first_day = first_day,
        last_day = last_day,
        label = label,

        mapchoice = mapchoice,
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

        overall_regions_data_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['quantiles_P'], 
        overall_departments_data_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['quantiles_P'],  

        first_day = first_day,
        last_day = last_day,
        label = label,
        
        mapchoice = mapchoice,
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

        overall_regions_data_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['quantiles_P'], 
        overall_departments_data_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['quantiles_P'],  

        first_day = first_day,
        last_day = last_day,
        label = label,
        
        mapchoice = mapchoice,
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

        overall_regions_data_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['quantiles_P'], 
        overall_departments_data_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['quantiles_P'],  

        first_day = first_day,
        last_day = last_day,
        label = label,
        
        mapchoice = mapchoice,
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

        overall_regions_data_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['quantiles_P'], 
        overall_departments_data_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['quantiles_P'],  

        first_day = first_day,
        last_day = last_day,
        label = label,
        
        mapchoice = mapchoice,
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

    charts_and_parameters = covfr.charts(data=None, department=department, region=None, top_number=top_dep)
    charts_and_parameters_positive_data = covfr.charts_positive_data(data=None, department=department, region=None, top_number=top_dep)
    label = covfr.request_label(department=department, region=None)
    
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

        overall_regions_data_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['quantiles_P'], 
        overall_departments_data_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['quantiles_P'],  

        first_day = first_day,
        last_day = last_day,
        label = label,
        
        mapchoice = mapchoice,
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
    
    charts_and_parameters = covfr.charts(data=None, department=None, region=region, top_number=top_dep)
    charts_and_parameters_positive_data = covfr.charts_positive_data(data=None, department=None, region=region, top_number=top_dep)
    label = covfr.request_label(department=None, region=region)

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

        overall_regions_data_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['data_P'],
        overall_regions_quantiles_P = orpdaj_reg["orpdaj"]["overall_regions_P_as_json"]['quantiles_P'], 
        overall_departments_data_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['data_P'],
        overall_departments_quantiles_P = odpdaj_dep["odpdaj"]["overall_departments_P_as_json"]['quantiles_P'],  

        first_day = first_day,
        last_day = last_day,
        label = label,
        
        mapchoice = mapchoice,
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