from flask import Flask, render_template, request, redirect, url_for

from cutils.covidclass import CovidFr

from cutils.rendertemplate import RenderPage

app = Flask(__name__)

covfr = CovidFr()
covid = covfr.load_df()
nprate, rprate, dprate = covfr.load_positive_df()
daily = covfr.dailycases(data=covid, pca=True)
daily_reg = covfr.regiondailycases(data=covid, feature='hosp')
##########################################################
# required html page variables
###############################
cv = dict(
    map_covid_reg = covfr.overall_regions_data_as_json(),
    map_covid_dep = covfr.overall_departments_data_as_json(),
    map_positive_reg = covfr.overall_regions_positive_data_as_json(),
    map_positive_dep = covfr.overall_departments_positive_data_as_json(),
    charts_impacted_dep = covfr.charts_impacted_dep(),
    charts_and_parameters_positive_data = covfr.charts_positive_data(),
    charts_and_parameters_covid_data = covfr.charts(),
    charts_pca_global = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn_fr, end_d_learn=covfr.default_end_d_learn_fr, alpha=covfr.default_alpha),
    charts_pca_hosp_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_fr_reg, end_d_learn=covfr.default_end_d_learn_fr_reg, alpha=covfr.default_alpha_reg),
    label = covfr.request_label(),
    department = covfr.default_department,
    region = covfr.default_region,
    first_day_fr = covfr.first_day_fr,
    last_day_fr = covfr.last_day_fr,
    map_choice = covfr.map_choice,
    criterion_choice = covfr.criterion_choice,
    number_all_dep = covfr.number_all_dep,
    global_pc = covfr.global_pc,
    normalize_states = covfr.normalize_states,
    alpha_smooth = covfr.alpha_smooth,
    pc_reg = covfr.pc_reg,
    map_select = covfr.default_map_select,
    top_dep = covfr.default_top_dep,
    criterion_select = covfr.default_criterion_select,
    pcdim = covfr.default_pcdim,
    normalize = covfr.default_normalize,
    start_d_learn_fr = covfr.default_start_d_learn_fr,
    end_d_learn_fr = covfr.default_end_d_learn_fr,
    alpha = covfr.default_alpha,
    pcdim_reg = covfr.default_pcdim_reg,
    normalize_reg = covfr.default_normalize_reg,
    start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg,
    end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg,
    alpha_reg = covfr.default_alpha_reg,

    state_covid = False,
    state_positive = False,
)
##########################################################

@app.route('/', methods=['GET', 'POST'])
def graphs():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        if covfr.need_covid_data_update():
            upstate_covid = True
        else:
            upstate_covid = False
        if covfr.need_positive_data_update():
            upstate_positive = True
        else:
            upstate_positive = False
        upcovfr = CovidFr()
        upcovid = upcovfr.load_df()
        upnprate, uprprate, updprate = upcovfr.load_positive_df()
        updaily = upcovfr.dailycases(data=upcovid, pca=True)
        updaily_reg = upcovfr.regiondailycases(data=upcovid, feature='hosp')
        ##########################################################
        # required html page variables
        ###############################
        upcv = dict(
            map_covid_reg = upcovfr.overall_regions_data_as_json(),
            map_covid_dep = upcovfr.overall_departments_data_as_json(),
            map_positive_reg = upcovfr.overall_regions_positive_data_as_json(),
            map_positive_dep = upcovfr.overall_departments_positive_data_as_json(),
            charts_impacted_dep = upcovfr.charts_impacted_dep(),
            charts_and_parameters_positive_data = upcovfr.charts_positive_data(),
            charts_and_parameters_covid_data = upcovfr.charts(),
            charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn_fr, end_d_learn=upcovfr.default_end_d_learn_fr, alpha=upcovfr.default_alpha),
            charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_fr_reg, end_d_learn=upcovfr.default_end_d_learn_fr_reg, alpha=upcovfr.default_alpha_reg),
            label = upcovfr.request_label(),
            department = upcovfr.default_department,
            region = upcovfr.default_region,
            first_day_fr = upcovfr.first_day_fr,
            last_day_fr = upcovfr.last_day_fr,
            map_choice = upcovfr.map_choice,
            criterion_choice = upcovfr.criterion_choice,
            number_all_dep = upcovfr.number_all_dep,
            global_pc = upcovfr.global_pc,
            normalize_states = upcovfr.normalize_states,
            alpha_smooth = upcovfr.alpha_smooth,
            pc_reg = upcovfr.pc_reg,
            map_select = upcovfr.default_map_select,
            top_dep = upcovfr.default_top_dep,
            criterion_select = upcovfr.default_criterion_select,
            pcdim = upcovfr.default_pcdim,
            normalize = upcovfr.default_normalize,
            start_d_learn_fr = upcovfr.default_start_d_learn_fr,
            end_d_learn_fr = upcovfr.default_end_d_learn_fr,
            alpha = upcovfr.default_alpha,
            pcdim_reg = upcovfr.default_pcdim_reg,
            normalize_reg = upcovfr.default_normalize_reg,
            start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg,
            alpha_reg = upcovfr.default_alpha_reg,

            state_covid = upstate_covid,
            state_positive = upstate_positive,
        )
        ##########################################################
        rp = RenderPage("graphs.html", **upcv)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    return rp.appview()

@app.route('/maps', methods=['GET', 'POST'])
def maps():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        if covfr.need_covid_data_update():
            upstate_covid = True
        else:
            upstate_covid = False
        if covfr.need_positive_data_update():
            upstate_positive = True
        else:
            upstate_positive = False
        upcovfr = CovidFr()
        upcovid = upcovfr.load_df()
        upnprate, uprprate, updprate = upcovfr.load_positive_df()
        updaily = upcovfr.dailycases(data=upcovid, pca=True)
        updaily_reg = upcovfr.regiondailycases(data=upcovid, feature='hosp')
        ##########################################################
        # required html page variables
        ###############################
        upcv = dict(
            map_covid_reg = upcovfr.overall_regions_data_as_json(),
            map_covid_dep = upcovfr.overall_departments_data_as_json(),
            map_positive_reg = upcovfr.overall_regions_positive_data_as_json(),
            map_positive_dep = upcovfr.overall_departments_positive_data_as_json(),
            charts_impacted_dep = upcovfr.charts_impacted_dep(),
            charts_and_parameters_positive_data = upcovfr.charts_positive_data(),
            charts_and_parameters_covid_data = upcovfr.charts(),
            charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn_fr, end_d_learn=upcovfr.default_end_d_learn_fr, alpha=upcovfr.default_alpha),
            charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_fr_reg, end_d_learn=upcovfr.default_end_d_learn_fr_reg, alpha=upcovfr.default_alpha_reg),
            label = upcovfr.request_label(),
            department = upcovfr.default_department,
            region = upcovfr.default_region,
            first_day_fr = upcovfr.first_day_fr,
            last_day_fr = upcovfr.last_day_fr,
            map_choice = upcovfr.map_choice,
            criterion_choice = upcovfr.criterion_choice,
            number_all_dep = upcovfr.number_all_dep,
            global_pc = upcovfr.global_pc,
            normalize_states = upcovfr.normalize_states,
            alpha_smooth = upcovfr.alpha_smooth,
            pc_reg = upcovfr.pc_reg,
            map_select = upcovfr.default_map_select,
            top_dep = upcovfr.default_top_dep,
            criterion_select = upcovfr.default_criterion_select,
            pcdim = upcovfr.default_pcdim,
            normalize = upcovfr.default_normalize,
            start_d_learn_fr = upcovfr.default_start_d_learn_fr,
            end_d_learn_fr = upcovfr.default_end_d_learn_fr,
            alpha = upcovfr.default_alpha,
            pcdim_reg = upcovfr.default_pcdim_reg,
            normalize_reg = upcovfr.default_normalize_reg,
            start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg,
            alpha_reg = upcovfr.default_alpha_reg,

            state_covid = upstate_covid,
            state_positive = upstate_positive,
        )
        ##########################################################
        rp = RenderPage("graphs.html", **upcv)
        rp.map_select = request.form.get('map_select')
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.map_select = request.form.get('map_select')
    return rp.appview()

@app.route("/top_dep_settings", methods=['GET', 'POST'])
def top_dep_settings():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        if covfr.need_covid_data_update():
            upstate_covid = True
        else:
            upstate_covid = False
        if covfr.need_positive_data_update():
            upstate_positive = True
        else:
            upstate_positive = False
        upcovfr = CovidFr()
        upcovid = upcovfr.load_df()
        upnprate, uprprate, updprate = upcovfr.load_positive_df()
        updaily = upcovfr.dailycases(data=upcovid, pca=True)
        updaily_reg = upcovfr.regiondailycases(data=upcovid, feature='hosp')
        ##########################################################
        # required html page variables
        ###############################
        upcv = dict(
            map_covid_reg = upcovfr.overall_regions_data_as_json(),
            map_covid_dep = upcovfr.overall_departments_data_as_json(),
            map_positive_reg = upcovfr.overall_regions_positive_data_as_json(),
            map_positive_dep = upcovfr.overall_departments_positive_data_as_json(),
            charts_impacted_dep = upcovfr.charts_impacted_dep(),
            charts_and_parameters_positive_data = upcovfr.charts_positive_data(),
            charts_and_parameters_covid_data = upcovfr.charts(),
            charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn_fr, end_d_learn=upcovfr.default_end_d_learn_fr, alpha=upcovfr.default_alpha),
            charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_fr_reg, end_d_learn=upcovfr.default_end_d_learn_fr_reg, alpha=upcovfr.default_alpha_reg),
            label = upcovfr.request_label(),
            department = upcovfr.default_department,
            region = upcovfr.default_region,
            first_day_fr = upcovfr.first_day_fr,
            last_day_fr = upcovfr.last_day_fr,
            map_choice = upcovfr.map_choice,
            criterion_choice = upcovfr.criterion_choice,
            number_all_dep = upcovfr.number_all_dep,
            global_pc = upcovfr.global_pc,
            normalize_states = upcovfr.normalize_states,
            alpha_smooth = upcovfr.alpha_smooth,
            pc_reg = upcovfr.pc_reg,
            map_select = upcovfr.default_map_select,
            top_dep = upcovfr.default_top_dep,
            criterion_select = upcovfr.default_criterion_select,
            pcdim = upcovfr.default_pcdim,
            normalize = upcovfr.default_normalize,
            start_d_learn_fr = upcovfr.default_start_d_learn_fr,
            end_d_learn_fr = upcovfr.default_end_d_learn_fr,
            alpha = upcovfr.default_alpha,
            pcdim_reg = upcovfr.default_pcdim_reg,
            normalize_reg = upcovfr.default_normalize_reg,
            start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg,
            alpha_reg = upcovfr.default_alpha_reg,

            state_covid = upstate_covid,
            state_positive = upstate_positive,
        )
        ##########################################################
        rp = RenderPage("graphs.html", **upcv)
        rp.top_dep = int(request.form.getlist('top_dep_settings')[0])
        rp.criterion_select = request.form.getlist('top_dep_settings')[1]
        rp.charts_impacted_dep = upcovfr.charts_impacted_dep(top_number=rp.top_dep)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.top_dep = int(request.form.getlist('top_dep_settings')[0])
    rp.criterion_select = request.form.getlist('top_dep_settings')[1]
    rp.charts_impacted_dep = covfr.charts_impacted_dep(top_number=rp.top_dep)
    return rp.appview()
    
@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        if covfr.need_covid_data_update():
            upstate_covid = True
        else:
            upstate_covid = False
        if covfr.need_positive_data_update():
            upstate_positive = True
        else:
            upstate_positive = False
        upcovfr = CovidFr()
        upcovid = upcovfr.load_df()
        upnprate, uprprate, updprate = upcovfr.load_positive_df()
        updaily = upcovfr.dailycases(data=upcovid, pca=True)
        updaily_reg = upcovfr.regiondailycases(data=upcovid, feature='hosp')
        ##########################################################
        # required html page variables
        ###############################
        upcv = dict(
            map_covid_reg = upcovfr.overall_regions_data_as_json(),
            map_covid_dep = upcovfr.overall_departments_data_as_json(),
            map_positive_reg = upcovfr.overall_regions_positive_data_as_json(),
            map_positive_dep = upcovfr.overall_departments_positive_data_as_json(),
            charts_impacted_dep = upcovfr.charts_impacted_dep(),
            charts_and_parameters_positive_data = upcovfr.charts_positive_data(),
            charts_and_parameters_covid_data = upcovfr.charts(),
            charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn_fr, end_d_learn=upcovfr.default_end_d_learn_fr, alpha=upcovfr.default_alpha),
            charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_fr_reg, end_d_learn=upcovfr.default_end_d_learn_fr_reg, alpha=upcovfr.default_alpha_reg),
            label = upcovfr.request_label(),
            department = upcovfr.default_department,
            region = upcovfr.default_region,
            first_day_fr = upcovfr.first_day_fr,
            last_day_fr = upcovfr.last_day_fr,
            map_choice = upcovfr.map_choice,
            criterion_choice = upcovfr.criterion_choice,
            number_all_dep = upcovfr.number_all_dep,
            global_pc = upcovfr.global_pc,
            normalize_states = upcovfr.normalize_states,
            alpha_smooth = upcovfr.alpha_smooth,
            pc_reg = upcovfr.pc_reg,
            map_select = upcovfr.default_map_select,
            top_dep = upcovfr.default_top_dep,
            criterion_select = upcovfr.default_criterion_select,
            pcdim = upcovfr.default_pcdim,
            normalize = upcovfr.default_normalize,
            start_d_learn_fr = upcovfr.default_start_d_learn_fr,
            end_d_learn_fr = upcovfr.default_end_d_learn_fr,
            alpha = upcovfr.default_alpha,
            pcdim_reg = upcovfr.default_pcdim_reg,
            normalize_reg = upcovfr.default_normalize_reg,
            start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg,
            alpha_reg = upcovfr.default_alpha_reg,

            state_covid = upstate_covid,
            state_positive = upstate_positive,
        )
        ##########################################################
        global_select = request.form.getlist('global_parameters')
        rp = RenderPage("graphs.html", **upcv)
        rp.pcdim = int(global_select[0])
        rp.normalize = eval(global_select[1])
        rp.start_d_learn_fr = global_select[2].split(" - ")[0]
        rp.end_d_learn_fr = global_select[2].split(" - ")[1]
        rp.alpha = float(global_select[3])
        rp.charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=rp.pcdim, normalize=rp.normalize, start_d_learn=rp.start_d_learn_fr, end_d_learn=rp.end_d_learn_fr, alpha=rp.alpha)
        return rp.appview()

    global_select = request.form.getlist('global_parameters')
    rp = RenderPage("graphs.html", **cv)
    rp.pcdim = int(global_select[0])
    rp.normalize = eval(global_select[1])
    rp.start_d_learn_fr = global_select[2].split(" - ")[0]
    rp.end_d_learn_fr = global_select[2].split(" - ")[1]
    rp.alpha = float(global_select[3])
    rp.charts_pca_global = covfr.pca_charts(data=daily, pcdim=rp.pcdim, normalize=rp.normalize, start_d_learn=rp.start_d_learn_fr, end_d_learn=rp.end_d_learn_fr, alpha=rp.alpha)
    return rp.appview()

@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        if covfr.need_covid_data_update():
            upstate_covid = True
        else:
            upstate_covid = False
        if covfr.need_positive_data_update():
            upstate_positive = True
        else:
            upstate_positive = False
        upcovfr = CovidFr()
        upcovid = upcovfr.load_df()
        upnprate, uprprate, updprate = upcovfr.load_positive_df()
        updaily = upcovfr.dailycases(data=upcovid, pca=True)
        updaily_reg = upcovfr.regiondailycases(data=upcovid, feature='hosp')
        ##########################################################
        # required html page variables
        ###############################
        upcv = dict(
            map_covid_reg = upcovfr.overall_regions_data_as_json(),
            map_covid_dep = upcovfr.overall_departments_data_as_json(),
            map_positive_reg = upcovfr.overall_regions_positive_data_as_json(),
            map_positive_dep = upcovfr.overall_departments_positive_data_as_json(),
            charts_impacted_dep = upcovfr.charts_impacted_dep(),
            charts_and_parameters_positive_data = upcovfr.charts_positive_data(),
            charts_and_parameters_covid_data = upcovfr.charts(),
            charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn_fr, end_d_learn=upcovfr.default_end_d_learn_fr, alpha=upcovfr.default_alpha),
            charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_fr_reg, end_d_learn=upcovfr.default_end_d_learn_fr_reg, alpha=upcovfr.default_alpha_reg),
            label = upcovfr.request_label(),
            department = upcovfr.default_department,
            region = upcovfr.default_region,
            first_day_fr = upcovfr.first_day_fr,
            last_day_fr = upcovfr.last_day_fr,
            map_choice = upcovfr.map_choice,
            criterion_choice = upcovfr.criterion_choice,
            number_all_dep = upcovfr.number_all_dep,
            global_pc = upcovfr.global_pc,
            normalize_states = upcovfr.normalize_states,
            alpha_smooth = upcovfr.alpha_smooth,
            pc_reg = upcovfr.pc_reg,
            map_select = upcovfr.default_map_select,
            top_dep = upcovfr.default_top_dep,
            criterion_select = upcovfr.default_criterion_select,
            pcdim = upcovfr.default_pcdim,
            normalize = upcovfr.default_normalize,
            start_d_learn_fr = upcovfr.default_start_d_learn_fr,
            end_d_learn_fr = upcovfr.default_end_d_learn_fr,
            alpha = upcovfr.default_alpha,
            pcdim_reg = upcovfr.default_pcdim_reg,
            normalize_reg = upcovfr.default_normalize_reg,
            start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg,
            alpha_reg = upcovfr.default_alpha_reg,

            state_covid = upstate_covid,
            state_positive = upstate_positive,
        )
        ##########################################################
        hosp_select = request.form.getlist('hosp_parameters')
        rp = RenderPage("graphs.html", **upcv)
        rp.pcdim_reg = int(hosp_select[0])
        rp.normalize_reg = eval(hosp_select[1])
        rp.start_d_learn_fr_reg = hosp_select[2].split(" - ")[0]
        rp.end_d_learn_fr_reg = hosp_select[2].split(" - ")[1]
        rp.alpha_reg = float(hosp_select[3])
        rp.charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=rp.pcdim_reg, normalize=rp.normalize_reg, start_d_learn=rp.start_d_learn_fr_reg, end_d_learn=rp.end_d_learn_fr_reg, alpha=rp.alpha_reg)
        return rp.appview()

    hosp_select = request.form.getlist('hosp_parameters')
    rp = RenderPage("graphs.html", **cv)
    rp.pcdim_reg = int(hosp_select[0])
    rp.normalize_reg = eval(hosp_select[1])
    rp.start_d_learn_fr_reg = hosp_select[2].split(" - ")[0]
    rp.end_d_learn_fr_reg = hosp_select[2].split(" - ")[1]
    rp.alpha_reg = float(hosp_select[3])
    rp.charts_pca_hosp_reg = covfr.pca_charts(data=daily_reg, pcdim=rp.pcdim_reg, normalize=rp.normalize_reg, start_d_learn=rp.start_d_learn_fr_reg, end_d_learn=rp.end_d_learn_fr_reg, alpha=rp.alpha_reg)
    return rp.appview()

@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        if covfr.need_covid_data_update():
            upstate_covid = True
        else:
            upstate_covid = False
        if covfr.need_positive_data_update():
            upstate_positive = True
        else:
            upstate_positive = False
        upcovfr = CovidFr()
        upcovid = upcovfr.load_df()
        upnprate, uprprate, updprate = upcovfr.load_positive_df()
        updaily = upcovfr.dailycases(data=upcovid, pca=True)
        updaily_reg = upcovfr.regiondailycases(data=upcovid, feature='hosp')
        ##########################################################
        # required html page variables
        ###############################
        upcv = dict(
            map_covid_reg = upcovfr.overall_regions_data_as_json(),
            map_covid_dep = upcovfr.overall_departments_data_as_json(),
            map_positive_reg = upcovfr.overall_regions_positive_data_as_json(),
            map_positive_dep = upcovfr.overall_departments_positive_data_as_json(),
            charts_impacted_dep = upcovfr.charts_impacted_dep(),
            charts_and_parameters_positive_data = upcovfr.charts_positive_data(),
            charts_and_parameters_covid_data = upcovfr.charts(),
            charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn_fr, end_d_learn=upcovfr.default_end_d_learn_fr, alpha=upcovfr.default_alpha),
            charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_fr_reg, end_d_learn=upcovfr.default_end_d_learn_fr_reg, alpha=upcovfr.default_alpha_reg),
            label = upcovfr.request_label(),
            department = upcovfr.default_department,
            region = upcovfr.default_region,
            first_day_fr = upcovfr.first_day_fr,
            last_day_fr = upcovfr.last_day_fr,
            map_choice = upcovfr.map_choice,
            criterion_choice = upcovfr.criterion_choice,
            number_all_dep = upcovfr.number_all_dep,
            global_pc = upcovfr.global_pc,
            normalize_states = upcovfr.normalize_states,
            alpha_smooth = upcovfr.alpha_smooth,
            pc_reg = upcovfr.pc_reg,
            map_select = upcovfr.default_map_select,
            top_dep = upcovfr.default_top_dep,
            criterion_select = upcovfr.default_criterion_select,
            pcdim = upcovfr.default_pcdim,
            normalize = upcovfr.default_normalize,
            start_d_learn_fr = upcovfr.default_start_d_learn_fr,
            end_d_learn_fr = upcovfr.default_end_d_learn_fr,
            alpha = upcovfr.default_alpha,
            pcdim_reg = upcovfr.default_pcdim_reg,
            normalize_reg = upcovfr.default_normalize_reg,
            start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg,
            alpha_reg = upcovfr.default_alpha_reg,

            state_covid = upstate_covid,
            state_positive = upstate_positive,
        )
        ##########################################################
        rp = RenderPage("graphs.html", **upcv)
        rp.department = department
        rp.charts_and_parameters_covid_data = upcovfr.charts(department=rp.department)
        rp.charts_and_parameters_positive_data = upcovfr.charts_positive_data(department=rp.department)
        rp.label = upcovfr.request_label(department=rp.department)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.department = department
    rp.charts_and_parameters_covid_data = covfr.charts(department=rp.department)
    rp.charts_and_parameters_positive_data = covfr.charts_positive_data(department=rp.department)
    rp.label = covfr.request_label(department=rp.department)
    return rp.appview()

@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):
    if covfr.need_covid_data_update() or covfr.need_positive_data_update():
        if covfr.need_covid_data_update():
            upstate_covid = True
        else:
            upstate_covid = False
        if covfr.need_positive_data_update():
            upstate_positive = True
        else:
            upstate_positive = False
        upcovfr = CovidFr()
        upcovid = upcovfr.load_df()
        upnprate, uprprate, updprate = upcovfr.load_positive_df()
        updaily = upcovfr.dailycases(data=upcovid, pca=True)
        updaily_reg = upcovfr.regiondailycases(data=upcovid, feature='hosp')
        ##########################################################
        # required html page variables
        ###############################
        upcv = dict(
            map_covid_reg = upcovfr.overall_regions_data_as_json(),
            map_covid_dep = upcovfr.overall_departments_data_as_json(),
            map_positive_reg = upcovfr.overall_regions_positive_data_as_json(),
            map_positive_dep = upcovfr.overall_departments_positive_data_as_json(),
            charts_impacted_dep = upcovfr.charts_impacted_dep(),
            charts_and_parameters_positive_data = upcovfr.charts_positive_data(),
            charts_and_parameters_covid_data = upcovfr.charts(),
            charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=upcovfr.default_pcdim, normalize=upcovfr.default_normalize, start_d_learn=upcovfr.default_start_d_learn_fr, end_d_learn=upcovfr.default_end_d_learn_fr, alpha=upcovfr.default_alpha),
            charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=upcovfr.default_pcdim_reg, normalize=upcovfr.default_normalize_reg, start_d_learn=upcovfr.default_start_d_learn_fr_reg, end_d_learn=upcovfr.default_end_d_learn_fr_reg, alpha=upcovfr.default_alpha_reg),
            label = upcovfr.request_label(),
            department = upcovfr.default_department,
            region = upcovfr.default_region,
            first_day_fr = upcovfr.first_day_fr,
            last_day_fr = upcovfr.last_day_fr,
            map_choice = upcovfr.map_choice,
            criterion_choice = upcovfr.criterion_choice,
            number_all_dep = upcovfr.number_all_dep,
            global_pc = upcovfr.global_pc,
            normalize_states = upcovfr.normalize_states,
            alpha_smooth = upcovfr.alpha_smooth,
            pc_reg = upcovfr.pc_reg,
            map_select = upcovfr.default_map_select,
            top_dep = upcovfr.default_top_dep,
            criterion_select = upcovfr.default_criterion_select,
            pcdim = upcovfr.default_pcdim,
            normalize = upcovfr.default_normalize,
            start_d_learn_fr = upcovfr.default_start_d_learn_fr,
            end_d_learn_fr = upcovfr.default_end_d_learn_fr,
            alpha = upcovfr.default_alpha,
            pcdim_reg = upcovfr.default_pcdim_reg,
            normalize_reg = upcovfr.default_normalize_reg,
            start_d_learn_fr_reg = upcovfr.default_start_d_learn_fr_reg,
            end_d_learn_fr_reg = upcovfr.default_end_d_learn_fr_reg,
            alpha_reg = upcovfr.default_alpha_reg,

            state_covid = upstate_covid,
            state_positive = upstate_positive,
        )
        ##########################################################
        rp = RenderPage("graphs.html", **upcv)
        rp.region = region
        rp.charts_and_parameters_covid_data = upcovfr.charts(region=rp.region)
        rp.charts_and_parameters_positive_data = upcovfr.charts_positive_data(region=rp.region)
        rp.label = upcovfr.request_label(region=rp.region)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.region = region
    rp.charts_and_parameters_covid_data = covfr.charts(region=rp.region)
    rp.charts_and_parameters_positive_data = covfr.charts_positive_data(region=rp.region)
    rp.label = covfr.request_label(region=rp.region)
    return rp.appview()

if __name__ == '__main__':
    app.run(debug=True)
