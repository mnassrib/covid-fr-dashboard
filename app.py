from flask import Flask, render_template, request, redirect, url_for

from cutils.covidclass import CovidFr

app = Flask(__name__)

covfr = CovidFr()

covid = covfr.load_df()
nprate, rprate, dprate = covfr.load_positive_df()

ordaj_reg = covfr.overall_regions_data_as_json()
oddaj_dep = covfr.overall_departments_data_as_json()
orpdaj_reg = covfr.overall_regions_positive_data_as_json()
odpdaj_dep = covfr.overall_departments_positive_data_as_json()

charts_impact_dep = covfr.charts_impacted_dep()
charts_and_parameters_covid_data = covfr.charts()
charts_and_parameters_positive_data = covfr.charts_positive_data()

label = covfr.request_label()

daily = covfr.dailycases(data=covid, pca=True)
daily_reg = covfr.regiondailycases(data=covid, feature='hosp')

graphJSON_pca_global = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn_fr, end_d_learn=covfr.default_end_d_learn_fr, alpha=covfr.default_alpha)
graphJSON_pca_hosp_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_fr_reg, end_d_learn=covfr.default_end_d_learn_fr_reg, alpha=covfr.default_alpha_reg)

##########################################################
# required html page variables
###############################
first_day_fr = covfr.first_day_fr
last_day_fr = covfr.last_day_fr
department = covfr.default_department
region = covfr.default_region
map_choice = covfr.map_choice
criterion_choice = covfr.criterion_choice
number_all_dep = covfr.number_all_dep
global_pc = covfr.global_pc
normalize_states = covfr.normalize_states
alpha_smooth = covfr.alpha_smooth
pc_reg = covfr.pc_reg
map_select = covfr.default_map_select
top_dep = covfr.default_top_dep
criterion_select = covfr.default_criterion_select
pcdim = covfr.default_pcdim
normalize = covfr.default_normalize
alpha = covfr.default_alpha
start_d_learn_fr = covfr.default_start_d_learn_fr
end_d_learn_fr = covfr.default_end_d_learn_fr
pcdim_reg = covfr.default_pcdim_reg
normalize_reg = covfr.default_normalize_reg
alpha_reg = covfr.default_alpha_reg
start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
##########################################################

@app.route('/', methods=['GET', 'POST'])
def graphs():

    return render_template(
        "graphs.html",
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

        impacted_dep_graphJSON = charts_impact_dep,
        positive_graphJSON = charts_and_parameters_positive_data,
        covid_graphJSON = charts_and_parameters_covid_data,
        positive_counters = charts_and_parameters_positive_data["counters"],
        covid_counters = charts_and_parameters_covid_data["counters"],

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
        criterion_select = criterion_select,
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

        graphJSON_pca_global = graphJSON_pca_global["graphJSON"],
        graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg["graphJSON"],
    )

@app.route('/maps', methods=['GET', 'POST'])
def maps():

    map_select = request.form.get('map_select')

    return render_template(
        "graphs.html",
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

        impacted_dep_graphJSON = charts_impact_dep,
        positive_graphJSON = charts_and_parameters_positive_data,
        covid_graphJSON = charts_and_parameters_covid_data,
        positive_counters = charts_and_parameters_positive_data["counters"],
        covid_counters = charts_and_parameters_covid_data["counters"],

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
        criterion_select = criterion_select,
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

        graphJSON_pca_global = graphJSON_pca_global["graphJSON"],
        graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg["graphJSON"],
    )

@app.route("/top_dep_settings", methods=['GET', 'POST'])
def top_dep_settings():

    top_dep = int(request.form.getlist('top_dep_settings')[0])
    criterion_select = request.form.getlist('top_dep_settings')[1]
    impacted_dep_graphJSON = covfr.charts_impacted_dep(top_number=top_dep)
    
    return render_template(
        "graphs.html",
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

        impacted_dep_graphJSON = charts_impact_dep,
        positive_graphJSON = charts_and_parameters_positive_data,
        covid_graphJSON = charts_and_parameters_covid_data,
        positive_counters = charts_and_parameters_positive_data["counters"],
        covid_counters = charts_and_parameters_covid_data["counters"],

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
        criterion_select = criterion_select,
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

        graphJSON_pca_global = graphJSON_pca_global["graphJSON"],
        graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg["graphJSON"],
    )

@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():

    global_select = request.form.getlist('global_parameters')

    pcdim = int(global_select[0])
    normalize = eval(global_select[1])
    start_d_learn_fr = global_select[2].split(" - ")[0]
    end_d_learn_fr = global_select[2].split(" - ")[1]
    alpha = float(global_select[3])

    graphJSON_pca_global = covfr.pca_charts(data=daily, pcdim=pcdim, normalize=normalize, start_d_learn=start_d_learn_fr, end_d_learn=end_d_learn_fr, alpha=alpha)

    return render_template(
        "graphs.html",
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

        impacted_dep_graphJSON = charts_impact_dep,
        positive_graphJSON = charts_and_parameters_positive_data,
        covid_graphJSON = charts_and_parameters_covid_data,
        positive_counters = charts_and_parameters_positive_data["counters"],
        covid_counters = charts_and_parameters_covid_data["counters"],

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
        criterion_select = criterion_select,
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

        graphJSON_pca_global = graphJSON_pca_global["graphJSON"],
        graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg["graphJSON"],
    )

@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():

    hosp_select = request.form.getlist('hosp_parameters')

    pcdim_reg = int(hosp_select[0])
    normalize_reg = eval(hosp_select[1])
    start_d_learn_fr_reg = hosp_select[2].split(" - ")[0]
    end_d_learn_fr_reg = hosp_select[2].split(" - ")[1]
    alpha_reg = float(hosp_select[3])

    graphJSON_pca_hosp_reg = covfr.pca_charts(data=daily_reg, pcdim=pcdim_reg, normalize=normalize_reg, start_d_learn=start_d_learn_fr_reg, end_d_learn=end_d_learn_fr_reg, alpha=alpha_reg)

    return render_template(
        "graphs.html",
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

        impacted_dep_graphJSON = charts_impact_dep,
        positive_graphJSON = charts_and_parameters_positive_data,
        covid_graphJSON = charts_and_parameters_covid_data,
        positive_counters = charts_and_parameters_positive_data["counters"],
        covid_counters = charts_and_parameters_covid_data["counters"],

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
        criterion_select = criterion_select,
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

        graphJSON_pca_global = graphJSON_pca_global["graphJSON"],
        graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg["graphJSON"],
    )

@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):

    charts_and_parameters_covid_data = covfr.charts(department=department)
    charts_and_parameters_positive_data = covfr.charts_positive_data(department=department)
    label = covfr.request_label(department=department)

    return render_template(
        "graphs.html",
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

        impacted_dep_graphJSON = charts_impact_dep,
        positive_graphJSON = charts_and_parameters_positive_data,
        covid_graphJSON = charts_and_parameters_covid_data,
        positive_counters = charts_and_parameters_positive_data["counters"],
        covid_counters = charts_and_parameters_covid_data["counters"],

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
        criterion_select = criterion_select,
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

        graphJSON_pca_global = graphJSON_pca_global["graphJSON"],
        graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg["graphJSON"],
    )

@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):

    charts_and_parameters_covid_data = covfr.charts(region=region)
    charts_and_parameters_positive_data = covfr.charts_positive_data(region=region)
    label = covfr.request_label(region=region)

    return render_template(
        "graphs.html",
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

        impacted_dep_graphJSON = charts_impact_dep,
        positive_graphJSON = charts_and_parameters_positive_data,
        covid_graphJSON = charts_and_parameters_covid_data,
        positive_counters = charts_and_parameters_positive_data["counters"],
        covid_counters = charts_and_parameters_covid_data["counters"],

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
        criterion_select = criterion_select,
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

        graphJSON_pca_global = graphJSON_pca_global["graphJSON"],
        graphJSON_pca_hosp_reg = graphJSON_pca_hosp_reg["graphJSON"],
    )

if __name__ == '__main__':
    app.run(debug=True)